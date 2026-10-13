#!/usr/bin/env python3
"""Self-tests for render_brief.py. Run: python3 test_render_brief.py (standard library only)."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_brief as rb  # noqa: E402

FIXTURES = Path(__file__).resolve().parent.parent / "references" / "fixtures"


class RollupTest(unittest.TestCase):
    def test_worst_of(self):
        self.assertEqual(rb.rollup_verdict({"a": "healthy", "b": "at-risk", "c": "moderate"}), "at-risk")

    def test_not_run_ignored(self):
        self.assertEqual(rb.rollup_verdict({"a": "not-run", "b": "healthy"}), "healthy")

    def test_nothing_ran(self):
        self.assertEqual(rb.rollup_verdict({"a": "not-run"}), "not-run")
        self.assertEqual(rb.rollup_verdict({}), "not-run")


class EscapeTest(unittest.TestCase):
    def test_html(self):
        self.assertEqual(rb.esc('<img src=x onerror="a">'), "&lt;img src=x onerror=&quot;a&quot;&gt;")

    def test_markdown_link_is_not_a_link(self):
        out = rb.md_block("see [x](javascript:alert(1)) and <b>bold</b>")
        self.assertNotIn("href", out)
        self.assertNotIn("<b>", out)

    def test_css_string(self):
        s = rb.css_string('a"; } body { x')
        self.assertNotIn('"', s[1:-1])
        self.assertNotIn("}", s)


class MergeTest(unittest.TestCase):
    def _run(self, findings):
        run = rb.Run(Path("."))
        for f in findings:
            f.update({"_dim": "security", "_sources": [f["source"]], "_ids": [f["id"]]})
        run.findings = findings
        rb.merge_findings(run)
        return run

    def test_merge_same_path_overlap_cwe(self):
        a = {"id": "SEC-A-001", "source": "x", "severity": "high", "confidence": "likely", "effort": "S",
             "locations": [{"path": "a.ts", "line_start": 10, "line_end": 20}], "refs": ["CWE-862"]}
        b = {"id": "SEC-B-001", "source": "y", "severity": "critical", "confidence": "confirmed", "effort": "S",
             "locations": [{"path": "a.ts", "line_start": 15, "line_end": 30}], "refs": ["CWE-862", "OWASP A01:2025"]}
        run = self._run([a, b])
        self.assertEqual(len(run.findings), 1)
        self.assertEqual(run.findings[0]["id"], "SEC-B-001")
        self.assertEqual(run.findings[0]["_ids"], ["SEC-B-001", "SEC-A-001"])

    def test_no_merge_without_shared_cwe(self):
        a = {"id": "SEC-A-001", "source": "x", "severity": "high", "confidence": "likely", "effort": "S",
             "locations": [{"path": "a.ts", "line_start": 10, "line_end": 20}], "refs": ["CWE-79"]}
        b = {"id": "SEC-B-001", "source": "y", "severity": "high", "confidence": "likely", "effort": "S",
             "locations": [{"path": "a.ts", "line_start": 10, "line_end": 20}], "refs": ["CWE-862"]}
        self.assertEqual(len(self._run([a, b]).findings), 2)

    def test_distinct_advisories_never_merge(self):
        fs = [{"id": f"SEC-NEXT-{n:03d}", "source": "next", "severity": "critical", "confidence": "confirmed", "effort": "S",
               "locations": [{"path": "package.json", "line_start": 1, "line_end": 1}],
               "refs": [f"CVE-2025-{1000 + n}", f"GHSA-aaaa-bbbb-{n:04d}", "CWE-1395", "CWE-1104"]} for n in range(1, 7)]
        run = self._run(fs)
        self.assertEqual(len(run.findings), 6)
        self.assertEqual(run.merges, [])

    def test_generic_cwe_is_not_a_merge_key(self):
        a = {"id": "A-1", "source": "x", "severity": "high", "confidence": "likely", "effort": "S",
             "locations": [{"path": "package.json", "line_start": 1}], "refs": ["CWE-1395"]}
        b = {"id": "B-1", "source": "y", "severity": "high", "confidence": "likely", "effort": "S",
             "locations": [{"path": "package.json", "line_start": 1}], "refs": ["CWE-1395"]}
        self.assertEqual(len(self._run([a, b]).findings), 2)

    def test_effort_words_cover_plan_buckets(self):
        for b in ("XS", "S", "M", "L", "XL"):
            self.assertIn(b, rb.EFFORT_WORDS)

    def test_sort_severity_then_confidence(self):
        fs = [{"id": "1", "severity": "low", "confidence": "confirmed"},
              {"id": "2", "severity": "high", "confidence": "possible"},
              {"id": "3", "severity": "high", "confidence": "confirmed"}]
        self.assertEqual([f["id"] for f in sorted(fs, key=rb.sort_key)], ["3", "2", "1"])


class FixtureTest(unittest.TestCase):
    def test_fixtures_render(self):
        brand = rb.load_brand(rb.DEFAULT_BRAND)
        for name in ("sample-foundation", "sample-full", "sample-mario"):
            with tempfile.TemporaryDirectory() as tmp:
                ws = Path(tmp) / name
                shutil.copytree(FIXTURES / name, ws)
                run = rb.load(ws)
                page = rb.build(run, brand, None)
                self.assertNotIn("<script", page.lower())
                self.assertNotIn("<img src=x", page)
                tier_dims = rb.TIERS[run.tier][1]
                for d in rb.FOLDERS:
                    self.assertEqual(f'<h2 id="{d}">' in page, d in tier_dims, f"{name}: {d}")

    def test_secret_masked(self):
        issues = []
        out = rb.mask_secrets("key ghp_" + "A" * 20, issues)
        self.assertIn("ghp_****", out)
        self.assertTrue(issues)


if __name__ == "__main__":
    unittest.main(verbosity=1)
