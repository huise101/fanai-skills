#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Install a local, reviewed skill. No network, dependencies, or config edits."""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from validate import NAME, SKILL, validate_skill, validate_tree


def default_target(kind: str) -> Path:
    home = Path.home()
    bases = {
        "agents": home / ".agents" / "skills",
        "pi": Path(os.environ.get("PI_CODING_AGENT_DIR", home / ".pi" / "agent")).expanduser() / "skills",
        "codex": Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser() / "skills",
        "claude": home / ".claude" / "skills",
    }
    return bases[kind] / NAME


def file_map(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file()}


def install(source: Path, target: Path, replace: bool = False) -> dict:
    source = source.resolve()
    target = target.expanduser()
    if target.is_symlink():
        raise ValueError("Refusing to replace a symlink destination")
    target = target.resolve()
    if target.name != NAME:
        raise ValueError(f"Destination must end with {NAME}")
    if source != target and (target.is_relative_to(source) or source.is_relative_to(target)):
        raise ValueError("Source and destination must not contain each other")
    errors = validate_skill(source) + validate_tree(source)
    if errors:
        raise ValueError("Source validation failed: " + "; ".join(errors))
    if target.exists():
        if not target.is_dir():
            raise ValueError("Destination exists and is not a directory")
        if any(p.is_symlink() for p in target.rglob("*")):
            raise ValueError("Destination contains a symlink; inspect it manually")
        if file_map(source) == file_map(target):
            return {"target": target, "changed": False, "backup": None}
        if not replace:
            raise ValueError("Different content already installed; review it before using --replace")
    target.parent.mkdir(parents=True, exist_ok=True)
    # Staging and backups sit outside skills/, preventing duplicate discovery.
    workspace = Path(tempfile.mkdtemp(prefix=".fanai-skills-install-", dir=target.parent.parent))
    stage = workspace / NAME
    backup = None
    try:
        shutil.copytree(source, stage)
        errors = validate_skill(stage) + validate_tree(stage)
        if errors or file_map(source) != file_map(stage):
            raise ValueError("Staging validation or byte-for-byte comparison failed")
        if target.is_symlink():
            raise ValueError("Destination became a symlink during staging")
        if target.exists():
            if not target.is_dir():
                raise ValueError("Destination changed during staging")
            if not replace:
                if file_map(source) == file_map(target):
                    return {"target": target, "changed": False, "backup": None}
                raise ValueError("Destination appeared during staging; refusing to overwrite")
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = target.parent.parent / "skill-backups" / f"{NAME}-{stamp}-{uuid.uuid4().hex[:8]}"
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
        try:
            stage.rename(target)
        except OSError:
            if backup is not None and not target.exists():
                backup.rename(target)
            raise
        return {"target": target, "changed": True, "backup": backup}
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--target", choices=("agents", "pi", "codex", "claude"), default="agents")
    group.add_argument("--path", type=Path, help=f"Full destination ending in {NAME}")
    parser.add_argument("--replace", action="store_true", help="Back up and replace differing content")
    args = parser.parse_args()
    try:
        result = install(SKILL, args.path if args.path else default_target(args.target), args.replace)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1
    print(("Installed: " if result["changed"] else "Already identical: ") + str(result["target"]))
    if result["backup"]:
        print("Previous installation preserved at: " + str(result["backup"]))
    print("Restart your tool or use /reload in Pi. No other skills/configuration were changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
