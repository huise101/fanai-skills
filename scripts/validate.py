#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline structural checks; not a prose-quality or AI-detector evaluation."""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from source_bundle import verify_bundle

NAME = "fanai-skills"
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / NAME
SKIP = {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules", "dist"}
REFERENCES = {"academic", "proposal", "writing", "web", "patterns", "examples",
              "reading-map", "acceptance-checklist", "conflicts"}
LICENSES = {
    "MIT.txt", "CC-BY-4.0.txt", "anti-defensive-writing-Skill.txt",
    "academic-humanizer.txt", "noai-flavor.txt", "humanizer.txt",
}


def text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if any(part in SKIP for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.suffix.lower() not in {".zip", ".png", ".jpg", ".pdf"}:
            yield path


def validate_skill(skill: Path) -> list[str]:
    errors = []
    if skill.name != NAME:
        errors.append(f"Skill directory must be named {NAME}")
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return errors + ["Missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        return errors + ["Frontmatter must use LF and --- delimiters"]
    front = match.group(1)
    name = re.search(r"^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$", front, re.M)
    if not name or name.group(1) != NAME:
        errors.append("Invalid or mismatched frontmatter name")
    # This project uses single-line JSON-compatible quoted YAML strings.
    for field in ("description", "license"):
        line = re.search(rf"^{field}: (.+)$", front, re.M)
        try:
            value = json.loads(line.group(1)) if line else None
        except (ValueError, TypeError):
            value = None
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Missing or invalid quoted {field}")
        if field == "description" and isinstance(value, str) and len(value) > 1024:
            errors.append("Description exceeds 1024 characters")
    if len(text.splitlines()) > 200:
        errors.append("Entry is too long; move details into references")
    if "../ccf-" in text or "ccf_skill_controls" in text:
        errors.append("Standalone skill must not require installed CCFA siblings")
    required = [skill / "NOTICE.md", skill / "agents" / "openai.yaml",
                skill / "scripts" / "check_invariants.py"]
    required += [skill / "references" / f"{ref}.md" for ref in REFERENCES]
    required += [skill / "licenses" / item for item in LICENSES]
    for path in required:
        if not path.is_file():
            errors.append(f"Missing {path.relative_to(skill).as_posix()}")
    ui = skill / "agents" / "openai.yaml"
    if ui.is_file():
        value = ui.read_text(encoding="utf-8")
        if 'display_name: "反aiskills"' not in value or "$fanai-skills" not in value:
            errors.append("UI name/default prompt is not synchronized")
    links = list(skill.rglob("*"))
    if any(path.is_symlink() for path in links):
        errors.append("Skill package must contain no symbolic links")
    if len(list(skill.rglob("SKILL.md"))) != 1:
        errors.append("Package must contain exactly one executable SKILL.md")
    errors.extend(verify_bundle(skill))
    return errors


def validate_tree(root: Path) -> list[str]:
    errors = []
    home_windows = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+", re.I)
    home_unix = re.compile(r"/(?:home|Users)/[^/\s]+/")
    drive_path = re.compile(r"[A-Za-z]:[\\/](?!/)")
    link_pattern = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")
    for path in text_files(root):
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{rel}: not UTF-8")
            continue
        if data.startswith(b"\xef\xbb\xbf") or "\ufffd" in text or "\x00" in text:
            errors.append(f"{rel}: BOM, replacement character, or NUL detected")
        if home_windows.search(text) or home_unix.search(text) or drive_path.search(text):
            errors.append(f"{rel}: machine-specific absolute path detected")
        # Upstream scripts are reference data, not executable package code.
        archived = "upstream" in path.relative_to(root).parts
        if not archived and path.suffix == ".py":
            try:
                ast.parse(text, filename=rel)
            except SyntaxError as exc:
                errors.append(f"{rel}: {exc}")
        if path.suffix != ".md":
            continue
        if not archived and re.search(r"\[TODO\b|\bTODO:", text):
            errors.append(f"{rel}: unfinished template")
        for raw in link_pattern.findall(text):
            dest = raw.strip().split(" \"", 1)[0].strip("<>")
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#)", dest, re.I):
                continue
            dest = unquote(dest.split("#", 1)[0])
            resolved = (path.parent / dest).resolve()
            if not resolved.is_relative_to(root.resolve()):
                errors.append(f"{rel}: link escapes package: {dest}")
            elif not resolved.exists():
                errors.append(f"{rel}: missing local link: {dest}")
    return errors


def validate_repository(root: Path) -> list[str]:
    errors = validate_skill(root / "skills" / NAME) + validate_tree(root)
    for name in ("README.md", "AGENTS.md", "LICENSE", ".gitignore", ".gitattributes", "scripts/install.py",
                 "scripts/build_release.py", "scripts/source_bundle.py", "scripts/sync_sources.py",
                 "tests/test_package.py", "tests/test_invariants.py", ".github/workflows/validate.yml"):
        if not (root / name).is_file():
            errors.append(f"Missing repository file: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, help="Check one installed skill only")
    args = parser.parse_args()
    try:
        errors = (validate_skill(args.skill_dir) + validate_tree(args.skill_dir)
                  if args.skill_dir else validate_repository(ROOT))
    except (OSError, UnicodeError) as exc:
        errors = [str(exc)]
    if errors:
        for item in errors:
            print(f"FAIL: {item}", file=sys.stderr)
        return 1
    print("PASS: structure, local links, licenses, encoding, and path-privacy checks")
    print("No model-behavior or detector-performance claim is made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
