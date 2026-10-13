#!/usr/bin/env python3
"""Symlink regression tests for the code-bloat scripts (audit M3, L3).

Fixtures (symlinks included) are created in a temp dir at run time; nothing with a symlink is committed.
Run: python3 test_symlinks.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECRET = "OUTSIDE_PRIVATE_CONTENT"


def run(script, *args):
    return subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True, timeout=60)


class SymlinkTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.outside = base / "outside"
        self.outside.mkdir()
        (self.outside / "private.ts").write_text(f"export const a = '{SECRET}';\nexport function leaked() {{\n  return 1;\n}}\n", encoding="utf-8")
        (self.outside / "dir").mkdir()
        (self.outside / "dir" / "inner.ts").write_text("export const b = 2;\n", encoding="utf-8")
        self.repo = base / "repo"
        (self.repo / "src").mkdir(parents=True)
        (self.repo / "src" / "ok.ts").write_text("export function ok() {\n  return 1;\n}\n", encoding="utf-8")
        os.symlink(self.outside / "private.ts", self.repo / "src" / "link.ts")
        os.symlink(self.outside / "dir", self.repo / "src" / "linkdir")
        os.symlink("/dev/zero", self.repo / "src" / "zero.ts")
        self.work = base / "work"
        self.work.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_size_profile(self):
        out = self.work / "size.json"
        r = run("size_profile.py", "--root", str(self.repo), "--json-out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(out.read_text())
        self.assertEqual(data["files"], 1)
        self.assertEqual(data["symlinks_skipped"], 3)
        self.assertTrue(any("symlink" in c for c in data["caps"]))
        self.assertNotIn(SECRET, r.stdout + out.read_text())

    def test_size_profile_refuses_output_in_root(self):
        r = run("size_profile.py", "--root", str(self.repo), "--json-out", str(self.repo / "o.json"))
        self.assertEqual(r.returncode, 2)
        self.assertFalse((self.repo / "o.json").exists())

    def test_jscpd_recount(self):
        report = self.work / "jscpd.json"
        report.write_text(json.dumps({"statistics": {"total": {}}, "duplicates": []}), encoding="utf-8")
        out = self.work / "jscpd-out.json"
        r = run("jscpd_recount.py", "--report", str(report), "--root", str(self.repo), "--json-out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(out.read_text())
        self.assertEqual(data["walk_files"], 1)
        self.assertGreaterEqual(data["symlinks_skipped"], 3)
        bad = run("jscpd_recount.py", "--report", str(report), "--root", str(self.repo), "--json-out", str(self.repo / "o.json"))
        self.assertEqual(bad.returncode, 2)

    def test_function_profile(self):
        out = self.work / "fn.json"
        r = run("function_profile.py", "--heuristic", str(self.repo), "--json-out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        text = out.read_text()
        self.assertNotIn("leaked", text)
        self.assertIn("ok", text)
        self.assertGreaterEqual(json.loads(text)["symlinks_skipped"], 3)
        bad = run("function_profile.py", "--heuristic", str(self.repo), "--json-out", str(self.repo / "o.json"))
        self.assertEqual(bad.returncode, 2)

    def test_knip_summarize(self):
        report = self.work / "knip.json"
        report.write_text(json.dumps({"files": ["src/link.ts", "src/ok.ts"], "issues": []}), encoding="utf-8")
        out = self.work / "knip-out.json"
        r = run("knip_summarize.py", "--report", str(report), "--root", str(self.repo), "--json-out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(out.read_text())
        by_path = {u["path"]: u["nonblank_lines"] for u in data["unused_files"]}
        self.assertEqual(by_path.get("src/link.ts"), 0, by_path)
        self.assertGreater(by_path.get("src/ok.ts") or 0, 0)
        self.assertGreaterEqual(data["symlinks_skipped"], 1)
        bad = run("knip_summarize.py", "--report", str(report), "--root", str(self.repo), "--json-out", str(self.repo / "o.json"))
        self.assertEqual(bad.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
