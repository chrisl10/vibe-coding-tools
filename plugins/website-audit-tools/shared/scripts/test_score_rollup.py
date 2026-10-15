#!/usr/bin/env python3
"""Tests for score-rollup.py. Run: python3 test_score_rollup.py (standard library only)."""

import contextlib
import importlib.util
import io
import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("score_rollup", HERE / "score-rollup.py")
sr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sr)

SKILL = HERE.parent.parent / "skills" / "audit-scoring-stinger" / "references"
TEMPLATE = SKILL / "templates" / "website-audit-scorecard-template.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

# An N/A ("N/A" text, blank, or non-number) child is masked out of BOTH the numerator and the
# denominator, and an all-N/A input shows "N/A" instead of #DIV/0!. Same math as _weighted().
MASKED_ROLLUP = re.compile(
    r'^IF\(SUMPRODUCT\(--ISNUMBER\((?P<v>[^()]+)\),(?P<w>[^()]+)\)=0,"N/A",'
    r'SUMPRODUCT\(--ISNUMBER\((?P=v)\),(?P=v),(?P=w)\)'
    r'/SUMPRODUCT\(--ISNUMBER\((?P=v)\),(?P=w)\)\)$'
)
LEAF_ROLLUP = re.compile(
    r'^IF\(SUMPRODUCT\(ISNUMBER\((?P<s>E\d+:E\d+)\)\*\((?P=s)>0\),(?P<w>H\d+:H\d+)\)=0,"N/A",'
    r'SUMPRODUCT\(ISNUMBER\((?P=s)\)\*\((?P=s)>0\),(?P=s),(?P=w)\)'
    r'/\(6\*SUMPRODUCT\(ISNUMBER\((?P=s)\)\*\((?P=s)>0\),(?P=w)\)\)\)$'
)


def sheet_formulas(xlsx: Path, sheet: str) -> dict:
    """Cell ref -> formula text (no leading '=') for one sheet, read with the standard library."""
    with zipfile.ZipFile(xlsx) as z:
        book = ET.fromstring(z.read("xl/workbook.xml"))
        rid = next(s.get(REL) for s in book.iterfind("m:sheets/m:sheet", NS) if s.get("name") == sheet)
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = next(r.get("Target") for r in rels if r.get("Id") == rid).lstrip("/")
        part = target if target.startswith("xl/") else f"xl/{target}"
        root = ET.fromstring(z.read(part))
    return {c.get("r"): c.find("m:f", NS).text
            for c in root.iterfind("m:sheetData/m:row/m:c", NS) if c.find("m:f", NS) is not None}


def leaf(cat, sub, n, score, **extra):
    row = {
        "leaf_id": f"{cat.upper()}-{sub.upper()}-{n:02d}",
        "category_key": cat,
        "subaudit_key": sub,
        "description": "example checkpoint",
        "score": score,
        "evidence_pointer": "07-security/headers-scan.md#L14",
        "justification": "observed in the captured response",
        "originating_bee": "web-security-posture-wasp-drone",
    }
    row.update(extra)
    return row


def template_demo(rubric):
    """The generator's illustrative data: per sub-audit [6, 6, 6, 0], first security leaf scored 1."""
    rows = []
    for cat in rubric["order"]:
        for sub in rubric["categories"][cat]["subaudits"]:
            for n, score in enumerate([6, 6, 6, 0], start=1):
                rows.append(("demo", leaf(cat, sub, n, score)))
    rows[0][1]["score"] = 1
    return rows


class ScoreRollupTest(unittest.TestCase):
    def setUp(self):
        self.rubric = sr.check_rubric(sr.default_rubric())

    def test_default_rubric_matches_generator_shape(self):
        self.assertEqual(self.rubric["order"], [
            "security", "revenue", "mission", "analytics",
            "technical", "foundational", "search", "content",
        ])
        self.assertEqual(sum(c["weight"] for c in self.rubric["categories"].values()), 100)
        self.assertAlmostEqual(self.rubric["cap"], 0.7699)
        self.assertEqual(self.rubric["categories"]["revenue"]["subaudits"]["visual_ux"], 7)
        self.assertAlmostEqual(self.rubric["categories"]["security"]["subaudits"]["headers"], 2.8571)

    def test_reproduces_documented_template_demo(self):
        # guides/01 section 5 and guides/02 section 6: security 96.03%, raw 99.2%, capped to C.
        result = sr.rollup(template_demo(self.rubric), self.rubric)
        self.assertAlmostEqual(result["categories"]["security"]["pct"], 0.9603, places=4)
        self.assertAlmostEqual(result["categories"]["revenue"]["pct"], 1.0)
        self.assertAlmostEqual(result["final_raw_pct"], 0.992, places=3)
        self.assertTrue(result["override_active"])
        self.assertEqual(result["override_triggers"], ["SECURITY-HEADERS-01"])
        self.assertAlmostEqual(result["effective_pct"], 0.7699)
        self.assertEqual(result["letter_grade"], "C")
        self.assertEqual(result["rejected"], [])

    def test_na_leaf_excluded_from_both_sides(self):
        rows = [("t", leaf("revenue", "visual_ux", 1, 6)), ("t", leaf("revenue", "visual_ux", 2, 0))]
        result = sr.rollup(rows, self.rubric)
        self.assertAlmostEqual(result["categories"]["revenue"]["subaudits"]["visual_ux"]["pct"], 1.0)

    def test_na_subaudits_and_categories_are_reported_and_excluded(self):
        rows = [("t", leaf("revenue", "visual_ux", 1, 3))]
        result = sr.rollup(rows, self.rubric)
        self.assertAlmostEqual(result["categories"]["revenue"]["pct"], 0.5)
        self.assertAlmostEqual(result["final_raw_pct"], 0.5)
        self.assertIn("revenue.nav_journey", result["na_subaudits"])
        self.assertIn("security", result["na_categories"])
        self.assertEqual(result["letter_grade"], "F")

    def test_override_is_a_ceiling_not_a_floor(self):
        rows = [("t", leaf("security", "headers", 1, 1)), ("t", leaf("revenue", "visual_ux", 1, 2))]
        result = sr.rollup(rows, self.rubric)
        self.assertTrue(result["override_active"])
        self.assertLess(result["final_raw_pct"], 0.7699)
        self.assertEqual(result["effective_pct"], result["final_raw_pct"])

    def test_non_security_one_does_not_trigger_override(self):
        rows = [("t", leaf("revenue", "visual_ux", 1, 1)), ("t", leaf("security", "headers", 1, 6))]
        self.assertFalse(sr.rollup(rows, self.rubric)["override_active"])

    def test_override_can_be_disabled(self):
        raw = sr.default_rubric()
        raw["security_override_enabled"] = False
        rubric = sr.check_rubric(raw)
        rows = [("t", leaf("security", "headers", 1, 1)), ("t", leaf("security", "headers", 2, 6))]
        self.assertFalse(sr.rollup(rows, rubric)["override_active"])

    def test_malformed_findings_are_rejected_not_scored(self):
        bad = [
            ("t", leaf("security", "headers", 1, 6, justification="TBD")),
            ("t", leaf("security", "headers", 2, 3, is_boolean_checkpoint=True)),
            ("t", leaf("security", "nope", 3, 6)),
            ("t", leaf("security", "headers", 4, 7)),
            ("t", {k: v for k, v in leaf("security", "headers", 5, 6).items() if k != "evidence_pointer"}),
            ("t", leaf("security", "headers", 6, 6)),
            ("t", leaf("security", "headers", 6, 5)),
        ]
        result = sr.rollup(bad, self.rubric)
        self.assertEqual(result["accepted"], 1)
        self.assertEqual(len(result["rejected"]), 6)
        self.assertTrue(all(r["reason"] for r in result["rejected"]))

    def test_cli_reads_directory_and_writes_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "findings").mkdir()
            (tmp / "findings" / "a.json").write_text(json.dumps([leaf("search", "tech_seo", 1, 6)]))
            (tmp / "findings" / "b.jsonl").write_text(json.dumps(leaf("search", "tech_aeo", 1, 3)) + "\n")
            out = tmp / "result.json"
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = sr.main(["--findings", str(tmp / "findings"), "--out", str(out)])
                missing = sr.main(["--findings", str(tmp / "missing")])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out.read_text())["accepted"], 2)
            self.assertEqual(missing, 2)


class ScorecardFormulaTest(unittest.TestCase):
    """The committed workbook must use the same N/A rule as rollup() at every level."""

    @classmethod
    def setUpClass(cls):
        cls.scorecard = sheet_formulas(TEMPLATE, "Scorecard")
        cls.executive = sheet_formulas(TEMPLATE, "Executive Scorecard")
        cls.rubric = sr.check_rubric(sr.default_rubric())

    def test_subaudit_rollups_mask_non_numeric_leaves(self):
        leaf = [f for ref, f in self.scorecard.items() if ref.startswith("L") and re.search(r"E\d+:E\d+", f)]
        expected = sum(len(c["subaudits"]) for c in self.rubric["categories"].values())
        self.assertEqual(len(leaf), expected)
        for formula in leaf:
            self.assertRegex(formula, LEAF_ROLLUP)

    def test_category_rollups_mask_na_subaudits_on_both_sides(self):
        cats = {ref: f for ref, f in self.scorecard.items() if "SubWt_" in f}
        self.assertEqual(len(cats), len(self.rubric["order"]))
        for ref, formula in cats.items():
            match = MASKED_ROLLUP.match(formula)
            self.assertIsNotNone(match, f"Scorecard!{ref} is not N/A-masked: {formula}")
            self.assertTrue(match["w"].startswith("SubWt_"), formula)

    def test_final_rollup_masks_na_categories_on_both_sides(self):
        final = [f for f in self.executive.values() if "CategoryWeights" in f]
        self.assertEqual(len(final), 1)
        self.assertEqual(MASKED_ROLLUP.match(final[0])["w"], "CategoryWeights")

    def test_no_unmasked_weight_divisor_remains(self):
        for sheet in (self.scorecard, self.executive):
            for ref, formula in sheet.items():
                self.assertNotIn("/SUM(", formula, ref)
        generator = (SKILL / "scripts" / "generate-scorecard-xlsx.py").read_text(encoding="utf-8")
        self.assertNotIn("/SUM(", generator)

    def test_effective_score_and_grade_show_na_when_everything_is_na(self):
        effective = [f for f in self.executive.values() if "SecurityOverrideCapPct" in f and "MIN(" in f]
        grade = [f for f in self.executive.values() if f.startswith("IF(ISNUMBER(") and "GradeTable" in f]
        self.assertEqual(len(effective), 1)
        self.assertTrue(effective[0].startswith("IF(ISNUMBER("), effective[0])
        self.assertTrue(effective[0].endswith(',"N/A")'), effective[0])
        self.assertEqual(len(grade), 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
