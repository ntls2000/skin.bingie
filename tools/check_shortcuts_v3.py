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

    # Skin Shortcuts v2 add-on strings (32000-32999) are not in the
    # skin's language resources; unresolved $LOCALIZE[x] is shown verbatim.
    for filename in ("menus.xml", "widgets.xml"):
        source = (SHORTCUTS / filename).read_text(encoding="utf-8")
        assert not re.search(r"\\$LOCALIZE\\[32\\d{3}\\]", source), (
            f"Untranslated Skin Shortcuts v2 labels in {filename}"
        )

    # French catalogue must cover every string ID defined in the English skin.
    english_po = (ROOT / "language/resource.language.en_gb/strings.po").read_text(encoding="utf-8")
    french_po = (ROOT / "language/resource.language.fr_fr/strings.po").read_text(encoding="utf-8")
    english_ids = re.findall(r'^msgctxt "#(\d+)"$', english_po, re.M)
    french_ids = re.findall(r'^msgctxt "#(\d+)"$', french_po, re.M)
    assert english_ids == french_ids, "French PO missing strings or different ordering"
    assert 'Language: fr_FR' in french_po, "French locale header missing"
    assert len(re.findall(r'^msgstr ""$', french_po, re.M)) == 1, "Empty French translation detected"
    assert len(french_ids) >= 500, "Unexpectedly short French catalogue"

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

    # Modern Netflix-inspired mode is opt-in and must not replace the safe legacy UI.
    modern = ET.parse(XML_DIR / "IncludesNetflixModern.xml").getroot()
    modern_includes = {node.get("name") for node in modern.findall("include")}
    assert {"NetflixModernTopNavigation", "NetflixModernHeroSurface"} <= modern_includes
    navigation = next(e for e in modern.findall("include")
                      if e.get("name") == "NetflixModernTopNavigation")
    assert any(c.get("id") == "900" and c.get("type") == "list"
               for c in navigation.iter("control")), "Modern menu must preserve Skin Shortcuts id 900"
    assert any((x.text or "").strip() == "skinshortcuts-modernnav"
               for x in navigation.iter("include")), "Modern menu must use its v3-generated four-item navbar"
    nav = next(x for x in menus.findall("menu") if x.get("name") == "modernnav")
    assert len(nav.findall("item")) == 4, "Four compact modern TV tabs are required"
    assert all(x.find("action") is not None for x in nav.findall("item"))
    hero = next(x for x in modern.findall("include")
                if x.get("name") == "NetflixModernHeroSurface")
    hero_ids = {x.get("id") for x in hero.iter("control")}
    assert {"49010", "49011"} <= hero_ids, "Modern hero Play and Info buttons missing"
    assert "Container(1508).ListItem.Title" in ET.tostring(hero, encoding="unicode")
    # Kodi-specific on/off routing and a larger gap beneath the feature.
    widget_factory = ET.parse(XML_DIR / "IncludesHomeWidgets.xml").getroot()
    base = next(e for e in widget_factory.findall("include") if e.get("name") == "widget_base")
    factory_options = base.findall("include")
    assert len(factory_options) == 2
    assert {x.get("condition") for x in factory_options} == {
        "Skin.HasSetting(NetflixModern2026)", "!Skin.HasSetting(NetflixModern2026)"
    }
    assert any(p.get("name") == "widgetStyle" and p.get("value") == "widget_layout_landscape"
               for x in factory_options for p in x.findall("param"))

    homepage = (XML_DIR / "IncludesHomeBingie.xml").read_text(encoding="utf-8")
    assert 'condition="Skin.HasSetting(NetflixModern2026) + Window.IsActive(Home)"' in homepage
    assert 'condition="!Skin.HasSetting(NetflixModern2026) | !Window.IsActive(Home)"' in homepage
    assert 'NetflixModernHeroSurface' in homepage
    skinsettings = (XML_DIR / "IncludesSkinSettings.xml").read_text(encoding="utf-8")
    assert "Skin.ToggleSetting(NetflixModern2026)" in skinsettings
    assert "ReloadSkin()" in skinsettings
    assert "type=manage&amp;menu=modernnav" in skinsettings
    assert 'end="0,155"' in homepage
    assert 'old hub title and old spotlight would overlap modern feature' in homepage

    assert "ActivateWindow(Settings)" in ET.tostring(modern, encoding="unicode")
    for locale in ("en_gb", "fr_fr"):
        po = (ROOT / f"language/resource.language.{locale}/strings.po").read_text(encoding="utf-8")
        assert 'msgctxt "#31610"' in po and 'msgctxt "#31611"' in po

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
