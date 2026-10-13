#!/usr/bin/env python3
"""Symlink regression tests for detect_ecosystems.py and secrets_fallback.py (audit M3, L3, L8).

Fixtures are created in a temp dir at run time. Run: python3 test_symlinks.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAKE = "ghp_" + "A1" * 18  # assembled at runtime, not a real token


def run(script, *args):
    return subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True, timeout=60)


class SymlinkTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        outside = base / "outside"
        outside.mkdir()
        (outside / "package.json").write_text(json.dumps({"dependencies": {"express": "4.18.2"}}), encoding="utf-8")
        (outside / "secret.txt").write_text(f"token = '{FAKE}'\n", encoding="utf-8")
        self.repo = base / "repo"
        self.repo.mkdir()
        (self.repo / "main.py").write_text("print('hi')\n", encoding="utf-8")
        os.symlink(outside / "package.json", self.repo / "package.json")
        os.symlink(outside / "secret.txt", self.repo / "notes.txt")
        os.symlink("/dev/zero", self.repo / "zero.txt")
        self.base = base

    def tearDown(self):
        self._tmp.cleanup()

    def test_detect_ecosystems_ignores_symlinked_manifest(self):
        r = run("detect_ecosystems.py", str(self.repo))
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertNotIn("express", r.stdout)
        self.assertGreaterEqual(data["coverage"]["symlinks_skipped"], 1)

    def test_secrets_fallback_skips_symlinks(self):
        r = run("secrets_fallback.py", str(self.repo))
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(data["hits"], [])
        self.assertTrue(any("symlink" in c for c in data["coverage"]["caps"]))
        self.assertEqual(data["root"], "repo")  # relative, never an absolute path (L8)
        self.assertNotIn(str(self.base), r.stdout)

    def test_secrets_fallback_refuses_output_in_repo(self):
        r = run("secrets_fallback.py", str(self.repo), "--json", str(self.repo / "o.json"))
        self.assertEqual(r.returncode, 2)
        self.assertFalse((self.repo / "o.json").exists())

    def test_secrets_fallback_history_streams(self):
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        env = {**os.environ, **env}
        (self.repo / "leak.py").write_text(f'T = "{FAKE}"\n', encoding="utf-8")
        for cmd in (["init", "-q"], ["add", "leak.py"], ["commit", "-qm", "x"]):
            subprocess.run(["git", "-C", str(self.repo), *cmd], check=True, env=env, capture_output=True)
        r = run("secrets_fallback.py", str(self.repo), "--history")
        data = json.loads(r.stdout)
        self.assertEqual(len(data["history_hits"]), 1)
        self.assertNotIn(FAKE, r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
