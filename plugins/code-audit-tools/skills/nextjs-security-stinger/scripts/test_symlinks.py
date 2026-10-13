#!/usr/bin/env python3
"""Symlink regression test for next_audit_scan.py (audit M3). Fixtures are built at run time."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class SymlinkTest(unittest.TestCase):
    def test_symlinked_files_and_dirs_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            outside = base / "outside"
            (outside / "app").mkdir(parents=True)
            (outside / "pkg.json").write_text(json.dumps({"dependencies": {"next": "14.0.0"}}), encoding="utf-8")
            (outside / "app" / "actions.ts").write_text("'use server'\nexport async function leakedAction() {}\n", encoding="utf-8")
            repo = base / "repo"
            (repo / "app").mkdir(parents=True)
            (repo / "app" / "page.tsx").write_text("export default function P() { return null }\n", encoding="utf-8")
            os.symlink(outside / "pkg.json", repo / "package.json")
            os.symlink(outside / "app" / "actions.ts", repo / "app" / "actions.ts")
            os.symlink(outside / "app", repo / "linked")
            os.symlink("/dev/zero", repo / "zero.ts")
            out = base / "out"
            r = subprocess.run([sys.executable, str(HERE / "next_audit_scan.py"), "--repo", str(repo), "--out", str(out)],
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            inv = (out / "next-inventory.json").read_text()
            self.assertNotIn("leakedAction", inv)
            data = json.loads(inv)
            self.assertEqual(data["apps"], [])
            self.assertEqual(data["symlinks_skipped"], 4)
            self.assertTrue(any("symlink" in c for c in data["caps"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
