#!/usr/bin/env python3
"""Static migration gate for Bingie / Skin Shortcuts 3 on Kodi 22.

This checks configuration structure and skin XML, not the Kodi GUI runtime.
"""
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SHORTCUTS = ROOT / "shortcuts"
XML_DIR = ROOT / "1080i"


def check():
    for folder in (XML_DIR, SHORTCUTS):
        for path in folder.rglob("*.xml"):
            try:
                ET.parse(path)
            except ET.ParseError as exc:
                raise AssertionError(f"Invalid XML {path.relative_to(ROOT)}: {exc}") from exc

    config = {name: ET.parse(SHORTCUTS / f"{name}.xml").getroot()
              for name in ("menus", "widgets", "backgrounds", "properties", "templates")}
    for name, root in config.items():
        assert root.tag == name, (name, root.tag)

    menus = config["menus"]
    names = {e.get("name") for e in menus.findall("menu")}
    required = {"mainmenu", "powermenu", "searchmenu", "tmdbsearchmenu",
                "moviehub", "tvshowhub", "newhub", "musichub",
                "customhub", "mylisthub", "somethinghub"}
    assert required <= names, f"Missing menus: {required - names}"
    main = next(item for item in menus.findall("menu")
                if item.get("name") == "mainmenu")
    assert any(item.get("required") == "true" and
               any("ActivateWindow(Settings)" in (act.text or "")
                   for act in item.findall("action"))
               for item in main.findall("item")), "Settings rescue must be required"
    shortcuts = main.find("item[@name='movies']")
    assert shortcuts is not None and shortcuts.get("submenu") == "movies"

    existing = {e.get("include") for e in config["templates"].findall("template")
                if e.get("include")}
    expected = {"Widgets", "moviehub", "tvshowhub", "newhub", "musichub",
                "customhub", "mylisthub", "somethinghub"}
    assert expected <= existing, f"Missing template outputs: {expected-existing}"
    templates = ET.tostring(config["templates"], encoding="unicode")
    assert not re.search(r"\$PYTHON\[|\$SKINSHORTCUTS\[", templates), "v2 template macros in v3 configuration"

    properties = config["properties"]
    mappings = properties.find("buttons")
    assert mappings is not None
    assert {str(e.get("id")) for e in mappings.findall("button")} >= {
        "309", "310", "4311", "31507", "315071", "31028", "31468", "581", "580", "21427"
    }
    dialog = ET.parse(XML_DIR / "script-skinshortcuts.xml").getroot()
    controls = {e.get("id") for e in dialog.iter("control") if e.get("id")}
    assert "211" in controls and "309" in controls and "310" in controls
    assert not {"101", "404", "308"} & controls
    home = (XML_DIR / "Home.xml").read_text(encoding="utf-8")
    assert "RunScript(script.skinshortcuts,type=buildxml)" in home
    bingie = (XML_DIR / "IncludesBingie.xml").read_text(encoding="utf-8")
    assert "skinshortcuts-powermenu" in bingie
    assert "skinshortcuts-mainmenu-submenu" in bingie
    assert "<onclick>ActivateWindow(Settings)</onclick>" in bingie

    for path in XML_DIR.rglob("*.xml"):
        text = path.read_text(encoding="utf-8-sig")
        if re.search(r"RunScript\(script\.skinshortcuts,type=manage&amp;group=", text):
            raise AssertionError(f"Legacy group= manage action in {path.relative_to(ROOT)}")
        if re.search(r"RunScript\(script\.skinshortcuts,type=widgets", text):
            raise AssertionError(f"Legacy v2 widget picker in {path.relative_to(ROOT)}")

    manifest = ET.parse(ROOT / "addon.xml").getroot()
    dep = next((e for e in manifest.iter("import") if e.get("addon") == "script.skinshortcuts"), None)
    assert dep is not None and dep.get("version") == "3.0.4", "v3 min dependency missing"
    assert "~beta" in manifest.get("version", ""), "Testing branch must not present as stable"
    print("OK: v3 XML, menus, templates, actions, required Settings fallback")
    print("Note: Runtime UI, widget generation, and data persistence still need Kodi 22 device tests.")


if __name__ == "__main__":
    try:
        check()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
