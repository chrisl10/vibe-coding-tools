#!/usr/bin/env python3
"""Regex fallback secrets scan for when gitleaks and trufflehog cannot run.

Scans the working tree and, optionally, the full git history (`git log -p
--all`), using a small port of gitleaks default rules (see
references/research/raw/secrets--gitleaks-default-rules.md). Every match is
redacted before it is printed: the first 4 characters are kept and the rest
become `****`, as the Audit My Code contract requires.

Standard library only. Read-only. Never contacts the network and never
verifies a secret against its provider.

Usage:
    python3 secrets_fallback.py ROOT [--history] [--no-tree] [--max-file-bytes N]
                                [--include-generic] [--json OUT.json]

Output: JSON with `hits` (rule, path, line, redacted match, commit when from
history) and `coverage` (files scanned, files skipped, caps). Exit 0 always
when the scan ran (hits are data, not an error); exit 2 on bad arguments.

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

SKIP_DIRS = {"node_modules", "vendor", ".git", "dist", "build", "target", ".venv", "venv",
             "__pycache__", ".next", ".svelte-kit", ".terraform", "coverage", ".gradle", "obj"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".tgz",
            ".jar", ".war", ".class", ".so", ".dylib", ".dll", ".exe", ".woff", ".woff2", ".ttf",
            ".otf", ".mp4", ".mov", ".mp3", ".wasm", ".bin", ".lockb", ".pyc", ".sqlite", ".db"}
LOCKFILES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "uv.lock",
             "Cargo.lock", "Gemfile.lock", "composer.lock", "go.sum", "bun.lock"}

END = r"(?:[`'\"\s;,]|\\[nr]|$)"
# (rule id, compiled regex, capture group index for the secret)
RULES = [
    ("aws-access-token", r"\b((?:A3T[A-Z0-9]|AKIA|ASIA|ABIA|ACCA)[A-Z2-7]{16})\b", 1),
    ("github-pat", r"\b(ghp_[0-9a-zA-Z]{36})\b", 1),
    ("github-oauth", r"\b(gho_[0-9a-zA-Z]{36})\b", 1),
    ("github-app-token", r"\b((?:ghu|ghs)_[0-9a-zA-Z]{36})\b", 1),
    ("github-fine-grained-pat", r"\b(github_pat_\w{82})", 1),
    ("gitlab-pat", r"\b(glpat-[\w-]{20})", 1),
    ("slack-bot-token", r"\b(xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*)", 1),
    ("slack-webhook-url", r"((?:https?://)?hooks\.slack\.com/(?:services|workflows|triggers)/[A-Za-z0-9+/]{43,56})", 1),
    ("stripe-access-token", r"\b((?:sk|rk)_(?:test|live|prod)_[a-zA-Z0-9]{10,99})" + END, 1),
    ("gcp-api-key", r"\b(AIza[\w-]{35})" + END, 1),
    ("openai-api-key", r"\b(sk-(?:proj|svcacct|admin)-[A-Za-z0-9_-]{20,}T3BlbkFJ[A-Za-z0-9_-]{20,}|sk-[a-zA-Z0-9]{20}T3BlbkFJ[a-zA-Z0-9]{20})", 1),
    ("anthropic-api-key", r"\b(sk-ant-(?:api03|admin01)-[a-zA-Z0-9_-]{80,100})", 1),
    ("npm-access-token", r"\b(npm_[A-Za-z0-9]{36})" + END, 1),
    ("sendgrid-api-token", r"\b(SG\.[A-Za-z0-9=_.-]{66})" + END, 1),
    ("shopify-access-token", r"\b(shpat_[a-fA-F0-9]{32})", 1),
    ("digitalocean-access-token", r"\b(doo_v1_[a-f0-9]{64})", 1),
    ("doppler-api-token", r"\b(dp\.pt\.[A-Za-z0-9]{43})", 1),
    ("huggingface-access-token", r"\b(hf_[A-Za-z]{34})" + END, 1),
    ("pypi-upload-token", r"(pypi-AgEIcHlwaS5vcmc[\w-]{50,1000})", 1),
    ("databricks-api-token", r"\b(dapi[a-f0-9]{32}(?:-\d)?)" + END, 1),
    ("private-key", r"(-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY(?: BLOCK)?-----)", 1),
    ("jwt", r"\b(ey[a-zA-Z0-9]{17,}\.ey[a-zA-Z0-9/\\_-]{17,}\.(?:[a-zA-Z0-9/\\_-]{10,}={0,2})?)" + END, 1),
    ("url-with-password", r"\b((?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|redis|rediss|amqps?)://[^\s:/@'\"]+:[^\s@'\"]{3,}@[^\s'\"]+)", 1),
]
GENERIC = ("generic-assignment",
           r"(?i)\b[\w.-]{0,40}(?:api[_-]?key|secret|token|passw(?:or)?d|auth|credential|private[_-]?key)[\w.-]{0,20}\s*(?:=|:|:=|=>)\s*['\"]([^'\"\s]{12,150})['\"]",
           1)
PLACEHOLDER = re.compile(r"(?i)(x{5,}|\*{3,}|changeme|example|placeholder|your[_-]|<[^>]+>|\$\{|\{\{|dummy|sample|fake|test_?key|redacted|0{8,})")


def redact(value: str) -> str:
    return value[:4] + "****" if len(value) > 4 else "****"


def compile_rules(include_generic: bool):
    rules = [(rid, re.compile(rx), g) for rid, rx, g in RULES]
    if include_generic:
        rules.append((GENERIC[0], re.compile(GENERIC[1]), GENERIC[2]))
    return rules


def scan_text(text: str, rules, path: str, commit=None, line_offset=0):
    hits = []
    for i, line in enumerate(text.splitlines(), start=1):
        if len(line) > 5000:
            line = line[:5000]
        for rid, rx, g in rules:
            for m in rx.finditer(line):
                val = m.group(g)
                if rid == "generic-assignment" and PLACEHOLDER.search(val):
                    continue
                hit = {"rule": rid, "path": path, "line": i + line_offset, "match": redact(val),
                       "placeholder_like": bool(PLACEHOLDER.search(val))}
                if commit:
                    hit["commit"] = commit
                hits.append(hit)
    return hits


def scan_tree(root: Path, rules, max_bytes: int):
    """Scan regular files inside root. Symlinks are never followed; returns a 4th value, the skipped-symlink count."""
    hits, scanned, skipped, symlinks = [], 0, [], 0
    root_real = os.path.realpath(root)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        kept = []
        for d in sorted(dirnames):
            if d in SKIP_DIRS:
                continue
            if os.path.islink(os.path.join(dirpath, d)):
                symlinks += 1
                continue
            kept.append(d)
        dirnames[:] = kept
        for fn in sorted(filenames):
            p = Path(dirpath) / fn
            relp = p.relative_to(root).as_posix()
            if p.suffix.lower() in SKIP_EXT or fn in LOCKFILES:
                continue
            if p.is_symlink():
                symlinks += 1
                continue
            try:
                st = os.lstat(p)
            except OSError:
                continue
            if not stat.S_ISREG(st.st_mode):
                continue
            real = os.path.realpath(p)
            if not (real == root_real or real.startswith(root_real + os.sep)):
                symlinks += 1
                continue
            if st.st_size > max_bytes:
                skipped.append(relp)
                continue
            try:
                with open(p, "rb") as fh:
                    raw = fh.read(max_bytes + 1)
            except OSError:
                continue
            if len(raw) > max_bytes:
                skipped.append(relp)
                continue
            if b"\x00" in raw[:4096]:
                continue
            scanned += 1
            hits += scan_text(raw.decode("utf-8", errors="replace"), rules, relp)
    return hits, scanned, skipped, symlinks


GIT_HARDEN = ["-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-c", "diff.external=",
              "-c", "core.pager=cat", "-c", "core.quotepath=off"]


def git_env():
    env = dict(os.environ)
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def scan_history(root: Path, rules, max_commits: int):
    """Scan added lines in `git log -p --all`, streaming the output. Returns hits and an error string or None."""
    cmd = ["git", *GIT_HARDEN, "-C", str(root), "log", "-p", "--all", "--no-color",
           "--no-ext-diff", "--no-textconv", "--unified=0", f"--max-count={max_commits}", "--format=COMMIT %H"]
    hits, commit, path = [], None, None
    with tempfile.TemporaryFile() as errf:
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=errf, env=git_env(), stdin=subprocess.DEVNULL)
        except OSError as exc:
            return [], f"git log failed: {exc.__class__.__name__}"
        timer = threading.Timer(900, proc.kill)
        timer.start()
        try:
            for raw in proc.stdout:
                line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                if line.startswith("COMMIT "):
                    commit = line[7:19]
                elif line.startswith("+++ b/"):
                    path = line[6:]
                elif line.startswith("+") and not line.startswith("+++") and path:
                    if Path(path).name in LOCKFILES:
                        continue
                    for h in scan_text(line[1:], rules, path, commit=commit):
                        h.pop("line", None)
                        hits.append(h)
            proc.wait()
        finally:
            timer.cancel()
            proc.stdout.close()
        if proc.returncode != 0:
            errf.seek(0)
            return [], "git log failed: " + errf.read().decode("utf-8", errors="replace").strip()[:200]
    return hits, None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Regex fallback secrets scan (redacted output).")
    ap.add_argument("root")
    ap.add_argument("--history", action="store_true", help="also scan added lines across all git history")
    ap.add_argument("--max-commits", type=int, default=20000)
    ap.add_argument("--max-file-bytes", type=int, default=1_000_000)
    ap.add_argument("--no-tree", action="store_true", help="skip the working-tree scan (use with --history on a bare clone)")
    ap.add_argument("--include-generic", action="store_true", help="add the noisy generic key=value rule")
    ap.add_argument("--json", metavar="OUT", help="write JSON here instead of stdout")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print("not a directory: " + args.root, file=sys.stderr)
        return 2
    if args.json:
        out_p = Path(args.json).resolve()
        if root == out_p or root in out_p.parents:
            print("refusing to write output inside the scanned repository: " + str(out_p), file=sys.stderr)
            return 2
    rules = compile_rules(args.include_generic)
    if args.no_tree:
        hits, scanned, skipped, symlinks = [], 0, [], 0
    else:
        hits, scanned, skipped, symlinks = scan_tree(root, rules, args.max_file_bytes)
    caps = (["working tree not scanned (--no-tree)"] if args.no_tree else []) + [f"regex fallback only: no entropy check, no provider verification ({len(rules)} rules)",
            "lock files and binary files are not scanned"]
    if symlinks:
        caps.append(f"{symlinks} symlink(s) skipped (never followed)")
    if skipped:
        caps.append(f"{len(skipped)} files over {args.max_file_bytes} bytes skipped")
    history_hits, history_error = [], None
    if args.history:
        history_hits, history_error = scan_history(root, rules, args.max_commits)
        caps.append(f"git history limited to {args.max_commits} commits on all refs")
        if history_error:
            caps.append("history not scanned: " + history_error)
    else:
        caps.append("git history not scanned (run with --history)")
    out = {"tool": "secrets_fallback.py", "root": root.name, "hits": hits, "history_hits": history_hits,
           "coverage": {"files_scanned": scanned, "files_skipped_large": skipped, "caps": caps}}
    text = json.dumps(out, indent=2)
    if args.json:
        Path(args.json).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
