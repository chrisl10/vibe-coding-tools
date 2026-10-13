#!/usr/bin/env python3
"""Candidate locator for react-security-stinger checks (contract 1.0 helper).

Walks the audited repository read-only and lists every line that matches a check's
detection pattern. The output is a list of CANDIDATES, not findings: every candidate must
be read and confirmed (or dismissed) by the Drone with the check's confirm rules in
references/checks-*.md before anything is written to findings.

Python 3.9+ standard library only. No ripgrep needed; when ripgrep is available the Drone may
use the same patterns from references/detection-patterns.md instead.

Usage:
    python3 sink_scan.py --repo <repo> [--paths apps/web] [--out candidates.json]
        [--checks RX-01 SD-02] [--max-files 20000] [--max-per-check 200]

Secret-looking matches are redacted to the first 4 characters plus ****.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".turbo", ".cache", "coverage", ".vercel", ".output", "out",
             "storybook-static", "vendor", "__snapshots__"}
SRC = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts", ".html", ".mdx"}
CONFIG_NAMES = re.compile(r"^(vite|vitest|webpack|rsbuild|parcel|react-router|waku)\.config\.|^package\.json$|^\.env")

I = re.IGNORECASE
P = [
    # id, description, regex, flags, applies-to ("src", "config", "env", "any")
    ("RX-01", "dangerouslySetInnerHTML with a value", r"dangerouslySetInnerHTML\s*=", 0, "src"),
    ("RX-02", "dynamic URL attribute (href, src, action, formAction, xlinkHref, data)",
     r"\b(href|src|action|formAction|xlinkHref|data|srcDoc)\s*=\s*\{(?!\s*[\"'](?!javascript:|data:)[^\"'{}]*[\"']\s*\})(?!\s*`/)", 0, "src"),
    ("RX-02", "literal javascript: or data:text/html URL", r"[\"'`]\s*(javascript:|data:text/html)", I, "src"),
    ("RX-03", "raw HTML DOM write", r"\.(innerHTML|outerHTML)\s*\+?=(?!=)|insertAdjacentHTML\s*\(|document\.write(ln)?\s*\(", 0, "src"),
    ("RX-04", "string evaluated as code", r"(?<![\w.])eval\s*\(|new\s+Function\s*\(|set(Timeout|Interval)\s*\(\s*[\"'`]", 0, "src"),
    ("RX-05", "markdown to HTML pipeline", r"rehype-raw|rehypeRaw|urlTransform\s*[:=]|\bmarked(\.parse)?\s*\(|markdown-it|showdown|new\s+showdown\.Converter|remark-html", 0, "src"),
    ("RX-06", "MDX compile or evaluate", r"next-mdx-remote|@mdx-js/mdx|mdx-bundler|\bcompileMDX\s*\(|\bbundleMDX\s*\(|blockJS\s*:\s*false|blockDangerousJS\s*:\s*false", 0, "src"),
    ("RX-07", "HTML-to-React parser", r"html-react-parser|react-html-parser|\bhtmr\b", 0, "src"),
    ("RX-08", "sanitizer configuration or hand-rolled sanitizer",
     r"ADD_TAGS|ADD_ATTR|ALLOW_UNKNOWN_PROTOCOLS|IN_PLACE|CUSTOM_ELEMENT_HANDLING|WHOLE_DOCUMENT|happy-dom|\.replace\(\s*/<\s*/?\s*script", 0, "src"),
    ("RX-09", "Trusted Types policy", r"trustedTypes\.createPolicy\s*\(|require-trusted-types-for", 0, "any"),
    ("RX-10", "CSS url() built from a variable", r"url\(\s*\$\{|url\(\s*[\"']?\s*\+", 0, "src"),
    ("RX-11", "target=_blank link", r"target\s*=\s*[\"'{`]*_blank", 0, "src"),
    ("RS-01", "state serialized into a script tag",
     r"__(PRELOADED|INITIAL|APOLLO|REDUX|RELAY|SSR|DATA)[A-Z_]*__|<script[^>]*dangerouslySetInnerHTML|JSON\.stringify\([^)]*\)\s*[}`]\s*<\/script", 0, "src"),
    ("RS-02", "bootstrapScriptContent", r"bootstrapScriptContent\s*:", 0, "src"),
    ("RS-03", "HTML shell built with string templates or placeholder replace",
     r"res\.(send|end|write)\s*\(\s*`[^`]*<|\.replace\(\s*[\"'`]<!--\s*(app|ssr|html|head)|renderToString\s*\(", I, "src"),
    ("RC-02", "'use server' directive (each Server Function is a public endpoint)", r"^\s*[\"']use server[\"']", 0, "src"),
    ("RC-05", "RSC closure encryption setting", r"enableActionEncryption\s*:\s*false|defineEncryptionKey", 0, "any"),
    ("RC-06", "server-only or taint markers (positive signal, list them)", r"[\"']server-only[\"']|experimental_taint(ObjectReference|UniqueValue)", 0, "src"),
    ("RC-07", "custom RSC request handling (check for an Origin check)",
     r"decodeReply\s*\(|decodeAction\s*\(|decodeFormState\s*\(|loadServerAction\s*\(|renderToPipeableStream.*react-server-dom", 0, "src"),
    ("RC-10", "dev server bound beyond localhost", r"--host\b|host\s*:\s*(true|[\"']0\.0\.0\.0[\"'])", 0, "config"),
    ("SD-01", "client-exposed env var with a secret-like name",
     r"\b(VITE|REACT_APP|PUBLIC|EXPO_PUBLIC)_[A-Z0-9_]*(SECRET|PRIVATE|PASSWORD|SERVICE_ROLE|TOKEN|API_KEY|ACCESS_KEY)[A-Z0-9_]*", 0, "any"),
    ("SD-02", "hardcoded credential pattern",
     r"\b(?:sk|rk)_(?:test|live|prod)_[a-zA-Z0-9]{10,99}|sk-ant-api03-[A-Za-z0-9_\-]{20,}|sk-(?:proj|svcacct|admin)-[A-Za-z0-9_\-]{20,}|"
     r"\bAIza[\w-]{35}|ghp_[0-9a-zA-Z]{36}|\b(?:A3T[A-Z0-9]|AKIA|ASIA|ABIA|ACCA)[A-Z2-7]{16}\b|xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*|"
     r"-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY", 0, "any"),
    ("SD-03", "env exposure configuration", r"envPrefix\s*:|[\"']process\.env[\"']\s*:|define\s*:\s*\{[^}]*process\.env\s*[,}]", 0, "config"),
    ("SD-04", "token written to web storage",
     r"(localStorage|sessionStorage)\.setItem\(\s*[\"'`][^\"'`]*(token|jwt|auth|session|refresh|access)", I, "src"),
    ("SD-06", "production source maps enabled", r"sourcemap\s*:\s*(true|[\"']hidden[\"'])|GENERATE_SOURCEMAP\s*=\s*true|devtool\s*:\s*[\"']source-map", 0, "any"),
    ("SD-08", "AI SDK allowed in the browser", r"dangerouslyAllowBrowser\s*:\s*true", 0, "src"),
    ("SD-09", "token or secret logged", r"console\.(log|info|debug)\([^)]*(token|secret|password|apiKey|api_key)", I, "src"),
    ("AR-01", "client-side route or role guard", r"\b(ProtectedRoute|PrivateRoute|RequireAuth|AuthGuard|RequireAdmin|withAuth)\b|\bisAdmin\b|role\s*===?\s*[\"']admin", 0, "src"),
    ("AR-02", "authorization from client-held data", r"jwt-decode|jwtDecode\s*\(|localStorage\.getItem\(\s*[\"'](role|isAdmin|user|permissions)", I, "src"),
    ("AR-03", "redirect or navigation target from the URL",
     r"(searchParams|URLSearchParams|query|params)[^\n]{0,40}\b(next|redirect|redirectTo|returnTo|return_to|returnUrl|callbackUrl|continue|dest|target)\b|"
     r"window\.location(\.href)?\s*=\s*(?![\"'`]\s*/)[^;\n]*|location\.(assign|replace)\s*\(|window\.open\s*\(", 0, "src"),
    ("AR-04", "postMessage listener or wildcard target", r"addEventListener\(\s*[\"']message[\"']|onmessage\s*=|postMessage\([^)]*,\s*[\"']\*[\"']", 0, "src"),
    ("AR-05", "cookie-credentialed request", r"credentials\s*:\s*[\"']include[\"']|withCredentials\s*[:=]\s*true|SameSite=None", I, "any"),
    ("AR-06", "token in a URL", r"[?&#](access_token|id_token|token|api_key|apikey)=", I, "src"),
    ("AI-01", "placeholder security left by a generator", r"(TODO|FIXME|XXX)[^\n]{0,60}(auth|permission|secur|validat|sanitiz|csrf|rate.?limit)", I, "src"),
    ("AI-02", "authorization helper that always allows",
     r"(isAuthorized|isAdmin|canAccess|checkPermission|hasPermission|isAllowed|verifyToken)\s*[=(][^\n{]*\{\s*return\s+true", 0, "src"),
]
COMPILED = [(cid, desc, re.compile(rx, flags | re.M), scope) for cid, desc, rx, flags, scope in P]
REDACT = {"SD-02"}
LITERAL_HTML = re.compile(r"__html\s*:\s*[\"'][^\"'$]*[\"']\s*\}")


def scope_of(p: Path) -> str:
    if p.name.startswith(".env"):
        return "env"
    if CONFIG_NAMES.match(p.name):
        return "config"
    if p.suffix in SRC:
        return "src"
    return ""


def redact(text: str, rx: re.Pattern) -> str:
    return rx.sub(lambda m: m.group(0)[:4] + "****", text)


def _inside(path: str, root_real: str) -> bool:
    real = os.path.realpath(path)
    return real == root_real or real.startswith(root_real + os.sep)


def walk(root: Path, max_files: int, caps: list, repo_real: str, stats: dict):
    """Yield regular, non-symlink files inside the repo. Symlinks (files and dirs) are skipped and counted."""
    n = 0
    if os.path.islink(root) or not _inside(str(root), repo_real):
        stats["symlinks"] += 1
        return
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir())
        except OSError:
            continue
        for p in entries:
            if os.path.islink(p):
                stats["symlinks"] += 1
                continue
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                continue
            if stat.S_ISDIR(mode):
                if p.name not in SKIP_DIRS:
                    stack.append(p)
                continue
            if not stat.S_ISREG(mode):
                continue
            if not scope_of(p):
                continue
            if not _inside(str(p), repo_real):
                stats["symlinks"] += 1
                continue
            n += 1
            if n > max_files:
                caps.append(f"stopped at --max-files {max_files}")
                return
            yield p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="List candidate lines for react-security-stinger checks.")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--paths", nargs="*", default=[])
    ap.add_argument("--out")
    ap.add_argument("--checks", nargs="*", default=[])
    ap.add_argument("--max-files", type=int, default=20000)
    ap.add_argument("--max-per-check", type=int, default=200)
    a = ap.parse_args(argv)
    repo = Path(a.repo).resolve()
    if not repo.is_dir():
        print(f"not a directory: {repo}", file=sys.stderr)
        return 2
    out_p = Path(a.out).resolve() if a.out else None
    if out_p is not None and (repo == out_p or repo in out_p.parents):
        print(f"refusing to write output inside the audited repository: {out_p}", file=sys.stderr)
        return 2
    repo_real = os.path.realpath(repo)
    stats = {"symlinks": 0}
    caps: list = []
    per_check: dict = {}
    candidates = []
    files = 0
    roots = [repo / p for p in a.paths] if a.paths else [repo]
    secret_rx = next(rx for cid, _, rx, _ in COMPILED if cid == "SD-02")
    for root in roots:
        if not root.exists():
            caps.append(f"path not found: {root}")
            continue
        for p in walk(root, a.max_files, caps, repo_real, stats):
            files += 1
            sc = scope_of(p)
            try:
                if os.lstat(p).st_size > 2_000_000:
                    caps.append(f"skipped file over 2 MB: {p.relative_to(repo)}")
                    continue
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for cid, desc, rx, scope in COMPILED:
                if a.checks and cid not in a.checks:
                    continue
                if not (scope == "any" or scope == sc or (scope == "config" and sc == "env")):
                    continue
                for i, line in enumerate(lines, 1):
                    if not rx.search(line):
                        continue
                    if cid == "RX-01" and LITERAL_HTML.search(line):
                        continue
                    per_check[cid] = per_check.get(cid, 0) + 1
                    if per_check[cid] > a.max_per_check:
                        continue
                    text = line.strip()[:240]
                    if cid in REDACT or sc == "env":
                        text = redact(text, secret_rx)
                        if sc == "env" and "=" in text:
                            k, _, v = text.partition("=")
                            text = f"{k}={v[:4]}****" if v else text
                    candidates.append({"check": cid, "what": desc, "path": str(p.relative_to(repo)), "line": i, "text": text})
    if stats["symlinks"]:
        caps.append(f"{stats['symlinks']} symlink(s) skipped (never followed)")
    for cid, n in per_check.items():
        if n > a.max_per_check:
            caps.append(f"{cid}: {n} matches, only the first {a.max_per_check} listed; rerun with --checks {cid} --max-per-check {n}")
    result = {"script": "sink_scan.py", "repo": str(repo), "files_scanned": files, "counts": per_check, "caps": caps, "candidates": candidates}
    text = json.dumps(result, indent=2)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text + "\n", encoding="utf-8")
        print(json.dumps({"files_scanned": files, "counts": per_check, "caps": caps}))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
