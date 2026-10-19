#!/usr/bin/env python3
"""Build a Kodi repository (ZIP packages, catalogue and checksum).

Run from any working directory after checking out ntls2000/skin.bingie.
Only files from the skin's public add-on are packaged; GitHub metadata,
release ZIP files and repository tooling are not included in the skin ZIP.
"""
import hashlib
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "repo"
SKIN_ID = "skin.bingie"
REPOSITORY_ID = "repository.ntls2000.bingie"
SKIN_DIRS = ("1080i", "colors", "extras", "fonts", "language", "media", "resources", "shortcuts")
SKIN_FILES = ("addon.xml", "LICENSE", "README.md")


def addon_details(path: Path, expected_id: str):
    element = ET.parse(path).getroot()
    if element.tag != "addon" or element.attrib.get("id") != expected_id:
        raise ValueError(f"Unexpected Kodi add-on manifest: {path}")
    version = element.attrib["version"]
    if not version or "/" in version or "\\" in version:
        raise ValueError(f"Invalid version in {path}")
    return element, version


def package(addon_id: str, version: str, files):
    directory = OUT / addon_id
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{addon_id}-{version}.zip"
    with ZipFile(target, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for local_path, addon_path in sorted(files, key=lambda entry: entry[1]):
            archive.write(local_path, arcname=f"{addon_id}/{addon_path}")
    return target


def skin_files():
    for name in SKIN_FILES:
        path = ROOT / name
        if path.is_file():
            yield (path, name)
    for directory in SKIN_DIRS:
        folder = ROOT / directory
        if folder.is_dir():
            for path in folder.rglob("*"):
                if path.is_file() and not path.is_symlink():
                    yield (path, path.relative_to(ROOT).as_posix())


def main():
    skin, skin_version = addon_details(ROOT / "addon.xml", SKIN_ID)
    repodir = ROOT / REPOSITORY_ID
    repository, repo_version = addon_details(repodir / "addon.xml", REPOSITORY_ID)
    OUT.mkdir(exist_ok=True)

    skin_zip = package(SKIN_ID, skin_version, skin_files())
    assets = [(repodir / "addon.xml", "addon.xml")]
    for original in ("icon.png", "fanart.jpg"):
        source = ROOT / "resources" / original
        if source.is_file():
            shutil.copy2(source, OUT / SKIN_ID / original)
            assets.append((source, original))
    repo_zip = package(REPOSITORY_ID, repo_version, assets)
    for name in ("icon.png", "fanart.jpg"):
        source = ROOT / "resources" / name
        if source.is_file():
            shutil.copy2(source, OUT / REPOSITORY_ID / name)

    addons = ET.Element("addons")
    addons.append(skin)
    addons.append(repository)
    ET.indent(addons, space="    ")
    xml_data = ET.tostring(addons, encoding="utf-8", xml_declaration=True) + b"\n"
    (OUT / "addons.xml").write_bytes(xml_data)
    (OUT / "addons.xml.md5").write_text(
        hashlib.md5(xml_data).hexdigest(), encoding="ascii"
    )
    for path in (skin_zip, repo_zip):
        print(f"Built {path.relative_to(ROOT)} ({path.stat().st_size:,} bytes)")
    print("Generated repo/addons.xml and repo/addons.xml.md5")


if __name__ == "__main__":
    main()
