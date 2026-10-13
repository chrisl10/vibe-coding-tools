#!/usr/bin/env python3
"""Run one project command inside the throwaway repo copy, with guard rails.

The Foundation audit may run the repository's test, lint and typecheck
commands, but only inside `<workspace>/.scratch/repo-copy/`, with a timeout,
without global installs, and with secrets stripped from the environment.

Only command shapes on a positive allowlist run (see SHAPES). The required
`--execution-allowed` flag records that the user consented to running the
repository's code (intake.json execution.allowed is true); without it nothing
runs.

Usage:
  run_in_copy.py --execution-allowed --copy <workspace>/.scratch/repo-copy --raw-dir <workspace>/00-foundation/raw \
      --label tests --timeout 600 -- npm test
  run_in_copy.py --parse-log <raw>/tests.log     # best-effort pass/fail counts

`--intake <workspace>/intake.json` additionally requires execution.allowed true and mode host.
`--audited-repo <repo>` snapshots `git status` of the real repository around the run; exit 3 means it changed.

Exit code is 0 when the guard rails allowed the run (whatever the command's own
exit status was; read the JSON). Exit 2 means the run was refused.

Python 3.11+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Positive allowlist of command shapes. Matched on the first non-flag token after the
# executable; any flag before that token (a global flag such as `--location`) is refused.
# Value kinds: a set of allowed subcommands, or None for "no subcommand, free arguments".
SUBCOMMANDS = {
    "npm": {"test", "run"}, "pnpm": {"test", "run"}, "yarn": {"test", "run"}, "bun": {"test", "run"},
    "go": {"test", "vet"}, "cargo": {"test", "check", "clippy"}, "ruff": {"check"}, "biome": {"check"}, "vitest": {"run"},
}
NO_SUBCOMMAND = {"pytest", "tsc", "eslint", "mypy", "pyright", "jest"}
# Installs are allowed only as these exact shapes: frozen to the lockfile, lifecycle scripts and builds off.
INSTALLS = {
    ("npm", "ci"): {"--ignore-scripts"},
    ("pnpm", "install"): {"--frozen-lockfile", "--ignore-scripts"},
    ("yarn", "install"): {"--immutable", "--mode=skip-build"},
    ("uv", "sync"): {"--frozen", "--no-install-project", "--no-build"},
}
PIP_FLAGS = ["--only-binary=:all:", "--no-deps", "-r"]  # then exactly one requirements file
MAKE_TARGET = re.compile(r"^[A-Za-z0-9_.-]+$")
SCRIPT_NAME = re.compile(r"^[A-Za-z0-9_:.-]+$")
DENY_ARGS = {"-g", "--global", "--force", "-exec", "-toolexec", "--print", "-p"}
SINGLE_DASH_DENY = ("-c", "-e", "-p")  # joined forms such as -cprint(1), -e..., -pfoo
DOUBLE_DASH_DENY = ("--eval", "--with", "--print", "--location", "--exec")
# Flags that move the working directory, project root, config, shell or toolchain. Refused anywhere.
REDIRECT_PREFIXES = ("--prefix", "-C", "--dir", "--cwd", "--manifest-path", "--target-dir", "--config", "--workspace", "-w", "--userconfig",
                     "--globalconfig", "--script-shell", "--rootdir", "--project", "-toolexec", "-vettool", "-modfile", "-overlay",
                     "--node-options", "--require", "-r")
PATH_ARG = re.compile(r"^(\./)?[A-Za-z0-9_.][A-Za-z0-9_./-]*$")
# After the subcommand, tools take a small fixed set of flags plus relative paths (not npm-style trailing arguments).
FIXED_FLAGS = {
    "go": {"-race", "-short", "-v"},
    "cargo": {"--workspace", "--all-targets", "--locked"},
    "pytest": {"-q", "-x", "-v", "-vv", "--tb=short", "--tb=line", "--no-header"},
    "tsc": {"--noEmit", "--pretty"},
    "eslint": {"--quiet"},
    "ruff": {"--quiet", "--no-cache"},
    "mypy": {"--strict", "--ignore-missing-imports"},
    "pyright": {"--outputjson"},
    "biome": set(),
    "vitest": {"--silent"},
    "jest": {"--ci", "--silent", "--runInBand", "--passWithNoTests"},
}
FLAG_PATTERNS = (re.compile(r"^--max-warnings=\d+$"),)
SECRET_ENV = re.compile(r"(?i)(token|secret|password|passwd|credential|api[_-]?key|private|auth|cookie|session|aws_|gh_|github_|npm_config__auth)")
KEEP_ENV = {"PATH", "LANG", "LC_ALL", "TERM", "TMPDIR", "SHELL", "USER", "LOGNAME"}


def refuse(msg: str) -> int:
    print(json.dumps({"refused": True, "reason": msg}))
    return 2


def parse_log(text: str) -> dict:
    """Best-effort counts from common runners. Returns passed, failed, runner or None values."""
    t = re.sub(r"\x1b\[[0-9;]*m", "", text)
    res = {"runner": None, "passed": None, "failed": None, "skipped": None}
    m = re.search(r"Tests:\s+(?:(\d+) failed,\s*)?(?:(\d+) skipped,\s*)?(?:(\d+) todo,\s*)?(?:(\d+) passed,\s*)?(\d+) total", t)
    if m:  # jest and vitest
        res.update(runner="jest-or-vitest", failed=int(m.group(1) or 0), skipped=int(m.group(2) or 0), passed=int(m.group(4) or 0))
        return res
    m = re.search(r"=+\s*(?:(\d+) failed)?[, ]*(?:(\d+) passed)?[, ]*(?:(\d+) skipped)?[^=\n]*\bin [\d.]+s", t)
    if m and (m.group(1) or m.group(2)):  # pytest
        res.update(runner="pytest", failed=int(m.group(1) or 0), passed=int(m.group(2) or 0), skipped=int(m.group(3) or 0))
        return res
    m = re.search(r"Tests\s+(?:(\d+) failed \| )?(\d+) passed", t)
    if m:  # vitest short form
        res.update(runner="vitest", failed=int(m.group(1) or 0), passed=int(m.group(2)))
        return res
    ms = re.findall(r"test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored", t)
    if ms:  # cargo
        res.update(runner="cargo", passed=sum(int(a) for a, _, _ in ms), failed=sum(int(b) for _, b, _ in ms), skipped=sum(int(c) for _, _, c in ms))
        return res
    oks, fails = len(re.findall(r"^ok\s+\S+", t, re.M)), len(re.findall(r"^(?:FAIL|--- FAIL)\b", t, re.M))
    if oks or fails:  # go test (package level)
        res.update(runner="go-test (packages)", passed=oks, failed=fails)
        return res
    m = re.search(r"^# pass (\d+)\s*$[\s\S]*?^# fail (\d+)\s*$", t, re.M)
    if m:  # node --test TAP
        res.update(runner="node:test", passed=int(m.group(1)), failed=int(m.group(2)))
        return res
    return res


def path_problem(a: str) -> str | None:
    """Absolute paths, home paths and '..' segments are refused, also in the value of --flag=value."""
    for v in {a, a.split("=", 1)[-1]}:
        if v.startswith(("/", "~")) or ".." in v.split("/") or re.match(r"^[A-Za-z]:[\\/]", v):
            return f"argument '{a}' is an absolute path or has a '..' segment; only relative paths inside the copy are allowed"
    return None


def vet_args(args: list[str], allow: tuple[str, ...] = ()) -> str | None:
    """Argument rules that apply anywhere in the command line."""
    for a in args:
        if a in allow:
            continue
        if a in DENY_ARGS:
            return f"argument '{a}' is not allowed"
        if a.startswith(REDIRECT_PREFIXES):
            return f"argument '{a}' is not allowed (it redirects the working directory, project root, config, shell or toolchain)"
        if a.startswith("--"):
            if a.startswith(DOUBLE_DASH_DENY):
                return f"argument '{a}' is not allowed (eval, print, --with, global-location and exec flags are blocked)"
        elif a.startswith("-") and len(a) > 1 and a.startswith(SINGLE_DASH_DENY):
            return f"argument '{a}' is not allowed (-c, -e and -p style eval flags are blocked, including joined forms)"
        if re.search(r"https?://", a, re.I):
            return f"argument '{a}' contains a URL; downloads are not allowed"
        if "@" in a:
            return f"argument '{a}' contains '@' (package version specs and registry fetches are not allowed)"
        if re.search(r"[|;&`$<>]", a):
            return "shell metacharacters are not allowed; pass a plain argument list"
        err = path_problem(a)
        if err:
            return err
    return None


def vet_tool_args(tool: str, args: list[str], copy: Path) -> str | None:
    """Only a fixed set of flags plus relative paths that stay inside the copy."""
    for a in args:
        if a in FIXED_FLAGS.get(tool, set()) or any(p.match(a) for p in FLAG_PATTERNS):
            continue
        if a.startswith("-") or not PATH_ARG.match(a):
            return f"argument '{a}' is not in the fixed flag set for {tool}; only relative paths and a few harmless flags are allowed"
        target = (copy / a.rstrip(".").rstrip("/") if a.endswith("...") else copy / a).resolve()
        if target != copy and copy not in target.parents:
            return f"path '{a}' resolves outside the copy (a symlink?)"
    return None


def vet_command(cmd: list[str], copy: Path) -> tuple[str | None, list[str]]:
    """Return (refusal reason or None, command to execute). Positive allowlist."""
    if os.sep in cmd[0] or cmd[0] != Path(cmd[0]).name:
        return "executables must be given by bare name, not by path", cmd
    exe, rest = cmd[0], cmd[1:]
    known = set(SUBCOMMANDS) | NO_SUBCOMMAND | {"make", "python", "python3", "pip", "uv"}
    if exe not in known:
        return f"command '{exe}' is not on the allowlist: {sorted(known)}", cmd
    err = vet_args(rest, allow=("-r",) if exe == "pip" else ())
    if err:
        return err, cmd
    if exe in NO_SUBCOMMAND:
        err = vet_tool_args(exe, rest, copy)
        return (err, cmd) if err else (None, cmd)
    if exe in ("python", "python3"):
        if rest[:2] == ["-m", "pytest"]:
            err = vet_tool_args("pytest", rest[2:], copy)
            return (err, cmd) if err else (None, cmd)
        return "python is allowed only as `python -m pytest ...`", cmd
    if exe == "pip":
        venv_pip = copy / ".venv" / "bin" / "pip"
        if not (len(rest) == 5 and rest[0] == "install" and rest[1:4] == PIP_FLAGS):
            return "pip is allowed only as `pip install --only-binary=:all: --no-deps -r <file>` through the copy's venv", cmd
        req = Path(rest[4])
        target = (copy / req).resolve() if not req.is_absolute() else req.resolve()
        if req.is_absolute() or ".." in req.parts or copy not in target.parents or not target.is_file():
            return "the requirements file must be an existing relative path inside the copy", cmd
        for line in target.read_text(errors="replace").splitlines():
            t = line.strip()
            if t.startswith("-") or "://" in t or "@" in t:
                return "requirements files with options, URLs or direct references are not allowed", cmd
        if not venv_pip.is_file():
            return "create the venv at <copy>/.venv first; pip is only run through it", cmd
        return None, [str(venv_pip)] + rest
    if exe == "make":
        if len(rest) != 1 or rest[0].startswith("-") or not MAKE_TARGET.match(rest[0]):
            return "make is allowed only as `make <target>` with a target matching ^[A-Za-z0-9_.-]+$ and no variables or flags", cmd
        return None, cmd
    if not rest:
        return f"'{exe}' needs an allowed subcommand", cmd
    sub = rest[0]
    if sub.startswith("-") or sub.startswith("+"):
        return f"global flag '{sub}' before the subcommand is not allowed", cmd
    if (exe, sub) in INSTALLS:
        if set(rest[1:]) != INSTALLS[(exe, sub)] or len(rest[1:]) != len(INSTALLS[(exe, sub)]):
            return f"'{exe} {sub}' is allowed only as `{exe} {sub} {' '.join(sorted(INSTALLS[(exe, sub)]))}` (frozen, no scripts)", cmd
        return None, cmd
    if sub not in SUBCOMMANDS.get(exe, set()):
        return f"'{exe} {sub}' is not on the allowlist of command shapes", cmd
    if exe in ("npm", "pnpm", "yarn", "bun"):
        # Nothing may trail `test`, and only a plain script name may follow `run`.
        if rest == ["test"] or (len(rest) == 2 and sub == "run" and SCRIPT_NAME.match(rest[1]) and not rest[1].startswith("-")):
            return None, cmd
        return f"'{exe}' is allowed only as `{exe} test` or `{exe} run <script>` with no trailing arguments (script name ^[A-Za-z0-9:_.-]+$)", cmd
    err = vet_tool_args(exe, rest[1:], copy)
    return (err, cmd) if err else (None, cmd)


def repo_snapshot(repo: Path) -> str | None:
    """Fingerprint of the audited repository's working tree, or None when it cannot be read.

    Lists `git status --porcelain --ignored -z` with the repository's own git config neutralized
    (no fsmonitor, no hooks, no optional index lock, so the audited `.git` is neither run nor
    rewritten), then adds size and mtime for every listed path so a second write to an existing
    untracked or ignored file still changes the fingerprint.
    """
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.devnull, "LANG": "C",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_OPTIONAL_LOCKS": "0",
           "GIT_TERMINAL_PROMPT": "0"}
    cmd = ["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-c", "core.untrackedCache=false",
           "-C", str(repo), "status", "--porcelain", "--ignored", "-z"]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=60, env=env)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    parts = []
    for entry in r.stdout.decode("utf-8", "replace").split("\0"):
        if not entry:
            continue
        path = repo / entry[3:]
        try:
            st = os.lstat(path)
            parts.append(f"{entry}\t{st.st_size}\t{st.st_mtime_ns}")
        except OSError:
            parts.append(f"{entry}\tmissing")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--copy", type=Path)
    ap.add_argument("--raw-dir", type=Path)
    ap.add_argument("--label", default="run")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--execution-allowed", action="store_true",
                    help="required: records user consent to run repository code (intake.json execution.allowed is true)")
    ap.add_argument("--intake", type=Path, help="<workspace>/intake.json; when given, execution.allowed must be true and mode must be host")
    ap.add_argument("--audited-repo", type=Path,
                    help="the real repository; its `git status` is snapshotted before and after the run and the run fails loudly if it changed")
    ap.add_argument("--parse-log", type=Path)
    ap.add_argument("--max-log-bytes", type=int, default=2_000_000)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    if a.parse_log:
        print(json.dumps(parse_log(a.parse_log.read_text(errors="replace")), indent=2))
        return 0
    if not a.execution_allowed:
        return refuse("--execution-allowed is required: the user has not consented to running repository code (intake.json execution.allowed must be true)")
    if a.intake:
        try:
            ex = (json.loads(a.intake.read_text(encoding="utf-8")).get("execution") or {})
        except (OSError, ValueError, AttributeError) as e:
            return refuse(f"--intake could not be read as JSON: {e.__class__.__name__}")
        if ex.get("allowed") is not True or ex.get("mode") != "host":
            return refuse("intake.json does not record execution.allowed true with mode host; host execution is not consented")
    if not (a.copy and a.raw_dir):
        return refuse("--copy and --raw-dir are required")
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    if not cmd:
        return refuse("no command given after --")
    copy = a.copy.resolve()
    if copy.name != "repo-copy" or copy.parent.name != ".scratch" or not copy.is_dir():
        return refuse("--copy must be an existing directory named repo-copy whose parent is .scratch (the throwaway copy)")
    if (copy / ".git").exists():
        return refuse("--copy contains .git; the throwaway copy must be an export, never a clone or the real repository")
    raw = a.raw_dir.resolve()
    if copy in raw.parents or raw == copy:
        return refuse("--raw-dir must be outside the copy so logs do not mix with the audited files")
    err, cmd = vet_command(cmd, copy)
    if err:
        return refuse(err)

    before = repo_snapshot(a.audited_repo) if a.audited_repo else None
    if a.audited_repo and before is None:
        print(json.dumps({"refused": True, "reason": f"cannot read git status of --audited-repo {a.audited_repo}; refusing to run without the change check"}))
        return 2
    home = Path(tempfile.mkdtemp(prefix="foundation-home-", dir=copy.parent))
    try:
        env = {k: v for k, v in os.environ.items() if k in KEEP_ENV and not SECRET_ENV.search(k)}
        env.update({"HOME": str(home), "CI": "1", "NO_COLOR": "1", "npm_config_update_notifier": "false", "npm_config_audit": "false",
                    "npm_config_fund": "false", "PIP_REQUIRE_VIRTUALENV": "1", "npm_config_cache": str(home / ".npm"),
                    "UV_CACHE_DIR": str(home / ".uv-cache"), "CARGO_HOME": str(home / ".cargo")})
        raw.mkdir(parents=True, exist_ok=True)
        log = raw / f"{re.sub(r'[^A-Za-z0-9_.-]', '-', a.label)}.log"
        start = time.time()
        timed_out = False
        try:
            p = subprocess.run(cmd, cwd=copy, env=env, capture_output=True, timeout=a.timeout)
            out, code = p.stdout + b"\n--- stderr ---\n" + p.stderr, p.returncode
        except subprocess.TimeoutExpired as e:
            timed_out, code = True, None
            out = (e.stdout or b"") + b"\n--- stderr ---\n" + (e.stderr or b"")
        except OSError as e:
            return refuse(f"could not start command: {e}")
        dur = round(time.time() - start, 1)
        text = out[: a.max_log_bytes].decode("utf-8", "replace")
        log.write_text(f"$ {' '.join(cmd)}\n(cwd: the throwaway copy, HOME redirected, CI=1)\n\n{text}", encoding="utf-8")
        if a.audited_repo and repo_snapshot(a.audited_repo) != before:
            print(json.dumps({"refused": False, "audited_repo_modified": True, "command": cmd, "log": str(log),
                              "error": "the audited repository changed during this run; stop, record a cap, and run nothing further"}, indent=2))
            return 3
        print(json.dumps({"refused": False, "command": cmd, "exit_code": code, "timed_out": timed_out, "seconds": dur, "timeout": a.timeout,
                          "log": str(log), "parsed": parse_log(text), "truncated": len(out) > a.max_log_bytes}, indent=2))
        return 0
    finally:
        shutil.rmtree(home, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
