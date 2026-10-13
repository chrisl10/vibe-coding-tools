#!/usr/bin/env python3
"""Self-test for the Foundation scripts. Builds a throwaway git repo that is
deliberately unhealthy, runs the scanner, and checks the findings it must make.
Run: python3 scripts/test_foundation.py"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Built at run time so the source tree never holds a key-shaped literal (the Nest secret scan).
FAKE_AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_in_copy  # noqa: E402


def sh(cwd, *cmd):
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


class ScanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        r = Path(cls.tmp.name) / "repo"
        r.mkdir()
        sh(r, "git", "init", "-q")
        write(r, "package.json", json.dumps({"name": "x", "scripts": {"test": 'echo "Error: no test specified" && exit 1'},
                                             "dependencies": {"left-pad": "1.0.0"}, "packageManager": "pnpm@9.0.0"}))
        write(r, "package-lock.json", json.dumps({"lockfileVersion": 3, "packages": {"": {"dependencies": {}}}}))
        write(r, "src/a.ts", "export const a = 1;\n" * 5)
        write(r, "src/b.ts", "export const b = process.env.API_TOKEN_X;\nconst c = process.env.DB_URL_X;\nconst d = process.env.THIRD_ONE_X;\n")
        write(r, "src/big.ts", "x\n" * 1200)
        write(r, "src/a.test.ts", "test('a', () => {});\n")
        write(r, ".env", "DB_PASSWORD=hunter2hunter2\nPLACEHOLDER=replace-me\n")
        write(r, "config.txt", "key = " + FAKE_AWS_KEY + "\n")
        write(r, "AGENTS.md", "# Agents\nSee `src/missing/file.ts` and `src/a.ts`.\n")
        write(r, "CLAUDE.md", "# Claude\nHello\n")
        write(r, ".github/workflows/ci.yml",
              "name: CI\non:\n  pull_request_target:\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n"
              "      - uses: actions/checkout@v4\n        with:\n          ref: ${{ github.event.pull_request.head.sha }}\n"
              "      - uses: some/thirdparty@v1\n      - run: echo \"${{ github.event.pull_request.title }}\"\n")
        write(r, ".nvmrc", "18\n")
        write(r, "wasp-nest.lock", "{not json")
        write(r, "README.md", "# x\nRun {install_command}\n")
        sh(r, "git", "add", "-A")
        sh(r, "git", "commit", "-qm", "init")
        out = Path(cls.tmp.name) / "scan.json"
        subprocess.run([sys.executable, str(HERE / "foundation_scan.py"), "--repo", str(r), "--out", str(out)], check=True, capture_output=True)
        cls.doc = json.loads(out.read_text())
        cls.ids = {f["id"]: f for f in cls.doc["findings"]}
        cls.repo, cls.out = r, out

    def test_expected_findings(self):
        for fid in ["FND-LIB-007", "FND-LIB-009", "FND-LIB-002", "FND-AGENT-002", "FND-AGENT-005", "FND-AGENT-006", "FND-CI-002", "FND-CI-003", "FND-CI-004",
                    "FND-TEST-002", "FND-DEPS-004", "FND-DEPS-006", "FND-DEPS-008", "FND-ENV-001", "FND-ENV-009", "FND-ENV-002",
                    "FND-DOCS-004", "FND-REPO-001"]:
            self.assertTrue(fid in self.ids, "missing " + fid)

    def test_no_secret_value_leaks(self):
        text = self.out.read_text()
        self.assertNotIn("hunter2hunter2", text)
        self.assertNotIn(FAKE_AWS_KEY, text)
        self.assertIn("AKIA****", text)

    def test_contract_shape(self):
        for f in self.doc["findings"]:
            self.assertEqual(f["dimension"], "foundation")
            if f["confidence"] == "possible":
                self.assertIn(f["severity"], ("info", "low", "medium"))
            self.assertRegex(f["id"], r"^FND-(LIB|AGENT|CI|TEST|LINT|DEPS|DOCS|REPO|ENV)-\d{3}$")
            self.assertNotIn("\u2014", json.dumps(f, ensure_ascii=False))
            self.assertNotIn("\u2013", json.dumps(f, ensure_ascii=False))
        self.assertEqual(len({f["id"] for f in self.doc["findings"]}), len(self.doc["findings"]))

    def test_measures_have_bands(self):
        for m in self.doc["measures"]:
            self.assertIn(m["band"], {"healthy", "moderate", "at-risk", "critical", "not-run"})

    def test_refuses_out_inside_repo(self):
        r = subprocess.run([sys.executable, str(HERE / "foundation_scan.py"), "--repo", str(self.repo), "--out", str(self.repo / "x.json")], capture_output=True)
        self.assertEqual(r.returncode, 2)

    def test_repo_untouched(self):
        st = subprocess.run(["git", "status", "--porcelain"], cwd=self.repo, capture_output=True, text=True).stdout
        self.assertEqual(st.strip(), "")

    def test_assemble_requires_resolution_then_writes(self):
        ws = Path(self.tmp.name) / "ws" / "00-foundation"
        cmd = [sys.executable, str(HERE / "assemble_foundation.py"), "--scan", str(self.out), "--out-dir", str(ws), "--summary", "Test summary."]
        bad = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("needs-drone-read", bad.stderr)
        j = Path(self.tmp.name) / "j.jsonl"
        lines = []
        for fid, f in self.ids.items():
            if "needs-drone-read" in f.get("tags", []):
                lines.append(json.dumps({"id": fid, "_action": "update", "tags": [t for t in f["tags"] if t != "needs-drone-read"]}))
        j.write_text("\n".join(lines) + "\n")
        ok = subprocess.run(cmd + ["--judgment", str(j)], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertTrue((ws / "findings.jsonl").exists())
        m = json.loads((ws / "metrics.json").read_text())
        self.assertEqual(m["dimension"], "foundation")
        self.assertIn(m["verdict"], {"healthy", "moderate", "at-risk", "critical"})


class QuotedRefTest(unittest.TestCase):
    """M4: a quoted ref: value on a pull_request_target head checkout must still fail CI-004."""

    def _scan(self, ref_value):
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp) / "repo"
            r.mkdir()
            sh(r, "git", "init", "-q")
            write(r, "package.json", json.dumps({"name": "x"}))
            write(r, ".github/workflows/ci.yml",
                  "name: CI\non:\n  pull_request_target:\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n"
                  "      - uses: actions/checkout@v4\n        with:\n          ref: " + ref_value + "\n")
            sh(r, "git", "add", "-A")
            sh(r, "git", "commit", "-qm", "init")
            out = Path(tmp) / "scan.json"
            subprocess.run([sys.executable, str(HERE / "foundation_scan.py"), "--repo", str(r), "--out", str(out)],
                           check=True, capture_output=True)
            doc = json.loads(out.read_text())
        return {f["id"] for f in doc["findings"]}

    def test_unquoted_double_and_single_quoted_all_fail(self):
        expr = "${{ github.event.pull_request.head.sha }}"
        for value in (expr, '"' + expr + '"', "'" + expr + "'"):
            self.assertIn("FND-CI-004", self._scan(value), value)


class RunnerTest(unittest.TestCase):
    def test_parse_pytest(self):
        self.assertEqual(run_in_copy.parse_log("===== 2 failed, 10 passed, 1 skipped in 3.20s =====")["passed"], 10)

    def test_parse_vitest_jest(self):
        r = run_in_copy.parse_log("Tests:       1 failed, 4 passed, 5 total")
        self.assertEqual((r["failed"], r["passed"]), (1, 4))
        r = run_in_copy.parse_log("      Tests  3 passed (3)")
        self.assertEqual(r["passed"], 3)

    def test_parse_cargo(self):
        r = run_in_copy.parse_log("test result: ok. 7 passed; 0 failed; 1 ignored; 0 measured")
        self.assertEqual((r["passed"], r["failed"]), (7, 0))

    @staticmethod
    def _run(t, cmd, *, flag=True, copy=None):
        copy = copy or Path(t) / ".scratch" / "repo-copy"
        copy.mkdir(parents=True, exist_ok=True)
        args = [sys.executable, str(HERE / "run_in_copy.py")] + (["--execution-allowed"] if flag else []) + \
               ["--copy", str(copy), "--raw-dir", str(Path(t) / "raw"), "--label", "v", "--"] + cmd
        return subprocess.run(args, capture_output=True, text=True)

    def test_refusals(self):
        with tempfile.TemporaryDirectory() as t:
            for bad in (["npm", "install", "-g", "x"], ["sudo", "ls"], ["curl", "http://x"], ["npx", "foo"], ["npm", "publish"], ["python3", "-c", "print(1)"]):
                r = self._run(t, bad)
                self.assertEqual(r.returncode, 2, bad)
            r = self._run(t, ["node", "--version"], copy=Path(t))  # not repo-copy under .scratch
            self.assertEqual(r.returncode, 2)

    def test_m1_bypasses_are_refused(self):
        """Every bypass probed in audit finding M1 must now be refused by the allowlist, not by the consent flag."""
        bypasses = [
            ["node", "-p", "1+1"], ["node", "--print", "7"], ["python3", "-cprint(42)"],
            ["npm", "x", "--version"], ["npm", "add", "--version"], ["npm", "--location", "global", "ls"],
            ["npm", "isntall"], ["npm", "in"], ["npm", "ins"], ["npm", "inst"], ["npm", "instal"],
            ["pnpm", "add", "left-pad"], ["pnpm", "exec", "foo"], ["yarn", "add", "left-pad"], ["bun", "add", "left-pad"],
            ["cargo", "+nightly", "install", "foo"], ["go", "run", "example.com/pkg@latest"],
            ["deno", "run", "https://example.com/x.ts"], ["uv", "run", "--with", "pkg", "python"], ["uv", "pip", "install", "pkg"],
            ["npm", "test", "-e", "x"], ["npm", "run", "x", "--", "--eval", "1"], ["pytest", "-p", "evil"], ["pytest", "-cfoo.ini"],
            ["npm", "run", "test", "--", "https://example.com/x"], ["npm", "test", "left-pad@1.0.0"],
            ["npm", "install"], ["npm", "ci"], ["pnpm", "install"], ["yarn", "install"], ["make", "test", "CC=evil"], ["make", "-f", "evil.mk"],
            ["make", "../x"], ["python3", "x.py"], ["node", "x.js"], ["./node_modules/.bin/jest"], ["uv", "sync"],
        ]
        with tempfile.TemporaryDirectory() as t:
            for bad in bypasses:
                r = self._run(t, bad)
                self.assertEqual(r.returncode, 2, (bad, r.stdout))
                reason = json.loads(r.stdout)["reason"]
                self.assertNotIn("--execution-allowed", reason, bad)

    def test_allowed_shapes_pass_vetting(self):
        with tempfile.TemporaryDirectory() as t:
            copy = (Path(t) / ".scratch" / "repo-copy")
            copy.mkdir(parents=True)
            (copy / ".venv" / "bin").mkdir(parents=True)
            (copy / ".venv" / "bin" / "pip").write_text("")
            (copy / "requirements.txt").write_text("requests==2.32.0\n")
            ok = [
                ["npm", "ci", "--ignore-scripts"], ["pnpm", "install", "--frozen-lockfile", "--ignore-scripts"],
                ["yarn", "install", "--immutable", "--mode=skip-build"],
                ["uv", "sync", "--frozen", "--no-install-project", "--no-build"],
                ["pip", "install", "--only-binary=:all:", "--no-deps", "-r", "requirements.txt"],
                ["npm", "test"], ["npm", "run", "lint"], ["pnpm", "run", "typecheck"], ["yarn", "test"], ["bun", "test"],
                ["pytest", "-x", "-q"], ["python3", "-m", "pytest"], ["go", "test", "./..."], ["go", "vet", "./..."],
                ["cargo", "test"], ["cargo", "clippy"], ["make", "test"], ["make", "build-all_2.x"], ["tsc", "--noEmit"],
                ["eslint", "."], ["ruff", "check", "."], ["mypy", "."], ["biome", "check", "."], ["vitest", "run"], ["jest"],
            ]
            for good in ok:
                err, resolved = run_in_copy.vet_command(good, copy.resolve())
                self.assertIsNone(err, (good, err))
            err, resolved = run_in_copy.vet_command(ok[4], copy.resolve())
            self.assertEqual(resolved[0], str(copy.resolve() / ".venv" / "bin" / "pip"))
            # a pip requirements file with a URL or option is refused, as are install shapes missing a safety flag
            (copy / "bad.txt").write_text("-e git+https://example.com/x.git\n")
            err, _ = run_in_copy.vet_command(["pip", "install", "--only-binary=:all:", "--no-deps", "-r", "bad.txt"], copy.resolve())
            self.assertIsNotNone(err)
            err, _ = run_in_copy.vet_command(["pip", "install", "--only-binary=:all:", "--no-deps", "-r", "../x.txt"], copy.resolve())
            self.assertIsNotNone(err)

    def test_allowed_run(self):
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / ".scratch" / "repo-copy"
            copy.mkdir(parents=True)
            (copy / "Makefile").write_text("hello:\n\t@echo hi\n")
            r = self._run(t, ["make", "hello"])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(json.loads(r.stdout)["exit_code"], 0)
            # the temporary HOME is removed after the run
            self.assertEqual([p.name for p in (Path(t) / ".scratch").iterdir() if p.name.startswith("foundation-home-")], [])

    def test_missing_consent_flag_refuses_everything(self):
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / ".scratch" / "repo-copy"
            copy.mkdir(parents=True)
            (copy / "Makefile").write_text("hello:\n\t@echo hi\n")
            r = self._run(t, ["make", "hello"], flag=False)
            self.assertEqual(r.returncode, 2)
            self.assertIn("--execution-allowed", json.loads(r.stdout)["reason"])
            self.assertFalse((Path(t) / "raw").exists())

    def test_copy_location_rules(self):
        with tempfile.TemporaryDirectory() as t:
            # wrong name under .scratch, and .scratch itself
            self.assertEqual(self._run(t, ["make", "x"], copy=Path(t) / ".scratch" / "other").returncode, 2)
            self.assertEqual(self._run(t, ["make", "x"], copy=Path(t) / ".scratch").returncode, 2)
            self.assertEqual(self._run(t, ["make", "x"], copy=Path(t) / "x" / ".scratch" / "deeper" / "repo-copy").returncode, 2)
            # a copy that holds .git is refused
            copy = Path(t) / "ok" / ".scratch" / "repo-copy"
            (copy / ".git").mkdir(parents=True)
            r = self._run(t, ["make", "x"], copy=copy)
            self.assertEqual(r.returncode, 2)
            self.assertIn(".git", json.loads(r.stdout)["reason"])

    def test_n1_redirect_flags_are_refused(self):
        """Audit N1: flags that move the working dir, project root, config, shell or toolchain must be refused."""
        with tempfile.TemporaryDirectory() as t:
            real = Path(t) / "realrepo"
            real.mkdir()
            (real / "package.json").write_text(json.dumps({"scripts": {"test": "touch marker.txt"}}))
            r_ = str(real)
            probes = [
                ["npm", "test", "--prefix", r_], ["npm", "test", "--prefix=" + r_], ["pnpm", "test", "-C", r_],
                ["cargo", "test", "--manifest-path", r_ + "/Cargo.toml"], ["npm", "run", "test", "--workspace=../../x"],
                ["npm", "--workspace=../..", "test"], ["npm", "test", "--script-shell=/bin/sh"], ["npm", "test", "--userconfig=/tmp/npmrc"],
                ["go", "test", "-toolexec=/usr/bin/true", "./..."], ["go", "vet", "-vettool=/bin/true"], ["go", "test", "-modfile=x.mod"],
                ["yarn", "test", "--cwd", r_], ["pytest", r_], ["pytest", "--rootdir=/"], ["cargo", "test", "--target-dir", r_],
                ["cargo", "test", "--config", "build.rustc-wrapper=x"], ["tsc", "--project", r_ + "/tsconfig.json"],
                ["pytest", "../outside"], ["eslint", "../../x"], ["npm", "test", "--", "--foo"], ["npm", "run", "test", "extra"],
                ["go", "test", "./../x"], ["jest", "--rootDir=x"], ["pytest", "--unknown-flag"], ["mypy", "--python-executable=/bin/sh"],
            ]
            for bad in probes:
                r = self._run(t, bad)
                self.assertEqual(r.returncode, 2, (bad, r.stdout))
                self.assertFalse((real / "marker.txt").exists(), bad)

    def test_n1_symlinked_path_out_of_copy_refused(self):
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / ".scratch" / "repo-copy"
            copy.mkdir(parents=True)
            (Path(t) / "elsewhere").mkdir()
            os.symlink(Path(t) / "elsewhere", copy / "linked")
            err, _ = run_in_copy.vet_command(["pytest", "linked"], copy.resolve())
            self.assertIn("outside the copy", err or "")
            err, _ = run_in_copy.vet_command(["pytest", "tests", "-q"], copy.resolve())
            self.assertIsNone(err)

    def test_n1_audited_repo_snapshot_fails_loudly(self):
        with tempfile.TemporaryDirectory() as t:
            real = Path(t) / "realrepo"
            real.mkdir()
            sh(real, "git", "init", "-q")
            copy = Path(t) / ".scratch" / "repo-copy"
            copy.mkdir(parents=True)
            (copy / "Makefile").write_text("hit:\n\t@touch " + str(real / "marker.txt") + "\nquiet:\n\t@true\n")
            base = [sys.executable, str(HERE / "run_in_copy.py"), "--execution-allowed", "--audited-repo", str(real),
                    "--copy", str(copy), "--raw-dir", str(Path(t) / "raw"), "--"]
            ok = subprocess.run(base + ["make", "quiet"], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            bad = subprocess.run(base + ["make", "hit"], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 3, bad.stdout + bad.stderr)
            self.assertTrue(json.loads(bad.stdout)["audited_repo_modified"])

    def test_n8_rewrite_of_existing_ignored_file_and_unreadable_repo(self):
        with tempfile.TemporaryDirectory() as t:
            real = Path(t) / "realrepo"
            real.mkdir()
            sh(real, "git", "init", "-q")
            (real / ".gitignore").write_text("cache.txt\n")
            (real / "cache.txt").write_text("old\n")
            copy = Path(t) / ".scratch" / "repo-copy"
            copy.mkdir(parents=True)
            (copy / "Makefile").write_text("hit:\n\t@printf 'new and longer\\n' > " + str(real / "cache.txt") + "\n")
            base = [sys.executable, str(HERE / "run_in_copy.py"), "--execution-allowed", "--copy", str(copy),
                    "--raw-dir", str(Path(t) / "raw")]
            bad = subprocess.run(base + ["--audited-repo", str(real), "--", "make", "hit"], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 3, bad.stdout + bad.stderr)
            missing = subprocess.run(base + ["--audited-repo", str(Path(t) / "not-a-repo"), "--", "make", "hit"],
                                     capture_output=True, text=True)
            self.assertEqual(missing.returncode, 2, missing.stdout + missing.stderr)

    def test_n4_intake_must_record_host_consent(self):
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / ".scratch" / "repo-copy"
            copy.mkdir(parents=True)
            (copy / "Makefile").write_text("hello:\n\t@echo hi\n")

            def go(execution, raw_text=None):
                f = Path(t) / "intake.json"
                f.write_text(raw_text if raw_text is not None else json.dumps({"execution": execution}))
                return subprocess.run([sys.executable, str(HERE / "run_in_copy.py"), "--execution-allowed", "--intake", str(f), "--copy", str(copy),
                                       "--raw-dir", str(Path(t) / "raw"), "--", "make", "hello"], capture_output=True, text=True)
            for bad in ({"allowed": False, "mode": "host"}, {"allowed": True, "mode": "container"}, {"allowed": True, "mode": "none"},
                        {"allowed": "yes", "mode": "host"}, {}):
                r = go(bad)
                self.assertEqual(r.returncode, 2, (bad, r.stdout))
                self.assertIn("intake.json", json.loads(r.stdout)["reason"])
            self.assertEqual(go(None, raw_text="{not json").returncode, 2)
            self.assertEqual(go({"allowed": True, "mode": "host"}).returncode, 0)
            # the intake file does not replace the flag
            r = subprocess.run([sys.executable, str(HERE / "run_in_copy.py"), "--intake", str(Path(t) / "intake.json"), "--copy", str(copy),
                                "--raw-dir", str(Path(t) / "raw"), "--", "make", "hello"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)


class SymlinkScanTest(unittest.TestCase):
    def test_n3_symlink_to_dev_zero_is_not_read(self):
        """Audit N3: a tracked symlink to /dev/zero must be skipped, not read forever."""
        if not os.path.exists("/dev/zero"):
            self.skipTest("no /dev/zero")
        with tempfile.TemporaryDirectory() as t:
            r = Path(t) / "repo"
            r.mkdir()
            sh(r, "git", "init", "-q")
            write(r, "src/a.ts", "export const a = 1;\n")
            os.symlink("/dev/zero", r / "src" / "x.ts")
            sh(r, "git", "add", "-A")
            sh(r, "git", "commit", "-qm", "init")
            out = Path(t) / "scan.json"
            p = subprocess.run([sys.executable, str(HERE / "foundation_scan.py"), "--repo", str(r), "--out", str(out)],
                               capture_output=True, timeout=60)  # a hang here raises TimeoutExpired and fails the test
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(out.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
