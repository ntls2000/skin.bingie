#!/usr/bin/env python3
"""One-time import of editable Bingie Python extension sources.

Uses the published open-source ZIPs from matke-84's official Bingie
repository. Files are extracted (NOT stored as opaque archives) into
addons-src/<addon-id>, preserving original authors, licenses and sources.

Existing addons-src directories are NEVER overwritten. To update or modify
an add-on, edit its local files and bump version in its addon.xml.
"""
from __future__ import annotations

import hashlib
from io import BytesIO
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
DESTINATION = ROOT / "addons-src"
OFFICIAL = "https://raw.githubusercontent.com/matke-84/repository.bingie/main/omega"

# source version, version of our independently editable fork
SOURCES = {
    "script.bingie.helper": ("1.1.2", "1.1.3"),
    "script.bingie.toolbox": ("1.0.0", "1.0.1"),
    "script.bingie.widgets": ("1.0.1", "1.0.2"),
    "plugin.video.tmdb.bingie.helper": ("1.0.3", "1.0.4"),
    "plugin.program.autocompletion": ("2.1.3", "2.1.4"),
    "script.module.bingie": ("1.0.1", "1.0.2"),
}
MAX_ZIP_BYTES = 15 * 1024 * 1024
MAX_UNPACK_BYTES = 60 * 1024 * 1024


def fetch_zip(addon_id: str, version: str) -> bytes:
    name = f"{addon_id}-{version}.zip"
    url = f"{OFFICIAL}/{addon_id}/{name}"
    with urlopen(Request(url, headers={"User-Agent": "ntls2000-bingie-addon-import"}), timeout=120) as response:
        payload = response.read(MAX_ZIP_BYTES + 1)
    if len(payload) > MAX_ZIP_BYTES:
        raise ValueError(f"ZIP too large: {addon_id}")
    print(f"Upstream {addon_id} {version}: {len(payload):,} bytes, sha256={hashlib.sha256(payload).hexdigest()}")
    return payload


def extract_safe(addon_id: str, payload: bytes, output: Path):
    size = 0
    with ZipFile(BytesIO(payload)) as archive:
        for item in archive.infolist():
            archive_path = PurePosixPath(item.filename)
            components = archive_path.parts
            if not components or components[0] != addon_id:
                raise ValueError(f"{addon_id}: unexpected entry {item.filename!r}")
            if len(components) < 2 or any(p in (".", "..") for p in components):
                if item.is_dir() and len(components) == 1:
                    continue
                raise ValueError(f"{addon_id}: unsafe entry {item.filename!r}")
            unix_mode = item.external_attr >> 16
            if stat.S_IFMT(unix_mode) == stat.S_IFLNK:
                raise ValueError(f"{addon_id}: symlink is not allowed")
            size += item.file_size
            if size > MAX_UNPACK_BYTES:
                raise ValueError(f"{addon_id}: uncompressed ZIP exceeds maximum")
            target = output.joinpath(*components[1:])
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(item) as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)


def import_one(addon_id: str, source_version: str, fork_version: str):
    target = DESTINATION / addon_id
    if target.exists():
        print(f"SKIP {addon_id}: local source exists; will not overwrite modifications")
        return
    payload = fetch_zip(addon_id, source_version)
    with tempfile.TemporaryDirectory(prefix="bingie-import-") as scratch:
        staging = Path(scratch) / addon_id
        staging.mkdir()
        extract_safe(addon_id, payload, staging)
        manifest_path = staging / "addon.xml"
        addon = ET.parse(manifest_path).getroot()
        if addon.get("id") != addon_id or addon.get("version") != source_version:
            raise ValueError(f"{addon_id}: expected ID/version {source_version}; got {addon.attrib}")
        metadata = addon.find("./extension[@point='xbmc.addon.metadata']")
        if metadata is None or not metadata.findtext("license"):
            raise ValueError(f"{addon_id}: upstream license metadata is missing; review redistribution first")
        old_provider = addon.get("provider-name", "")
        addon.set("provider-name", f"{old_provider}, ntls2000" if old_provider else "ntls2000")
        addon.set("version", fork_version)
        ET.indent(addon, space="    ")
        ET.ElementTree(addon).write(manifest_path, encoding="utf-8", xml_declaration=True)
        # Store the origin and intact upstream version in a separate text file.
        (staging / "UPSTREAM-ORIGIN.txt").write_text(
            f"Source: {OFFICIAL}/{addon_id}/{addon_id}-{source_version}.zip\n"
            f"Original version: {source_version}\n"
            f"Fork release version: {fork_version}\n"
            f"Upstream ZIP SHA256: {hashlib.sha256(payload).hexdigest()}\n"
            "Original credits, license notices and bundled source files are retained.\n",
            encoding="utf-8",
        )
        DESTINATION.mkdir(exist_ok=True)
        shutil.move(str(staging), str(target))
    print(f"Imported {addon_id} into editable source folder {target.relative_to(ROOT)}")


def main():
    for addon_id, (source_version, fork_version) in SOURCES.items():
        import_one(addon_id, source_version, fork_version)
    print("Editable add-on sources ready. Build with python3 tools/build_kodi_repo.py")


if __name__ == "__main__":
    main()
