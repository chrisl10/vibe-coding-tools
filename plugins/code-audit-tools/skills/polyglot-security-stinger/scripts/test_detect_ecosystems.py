#!/usr/bin/env python3
"""Self-test for detect_ecosystems.py. Standard library only.

Run: python3 test_detect_ecosystems.py   (exit 0 when every check passes)

Builds a throwaway monorepo fixture in a temp directory, runs the detector,
and checks ids, paths, versions, routing, skips, and worktree handling.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import detect_ecosystems as de  # noqa: E402


def w(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def build(root: Path):
    w(root, "package.json", json.dumps({"private": True, "workspaces": ["apps/*", "services/api"], "devDependencies": {"turbo": "2.0.0"}}))
    w(root, "package-lock.json", json.dumps({"lockfileVersion": 3, "packages": {
        "node_modules/next": {"version": "15.5.2"}, "node_modules/react": {"version": "19.1.0"},
        "node_modules/express": {"version": "5.1.0"}, "node_modules/@sveltejs/kit": {"version": "2.27.0"}}}))
    w(root, "apps/web/package.json", json.dumps({"dependencies": {"next": "^15.5.0", "react": "^19.0.0"}}))
    w(root, "apps/admin/package.json", json.dumps({"dependencies": {"react": "^18.3.1", "react-dom": "^18"}}))
    w(root, "apps/site/package.json", json.dumps({"devDependencies": {"@sveltejs/kit": "^2.20.0", "svelte": "^5.0.0"}}))
    w(root, "services/api/package.json", json.dumps({"main": "index.js", "engines": {"node": ">=22"}, "dependencies": {"express": "^5.0.0"}}))
    w(root, "node_modules/fastify/package.json", json.dumps({"dependencies": {"fastify": "1"}}))
    w(root, "services/py/pyproject.toml", '[project]\nname="s"\nrequires-python=">=3.12"\ndependencies=["fastapi>=0.115"]\n')
    w(root, "services/py/uv.lock", '[[package]]\nname = "fastapi"\nversion = "0.116.1"\n')
    w(root, "tools/pyproject.toml", "[tool.ruff]\nline-length = 100\n")
    w(root, "services/go/go.mod", "module x\n\ngo 1.24.0\n\nrequire github.com/gin-gonic/gin v1.10.1\n")
    w(root, "services/rs/Cargo.toml", '[workspace]\nmembers=["crates/*"]\n')
    w(root, "services/rs/crates/web/Cargo.toml", '[package]\nname="web"\nversion="0.1.0"\nrust-version="1.85"\n[dependencies]\naxum="0.8"\n')
    w(root, "services/rs/Cargo.lock", '[[package]]\nname = "axum"\nversion = "0.8.4"\n')
    w(root, "services/rails/Gemfile", "ruby '3.3.5'\ngem 'rails', '~> 8.0'\n")
    w(root, "services/rails/Gemfile.lock", "GEM\n  specs:\n    rails (8.0.2)\n")
    w(root, "services/laravel/composer.json", json.dumps({"require": {"php": "^8.3", "laravel/framework": "^12.0"}}))
    w(root, "legacy/index.php", "<?php echo 1;")
    w(root, "services/spring/pom.xml", "<project><parent><artifactId>spring-boot-starter-parent</artifactId><version>3.5.4</version></parent><properties><java.version>21</java.version></properties><groupId>org.springframework.boot</groupId></project>")
    w(root, "services/spring/mod/pom.xml", "<project><groupId>org.springframework.boot</groupId></project>")
    w(root, "services/dotnet/Api.csproj", '<Project Sdk="Microsoft.NET.Sdk.Web"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>')
    w(root, ".github/workflows/ci.yml", "on: push\n")
    w(root, "infra/main.tf", 'resource "x" "y" {}\n')
    w(root, "Dockerfile", "FROM scratch\n")
    # a nested agent worktree that must be skipped
    w(root, ".claude/worktrees/copy/package.json", json.dumps({"dependencies": {"express": "^4"}}))
    # a linked git worktree folder elsewhere
    w(root, "other-wt/.git", "gitdir: /somewhere/.git/worktrees/other-wt\n")
    w(root, "other-wt/package.json", json.dumps({"dependencies": {"koa": "^2"}}))


class DetectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name).resolve()
        build(cls.root)
        try:
            os.symlink("/", cls.root / "loop")
        except OSError:
            pass
        cls.out = de.detect(cls.root, [], 2_000_000)
        cls.stacks = {s["id"]: s for s in cls.out["stacks"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_shape(self):
        for s in self.out["stacks"]:
            self.assertEqual(set(s), {"id", "version", "paths"})

    def test_ids_and_paths(self):
        expect = {"nextjs": ["apps/web"], "react": ["apps/admin"], "sveltekit": ["apps/site"],
                  "node-server": ["services/api"], "python": ["services/py"], "go": ["services/go"],
                  "rust": ["services/rs/crates/web"], "ruby": ["services/rails"],
                  "php": ["legacy", "services/laravel"], "java-kotlin": ["services/spring"],
                  "dotnet": ["services/dotnet"]}
        for sid, paths in expect.items():
            self.assertIn(sid, self.stacks, sid)
            self.assertEqual(self.stacks[sid]["paths"], paths, sid)

    def test_versions(self):
        self.assertEqual(self.stacks["nextjs"]["version"], "15.5.2")
        self.assertEqual(self.stacks["node-server"]["version"], "22")
        self.assertEqual(self.stacks["python"]["version"], "3.12")
        self.assertEqual(self.stacks["go"]["version"], "1.24.0")
        self.assertEqual(self.stacks["rust"]["version"], "1.85")
        self.assertEqual(self.stacks["ruby"]["version"], "3.3.5")
        self.assertEqual(self.stacks["java-kotlin"]["version"], "21")
        self.assertEqual(self.stacks["dotnet"]["version"], "10.0")
        fw = {f["name"]: f["version"] for f in self.out["details"]["python"][0]["frameworks"]}
        self.assertEqual(fw["fastapi"], "0.116.1")

    def test_skips(self):
        all_paths = [p for s in self.out["stacks"] for p in s["paths"]]
        self.assertFalse(any(p.startswith(("node_modules", ".claude", "other-wt", "tools", "loop")) for p in all_paths), all_paths)
        self.assertIn(".claude/worktrees", self.out["coverage"]["skipped_worktrees"])

    def test_routing(self):
        r = self.out["routing"]
        self.assertEqual(r["nextjs-security-wasp-drone"], ["apps/web"])
        self.assertIn("apps/web", r["react-security-wasp-drone"])
        ids = {x["id"] for x in r["polyglot-security-wasp-drone"]}
        self.assertTrue({"node-server", "python", "go", "dotnet"} <= ids)

    def test_infra(self):
        self.assertEqual(self.out["infra"]["github_workflows"], [".github/workflows/ci.yml"])
        self.assertEqual(self.out["infra"]["terraform_dirs"], ["infra"])
        self.assertEqual(self.out["infra"]["dockerfiles"], ["Dockerfile"])

    def test_cli_stacks_only(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = de.main([str(self.root), "--stacks-only", "--compact"])
        self.assertEqual(rc, 0)
        self.assertIsInstance(json.loads(buf.getvalue()), list)


class YarnLockRedosTest(unittest.TestCase):
    """M5 regression: a crafted yarn.lock must not stall the resolver."""

    def _resolve(self, lock_text: str):
        import time
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            w(root, "yarn.lock", lock_text)
            reader = de.Reader(5_000_000, [])
            t0 = time.monotonic()
            res = de.npm_resolved(reader, root, root, "react")
            return res, time.monotonic() - t0

    def test_pathological_lock_returns_quickly(self):
        res, secs = self._resolve("react@1:\n" + "  a\n" * 40 + "zzz\n")
        self.assertEqual(res, (None, None))
        self.assertLess(secs, 1.0)

    def test_normal_lock_still_resolves(self):
        res, _ = self._resolve('react@^18.0.0:\n  version "18.2.0"\n  resolved "x"\n')
        self.assertEqual(res[0], "18.2.0")
        res, _ = self._resolve('"react@npm:^19.0.0":\n  version: 19.1.0\n  resolution: "react@npm:19.1.0"\n')
        self.assertEqual(res[0], "19.1.0")


if __name__ == "__main__":
    unittest.main(verbosity=1)
