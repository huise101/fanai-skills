#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify complete pinned upstream snapshots, without executing or downloading them."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

SOURCES = {
    "anti-defensive-writing-Skill": {
        "url": "https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill",
        "commit": "e65bd9d8bf8ed8b9af809e5aff8237d76370876d",
        "file_count": 14,
    },
    "academic-humanizer": {
        "url": "https://github.com/AIScientists-Dev/academic-humanizer",
        "commit": "94b88b23703bed7df507acae7d6d5876209a0cdf",
        "file_count": 10,
    },
    "noai-flavor": {
        "url": "https://github.com/yiancode/noai-flavor",
        "commit": "ae232f32bb7a3e7ff310b8bccceaeaf60dbc25d8",
        "file_count": 48,
    },
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(path: str) -> bool:
    item = PurePosixPath(path)
    return bool(path) and not item.is_absolute() and ".." not in item.parts and "\\" not in path


def verify_bundle(skill: Path) -> list[str]:
    base = skill / "upstream"
    manifest_path = base / "manifest.json"
    if not manifest_path.is_file():
        return ["Missing complete upstream manifest"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        return [f"Invalid upstream manifest: {exc}"]
    errors = []
    entries = manifest.get("sources", [])
    if {x.get("name") for x in entries} != set(SOURCES) or len(entries) != len(SOURCES):
        return ["Upstream source set must contain the three pinned unique projects"]
    mirrored = set()
    archives = set()
    all_originals = set()
    for source in entries:
        name = source["name"]
        expected = SOURCES[name]
        if source.get("commit") != expected["commit"] or source.get("url") != expected["url"]:
            errors.append(f"{name}: source identity/version mismatch")
        files = source.get("files", [])
        if len(files) != expected["file_count"] or len({f.get("path") for f in files}) != len(files):
            errors.append(f"{name}: incomplete or duplicate original-file inventory")
        archive_rel = source.get("archive", {}).get("path", "")
        if not safe_path(archive_rel):
            errors.append(f"{name}: unsafe archive path")
            continue
        archives.add(archive_rel)
        archive_path = base / archive_rel
        if not archive_path.is_file():
            errors.append(f"{name}: missing original snapshot ZIP")
            continue
        if digest(archive_path.read_bytes()) != source["archive"].get("sha256"):
            errors.append(f"{name}: snapshot ZIP checksum mismatch")
        try:
            with zipfile.ZipFile(archive_path) as archive:
                if archive.testzip() is not None:
                    errors.append(f"{name}: corrupt snapshot ZIP")
                if set(archive.namelist()) != {f.get("path") for f in files}:
                    errors.append(f"{name}: ZIP does not contain exactly the tracked original files")
                for item in files:
                    original = item.get("path", "")
                    mirror = item.get("mirror", "")
                    if not safe_path(original) or not safe_path(mirror):
                        errors.append(f"{name}: unsafe original/mirror path")
                        continue
                    all_originals.add(f"{name}/{original}")
                    mirrored.add(mirror)
                    data = archive.read(original)
                    if digest(data) != item.get("sha256") or len(data) != item.get("bytes"):
                        errors.append(f"{name}/{original}: original bytes mismatch")
                    actual_blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
                    if actual_blob != item.get("git_blob"):
                        errors.append(f"{name}/{original}: original Git blob mismatch")
                    path = base / mirror
                    if not path.is_file() or digest(path.read_bytes()) != item.get("mirror_sha256"):
                        errors.append(f"{name}/{original}: browsable mirror missing/changed")
                    transformations = item.get("mirror_transformations")
                    if not isinstance(transformations, list) or item.get("mirror_modified") != bool(transformations):
                        errors.append(f"{name}/{original}: missing/inconsistent mirror transformation log")
                    elif any(t.get("kind") not in {"rename-entry", "renamed-skill-link", "upstream-link-repair"}
                             or not t.get("from") or not t.get("to") for t in transformations):
                        errors.append(f"{name}/{original}: invalid mirror transformation record")
                    if item.get("role") not in {"rule", "example", "documentation", "asset", "license", "tooling"}:
                        errors.append(f"{name}/{original}: unclassified coverage")
                    if item.get("role") == "rule" and not item.get("read_groups"):
                        errors.append(f"{name}/{original}: rule missing an applicable reading group")
                    for group in item.get("read_groups", []):
                        if mirror not in manifest.get("reading_groups", {}).get(group, []):
                            errors.append(f"{name}/{original}: declared reading group lacks this source")
        except (OSError, KeyError, zipfile.BadZipFile) as exc:
            errors.append(f"{name}: archive error: {exc}")
    for group, paths in manifest.get("reading_groups", {}).items():
        if not paths:
            errors.append(f"Empty reading group: {group}")
        for path in paths:
            if path not in mirrored:
                errors.append(f"Reading group {group}: missing source mirror {path}")
    expected_count = sum(s["file_count"] for s in SOURCES.values())
    rule_count = sum(f.get("role") == "rule" for s in entries for f in s.get("files", []))
    if len(all_originals) != expected_count or len(mirrored) != expected_count:
        errors.append("Original/mirror coverage is incomplete or colliding")
    expected_coverage = {"source_count": 3, "original_files": expected_count,
                         "rule_files": rule_count, "archive_count": 3}
    if manifest.get("coverage") != expected_coverage:
        errors.append("Coverage summary differs from the verified source inventory")
    actual = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
    expected_files = mirrored | archives | {"manifest.json"}
    if actual != expected_files:
        errors.append("Upstream directory differs from the exhaustive manifest")
    for group in {"academic", "proposal", "writing", "web", "common-text", "anti-zh", "anti-en",
                  "wechat", "zhihu", "xiaohongshu", "text-examples", "web-examples"}:
        if group not in manifest.get("reading_groups", {}):
            errors.append(f"Missing required reading group: {group}")
    return errors
