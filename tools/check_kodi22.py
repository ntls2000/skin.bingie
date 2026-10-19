#!/usr/bin/env python3
"""Static sanity checks for the Bingie skin on Kodi 21 Omega / Kodi 22 Piers.

This checks XML syntax and known Kodi 22 removals. It cannot prove that
third-party Python add-ons work with Kodi 22 or replace device testing.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
REMOVED_PIERS_INFOLABELS = (
    re.compile(r"\bPlayer\.Cutlist\b", re.IGNORECASE),
    re.compile(r"\bSlideshow\.EXIFSoftware\b", re.IGNORECASE),
    re.compile(r"\bSystem\.PVRCount\b", re.IGNORECASE),
    re.compile(r"\bListItem\.BackendInstanceName\b", re.IGNORECASE),
    re.compile(r"\bSystem\.Locale\(\s*timezone(?:country)?\s*\)", re.IGNORECASE),
)
SKIN_PATHS = ("1080i", "shortcuts", "colors")


def check():
    problems = []
    files = [ROOT / "addon.xml"]
    for dirname in SKIN_PATHS:
        files.extend(sorted((ROOT / dirname).rglob("*.xml")))
    for path in files:
        relative_path = path.relative_to(ROOT)
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            problems.append(f"{relative_path}: invalid XML: {exc}")
            continue
        content = path.read_text(encoding="utf-8-sig")
        for lineno, line in enumerate(content.splitlines(), start=1):
            for obsolete in REMOVED_PIERS_INFOLABELS:
                if obsolete.search(line):
                    problems.append(f"{relative_path}:{lineno}: removed Kodi 22 label: {obsolete.pattern}")

    manifest = ET.parse(ROOT / "addon.xml").getroot()
    if manifest.get("id") != "skin.bingie":
        problems.append("addon.xml: expected skin.bingie ID")
    deps = {item.get("addon"): item.get("version") for item in manifest.findall("./requires/import")}
    # Kodi 22 supports Omega's skin ABI 5.17.0. Do not raise the minimum
    # to 5.18.0, which would unnecessarily exclude Kodi 21 users.
    if deps.get("xbmc.gui") != "5.17.0":
        problems.append("addon.xml: keep xbmc.gui 5.17.0 for Kodi 21/22 support")
    for filename in ("Home.xml", "DialogSelect.xml", "VideoOSD.xml"):
        if not (ROOT / "1080i" / filename).exists():
            problems.append(f"1080i/{filename}: required skin window is missing")
    if problems:
        print("\n".join("ERROR " + problem for problem in problems), file=sys.stderr)
        return 1
    print(f"OK: {len(files)} XML manifests/views parsed and Kodi 22 removed labels checked")
    print("NOTE: External Bingie Python dependencies and actual Kodi GUI must be tested on Kodi 22.")
    return 0


if __name__ == "__main__":
    sys.exit(check())
