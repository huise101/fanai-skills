#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compare text invariants offline; never rewrite files or infer scientific validity."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import sys
from pathlib import Path

# CJK prose often has no spaces before numbers; ASCII unit suffixes are also valid.
NUMBER = re.compile(r"(?<![A-Za-z0-9_.])[-+−]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?:\s*%)?(?![0-9.])")
CITE = re.compile(r"\\(?:[A-Za-z]*cite[A-Za-z]*\*?)(?:\[[^\]]*\])*\{([^}]*)\}")
REFERENCE = re.compile(r"\\(?:[A-Za-z]*ref\*?)\{([^}]*)\}")
MATH = re.compile(
    r"\$\$(.*?)\$\$|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$|"
    r"\\\((.*?)\\\)|\\\[(.*?)\\\]|"
    r"\\begin\{(equation\*?|align\*?|gather\*?)\}(.*?)\\end\{\5\}", re.S)


def extract(text: str) -> dict[str, Counter]:
    citations = Counter(key.strip() for match in CITE.findall(text) for key in match.split(",") if key.strip())
    refs = Counter(key.strip() for key in REFERENCE.findall(text))
    math = Counter()
    for match in MATH.finditer(text):
        groups = match.groups()
        body = next((groups[n] for n in (0, 1, 2, 3, 5) if groups[n] is not None), "")
        math[re.sub(r"\s+", "", body)] += 1
    numbers = Counter(re.sub(r"\s+", "", m.group(0)) for m in NUMBER.finditer(text))
    return {"numbers": numbers, "citation_keys": citations, "cross_reference_keys": refs, "math_expressions": math}


def compare(before: str, after: str) -> dict:
    left, right = extract(before), extract(after)
    changes = {}
    for category in left:
        removed, added = left[category] - right[category], right[category] - left[category]
        if removed or added:
            changes[category] = {"removed": dict(removed), "added": dict(added)}
    return {"status": "differences_need_review" if changes else "no_detected_invariant_changes",
            "changes": changes,
            "limits": "Checks numeric literals and recognized LaTeX citations/references/math only. Does not verify units, prose meaning, evidence, disclosure, Word/PDF objects, or authorized-change intent."}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path, help="UTF-8 original text/Markdown/LaTeX")
    parser.add_argument("after", type=Path, help="UTF-8 revised text/Markdown/LaTeX")
    args = parser.parse_args()
    result = compare(args.before.read_text(encoding="utf-8-sig"), args.after.read_text(encoding="utf-8-sig"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["changes"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
