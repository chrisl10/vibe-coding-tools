#!/usr/bin/env python3
"""React and React Server Components version check for Audit My Code (contract 1.0).

Reads package.json files plus package-lock.json, pnpm-lock.yaml, and yarn.lock (classic and
Berry), resolves the installed versions of React, react-server-dom-*, @vitejs/plugin-rsc,
React Router, Waku, and a few React-ecosystem libraries with 2025-2026 advisories, and
compares them against the advisory table in this file. It writes contract-shaped findings
(one JSON object per line) and prints a JSON summary of what it detected.

Python 3.9+ standard library only. Reads the audited repository, never writes to it.

Usage:
    python3 react_version_check.py --repo <repo> [--paths apps/web packages/ui]
        [--out <workspace>/02-security/raw/react-security-wasp-drone/version-findings.jsonl]
        [--summary <file.json>] [--start-id 1] [--max-files 20000]

Exit codes: 0 ran (findings or not), 2 bad arguments.

Advisory data: references/advisory-table.md is the human-readable copy of ADVISORIES below,
and every row cites a raw research file. Keep the two in sync when either changes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

SOURCE = "react-security-wasp-drone"
TABLE_AS_OF = "2026-09-30"
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".turbo", ".cache", "coverage", ".vercel", ".output", "out"}
SRC_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts"}

RSDW = ["react-server-dom-webpack", "react-server-dom-parcel", "react-server-dom-turbopack"]
GUIDE_RSC = "react-security-stinger/guides/02-rsc-and-server-functions.md"
GUIDE_SC = "react-security-stinger/guides/06-supply-chain-and-ai-patterns.md"
GUIDE_RR = "react-security-stinger/guides/04-auth-routing-client-trust.md"
GUIDE_XSS = "react-security-stinger/guides/01-xss-and-injection-sinks.md"


def r(lo, hi, fixed, hi_inclusive=False):
    """One affected range: lo inclusive, hi exclusive unless hi_inclusive, fixed = recommended version."""
    return {"lo": lo, "hi": hi, "hi_inclusive": hi_inclusive, "fixed": fixed}


def rsdw_lines(fixes):
    """Ranges for the three react-server-dom-* minor lines from a (19.0 fix, 19.1 fix, 19.2 fix) tuple."""
    f0, f1, f2 = fixes
    return [r("19.0.0", f0, f0), r("19.1.0", f1, f1), r("19.2.0", f2, f2)]


# precondition values:
#   none        version alone is enough (the package is only installed for this feature)
#   rsc         needs a server that runs React Server Components (true when rsdw or plugin-rsc is installed)
#   dev-server  only reachable on the development server
#   rr-framework  React Router Framework Mode (@react-router/dev or react-router.config.*)
#   rr-ssr      React Router Framework or Data Mode with server rendering
#   rr-data-or-framework  Framework or Data Mode (createBrowserRouter, loaders, actions)
#   rr-rsc      React Router unstable RSC APIs
#   rr-file-session  createFileSessionStorage in use
#   untrusted-mdx    MDX compiled from user-supplied content
#   sanitizer-config DOMPurify options or modes named in the advisory
#   any-use     depends on how the library is fed; manual review
ADVISORIES = [
    # React Server Components: react-server-dom-webpack / -parcel / -turbopack
    {"ids": ["CVE-2025-55182", "GHSA-fv66-9v8q-g76r"], "packages": RSDW, "severity": "critical", "cwe": ["CWE-502"],
     "summary": "remote code execution from one crafted request to the server (React2Shell)",
     "ranges": [r("19.0.0", "19.0.1", "19.0.1"), r("19.1.0", "19.1.2", "19.1.2"), r("19.2.0", "19.2.1", "19.2.1")],
     "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    {"ids": ["CVE-2025-55183", "GHSA-925w-6v3x-g4j4"], "packages": RSDW, "severity": "medium", "cwe": ["CWE-497", "CWE-502"],
     "summary": "a crafted request can return the source code of a Server Function, including secrets hardcoded in it",
     "ranges": rsdw_lines(("19.0.2", "19.1.3", "19.2.2")), "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    {"ids": ["CVE-2025-55184", "GHSA-2m3v-v2m8-q956"], "packages": RSDW, "severity": "high", "cwe": ["CWE-400", "CWE-502"],
     "summary": "a crafted request can hang the server in an infinite loop",
     "ranges": rsdw_lines(("19.0.2", "19.1.3", "19.2.2")), "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    {"ids": ["CVE-2025-67779", "GHSA-7gmr-mq3h-m5h9"], "packages": RSDW, "severity": "high", "cwe": ["CWE-400", "CWE-502"],
     "summary": "the first denial-of-service fix was incomplete; a crafted request can still hang the server",
     "ranges": [r("19.0.2", "19.0.3", "19.0.3"), r("19.1.3", "19.1.4", "19.1.4"), r("19.2.2", "19.2.3", "19.2.3")],
     "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    {"ids": ["CVE-2026-23864", "GHSA-83fc-fqcc-2hmg"], "packages": RSDW, "severity": "high", "cwe": ["CWE-400", "CWE-502"],
     "summary": "crafted requests can crash the server or exhaust its memory or CPU",
     "ranges": rsdw_lines(("19.0.4", "19.1.5", "19.2.4")), "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    {"ids": ["CVE-2026-23869", "GHSA-479c-33wc-g2pg"], "packages": RSDW, "severity": "high", "cwe": ["CWE-400", "CWE-502"],
     "summary": "a crafted request can pin the server CPU for up to a minute",
     "ranges": rsdw_lines(("19.0.5", "19.1.6", "19.2.5")), "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    {"ids": ["CVE-2026-23870", "GHSA-rv78-f8rc-xrxh"], "packages": RSDW, "severity": "high", "cwe": ["CWE-400", "CWE-770"],
     "summary": "crafted form data can exhaust server memory or CPU",
     "ranges": rsdw_lines(("19.0.6", "19.1.7", "19.2.6")), "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    {"ids": ["CVE-2026-44907", "GHSA-wx67-qw84-cm4g"], "packages": RSDW, "severity": "high", "cwe": ["CWE-400", "CWE-770"],
     "summary": "many duplicate action fields in one request drive server CPU use up quadratically",
     "ranges": rsdw_lines(("19.0.8", "19.1.9", "19.2.8")), "precondition": "rsc", "raw": "rsc--github-react-security-advisories.md"},
    # @vitejs/plugin-rsc vendors react-server-dom-webpack
    {"ids": ["CVE-2025-55182", "GHSA-fmh4-wr37-44fp"], "packages": ["@vitejs/plugin-rsc"], "severity": "critical", "cwe": ["CWE-502"],
     "summary": "the bundled React Server Components runtime allows remote code execution (React2Shell)",
     "ranges": [r("0.0.0", "0.5.3", "0.5.3")], "precondition": "none", "raw": "rsc--vite-plugin-rsc-advisories.md"},
    {"ids": ["CVE-2025-67489", "GHSA-j76j-5p5g-9wfr"], "packages": ["@vitejs/plugin-rsc"], "severity": "critical", "cwe": ["CWE-94"],
     "summary": "remote code execution through unsafe dynamic imports on the development server",
     "ranges": [r("0.0.0", "0.5.6", "0.5.6")], "precondition": "dev-server", "raw": "rsc--vite-plugin-rsc-advisories.md"},
    {"ids": ["CVE-2025-55183", "CVE-2025-67779", "GHSA-c6m7-q6pr-c64r", "GHSA-cpqf-f22c-r95x"], "packages": ["@vitejs/plugin-rsc"],
     "severity": "high", "cwe": ["CWE-400", "CWE-497"],
     "summary": "the bundled runtime leaks Server Function source code and can be hung by a crafted request",
     "ranges": [r("0.0.0", "0.5.7", "0.5.7")], "precondition": "none", "raw": "rsc--vite-plugin-rsc-advisories.md"},
    {"ids": ["CVE-2025-68155", "GHSA-g239-q96q-x4qm"], "packages": ["@vitejs/plugin-rsc"], "severity": "high", "cwe": ["CWE-22"],
     "summary": "arbitrary file read through a development-server endpoint",
     "ranges": [r("0.0.0", "0.5.8", "0.5.8")], "precondition": "dev-server", "raw": "rsc--vite-plugin-rsc-advisories.md"},
    {"ids": ["CVE-2026-23869", "CVE-2026-23870", "CVE-2026-44907", "GHSA-v457-wxvj-p9w9", "GHSA-w94c-4vhp-22gx", "GHSA-p2w6-cmq4-qjfj"],
     "packages": ["@vitejs/plugin-rsc"], "severity": "high", "cwe": ["CWE-400", "CWE-770"],
     "summary": "the bundled runtime can be driven to exhaust server CPU or memory by crafted requests",
     "ranges": [r("0.0.0", "0.5.29", "0.5.29")], "precondition": "none", "raw": "rsc--vite-plugin-rsc-advisories.md"},
    # React Router
    {"ids": ["CVE-2025-61686", "GHSA-9583-h5hc-x8cw"], "packages": ["@react-router/node"], "severity": "critical", "cwe": ["CWE-22"],
     "summary": "file access on the server when createFileSessionStorage is used with unsigned cookies",
     "ranges": [r("7.0.0", "7.9.3", "7.9.4", True)], "precondition": "rr-file-session", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2025-31137", "GHSA-4q56-crqp-v477"], "packages": ["@react-router/express"], "severity": "high", "cwe": ["CWE-20"],
     "summary": "request URLs can be manipulated through Host or X-Forwarded-Host headers",
     "ranges": [r("7.0.0", "7.4.0", "7.4.1", True)], "precondition": "none", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2025-43864", "CVE-2025-43865", "GHSA-f46r-rw29-r322", "GHSA-cpj6-fhp6-mr6j"], "packages": ["react-router"],
     "severity": "high", "cwe": ["CWE-345"],
     "summary": "cache poisoning denial of service and pre-render data spoofing in Framework Mode",
     "ranges": [r("7.0.0", "7.5.1", "7.5.2", True)], "precondition": "rr-framework", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2025-59057", "GHSA-3cgp-3xvw-98x8"], "packages": ["react-router"], "severity": "high", "cwe": ["CWE-79"],
     "summary": "cross-site scripting through the Meta component when it renders JSON-LD script tags",
     "ranges": [r("7.0.0", "7.8.2", "7.9.0", True)], "precondition": "rr-framework", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-22029", "CVE-2026-21884", "GHSA-2w69-qvjg-hvjx", "GHSA-8v8x-cx79-35w7"], "packages": ["react-router"],
     "severity": "high", "cwe": ["CWE-79", "CWE-601"],
     "summary": "cross-site scripting through redirects from loaders or actions and through ScrollRestoration keys during server rendering",
     "ranges": [r("7.0.0", "7.11.0", "7.12.0", True)], "precondition": "rr-data-or-framework", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-22030", "GHSA-h5cw-625j-3rxh"], "packages": ["react-router"], "severity": "medium", "cwe": ["CWE-352", "CWE-346"],
     "summary": "cross-site request forgery against server route actions",
     "ranges": [r("7.0.0", "7.12.0", "7.12.0")], "precondition": "rr-framework", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2025-68470", "CVE-2026-53669", "CVE-2026-40181", "GHSA-9jcx-v3wj-wh4m", "GHSA-wrjc-x8rr-h8h6", "GHSA-2j2x-hqr9-3h42"],
     "packages": ["react-router"], "severity": "medium", "cwe": ["CWE-601"],
     "summary": "untrusted paths passed to navigation can send users to an external site",
     "ranges": [r("6.0.0", "7.18.0", "7.18.0")], "precondition": "any-use", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-53668", "GHSA-jjmj-jmhj-qwj2"], "packages": ["react-router-dom"], "severity": "medium", "cwe": ["CWE-601", "CWE-79"],
     "summary": "an open redirect that can lead to cross-site scripting",
     "ranges": [r("6.30.2", "6.30.4", "6.30.6", True)], "precondition": "any-use", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-53668", "GHSA-jjmj-jmhj-qwj2"], "packages": ["react-router"], "severity": "medium", "cwe": ["CWE-601", "CWE-79"],
     "summary": "an open redirect that can lead to cross-site scripting",
     "ranges": [r("7.9.6", "7.12.0", "7.13.0", True)], "precondition": "any-use", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-33245", "CVE-2026-53667", "GHSA-8646-j5j9-6r62", "GHSA-h8fp-f39c-q6mh"], "packages": ["react-router"],
     "severity": "high", "cwe": ["CWE-79"],
     "summary": "cross-site scripting through javascript: redirect targets and error handling in the unstable RSC mode",
     "ranges": [r("7.7.0", "7.18.0", "7.18.0")], "precondition": "rr-rsc", "raw": "router--react-router-advisories.md"},
    {"ids": ["GHSA-qwww-vcr4-c8h2"], "packages": ["react-router"], "severity": "medium", "cwe": ["CWE-352"],
     "summary": "cross-site request forgery bypass in the unstable RSC mode (the action runs before the 400 response)",
     "ranges": [r("7.12.0", "7.18.2", "7.18.2"), r("8.0.0", "8.3.0", "8.3.0")], "precondition": "rr-rsc", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-33244", "GHSA-f22v-gfqf-p8f3"], "packages": ["react-router"], "severity": "medium", "cwe": ["CWE-79"],
     "summary": "stored cross-site scripting through prerendered redirect pages",
     "ranges": [r("7.5.1", "7.13.2", "7.13.2")], "precondition": "rr-framework", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-34077", "CVE-2026-42342", "CVE-2026-55685", "GHSA-rxv8-25v2-qmq8", "GHSA-8x6r-g9mw-2r78", "GHSA-chx6-hx7r-mcp5"],
     "packages": ["react-router"], "severity": "high", "cwe": ["CWE-400"],
     "summary": "unauthenticated denial of service against the server through single-fetch and the __manifest endpoint",
     "ranges": [r("7.0.0", "7.18.0", "7.18.0")], "precondition": "rr-framework", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-42211", "GHSA-49rj-9fvp-4h2h"], "packages": ["react-router"], "severity": "high", "cwe": ["CWE-502"],
     "summary": "possible remote code execution when chained onto a prototype pollution bug elsewhere in the app",
     "ranges": [r("7.0.0", "7.14.1", "7.14.2", True)], "precondition": "rr-framework", "raw": "router--react-router-advisories.md"},
    {"ids": ["CVE-2026-53666", "GHSA-337j-9hxr-rhxg"], "packages": ["react-router"], "severity": "medium", "cwe": ["CWE-94"],
     "summary": "attacker input in server-rendering errors can trigger unexpected code on the client",
     "ranges": [r("6.4.0", "7.18.0", "7.18.0")], "precondition": "rr-ssr", "raw": "router--react-router-advisories.md"},
    # Waku
    {"ids": ["CVE-2026-49455", "CVE-2026-49456", "GHSA-75w3-gmqx-993q", "GHSA-43fc-v873-qw85"], "packages": ["waku"],
     "severity": "medium", "cwe": ["CWE-352", "CWE-601"],
     "summary": "cross-origin request forgery on Server Action dispatch and an open redirect helper",
     "ranges": [r("0.0.0", "1.0.0-beta.0", "1.0.0-beta.1", True)], "precondition": "none", "raw": "router--waku-advisories.md"},
    # Content and sanitizer libraries
    {"ids": ["CVE-2026-0969", "GHSA-g4xw-jxrg-5f6m"], "packages": ["next-mdx-remote"], "severity": "high", "cwe": ["CWE-94"],
     "summary": "compiling untrusted MDX can run attacker code on the server",
     "ranges": [r("4.3.0", "6.0.0", "6.0.0")], "precondition": "untrusted-mdx", "raw": "xss--mdx-next-mdx-remote-cve-2026-0969.md"},
    {"ids": ["CVE-2026-41680", "GHSA-6v9c-7cg6-27q7"], "packages": ["marked"], "severity": "high", "cwe": ["CWE-674", "CWE-400"],
     "summary": "crafted markdown crashes the parser by running out of memory",
     "ranges": [r("18.0.0", "18.0.2", "18.0.2")], "precondition": "any-use", "raw": "xss--marked-readme-and-advisories.md"},
    {"ids": ["CVE-2026-47423", "GHSA-87xg-pxx2-7hvx"], "packages": ["dompurify"], "severity": "high", "cwe": ["CWE-79"],
     "summary": "a sanitizer bypass lets script through via the selectedcontent element",
     "ranges": [r("3.4.4", "3.4.5", "3.4.5")], "precondition": "none", "raw": "xss--dompurify-readme-and-advisories.md"},
    {"ids": ["CVE-2026-41238", "CVE-2026-41239", "CVE-2026-41240", "CVE-2026-49458", "CVE-2026-49459", "CVE-2026-49978",
             "GHSA-h8r8-wccr-v5f2", "GHSA-cjmm-f4jc-qw8r", "GHSA-cj63-jhhr-wcxv", "GHSA-39q2-94rc-95cp", "GHSA-76mc-f452-cxcm"],
     "packages": ["dompurify"], "severity": "medium", "cwe": ["CWE-79"],
     "summary": "several sanitizer bypasses, most tied to specific options (IN_PLACE, ADD_TAGS, ADD_ATTR, SAFE_FOR_TEMPLATES, hooks)",
     "ranges": [r("0.0.0", "3.4.7", "3.4.7")], "precondition": "sanitizer-config", "raw": "xss--dompurify-readme-and-advisories.md"},
    {"ids": ["GHSA-5c6j-r48x-rmvq", "GHSA-qj8w-gfj5-8c6v", "CVE-2026-34043"], "packages": ["serialize-javascript"], "severity": "high",
     "cwe": ["CWE-94", "CWE-400"],
     "summary": "code execution and denial of service when serializing attacker-influenced objects",
     "ranges": [r("0.0.0", "7.0.5", "7.0.5")], "precondition": "any-use", "raw": "ssr--serialize-javascript-advisories.md"},
]

# Packages that are a finding by their presence (unmaintained or deprecated), severity low.
UNMAINTAINED = {
    "react-scripts": ("Create React App is deprecated and has no active maintainers", "secrets--cra-env-and-sunset.md",
                      "Migrate the build to Vite (or a React framework) and move any REACT_APP_ values that are secrets to a server."),
    "react-html-parser": ("react-html-parser has had no release since 2017 and does not sanitize HTML", "xss--html-react-parser-readme.md",
                          "Replace it with react-markdown or html-react-parser fed only DOMPurify-sanitized input."),
    "draft-js": ("draft-js is archived by its maintainers", "xss--html-react-parser-readme.md",
                 "Plan a move to a maintained editor; until then sanitize any HTML it imports or exports."),
}

WATCH = sorted({p for a in ADVISORIES for p in a["packages"]} | set(UNMAINTAINED) | {"react", "react-dom", "next", "@react-router/dev", "rwsdk", "@parcel/rsc"})


# ---------------------------------------------------------------- versions

VER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?")


def parse_ver(v: str):
    m = VER_RE.match(v.strip())
    if not m:
        return None
    pre = m.group(4)
    pre_key = tuple(int(x) if x.isdigit() else x for x in pre.split(".")) if pre else None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), pre_key)


def cmp_ver(a, b) -> int:
    if a[:3] != b[:3]:
        return -1 if a[:3] < b[:3] else 1
    pa, pb = a[3], b[3]
    if pa == pb:
        return 0
    if pa is None:
        return 1  # release sorts after its prereleases
    if pb is None:
        return -1
    for x, y in zip(pa, pb):
        if x == y:
            continue
        if isinstance(x, int) and isinstance(y, int):
            return -1 if x < y else 1
        if isinstance(x, int):
            return -1
        if isinstance(y, int):
            return 1
        return -1 if x < y else 1
    return -1 if len(pa) < len(pb) else (1 if len(pa) > len(pb) else 0)


def in_range(ver, rng) -> bool:
    lo, hi = parse_ver(rng["lo"]), parse_ver(rng["hi"])
    if cmp_ver(ver, lo) < 0:
        return False
    c = cmp_ver(ver, hi)
    return c <= 0 if rng["hi_inclusive"] else c < 0


def is_canary(v: str) -> bool:
    return bool(re.search(r"-(canary|experimental|rc|next|beta|alpha)", v))


# ---------------------------------------------------------------- lockfile parsing

def find_line(lines: list[str], *needles: str) -> int:
    for i, line in enumerate(lines, 1):
        if all(n in line for n in needles):
            return i
    return 1


def parse_package_lock(path: Path, text: str) -> list[dict]:
    out = []
    data = json.loads(text)
    lines = text.splitlines()
    pkgs = data.get("packages")
    if isinstance(pkgs, dict):
        for key, meta in pkgs.items():
            if "node_modules/" not in key or not isinstance(meta, dict):
                continue
            name = key.rsplit("node_modules/", 1)[1]
            if name in WATCH and meta.get("version"):
                out.append({"name": name, "version": meta["version"], "file": path, "line": find_line(lines, f'"{key}"'), "how": "lockfile"})
        return out

    def walk(deps: dict):
        for name, meta in (deps or {}).items():
            if not isinstance(meta, dict):
                continue
            if name in WATCH and meta.get("version"):
                out.append({"name": name, "version": meta["version"], "file": path, "line": find_line(lines, f'"{name}"', "{"), "how": "lockfile"})
            walk(meta.get("dependencies"))

    walk(data.get("dependencies"))
    return out


PNPM_KEY = re.compile(r"^\s{2}'?/?((?:@[^/@\s]+/)?[^/@\s(]+)[@/]([0-9][^:('\s]*)")


def parse_pnpm(path: Path, text: str) -> list[dict]:
    out, seen = [], set()
    in_section = False
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^(packages|snapshots):\s*$", line):
            in_section = True
            continue
        if re.match(r"^\S", line):
            in_section = False
        if not in_section:
            continue
        m = PNPM_KEY.match(line)
        if m and m.group(1) in WATCH:
            key = (m.group(1), m.group(2))
            if key not in seen:
                seen.add(key)
                out.append({"name": m.group(1), "version": m.group(2), "file": path, "line": i, "how": "lockfile"})
    return out


YARN_HEADER = re.compile(r'^"?((?:@[^/@\s"]+/)?[^@\s",]+)@')


def parse_yarn(path: Path, text: str) -> list[dict]:
    out, seen = [], set()
    current, header_line = None, 0
    for i, line in enumerate(text.splitlines(), 1):
        if line and not line.startswith((" ", "#")) and line.rstrip().endswith(":"):
            first = line.split(",")[0].strip()
            m = YARN_HEADER.match(first)
            current = m.group(1) if m else None
            header_line = i
            continue
        if current and current in WATCH:
            m = re.match(r'^\s+version:?\s+"?([0-9][^"\s]*)"?', line)
            if m:
                key = (current, m.group(1))
                if key not in seen:
                    seen.add(key)
                    out.append({"name": current, "version": m.group(1), "file": path, "line": header_line, "how": "lockfile"})
                current = None
    return out


def parse_manifest(path: Path, text: str) -> list[dict]:
    out = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return out
    lines = text.splitlines()
    for section in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
        for name, spec in (data.get(section) or {}).items():
            if name in WATCH and isinstance(spec, str):
                m = re.search(r"(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)", spec)
                out.append({"name": name, "version": m.group(1) if m else spec, "spec": spec, "section": section,
                            "file": path, "line": find_line(lines, f'"{name}"'), "how": "manifest"})
    return out


# ---------------------------------------------------------------- repository walk

MAX_READ_BYTES = 2_000_000
STATS = {"symlinks": 0}
REPO_REAL = {"root": ""}


def _inside(path, root_real: str) -> bool:
    real = os.path.realpath(path)
    return real == root_real or real.startswith(root_real + os.sep)


def safe_read_text(p: Path, limit: int = MAX_READ_BYTES):
    """Read a regular, non-symlink file inside the repo, or return None (symlinks counted)."""
    try:
        if os.path.islink(p):
            STATS["symlinks"] += 1
            return None
        st = os.lstat(p)
        if not stat.S_ISREG(st.st_mode) or st.st_size > limit:
            return None
        if REPO_REAL["root"] and not _inside(p, REPO_REAL["root"]):
            STATS["symlinks"] += 1
            return None
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def walk_files(root: Path, max_files: int, caps: list[str]):
    count = 0
    if os.path.islink(root):
        STATS["symlinks"] += 1
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
                STATS["symlinks"] += 1
                continue
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                continue
            if stat.S_ISDIR(mode):
                if p.name not in SKIP_DIRS:
                    stack.append(p)
            elif stat.S_ISREG(mode):
                count += 1
                if count > max_files:
                    caps.append(f"file walk stopped at --max-files {max_files}; rerun with a higher limit")
                    return
                yield p


def collect(repo: Path, paths: list[str], max_files: int):
    caps: list[str] = []
    roots = [repo / p for p in paths] if paths else [repo]
    installs, manifests, lockfiles, source_files = [], [], [], []
    seen_files = set()
    # lockfiles may sit at the repo root of a monorepo, above the stack path
    candidates = set()
    for root in roots:
        cur = root
        while True:
            candidates.add(cur)
            if cur == repo or repo not in cur.parents:
                break
            cur = cur.parent
    for d in sorted(candidates):
        for name in ("package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb"):
            p = d / name
            if p.is_file() and not os.path.islink(p):
                lockfiles.append(p)
            elif os.path.islink(p):
                STATS["symlinks"] += 1
    for root in roots:
        if not root.exists():
            caps.append(f"stack path not found: {root.relative_to(repo) if repo in root.parents else root}")
            continue
        for p in walk_files(root, max_files, caps):
            if p in seen_files:
                continue
            seen_files.add(p)
            if p.name == "package.json":
                manifests.append(p)
            elif p.name in ("package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb") and p not in lockfiles:
                lockfiles.append(p)
            elif p.suffix in SRC_EXT or p.name.startswith("react-router.config"):
                source_files.append(p)
    for lf in lockfiles:
        if lf.name.startswith("bun.lock"):
            caps.append(f"{lf.name} is not parsed by this script; read versions by hand")
            continue
        try:
            text = safe_read_text(lf)
            if text is None:
                continue
            if lf.name.endswith(".json"):
                installs += parse_package_lock(lf, text)
            elif lf.name == "pnpm-lock.yaml":
                installs += parse_pnpm(lf, text)
            else:
                installs += parse_yarn(lf, text)
        except (OSError, ValueError) as e:
            caps.append(f"could not parse {lf.name}: {e}")
    declared = []
    for mf in manifests:
        mtext = safe_read_text(mf)
        if mtext is not None:
            declared += parse_manifest(mf, mtext)
    return installs, declared, lockfiles, source_files, caps


FEATURE_PATTERNS = {
    "rr-file-session": re.compile(r"createFileSessionStorage"),
    "rr-data-router": re.compile(r"create(Browser|Hash|Memory|Static)Router|RouterProvider"),
    "rr-rsc": re.compile(r"unstable_(RSC|matchRSCServerRequest|routeRSCServerRequest|createCallServer)"),
    "dompurify-risky-options": re.compile(r"IN_PLACE|ADD_TAGS|ADD_ATTR|SAFE_FOR_TEMPLATES|CUSTOM_ELEMENT_HANDLING|USE_PROFILES|addHook\("),
    "mdx-compile": re.compile(r"\b(serialize|compileMDX|evaluate|bundleMDX)\s*\("),
    "use-server": re.compile(r"""^\s*['"]use server['"]""", re.M),
}


def detect_features(source_files: list[Path], installed_names: set[str], repo: Path) -> dict:
    hits = {k: [] for k in FEATURE_PATTERNS}
    rr_config = False
    for p in source_files:
        if p.name.startswith("react-router.config"):
            rr_config = True
        text = safe_read_text(p, 1_000_000)
        if text is None:
            continue
        for k, rx in FEATURE_PATTERNS.items():
            if len(hits[k]) < 5 and rx.search(text):
                hits[k].append(str(p.relative_to(repo)))
    feats = {
        "rsc": bool(installed_names & set(RSDW + ["@vitejs/plugin-rsc", "waku", "rwsdk", "@parcel/rsc"])),
        "rr-framework": "@react-router/dev" in installed_names or rr_config,
        "rr-data-or-framework": bool(hits["rr-data-router"]) or "@react-router/dev" in installed_names or rr_config,
        "rr-ssr": "@react-router/dev" in installed_names or rr_config,
        "rr-rsc": bool(hits["rr-rsc"]),
        "rr-file-session": bool(hits["rr-file-session"]),
        "sanitizer-config": bool(hits["dompurify-risky-options"]),
        "untrusted-mdx": False,  # needs a human read of where the MDX comes from
        "dev-server": False,     # only reachable when the dev server is exposed; never assumed
        "any-use": False,
        "none": True,
    }
    return {"flags": feats, "evidence": {k: v for k, v in hits.items() if v}}


# ---------------------------------------------------------------- findings

SEV_ORDER = ["info", "low", "medium", "high", "critical"]
OWASP = {"CWE-79": "OWASP A05:2025", "CWE-94": "OWASP A05:2025", "CWE-20": "OWASP A05:2025", "CWE-601": "OWASP A01:2025",
         "CWE-352": "OWASP A01:2025", "CWE-22": "OWASP A01:2025", "CWE-497": "OWASP A01:2025", "CWE-502": "OWASP A08:2025",
         "CWE-345": "OWASP A08:2025", "CWE-346": "OWASP A07:2025"}
PRECONDITION_TEXT = {
    "rsc": "the app runs a React Server Components server",
    "dev-server": "the development server is reachable from other machines (for example started with --host)",
    "rr-framework": "React Router Framework Mode is used",
    "rr-ssr": "React Router renders on the server",
    "rr-data-or-framework": "React Router Data Mode or Framework Mode is used",
    "rr-rsc": "React Router's unstable RSC APIs are used",
    "rr-file-session": "createFileSessionStorage is used",
    "untrusted-mdx": "MDX from users or other untrusted sources is compiled",
    "sanitizer-config": "DOMPurify runs with the options named in the advisories",
    "any-use": "untrusted input reaches the affected API",
    "none": "the package is installed",
}


def cap_severity(sev: str, confidence: str) -> str:
    if confidence == "possible" and SEV_ORDER.index(sev) > SEV_ORDER.index("medium"):
        return "medium"
    return sev


def rel(p: Path, repo: Path) -> str:
    try:
        return str(p.relative_to(repo))
    except ValueError:
        return str(p)


def evaluate(installs, declared, feats, repo: Path, start_id: int, caps: list[str]):
    findings = []
    nid = start_id
    have_lock = {i["name"] for i in installs}
    declared_in = {}
    for d in declared:
        declared_in.setdefault(d["name"], rel(d["file"], repo))
    targets = list(installs) + [d for d in declared if d["name"] not in have_lock]
    seen = set()
    for inst in targets:
        key = (inst["name"], inst["version"], rel(inst["file"], repo))
        if key in seen:
            continue
        seen.add(key)
        name = inst["name"]
        if name in UNMAINTAINED:
            if name in {f["_pkg"] for f in findings if "_pkg" in f}:
                continue
            why, raw, fix = UNMAINTAINED[name]
            f = make_finding(nid, title=f"The app depends on {name}, which is no longer maintained.",
                             severity="low", confidence="confirmed", inst=inst, repo=repo,
                             evidence_extra=why, why=f"{why}. Unmaintained packages stop receiving security fixes.",
                             remediation=fix, effort="M", refs=["CWE-1104", "OWASP A03:2025", GUIDE_SC, f"raw/{raw}"],
                             verified="Package found in the lockfile or package.json; maintenance status from the npm registry and project notices in the research archive.")
            f["_pkg"] = name
            findings.append(f)
            nid += 1
            continue
        if is_canary(inst["version"]) and (name in RSDW or name in ("react", "react-dom", "@vitejs/plugin-rsc")):
            caps.append(f"{name} {inst['version']} is a prerelease build; prereleases are not compared with the advisory table, check by hand")
            continue
        ver = parse_ver(inst["version"])
        if ver is None:
            continue
        matched = []
        for adv in ADVISORIES:
            if name not in adv["packages"]:
                continue
            for rng in adv["ranges"]:
                if in_range(ver, rng):
                    matched.append((adv, rng))
                    break
        if not matched:
            continue
        scored = []
        for adv, rng in matched:
            met = bool(feats["flags"].get(adv["precondition"], False))
            conf = "likely" if (met and inst["how"] == "lockfile") else "possible"
            scored.append((SEV_ORDER.index(cap_severity(adv["severity"], conf)), conf == "likely", adv, conf))
        scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
        _, _, top, confidence = scored[0]
        severity = cap_severity(top["severity"], confidence)
        fixed = max((parse_ver(rng["fixed"]), rng["fixed"]) for _, rng in matched)[1]
        unmet = sorted({a["precondition"] for a, _ in matched if not feats["flags"].get(a["precondition"], False)})
        ids = []
        for a, _ in matched:
            for i in a["ids"]:
                if i not in ids:
                    ids.append(i)
        cwes = sorted({c for a, _ in matched for c in a["cwe"]})
        owasp = sorted({OWASP[c] for c in cwes if c in OWASP} | {"OWASP A03:2025"})
        guide = GUIDE_RSC if name in RSDW or name in ("@vitejs/plugin-rsc", "waku") else (
            GUIDE_RR if name.startswith(("react-router", "@react-router", "@remix-run")) else GUIDE_XSS)
        summaries = "; ".join(sorted({a["summary"] for a, _ in matched}))
        pre_text = "; ".join(sorted({PRECONDITION_TEXT[a["precondition"]] for a, _ in matched}))
        vendored = " @vitejs/plugin-rsc ships its own copy of react-server-dom-webpack, so upgrade the plugin itself." if name == "@vitejs/plugin-rsc" else ""
        source_note = "declared range in package.json (no lockfile entry found)" if inst["how"] == "manifest" else "resolved in the lockfile"
        manifest = declared_in.get(name, "the package.json that declares it")
        major_jump = parse_ver(fixed)[0] > ver[0]
        findings.append(make_finding(
            nid,
            title=f"{name} {inst['version']} has known security holes, the worst: {top['summary']}.",
            severity=severity, confidence=confidence, inst=inst, repo=repo,
            evidence_extra=f"{source_note}; matches {', '.join(ids)} (advisory table as of {TABLE_AS_OF})",
            why=(f"Affected by published advisories: {summaries}. They apply when: {pre_text}."
                 + ("" if not unmet else f" Not yet shown for this repo by the script: {'; '.join(PRECONDITION_TEXT[p] for p in unmet)}.")),
            remediation=(f"Upgrade {name} from {inst['version']} to {fixed} or later in {manifest} "
                         f"and regenerate the lockfile.{vendored}"),
            effort="M" if major_jump else "S",
            refs=ids + cwes + owasp + ["CWE-1395", guide] + sorted({f"raw/{a['raw']}" for a, _ in matched}),
            verified=(f"Version {source_note}; compared with the advisory ranges in react_version_check.py. "
                      f"Preconditions found by source scan: {json.dumps({p: feats['flags'].get(p) for p in sorted({a['precondition'] for a, _ in matched})})}."),
            tags=["dependency", "version-check"] + (["rsc"] if name in RSDW or name == "@vitejs/plugin-rsc" else []),
        ))
        nid += 1
    for f in findings:
        f.pop("_pkg", None)
    # React 18 or older: javascript: URLs are not blocked
    for inst in installs:
        if inst["name"] == "react":
            v = parse_ver(inst["version"])
            if v and v[0] < 19:
                findings.append(make_finding(
                    nid, title=f"The app runs React {inst['version']}, which does not block javascript: links.",
                    severity="info", confidence="confirmed", inst=inst, repo=repo,
                    evidence_extra="React 18 and older only warn in development about javascript: URLs; React 19 replaces them",
                    why="Any link or form address built from user data can run script when clicked, so the URL checks in guide 01 apply at full strength.",
                    remediation="Plan the React 19 upgrade; until then validate every dynamic href, src, action, and formAction against an allow-list of schemes.",
                    effort="L", refs=["CWE-79", "OWASP A05:2025", GUIDE_XSS, "raw/xss--react-dom-url-sanitization-source.md"],
                    verified="Version resolved in the lockfile; behavior read from React 18.3.1 and 19.2.0 source.",
                    tags=["react-18"]))
                nid += 1
                break
    return findings, nid


def make_finding(nid, title, severity, confidence, inst, repo, evidence_extra, why, remediation, effort, refs, verified, tags=None):
    path = rel(inst["file"], repo)
    excerpt = ""
    ftext = safe_read_text(inst["file"])
    if ftext is not None:
        lines = ftext.splitlines()
        lo = max(0, inst["line"] - 1)
        excerpt = "\n".join(lines[lo:lo + 3])
    return {
        "id": f"SEC-REACT-{nid:03d}",
        "dimension": "security",
        "source": SOURCE,
        "title": title,
        "severity": severity,
        "confidence": confidence,
        "locations": [{"path": path, "line_start": inst["line"], "line_end": inst["line"] + 2}],
        "evidence": f"{path}:{inst['line']}\n{excerpt}\n({evidence_extra})",
        "why_it_matters": why,
        "remediation": remediation,
        "effort": effort,
        "refs": refs,
        "verified_by": verified,
        "tags": tags or ["dependency"],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", required=True, help="audited repository root (read only)")
    ap.add_argument("--paths", nargs="*", default=[], help="stack paths relative to the repo (default: whole repo)")
    ap.add_argument("--out", help="write findings JSONL here (default: stdout only)")
    ap.add_argument("--summary", help="write the detection summary JSON here")
    ap.add_argument("--start-id", type=int, default=1, help="first SEC-REACT number to use")
    ap.add_argument("--max-files", type=int, default=20000)
    a = ap.parse_args(argv)
    repo = Path(a.repo).resolve()
    if not repo.is_dir():
        print(f"not a directory: {repo}", file=sys.stderr)
        return 2
    for o in (a.out, a.summary):
        if o:
            op = Path(o).resolve()
            if repo == op or repo in op.parents:
                print(f"refusing to write output inside the audited repository: {op}", file=sys.stderr)
                return 2
    REPO_REAL["root"] = os.path.realpath(repo)
    installs, declared, lockfiles, source_files, caps = collect(repo, a.paths, a.max_files)
    if STATS["symlinks"]:
        caps.append(f"{STATS['symlinks']} symlink(s) skipped (never followed)")
    if not lockfiles:
        caps.append("no lockfile found; versions come from package.json ranges and every version finding is capped at confidence possible")
    names = {i["name"] for i in installs} or {d["name"] for d in declared}
    feats = detect_features(source_files, names, repo)
    findings, _ = evaluate(installs, declared, feats, repo, a.start_id, caps)
    if "next" in names:
        caps.append("next is installed: Next.js bundles its own React Server Components runtime; its version check belongs to nextjs-security-wasp-drone")
    summary = {
        "script": "react_version_check.py", "advisory_table_as_of": TABLE_AS_OF, "repo": str(repo), "paths": a.paths,
        "lockfiles": [rel(p, repo) for p in lockfiles],
        "installed": sorted({(i["name"], i["version"], rel(i["file"], repo)) for i in installs}),
        "declared": sorted({(d["name"], d.get("spec", d["version"]), rel(d["file"], repo)) for d in declared}),
        "features": feats,
        "findings": len(findings),
        "by_severity": {s: sum(1 for f in findings if f["severity"] == s) for s in reversed(SEV_ORDER)},
        "caps": caps,
    }
    lines = "".join(json.dumps(f) + "\n" for f in findings)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(lines, encoding="utf-8")
    else:
        sys.stdout.write(lines)
    if a.summary:
        Path(a.summary).parent.mkdir(parents=True, exist_ok=True)
        Path(a.summary).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("lockfiles", "findings", "by_severity", "caps")}), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
