#!/usr/bin/env python3
"""Self-contained test for build_plan.py. Run: python3 test_build_plan.py"""
import json, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_plan  # noqa: E402


def f(i, dim, sev, path, cwe=None, effort="S", conf="confirmed", tags=None, l0=1, l1=5):
    return {"id": i, "dimension": dim, "source": "x", "title": "t " + i, "severity": sev,
            "confidence": conf, "locations": [{"path": path, "line_start": l0, "line_end": l1}] if path else [],
            "evidence": "e", "why_it_matters": "w", "remediation": "r", "effort": effort,
            "refs": [cwe] if cwe else [], "verified_by": "v", "tags": tags or []}


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name)
        rows = {
            "02-security": [f("SEC-NEXT-001", "security", "critical", "apps/web/a.ts", "CWE-862"),
                            f("SEC-GEN-002", "security", "high", "apps/web/a.ts", "CWE-862", l0=3, l1=9),
                            f("SEC-GEN-003", "security", "medium", "apps/web/b.ts", "CWE-862", effort="M")],
            "01-bloat": [f("BLOAT-DUP-001", "bloat", "medium", "src/adapters/x.ts", effort="M"),
                         f("BLOAT-DUP-002", "bloat", "medium", "src/adapters/y.ts", effort="M")],
            "03-quality": [f("QA-TEST-001", "quality", "medium", "src/adapters/x.ts", effort="M", tags=["tests"]),
                           f("QA-INFO-001", "quality", "info", None)],
        }
        for d, rs in rows.items():
            (self.ws / d).mkdir()
            (self.ws / d / "findings.jsonl").write_text("\n".join(json.dumps(r) for r in rs) + "\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_plan(self):
        plan = build_plan.build(self.ws, None, 2)
        ids = {i for it in plan["items"] for i in it["finding_ids"]}
        self.assertNotIn("SEC-GEN-002", ids)
        self.assertIn("SEC-GEN-002", [m for it in plan["items"] for m in it["merged_duplicate_ids"]])
        sec = [i for i in plan["items"] if i["kind"] == "CWE-862"][0]
        self.assertEqual(sec["wave"], "now")
        self.assertEqual(sec["max_severity"], "critical")
        dup = [i for i in plan["items"] if i["kind"] == "BLOAT-DUP"][0]
        self.assertEqual(len(dup["finding_ids"]), 2)
        self.assertEqual(plan["inputs"]["no_action_info_ids"], ["QA-INFO-001"])
        self.assertTrue(all(i["proposed_docs"]["prd"]["path"].startswith("library/requirements/backlog/prd-") for i in plan["items"]))

    def test_distinct_advisories_stay_separate(self):
        with tempfile.TemporaryDirectory() as d:
            ws = Path(d)
            (ws / "02-security").mkdir()
            rows = []
            for n in range(1, 7):
                r = f(f"SEC-NEXT-{n:03d}", "security", "critical", "package.json", "CWE-1395", l0=1, l1=1)
                r["refs"] = [f"CVE-2025-{1000 + n}", "CWE-1395", "CWE-1104"]
                rows.append(r)
            (ws / "02-security" / "findings.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
            plan = build_plan.build(ws, None, 2)
            self.assertEqual(sum(len(it["finding_ids"]) for it in plan["items"]), 6)
            self.assertEqual([m for it in plan["items"] for m in it["merged_duplicate_ids"]], [])

    def test_manifest_not_a_dependency_and_foundation_owner(self):
        with tempfile.TemporaryDirectory() as d:
            ws = Path(d)
            for sub, dim, i, cwe in (("00-foundation", "foundation", "FND-TEST-002", None),
                                     ("02-security", "security", "SEC-NEXT-001", "CWE-79")):
                (ws / sub).mkdir()
                (ws / sub / "findings.jsonl").write_text(json.dumps(f(i, dim, "high", "package.json", cwe, l0=1, l1=1)) + "\n")
            plan = build_plan.build(ws, None, 2)
            self.assertTrue(all(it["depends_on"] == [] for it in plan["items"]))
            fnd = [it for it in plan["items"] if "foundation" in it["dimensions"]][0]
            self.assertEqual(fnd["owner_drone"], "github-repo-health-wasp-drone")

    def test_effort_buckets(self):
        self.assertEqual([build_plan.hours_to_bucket(h) for h in (0.5, 2, 6, 20, 30)], ["XS", "S", "M", "L", "XL"])

    def test_cli(self):
        self.assertEqual(build_plan.main([str(self.ws), "--quiet"]), 0)
        plan = json.loads((self.ws / "04-remediation" / "plan.json").read_text())
        self.assertEqual(plan["uncovered_finding_ids"], [])

    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(build_plan.main([d, "--quiet"]), 1)


if __name__ == "__main__":
    unittest.main()
