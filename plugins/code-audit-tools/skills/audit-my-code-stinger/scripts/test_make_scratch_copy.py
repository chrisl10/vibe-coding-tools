#!/usr/bin/env python3
"""Tests for make_scratch_copy.py (standard library plus a git binary)."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("make_scratch_copy", HERE / "make_scratch_copy.py")
msc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(msc)


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=Example Owner", "-c", "user.email=owner@example.com",
                    "-c", "commit.gpgsign=false", "-C", str(repo), *args],
                   check=True, capture_output=True, env=msc.git_env())


def run(*args: str) -> tuple[int, dict | None]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = msc.main(list(args))
    return code, (json.loads(out.getvalue()) if code == 0 else None)


class MakeScratchCopyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name).resolve()
        self.repo = root / "example-repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        files = {
            "src/app.js": "console.log(1)\n",
            "README.md": "# example\n",
            ".env": "SECRET=1\n",
            ".env.local": "SECRET=2\n",
            ".env.example": "SECRET=\n",
            "certs/server.pem": "x\n",
            "config/.npmrc": "//registry/:_authToken=x\n",
            "infra/main.tfstate.backup": "{}\n",
            ".gitignore": "ignored.log\n",
        }
        for rel, text in files.items():
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        self.symlinks = True
        try:
            os.symlink("app.js", self.repo / "src" / "alias.js")
            os.symlink("../../outside.txt", self.repo / "src" / "escape.txt")
        except (OSError, NotImplementedError):
            self.symlinks = False
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "init")
        (self.repo / "untracked.txt").write_text("new\n")
        (self.repo / "ignored.log").write_text("noise\n")
        self.dest = root / "workspace" / ".scratch" / "repo-copy"

    def tearDown(self):
        self.tmp.cleanup()

    def test_head_copy_excludes_secrets_and_escaping_links(self):
        code, summary = run(str(self.repo), str(self.dest))
        self.assertEqual(code, 0)
        self.assertTrue((self.dest / "src" / "app.js").is_file())
        self.assertTrue((self.dest / ".env.example").is_file())
        for rel in (".env", ".env.local", "certs/server.pem", "config/.npmrc", "infra/main.tfstate.backup"):
            self.assertFalse((self.dest / rel).exists(), rel)
            self.assertIn(rel, summary["excluded"])
        self.assertFalse((self.dest / "untracked.txt").exists())
        self.assertFalse((self.dest / ".git").exists())
        if self.symlinks:
            self.assertTrue((self.dest / "src" / "alias.js").is_symlink())
            self.assertFalse(os.path.lexists(self.dest / "src" / "escape.txt"))
            self.assertIn("src/escape.txt", [s["path"] for s in summary["skipped"]])
        self.assertFalse(summary["submodules_not_copied"])

    def test_chained_links_cannot_leave_the_copy(self):
        if not self.symlinks:
            self.skipTest("symlinks unavailable")
        (self.repo / "a").mkdir()
        os.symlink("..", self.repo / "a" / "up")  # resolves to the copy root: allowed
        os.symlink("a/up/..", self.repo / "b")  # lexically inside, really the copy's parent
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "chain")
        for extra in ((), ("--working-tree",)):
            with self.subTest(mode=extra):
                dest = self.dest.with_name("copy" + "".join(extra).replace("-", "_"))
                code, summary = run(str(self.repo), str(dest), *extra)
                self.assertEqual(code, 0)
                self.assertTrue((dest / "a" / "up").is_symlink())
                self.assertFalse(os.path.lexists(dest / "b"))
                self.assertIn("b", [s["path"] for s in summary["skipped"]])

    def test_working_tree_copy_includes_untracked_but_not_ignored(self):
        code, summary = run(str(self.repo), str(self.dest), "--working-tree")
        self.assertEqual(code, 0)
        self.assertEqual(summary["mode"], "working-tree")
        self.assertTrue((self.dest / "untracked.txt").is_file())
        self.assertFalse((self.dest / "ignored.log").exists())
        self.assertFalse((self.dest / ".env").exists())

    def test_audited_repository_is_untouched_and_unsafe_targets_refused(self):
        before = sorted(p.relative_to(self.repo).as_posix() for p in self.repo.rglob("*") if ".git" not in p.parts)
        self.assertEqual(run(str(self.repo), str(self.repo / "copy"))[0], 2)
        self.assertEqual(run(str(self.repo), str(self.dest), "--ref=--output=/tmp/x")[0], 2)
        self.dest.mkdir(parents=True)
        (self.dest / "keep.txt").write_text("x")
        self.assertEqual(run(str(self.repo), str(self.dest))[0], 2)
        after = sorted(p.relative_to(self.repo).as_posix() for p in self.repo.rglob("*") if ".git" not in p.parts)
        self.assertEqual(before, after)

    def test_bad_ref_fails_cleanly(self):
        self.assertEqual(run(str(self.repo), str(self.dest), "--ref", "no-such-ref")[0], 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
