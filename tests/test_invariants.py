# SPDX-License-Identifier: MIT
"""Tests for limited invariant detection; no model or detector evaluation."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "fanai-skills" / "scripts"))
import check_invariants


class InvariantTests(unittest.TestCase):
    def test_preserved_facts_pass_after_prose_cleanup(self):
        before = r"In recent years, accuracy is 84.2% versus 81.0% (Table 2) \cite{base2024}."
        after = r"Accuracy is 84.2% versus 81.0% (Table 2) \cite{base2024}."
        self.assertEqual(check_invariants.compare(before, after)["changes"], {})

    def test_changed_number_is_flagged(self):
        result = check_invariants.compare("Accuracy 84.2%", "Accuracy 94.2%")
        self.assertIn("84.2%", result["changes"]["numbers"]["removed"])
        self.assertIn("94.2%", result["changes"]["numbers"]["added"])

    def test_changed_number_next_to_chinese_text_is_flagged(self):
        result = check_invariants.compare("准确率84.2%", "准确率94.2%")
        self.assertEqual(result["changes"]["numbers"]["removed"], {"84.2%": 1})

    def test_changed_number_without_space_before_unit_is_flagged(self):
        result = check_invariants.compare("质量22.19dB", "质量20.61dB")
        self.assertEqual(result["changes"]["numbers"]["removed"], {"22.19": 1})

    def test_missing_citation_key_is_flagged(self):
        result = check_invariants.compare(r"\cite{alpha,beta}", r"\cite{alpha}")
        self.assertEqual(result["changes"]["citation_keys"]["removed"], {"beta": 1})

    def test_optional_citation_arguments_and_key_order(self):
        result = check_invariants.compare(r"\citep[see][p. X]{alpha,beta}", r"\cite{beta,alpha}")
        self.assertEqual(result["changes"], {})

    def test_duplicate_citation_loss_is_flagged(self):
        result = check_invariants.compare(r"\cite{alpha} and \cite{alpha}", r"\cite{alpha}")
        self.assertEqual(result["changes"]["citation_keys"]["removed"], {"alpha": 1})

    def test_cross_reference_loss_is_flagged(self):
        result = check_invariants.compare(r"Eq. \eqref{eq:method}", "the method")
        self.assertEqual(result["changes"]["cross_reference_keys"]["removed"], {"eq:method": 1})

    def test_math_symbol_change_is_flagged(self):
        result = check_invariants.compare(r"$w_t=x+y$", r"$w_t=x-y$")
        self.assertIn("math_expressions", result["changes"])

    def test_math_whitespace_change_is_not_a_fact_change(self):
        self.assertEqual(check_invariants.compare(r"$x + y$", r"$x+y$")["changes"], {})

    def test_equation_environment_change_is_flagged(self):
        result = check_invariants.compare(r"\begin{equation}x+y\end{equation}",
                                          r"\begin{equation}x-y\end{equation}")
        self.assertIn("math_expressions", result["changes"])

    def test_utf8_command_line_returns_failure_for_changed_cjk_number(self):
        with tempfile.TemporaryDirectory() as directory:
            before = Path(directory) / "before.tex"
            after = Path(directory) / "after.tex"
            before.write_text("准确率84.2%", encoding="utf-8")
            after.write_text("准确率94.2%", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(Path(check_invariants.__file__)),
                                     str(before), str(after)], capture_output=True)
            self.assertEqual(result.returncode, 1)
            parsed = json.loads(result.stdout.decode("utf-8"))
            self.assertIn("numbers", parsed["changes"])

    def test_explicitly_reports_semantic_limits(self):
        result = check_invariants.compare("may help; not evaluated", "proves superiority")
        self.assertEqual(result["changes"], {})
        self.assertIn("Does not verify", result["limits"])
        self.assertNotIn("passed", result["status"])


if __name__ == "__main__":
    unittest.main()
