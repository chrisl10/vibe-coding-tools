#!/usr/bin/env python3
"""Symlink regression test for sveltekit_audit_scan.py (audit M3). Fixtures are built at run time."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class SymlinkTest(unittest.TestCase):
    def test_symlinks_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            outside = base / "outside"
            outside.mkdir()
            (outside / "+page.server.ts").write_text("export const load = () => ({ leakedLoad: 1 });\n", encoding="utf-8")
            (outside / "package-lock.json").write_text(json.dumps({"packages": {"node_modules/svelte": {"version": "4.0.0"}}}), encoding="utf-8")
            repo = base / "repo"
            (repo / "src" / "routes").mkdir(parents=True)
            (repo / "src" / "routes" / "+page.svelte").write_text("<p>ok</p>\n", encoding="utf-8")
            os.symlink(outside / "+page.server.ts", repo / "src" / "routes" / "+page.server.ts")
            os.symlink(outside / "package-lock.json", repo / "package-lock.json")
            os.symlink(outside, repo / "src" / "linked")
            os.symlink("/dev/zero", repo / "src" / "zero.ts")
            out = base / "out"
            r = subprocess.run([sys.executable, str(HERE / "sveltekit_audit_scan.py"), "--repo", str(repo), "--out-dir", str(out)],
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            inv = (out / "sveltekit-inventory.json").read_text()
            self.assertNotIn("leakedLoad", inv)
            data = json.loads(inv)
            self.assertEqual(data["versions"], {})
            self.assertGreaterEqual(data["symlinks_skipped"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
