# SPDX-License-Identifier: MIT
"""Deterministic packaging/installation tests, not model-behavior tests."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_release
import install
import validate


class StructureTests(unittest.TestCase):
    def test_repository_structure(self):
        self.assertEqual(validate.validate_repository(ROOT), [])

    def test_standalone_skill(self):
        self.assertEqual(validate.validate_skill(validate.SKILL), [])
        self.assertEqual(validate.validate_tree(validate.SKILL), [])

    def test_missing_license_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / validate.NAME
            shutil.copytree(validate.SKILL, copy)
            (copy / "licenses" / "noai-flavor.txt").unlink()
            self.assertTrue(any("noai-flavor" in e for e in validate.validate_skill(copy)))

    def test_broken_link_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.md"
            path.write_text("[missing](missing.md)\n", encoding="utf-8")
            self.assertTrue(any("missing local link" in e for e in validate.validate_tree(path.parent)))

    def test_non_utf8_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.md"
            path.write_bytes(bytes([0xff, 0xfe, 0x61]))
            self.assertTrue(any("not UTF-8" in e for e in validate.validate_tree(path.parent)))

    def test_default_targets_honor_environment(self):
        with patch.dict(os.environ, {"CODEX_HOME": "codex-test", "PI_CODING_AGENT_DIR": "pi-test"}):
            self.assertEqual(install.default_target("codex"), Path("codex-test/skills/fanai-skills"))
            self.assertEqual(install.default_target("pi"), Path("pi-test/skills/fanai-skills"))
            self.assertEqual(install.default_target("agents"), Path.home() / ".agents/skills/fanai-skills")


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="fanai-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source" / validate.NAME
        self.target = self.root / "tool" / "skills" / validate.NAME
        shutil.copytree(validate.SKILL, self.source)

    def test_install_preserves_all_bytes_and_notices(self):
        result = install.install(self.source, self.target)
        self.assertTrue(result["changed"])
        self.assertEqual(install.file_map(self.source), install.file_map(self.target))
        self.assertTrue((self.target / "licenses" / "CC-BY-4.0.txt").is_file())

    def test_identical_reinstall_does_not_write(self):
        install.install(self.source, self.target)
        before = (self.target / "SKILL.md").stat().st_mtime_ns
        result = install.install(self.source, self.target)
        self.assertFalse(result["changed"])
        self.assertEqual((self.target / "SKILL.md").stat().st_mtime_ns, before)

    def test_differing_install_requires_explicit_replace(self):
        install.install(self.source, self.target)
        extra = self.target / "user-note.txt"
        extra.write_text("keep this", encoding="utf-8")
        before = install.file_map(self.target)
        with self.assertRaises(ValueError):
            install.install(self.source, self.target)
        self.assertEqual(install.file_map(self.target), before)

    def test_explicit_replace_keeps_backup_outside_skills(self):
        install.install(self.source, self.target)
        (self.target / "user-note.txt").write_text("old custom content", encoding="utf-8")
        before = install.file_map(self.target)
        result = install.install(self.source, self.target, replace=True)
        self.assertTrue(result["backup"].is_dir())
        self.assertFalse(result["backup"].is_relative_to(self.target.parent))
        self.assertEqual(install.file_map(result["backup"]), before)
        self.assertEqual(install.file_map(self.target), install.file_map(self.source))

    def test_failed_swap_restores_old_installation(self):
        install.install(self.source, self.target)
        (self.target / "user-note.txt").write_text("old content", encoding="utf-8")
        before = install.file_map(self.target)
        original = Path.rename

        def fail_stage(path, destination):
            if path.parent.name.startswith(".fanai-skills-install-"):
                raise OSError("simulated swap failure")
            return original(path, destination)

        with patch.object(Path, "rename", fail_stage):
            with self.assertRaises(OSError):
                install.install(self.source, self.target, replace=True)
        self.assertEqual(install.file_map(self.target), before)
        self.assertEqual(list(self.target.parent.parent.glob(".fanai-skills-install-*")), [])

    def test_other_skills_are_untouched(self):
        other = self.target.parent / "unrelated" / "SKILL.md"
        other.parent.mkdir(parents=True)
        other.write_text("unrelated content", encoding="utf-8")
        install.install(self.source, self.target)
        self.assertEqual(other.read_text(encoding="utf-8"), "unrelated content")

    def test_concurrent_destination_is_not_overwritten(self):
        original = shutil.copytree

        def copy_then_concurrent_install(source, destination, *args, **kwargs):
            result = original(source, destination, *args, **kwargs)
            if Path(source) == self.source:
                self.target.mkdir(parents=True)
                (self.target / "concurrent.txt").write_text("preserve", encoding="utf-8")
            return result

        with patch.object(install.shutil, "copytree", copy_then_concurrent_install):
            with self.assertRaises(ValueError):
                install.install(self.source, self.target)
        self.assertEqual((self.target / "concurrent.txt").read_text(encoding="utf-8"), "preserve")

    def test_rejects_wrong_directory_name(self):
        with self.assertRaises(ValueError):
            install.install(self.source, self.target.with_name("wrong-name"))

    def test_rejects_destination_inside_source(self):
        with self.assertRaises(ValueError):
            install.install(self.source, self.source / "nested" / validate.NAME)

    def test_rejects_file_destination(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_text("not a directory", encoding="utf-8")
        with self.assertRaises(ValueError):
            install.install(self.source, self.target, replace=True)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "not a directory")

    def test_rejects_symlink_destination(self):
        self.target.parent.mkdir(parents=True)
        actual = self.root / "real"
        actual.mkdir()
        try:
            self.target.symlink_to(actual, target_is_directory=True)
        except OSError:
            self.skipTest("Creating symlinks requires privileges on this system")
        with self.assertRaises(ValueError):
            install.install(self.source, self.target, replace=True)


class ReleaseTests(unittest.TestCase):
    def test_release_is_reproducible_and_has_no_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(*validate.SKIP))
            first, digest, count = build_release.build(copy)
            data = first.read_bytes()
            second, other_digest, other_count = build_release.build(copy)
            self.assertEqual(data, second.read_bytes())
            self.assertEqual(digest, other_digest)
            self.assertEqual(count, other_count)
            with zipfile.ZipFile(second) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn("fanai-skills/skills/fanai-skills/SKILL.md", archive.namelist())
                self.assertIn("fanai-skills/skills/fanai-skills/NOTICE.md", archive.namelist())
                self.assertFalse(any("__pycache__" in n or "/.git/" in n or "/dist/" in n
                                     for n in archive.namelist()))


if __name__ == "__main__":
    unittest.main()
