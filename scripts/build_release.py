#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build a deterministic, validated source ZIP without local/cache files."""
from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import zipfile
from pathlib import Path

from validate import ROOT, SKIP, validate_repository


def release_files(root: Path) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Do not release symlinks: {rel}")
        if path.is_file():
            if rel.parts[0] not in {"skills", "scripts", "tests", ".github", "README.md", "LICENSE", ".gitignore"}:
                raise ValueError(f"Unexpected release file; inspect it: {rel}")
            files.append(path)
    return files


def build(root: Path) -> tuple[Path, str, int]:
    errors = validate_repository(root)
    if errors:
        raise ValueError("Release validation failed: " + "; ".join(errors))
    files = release_files(root)
    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    destination = dist / "fanai-skills-github.zip"
    fd, name = tempfile.mkstemp(prefix=".fanai-release-", suffix=".zip", dir=dist)
    os.close(fd)
    temporary = Path(name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                entry = zipfile.ZipInfo("fanai-skills/" + path.relative_to(root).as_posix(), (2026, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(entry, path.read_bytes())
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise ValueError("ZIP integrity test failed")
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        temporary.replace(destination)
        (dist / "fanai-skills-github.sha256").write_text(
            digest + "  " + destination.name + "\n", encoding="utf-8")
    finally:
        if temporary.exists():
            temporary.unlink()
    return destination, digest, len(files)


def main() -> int:
    try:
        path, digest, count = build(ROOT)
    except (OSError, ValueError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Built {path} ({count} files)")
    print("SHA256 " + digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
