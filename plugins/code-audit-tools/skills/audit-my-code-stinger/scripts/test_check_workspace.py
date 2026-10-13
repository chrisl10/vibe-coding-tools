#!/usr/bin/env python3
"""Tests for check_workspace.py and merge_security.py (standard library only)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def finding(fid: str, dimension: str, severity: str = "medium", confidence: str = "likely") -> dict:
    return {
        "id": fid, "dimension": dimension, "source": "test-wasp-drone", "title": "A thing is wrong",
        "severity": severity, "confidence": confidence,
        "locations": [{"path": "src/a.ts", "line_start": 1, "line_end": 2}],
        "evidence": "const a = 1", "why_it_matters": "It matters.", "remediation": "Change src/a.ts.",
        "effort": "S", "refs": ["CWE-79"], "verified_by": "Read the call site.",
    }


def metrics(dimension: str, verdict: str = "moderate") -> dict:
    return {
        "dimension": dimension, "verdict": verdict, "summary": "Summary.",
        "measures": [{"key": "k", "label": "K", "value": 1, "threshold": "t", "band": "moderate"}],
        "coverage": {"files_scanned": 1, "skipped": [], "caps": []},
    }


def write_workspace(root: Path, tier: str = "foundation", execution: dict | None = None) -> None:
    intake = {
        "contract": "1.0", "tier": tier, "repo": {"name": "acme"}, "stacks": [], "scope": {},
        "workspace": str(root),
        "execution": execution if execution is not None else {"allowed": False, "mode": "none"},
    }
    (root / "intake.json").write_text(json.dumps(intake))
    (root / "evidence-index.md").write_text("# Evidence\n")
    folder = root / "00-foundation"
    folder.mkdir()
    (folder / "metrics.json").write_text(json.dumps(metrics("foundation")))
    (folder / "findings.jsonl").write_text(json.dumps(finding("FND-CI-001", "foundation")) + "\n")
    (folder / "notes.md").write_text("# Notes\n")


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True)


class CheckWorkspaceTests(unittest.TestCase):
    def test_clean_workspace_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_workspace(Path(tmp))
            result = run("check_workspace.py", tmp)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_possible_confidence_cannot_be_high(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_workspace(root)
            bad = finding("FND-CI-002", "foundation", severity="high", confidence="possible")
            with (root / "00-foundation" / "findings.jsonl").open("a") as fh:
                fh.write(json.dumps(bad) + "\n")
            result = run("check_workspace.py", tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot carry severity above medium", result.stdout)

    def test_missing_execution_consent_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_workspace(root)
            intake = json.loads((root / "intake.json").read_text())
            del intake["execution"]
            (root / "intake.json").write_text(json.dumps(intake))
            result = run("check_workspace.py", tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("execution", result.stdout)

    def test_inconsistent_execution_consent_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_workspace(Path(tmp), execution={"allowed": True, "mode": "none"})
            result = run("check_workspace.py", tmp)
            self.assertEqual(result.returncode, 1)

    def test_unredacted_secret_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_workspace(root)
            leaky = finding("FND-ENV-001", "foundation")
            leaky["evidence"] = "token = " + "ghp_" + "A" * 30
            with (root / "00-foundation" / "findings.jsonl").open("a") as fh:
                fh.write(json.dumps(leaky) + "\n")
            result = run("check_workspace.py", tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unredacted", result.stdout)


class MergeSecurityTests(unittest.TestCase):
    def test_merge_sets_verdict_and_keeps_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "02-security"
            folder.mkdir()
            for source, sev in (("react-security-wasp-drone", "medium"), ("nextjs-security-wasp-drone", "high")):
                (folder / f"findings-{source}.jsonl").write_text(
                    json.dumps(finding(f"SEC-{source[:4].upper()}-001", "security", severity=sev)) + "\n")
                (folder / f"metrics-{source}.json").write_text(json.dumps(metrics("security", "healthy")))
                (folder / f"notes-{source}.md").write_text(f"Notes from {source}.\n")
            result = run("merge_security.py", tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            merged = json.loads((folder / "metrics.json").read_text())
            self.assertEqual(merged["verdict"], "at-risk")
            self.assertEqual(len((folder / "findings.jsonl").read_text().splitlines()), 2)
            self.assertIn("Notes from react-security-wasp-drone.", (folder / "notes.md").read_text())
            self.assertTrue((folder / "findings-react-security-wasp-drone.jsonl").exists())


class VerdictAndEvidenceTests(unittest.TestCase):
    def merged_verdict(self, measures_band: str, source_verdict: str, with_finding: bool) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "02-security"
            folder.mkdir()
            line = json.dumps(finding("SEC-POLY-001", "security", severity="low")) + "\n" if with_finding else ""
            (folder / "findings-polyglot-security-wasp-drone.jsonl").write_text(line)
            m = metrics("security", source_verdict)
            m["measures"][0]["band"] = measures_band
            (folder / "metrics-polyglot-security-wasp-drone.json").write_text(json.dumps(m))
            (folder / "notes-polyglot-security-wasp-drone.md").write_text("Notes.\n")
            run("merge_security.py", tmp)
            return json.loads((folder / "metrics.json").read_text())["verdict"]

    def test_single_critical_band_is_at_risk(self) -> None:
        self.assertEqual(self.merged_verdict("critical", "healthy", True), "at-risk")

    def test_nothing_ran_is_not_run(self) -> None:
        self.assertEqual(self.merged_verdict("not-run", "not-run", False), "not-run")

    def test_stricter_source_verdict_wins(self) -> None:
        self.assertEqual(self.merged_verdict("healthy", "critical", True), "critical")

    def test_per_source_check_accepts_per_source_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_workspace(root, tier="basic")
            folder = root / "02-security"
            folder.mkdir()
            src = "react-security-wasp-drone"
            (folder / f"findings-{src}.jsonl").write_text(json.dumps(finding("SEC-REACT-001", "security")) + "\n")
            (folder / f"metrics-{src}.json").write_text(json.dumps(metrics("security")))
            (folder / f"notes-{src}.md").write_text("Notes.\n")
            result = run("check_workspace.py", tmp, "--dimension", "security")
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_evidence_index_collects_sections_and_unlisted_raw(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_workspace(root)
            raw = root / "00-foundation" / "raw"
            raw.mkdir()
            (raw / "scan.json").write_text("{}")
            (raw / "orphan.log").write_text("x")
            (root / "00-foundation" / "notes.md").write_text(
                "# Notes\n\n## Evidence\n\n- `00-foundation/raw/scan.json` - scanner output\n\n## Other\n- not evidence\n")
            result = run("build_evidence_index.py", tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            index = (root / "evidence-index.md").read_text()
            self.assertIn("scanner output", index)
            self.assertIn("orphan.log` - not described by its Drone", index)
            self.assertNotIn("not evidence", index)


if __name__ == "__main__":
    unittest.main()
