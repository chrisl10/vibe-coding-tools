#!/usr/bin/env python3
"""Deterministic first pass for a SvelteKit / Svelte security audit (read only).

Usage:
    python3 sveltekit_audit_scan.py --repo PATH --out-dir DIR [--paths apps/web ...]
                                    [--advisories advisories.json] [--id-start 1]

What it does, and nothing more:
  1. Reads installed versions of svelte, @sveltejs/kit, devalue and the official adapters
     from lockfiles (package-lock.json, npm-shrinkwrap.json, pnpm-lock.yaml, yarn.lock,
     bun.lock), then node_modules/<pkg>/package.json, never from package.json ranges alone.
  2. Matches every installed version against advisories.json (GitHub advisories, see
     references/advisory-table.md) and writes contract-shaped findings for each match to
     <out-dir>/sveltekit-version-findings.jsonl.
  3. Inventories the attack surface for manual review: server loads, universal loads,
     +server endpoints, form actions, hooks, remote functions, {@html} and innerHTML sinks,
     svelte.config settings, PUBLIC_ env names, cookie options, redirects built from input,
     module-level stores, service worker caching. Written to <out-dir>/sveltekit-inventory.json.

It never writes inside --repo, never runs package managers, never prints env values.
Python 3.11 standard library only. Exit code 0 on success, 2 on bad arguments.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

SOURCE = "sveltekit-security-wasp-drone"
PACKAGES = [
    "svelte",
    "@sveltejs/kit",
    "devalue",
    "@sveltejs/adapter-node",
    "@sveltejs/adapter-vercel",
    "@sveltejs/adapter-cloudflare",
    "@sveltejs/adapter-netlify",
    "@sveltejs/adapter-static",
    "@sveltejs/adapter-auto",
    "@sveltejs/vite-plugin-svelte",
    "mdsvex",
]
SKIP_DIRS = {"node_modules", ".svelte-kit", ".git", "build", "dist", ".vercel", ".netlify",
             ".output", ".wrangler", "coverage", ".turbo", ".next", "vendor"}
CODE_EXT = {".ts", ".js", ".mjs", ".cjs", ".mts", ".cts", ".svelte"}
MARKUP_EXT = {".svelte", ".md", ".svx"}
MAX_FILE_BYTES = 1_500_000

# ---------------------------------------------------------------- safe reads (never follow symlinks)

STATS = {"symlinks": 0}
REPO_REAL = {"root": ""}


def _inside(path, root_real: str) -> bool:
    real = os.path.realpath(path)
    return real == root_real or real.startswith(root_real + os.sep)


def safe_read(p: Path, limit: int = MAX_FILE_BYTES, errors: str = "strict") -> str:
    """Read a regular, non-symlink file inside the repo. Raises OSError for anything else."""
    if os.path.islink(p):
        STATS["symlinks"] += 1
        raise OSError("symlink not followed")
    st = os.lstat(p)
    if not stat.S_ISREG(st.st_mode) or st.st_size > limit:
        raise OSError("not a regular file or over size cap")
    if REPO_REAL["root"] and not _inside(p, REPO_REAL["root"]):
        STATS["symlinks"] += 1
        raise OSError("outside repository")
    return p.read_text(encoding="utf-8", errors=errors)

# ---------------------------------------------------------------- semver

SEMVER = re.compile(r"^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:-([0-9A-Za-z.-]+))?(?:\+.*)?$")


def parse_version(text: str):
    m = SEMVER.match(text.strip())
    if not m:
        return None
    major, minor, patch, pre = m.groups()
    pre_key = tuple(int(p) if p.isdigit() else p for p in pre.split(".")) if pre else None
    return (int(major), int(minor or 0), int(patch or 0), pre_key)


def cmp_versions(a, b) -> int:
    if a[:3] != b[:3]:
        return -1 if a[:3] < b[:3] else 1
    pa, pb = a[3], b[3]
    if pa == pb:
        return 0
    if pa is None:
        return 1  # release sorts after prerelease
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


COMPARATOR = re.compile(r"(>=|<=|>|<|=)?\s*(v?\d+(?:\.\d+){0,2}(?:-[0-9A-Za-z.-]+)?)")


def in_range(version: str, spec: str) -> bool | None:
    """True if version satisfies spec (advisory style: '>= 2.49.0, <= 2.49.4', '< 5.3.2',
    '= 4.0.0', alternatives with '||'). None if either side cannot be parsed."""
    v = parse_version(version)
    if v is None or not spec:
        return None
    for alternative in spec.split("||"):
        comparators = COMPARATOR.findall(alternative)
        if not comparators:
            return None
        ok = True
        for op, ver in comparators:
            target = parse_version(ver)
            if target is None:
                return None
            c = cmp_versions(v, target)
            op = op or "="
            if not ((op == ">=" and c >= 0) or (op == "<=" and c <= 0) or (op == ">" and c > 0)
                    or (op == "<" and c < 0) or (op == "=" and c == 0)):
                ok = False
                break
        if ok:
            return True
    return False

# ---------------------------------------------------------------- lockfiles


def add(found: dict, name: str, version: str, where: str) -> None:
    if name in PACKAGES and parse_version(version):
        found.setdefault(name, {}).setdefault(version, set()).add(where)


def read_npm_lock(path: Path, found: dict, rel: str) -> None:
    try:
        data = json.loads(safe_read(path, 5_000_000))
    except (OSError, ValueError):
        return
    for key, meta in (data.get("packages") or {}).items():
        if not key or "node_modules/" not in key or not isinstance(meta, dict):
            continue
        name = key.rsplit("node_modules/", 1)[1]
        if meta.get("version"):
            add(found, name, meta["version"], rel)

    def walk(deps: dict) -> None:
        for name, meta in (deps or {}).items():
            if isinstance(meta, dict):
                if meta.get("version"):
                    add(found, name, meta["version"], rel)
                walk(meta.get("dependencies") or {})
    walk(data.get("dependencies") or {})


PNPM_LINE = re.compile(r"^\s+'?/?((?:@[^@/\s']+/)?[^@/\s'(]+)[@/](\d[^\s:'()_]*)")


def read_pnpm_lock(path: Path, found: dict, rel: str) -> None:
    try:
        lines = safe_read(path, 5_000_000).splitlines()
    except OSError:
        return
    section = ""
    for line in lines:
        if line and not line.startswith(" "):
            section = line.rstrip(":").strip()
            continue
        if section not in {"packages", "snapshots"}:
            continue
        m = PNPM_LINE.match(line)
        if m and line.rstrip().endswith(":"):
            add(found, m.group(1), m.group(2), rel)


YARN_HEAD = re.compile(r'^"?((?:@[^@/\s"]+/)?[^@/\s",]+)@')
YARN_VER = re.compile(r'^\s+version:?\s+"?([^"\s]+)"?')


def read_yarn_lock(path: Path, found: dict, rel: str) -> None:
    try:
        lines = safe_read(path, 5_000_000).splitlines()
    except OSError:
        return
    current = None
    for line in lines:
        if line and not line.startswith(" ") and not line.startswith("#"):
            m = YARN_HEAD.match(line.strip())
            current = m.group(1) if m else None
            continue
        if current:
            m = YARN_VER.match(line)
            if m:
                add(found, current, m.group(1), rel)
                current = None


BUN_ENTRY = re.compile(r'"((?:@[^@/\s"]+/)?[^@/\s"]+)@(\d[^"]*)"')


def read_bun_lock(path: Path, found: dict, rel: str) -> None:
    try:
        text = safe_read(path, 5_000_000)
    except OSError:
        return
    for name, version in BUN_ENTRY.findall(text):
        add(found, name, version, rel)


def find_versions(repo: Path, roots: list[Path]) -> tuple[dict, list[str], dict]:
    found: dict = {}
    lockfiles: list[str] = []
    declared: dict = {}
    candidates: set[Path] = set()
    for root in roots + [repo]:
        p = root
        while True:
            candidates.add(p)
            if p == repo or repo not in p.parents:
                break
            p = p.parent
    readers = {"package-lock.json": read_npm_lock, "npm-shrinkwrap.json": read_npm_lock,
               "pnpm-lock.yaml": read_pnpm_lock, "yarn.lock": read_yarn_lock, "bun.lock": read_bun_lock}
    for d in sorted(candidates):
        for fname, reader in readers.items():
            f = d / fname
            if f.is_file():
                rel = str(f.relative_to(repo))
                lockfiles.append(rel)
                reader(f, found, rel)
        if (d / "bun.lockb").is_file():
            lockfiles.append(str((d / "bun.lockb").relative_to(repo)) + " (binary, not parsed)")
        for name in PACKAGES:
            pj = d / "node_modules" / name / "package.json"
            if pj.is_file():
                try:
                    v = json.loads(safe_read(pj, 5_000_000)).get("version")
                    if v:
                        add(found, name, v, str(pj.relative_to(repo)))
                except (OSError, ValueError):
                    pass
        pkg = d / "package.json"
        if pkg.is_file():
            try:
                data = json.loads(safe_read(pkg, 5_000_000))
            except (OSError, ValueError):
                data = {}
            for block in ("dependencies", "devDependencies", "peerDependencies"):
                for name, rng in (data.get(block) or {}).items():
                    if name in PACKAGES:
                        declared.setdefault(name, []).append({"file": str(pkg.relative_to(repo)), "range": rng})
    return found, lockfiles, declared

# ---------------------------------------------------------------- file walk


def iter_files(roots: list[Path]):
    seen = set()
    for root in roots:
        if root.is_file():
            yield root
            continue
        stack = [root]
        while stack:
            d = stack.pop()
            try:
                entries = sorted(d.iterdir())
            except OSError:
                continue
            for e in entries:
                if os.path.islink(e):
                    STATS["symlinks"] += 1
                    continue
                if e.is_dir():
                    if e.name not in SKIP_DIRS:
                        stack.append(e)
                elif e.is_file() and e not in seen:
                    seen.add(e)
                    yield e


def read_text(p: Path) -> str | None:
    try:
        return safe_read(p, MAX_FILE_BYTES, "replace")
    except OSError:
        return None


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1

# ---------------------------------------------------------------- inventory patterns

ROUTE_FILE = re.compile(r"^\+(page|layout)(\.server)?\.(ts|js)$|^\+server\.(ts|js)$")
HOOKS_FILE = re.compile(r"^hooks(\.server|\.client)?\.(ts|js)$")
REMOTE_FILE = re.compile(r"\.remote\.(ts|js)$")
SVELTE_CONFIG = re.compile(r"^svelte\.config\.(js|ts|mjs|cjs)$")
SW_FILE = re.compile(r"^service-worker(\.(ts|js)|/index\.(ts|js))$")

EXPORT_FN = re.compile(r"export\s+(?:async\s+)?(?:function\s+|const\s+|let\s+)(\w+)")
HTTP_VERBS = {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD", "fallback"}
ACTIONS_BLOCK = re.compile(r"export\s+const\s+actions\b[^=]*=\s*\{", re.S)
PAGE_OPTION = re.compile(r"export\s+const\s+(prerender|ssr|csr|trailingSlash|config)\s*=\s*([^;\n]+)")
AUTH_HINT = re.compile(
    r"locals\.(user|session|auth|account|member)|getUser\w*\(|requireUser|requireAuth|"
    r"assertAuth|ensureAuth|getSession\(|auth\(\)|error\(\s*40[13]|redirect\(\s*30[1237][^)]*login|"
    r"isAdmin|hasRole|role\s*[!=]==|permissions?\b")
REMOTE_EXPORT = re.compile(
    r"export\s+const\s+(\w+)\s*(?::[^=]+)?=\s*(query\.batch|query\.live|query|form|command|prerender)\s*\(\s*([^\n]{0,80})")
HTML_TAG = re.compile(r"\{@html\s+([^}]{0,200})\}")
DOM_SINK = re.compile(r"\.(innerHTML|outerHTML)\s*=|insertAdjacentHTML\s*\(|document\.write\s*\(|createContextualFragment\s*\(")
SANITIZER = re.compile(r"DOMPurify|sanitize|purify|escapeHtml|escape\(|xss\(|sanitizeHtml", re.I)
MARKDOWN_LIB = re.compile(r"from\s+['\"](marked|markdown-it|mdsvex|snarkdown|showdown|remark[\w-]*|rehype[\w-]*|micromark|svelte-exmarkdown|@html-eslint[\w/-]*)['\"]")
ENV_IMPORT = re.compile(r"import\s*\{([^}]*)\}\s*from\s*['\"]\$env/(static|dynamic)/(public|private)['\"]")
ENV_DYNAMIC_PUBLIC = re.compile(r"\benv\.(PUBLIC_\w+)")
PUBLIC_NAME = re.compile(r"\b(PUBLIC_[A-Z0-9_]+)\b")
SECRETISH = re.compile(r"SECRET|PRIVATE|PASSWORD|PASSWD|SERVICE_ROLE|DATABASE_URL|DB_URL|CONN|TOKEN|"
                       r"(?<!PUBLISHABLE_)(?<!ANON_)(?<!SITE_)KEY(?!_ID)", re.I)
COOKIE_SET = re.compile(r"cookies\.(set|serialize)\s*\(([^;]{0,400})", re.S)
COOKIE_WEAK = re.compile(r"httpOnly\s*:\s*false|secure\s*:\s*false|sameSite\s*:\s*['\"]none['\"]", re.I)
REDIRECT_CALL = re.compile(r"redirect\(\s*(\d{3})\s*,\s*([^)\n]{1,160})")
REDIRECT_DYNAMIC = re.compile(r"searchParams|url\.|params\.|formData|data\.|get\(|request\.|`\$\{|\+\s*\w")
STORE_MODULE = re.compile(r"^export\s+(?:const|let)\s+(\w+)\s*=\s*(writable|readable|derived|persisted|\$state)\s*[(<]", re.M)
MODULE_LET = re.compile(r"^(?:let|var)\s+(\w+)\s*(?::[^=;\n]+)?(?:=|;)", re.M)
SEARCH_ITER = re.compile(r"url\.searchParams\.(entries|keys|forEach)\(|\[\.\.\.(?:event\.)?url\.searchParams|for\s*\(\s*const\s+\[[^\]]+\]\s+of\s+(?:event\.)?url\.searchParams|Object\.fromEntries\(\s*(?:event\.)?url\.searchParams")
SPREAD_ATTR = re.compile(r"<[a-zA-Z][\w:-]*[^>]*\{\.\.\.\s*[\w.]+\s*\}")
SVELTE_ELEMENT = re.compile(r"<svelte:element\s+this=\{")
HYDRATABLE = re.compile(r"\bhydratable\s*\(")
OPTION_DYNAMIC = re.compile(r"<option\b[^>]*>\s*\{(?!/)")
CONTENTEDITABLE_BIND = re.compile(r"contenteditable[^>]*bind:(innerText|textContent|innerHTML)")
TRANSFORM_ERROR = re.compile(r"transformError")
DEVALUE_IMPORT = re.compile(r"from\s+['\"]devalue['\"]")
BUFFER_RETURN = re.compile(r"Buffer\.from\(|readFileSync\(|new\s+Uint8Array\(")
ERROR_DYNAMIC = re.compile(r"error\(\s*\d{3}\s*,\s*(`[^`]*\$\{|[^'\"`)\s][^)]*)")
HANDLE_FETCH = re.compile(r"export\s+(?:async\s+)?(?:function|const)\s+handleFetch")
HOOK_EXPORTS = ("handle", "handleFetch", "handleError", "handleValidationError", "init", "reroute", "transport")
TRUST_HEADERS = re.compile(r"x-forwarded-(for|host|proto)|cf-connecting-ip|x-real-ip", re.I)
FETCH_DYNAMIC = re.compile(r"\bfetch\(\s*(`[^`]*\$\{|[a-zA-Z_][\w.]*\s*[,)])")


def top_level_keys(body: str) -> list[str]:
    """Keys of an object literal whose opening brace was just consumed (depth 1 only)."""
    keys: list[str] = []
    depth, i, n, expect_key = 1, 0, len(body), True
    key_rx = re.compile(r"\s*(?:async\s+)?['\"]?([A-Za-z_$][\w$-]*)['\"]?\s*(?::|\()")
    while i < n and depth > 0:
        ch = body[i]
        if ch in "'\"`":
            q = ch
            i += 1
            while i < n and body[i] != q:
                i += 2 if body[i] == "\\" else 1
        elif ch == "/" and body[i:i + 2] == "//":
            i = body.find("\n", i)
            i = n if i < 0 else i
            continue
        elif ch == "/" and body[i:i + 2] == "/*":
            i = body.find("*/", i)
            i = n if i < 0 else i + 2
            continue
        elif ch in "{([":
            depth += 1
        elif ch in "})]":
            depth -= 1
        elif ch == "," and depth == 1:
            expect_key = True
        if depth == 1 and expect_key and (ch in "{," or i == 0):
            m = key_rx.match(body, i + (0 if i == 0 and ch not in "{," else 1))
            if m:
                keys.append(m.group(1))
                expect_key = False
        i += 1
    return sorted(set(keys))


def config_inventory(text: str) -> dict:
    out: dict = {}
    m = re.search(r"from\s+['\"](@sveltejs/adapter-[\w-]+|svelte-adapter-[\w-]+|[\w@/.-]*adapter[\w@/.-]*)['\"]", text)
    out["adapter_import"] = m.group(1) if m else None
    out["csrf_checkOrigin_false"] = bool(re.search(r"checkOrigin\s*:\s*false", text))
    tm = re.search(r"trustedOrigins\s*:\s*\[([^\]]*)\]", text)
    out["csrf_trustedOrigins"] = [s.strip().strip("'\"") for s in tm.group(1).split(",") if s.strip()] if tm else []
    out["csrf_trusts_all"] = "*" in out["csrf_trustedOrigins"]
    out["csp_present"] = bool(re.search(r"\bcsp\s*:", text))
    cm = re.search(r"mode\s*:\s*['\"](hash|nonce|auto)['\"]", text)
    out["csp_mode"] = cm.group(1) if cm else None
    out["csp_unsafe_inline_script"] = bool(re.search(r"['\"]script-src['\"]\s*:\s*\[[^\]]*unsafe-(inline|eval)", text))
    out["csp_report_only_only"] = bool(re.search(r"reportOnly\s*:", text)) and not bool(re.search(r"directives\s*:", text))
    out["remote_functions_enabled"] = bool(re.search(r"remoteFunctions\s*:\s*true", text))
    out["paths_relative_false"] = bool(re.search(r"relative\s*:\s*false", text))
    out["dangerZone_present"] = "dangerZone" in text
    pm = re.search(r"publicPrefix\s*:\s*['\"]([^'\"]*)['\"]", text)
    out["env_publicPrefix"] = pm.group(1) if pm else None
    out["prerender_handleHttpError"] = bool(re.search(r"handleHttpError", text))
    out["serviceWorker_register_false"] = bool(re.search(r"register\s*:\s*false", text))
    return out


def scan(repo: Path, roots: list[Path]) -> dict:
    inv: dict = {
        "routes": [], "hooks": [], "remote_functions": [], "html_sinks": [], "dom_sinks": [],
        "markdown_libraries": [], "svelte_config": [], "env_public_names": [], "env_private_imports_in_client": [],
        "cookie_options_weakened": [], "redirects_dynamic": [], "module_level_state": [], "service_workers": [],
        "error_with_dynamic_message": [], "signals": {}, "files_scanned": 0, "skipped_large_files": [],
    }
    sig = {k: [] for k in ("search_params_iteration", "spread_attributes", "svelte_element", "hydratable",
                           "contenteditable_bind", "transform_error", "devalue_direct_import",
                           "buffer_like_in_server_load", "query_batch", "remote_form", "prerender_true",
                           "trusted_proxy_headers", "dynamic_fetch_in_server", "handle_redirect", "option_dynamic")}
    for f in iter_files(roots):
        rel = str(f.relative_to(repo))
        ext = f.suffix
        name = f.name
        is_code = ext in CODE_EXT
        is_markup = ext in MARKUP_EXT
        if not (is_code or is_markup or SVELTE_CONFIG.match(name)):
            continue
        text = read_text(f)
        if text is None:
            inv["skipped_large_files"].append(rel)
            continue
        inv["files_scanned"] += 1
        in_routes = "/routes/" in "/" + rel.replace("\\", "/")
        server_side = name.endswith((".server.ts", ".server.js")) or "/lib/server/" in "/" + rel or \
            bool(re.match(r"^\+server\.(ts|js)$", name)) or bool(REMOTE_FILE.search(name)) or \
            bool(re.match(r"^hooks\.server\.", name))

        if SVELTE_CONFIG.match(name):
            inv["svelte_config"].append({"path": rel, **config_inventory(text)})
            continue

        if in_routes and ROUTE_FILE.match(name):
            kind = ("endpoint" if name.startswith("+server") else
                    ("server_" if ".server." in name else "universal_") + ("page" if name.startswith("+page") else "layout"))
            exports = sorted(set(EXPORT_FN.findall(text)))
            entry = {"path": rel, "kind": kind, "exports": exports,
                     "http_methods": sorted(e for e in exports if e in HTTP_VERBS),
                     "has_load": "load" in exports, "actions": [],
                     "page_options": {k: v.strip() for k, v in PAGE_OPTION.findall(text)},
                     "auth_hint_lines": sorted(set(line_of(text, m.start()) for m in AUTH_HINT.finditer(text)))[:20]}
            am = ACTIONS_BLOCK.search(text)
            if am:
                entry["actions"] = top_level_keys(text[am.end(): am.end() + 20000])
                entry["actions_line"] = line_of(text, am.start())
            entry["needs_manual_authz_review"] = bool(entry["http_methods"] or entry["actions"] or
                                                        (entry["has_load"] and kind.startswith("server_")))
            entry["auth_hint_found"] = bool(entry["auth_hint_lines"])
            if re.search(r"prerender\s*=\s*true", text):
                sig["prerender_true"].append(rel)
            if kind.startswith("universal_") and ENV_IMPORT.search(text) and "private" in [m[2] for m in ENV_IMPORT.findall(text)]:
                inv["env_private_imports_in_client"].append(rel)
            if kind.startswith("server_") and BUFFER_RETURN.search(text):
                sig["buffer_like_in_server_load"].append(rel)
            inv["routes"].append(entry)

        if HOOKS_FILE.match(name) and "/src/" in "/" + rel:
            exports = set(EXPORT_FN.findall(text))
            h = {"path": rel, "exports": sorted(e for e in exports if e in HOOK_EXPORTS),
                 "uses_sequence": "sequence(" in text,
                 "sets_locals": sorted(set(re.findall(r"event\.locals\.(\w+)\s*=", text))),
                 "route_id_checks": [line_of(text, m.start()) for m in re.finditer(r"route\.id|url\.pathname", text)][:30],
                 "filterSerializedResponseHeaders": "filterSerializedResponseHeaders" in text,
                 "handleFetch_copies_cookie": bool(HANDLE_FETCH.search(text)) and bool(re.search(r"headers\.set\(\s*['\"](cookie|authorization)['\"]", text, re.I)),
                 "redirect_lines": [line_of(text, m.start()) for m in REDIRECT_CALL.finditer(text)][:20]}
            if h["redirect_lines"]:
                sig["handle_redirect"].append(rel)
            inv["hooks"].append(h)

        if REMOTE_FILE.search(name):
            for m in REMOTE_EXPORT.finditer(text):
                arg = m.group(3).strip()
                if re.match(r"['\"]unchecked['\"]", arg):
                    validation = "unchecked"
                elif re.match(r"(async\b|\(|function\b)", arg):
                    validation = "none (no argument accepted)"
                else:
                    validation = "schema"
                kind = m.group(2)
                inv["remote_functions"].append({"path": rel, "line": line_of(text, m.start()), "name": m.group(1),
                                                "kind": kind, "validation": validation})
                if kind == "query.batch":
                    sig["query_batch"].append(f"{rel}:{line_of(text, m.start())}")
                if kind == "form":
                    sig["remote_form"].append(f"{rel}:{line_of(text, m.start())}")

        if is_markup:
            for m in HTML_TAG.finditer(text):
                expr = m.group(1).strip()
                inv["html_sinks"].append({"path": rel, "line": line_of(text, m.start()), "expression": expr[:160],
                                          "sanitizer_in_expression": bool(SANITIZER.search(expr)),
                                          "sanitizer_in_file": bool(SANITIZER.search(text))})
            for rx, key in ((SPREAD_ATTR, "spread_attributes"), (SVELTE_ELEMENT, "svelte_element"),
                            (CONTENTEDITABLE_BIND, "contenteditable_bind"), (OPTION_DYNAMIC, "option_dynamic")):
                for m in rx.finditer(text):
                    sig[key].append(f"{rel}:{line_of(text, m.start())}")
        if is_code or is_markup:
            for m in DOM_SINK.finditer(text):
                inv["dom_sinks"].append({"path": rel, "line": line_of(text, m.start()),
                                         "snippet": text[m.start(): m.start() + 120].split("\n")[0]})
            for m in MARKDOWN_LIB.finditer(text):
                inv["markdown_libraries"].append({"path": rel, "line": line_of(text, m.start()), "library": m.group(1)})
            for m in ENV_IMPORT.finditer(text):
                if m.group(3) == "public":
                    for n in [x.strip() for x in m.group(1).split(",") if x.strip()]:
                        inv["env_public_names"].append({"path": rel, "line": line_of(text, m.start()), "name": n,
                                                        "looks_secret": bool(SECRETISH.search(n))})
            for m in ENV_DYNAMIC_PUBLIC.finditer(text):
                inv["env_public_names"].append({"path": rel, "line": line_of(text, m.start()), "name": m.group(1),
                                                "looks_secret": bool(SECRETISH.search(m.group(1)))})
            if ext == ".svelte" and re.search(r"\$env/(static|dynamic)/private|\$lib/server", text):
                inv["env_private_imports_in_client"].append(rel)
            for m in COOKIE_SET.finditer(text):
                if COOKIE_WEAK.search(m.group(2)):
                    inv["cookie_options_weakened"].append({"path": rel, "line": line_of(text, m.start()),
                                                           "snippet": " ".join(m.group(0).split())[:200]})
            for m in REDIRECT_CALL.finditer(text):
                target = m.group(2).strip()
                literal = re.match(r"^(['\"])[^'\"]*\1\s*$", target) or re.match(r"^`[^`$]*`\s*$", target)
                if not literal:
                    inv["redirects_dynamic"].append({"path": rel, "line": line_of(text, m.start()),
                                                     "status": m.group(1), "target": target[:120]})
            for m in ERROR_DYNAMIC.finditer(text):
                inv["error_with_dynamic_message"].append({"path": rel, "line": line_of(text, m.start()),
                                                          "snippet": m.group(0)[:120]})
            for rx, key in ((SEARCH_ITER, "search_params_iteration"), (HYDRATABLE, "hydratable"),
                            (TRANSFORM_ERROR, "transform_error"), (DEVALUE_IMPORT, "devalue_direct_import"),
                            (TRUST_HEADERS, "trusted_proxy_headers")):
                for m in rx.finditer(text):
                    sig[key].append(f"{rel}:{line_of(text, m.start())}")
            if server_side:
                for m in FETCH_DYNAMIC.finditer(text):
                    sig["dynamic_fetch_in_server"].append(f"{rel}:{line_of(text, m.start())}")
            if ext in {".ts", ".js"} and not in_routes:
                for m in STORE_MODULE.finditer(text):
                    inv["module_level_state"].append({"path": rel, "line": line_of(text, m.start()),
                                                      "name": m.group(1), "kind": m.group(2)})
            if ext in {".ts", ".js"} and (server_side or (in_routes and ".server." in name)):
                for m in MODULE_LET.finditer(text):
                    inv["module_level_state"].append({"path": rel, "line": line_of(text, m.start()),
                                                      "name": m.group(1), "kind": "module let in server file"})
        if SW_FILE.match(name) or rel.replace("\\", "/").endswith(("src/service-worker.ts", "src/service-worker.js")):
            inv["service_workers"].append({"path": rel, "caches_runtime_responses": "cache.put" in text,
                                           "respects_no_store": "no-store" in text,
                                           "skips_non_get": bool(re.search(r"method\s*!==\s*['\"]GET['\"]", text))})
    inv["signals"] = sig
    path_guards = [h["path"] for h in inv["hooks"] if h["route_id_checks"]]
    unguarded_remote = [f"{r['path']}:{r['line']}" for r in inv["remote_functions"] if r["kind"] != "prerender"]
    inv["cross_checks"] = {
        # route.id and url.pathname are client-chosen for remote calls, so a path guard never covers them
        "remote_functions_with_path_guard_only_risk": unguarded_remote if path_guards else [],
        "endpoints_without_auth_hint": [r["path"] for r in inv["routes"] if r["kind"] == "endpoint" and not r["auth_hint_found"]],
        "action_files_without_auth_hint": [r["path"] for r in inv["routes"] if r["actions"] and not r["auth_hint_found"]],
        "unsanitized_html_sinks": [f"{h['path']}:{h['line']}" for h in inv["html_sinks"] if not h["sanitizer_in_expression"]],
    }
    return inv

# ---------------------------------------------------------------- advisory matching


SEV_ORDER = ["info", "low", "medium", "high", "critical"]


def precondition_met(adv: dict, inv: dict, versions: dict) -> tuple[bool | None, str]:
    """Return (met, reason). None means cannot be judged from static signals."""
    g = adv["ghsa"]
    s = inv["signals"]
    cfg_remote = any(c.get("remote_functions_enabled") for c in inv["svelte_config"])
    adapters = [c.get("adapter_import") or "" for c in inv["svelte_config"]]
    uses_node = any("adapter-node" in a for a in adapters) or "@sveltejs/adapter-node" in versions
    has_post = any(r["actions"] or set(r["http_methods"]) & {"POST", "PUT", "PATCH", "DELETE", "fallback"} for r in inv["routes"])
    uses_vercel = any("adapter-vercel" in a for a in adapters) or "@sveltejs/adapter-vercel" in versions
    table = {
        "GHSA-866w-xmhq-wj7x": (bool(s["remote_form"]), "remote form functions found" if s["remote_form"] else "no remote form function found"),
        "GHSA-wqjv-9729-c5q2": (bool(s["remote_form"]), "remote form functions found" if s["remote_form"] else "no remote form function found"),
        "GHSA-fpg4-jhqr-589c": (bool(s["remote_form"]) and cfg_remote, "remote form plus experimental flag" if s["remote_form"] else "no remote form function found"),
        "GHSA-88qp-p4qg-rqm6": (bool(s["remote_form"]) and cfg_remote, "remote form plus experimental flag" if s["remote_form"] else "no remote form function found"),
        "GHSA-vrhm-gvg7-fpcf": (bool(s["remote_form"]) and cfg_remote, "remote form plus experimental flag" if s["remote_form"] else "no remote form function found"),
        "GHSA-j2f3-wq62-6q46": (bool(s["remote_form"]), "remote form functions found" if s["remote_form"] else "no remote form function found"),
        "GHSA-hgv7-v322-mmgr": (bool(s["query_batch"]), "query.batch used" if s["query_batch"] else "query.batch not found"),
        "GHSA-3f6h-2hrp-w5wx": (bool(s["handle_redirect"]), "redirect() inside hooks" if s["handle_redirect"] else "no redirect() in hooks"),
        "GHSA-2crg-3p73-43xp": (uses_node, "adapter-node in use" if uses_node else "adapter-node not detected"),
        "GHSA-j62c-4x62-9r35": (bool(s["prerender_true"]), "prerendered routes found" + (" and adapter-node (check ORIGIN)" if uses_node else "") if s["prerender_true"] else "no prerender = true found"),
        "GHSA-9pq4-5hcf-288c": (uses_vercel, "adapter-vercel in use" if uses_vercel else "adapter-vercel not detected"),
        "GHSA-6q87-84jw-cjhp": (bool(s["search_params_iteration"]), "searchParams iteration found" if s["search_params_iteration"] else "no searchParams iteration found"),
        "GHSA-rjjv-87mx-6x3h": (False, "dev server only"),
        "GHSA-5p75-vc5g-8rv2": (has_post, "SvelteKit 1 origin check is bypassable for every form action and POST endpoint" if has_post else "no actions or mutating endpoints found"),
        "GHSA-gv7g-x59x-wf8f": (has_post, "SvelteKit 1 origin check is bypassable for every form action and POST endpoint" if has_post else "no actions or mutating endpoints found"),
        "GHSA-g5m6-hxpp-fc49": (uses_node, "adapter-node in use" if uses_node else "adapter-node not detected (preview server also affected)"),
        "GHSA-h7h7-mm68-gmrc": (bool(s["option_dynamic"]), "option element with dynamic content found" if s["option_dynamic"] else "no option element with dynamic content found"),
        "GHSA-mh2x-fcqh-fmqv": (bool(inv["error_with_dynamic_message"]), "error() with a non-literal message found" if inv["error_with_dynamic_message"] else "no dynamic error() message found"),
        "GHSA-f3cj-j4f6-wq85": (bool(s["hydratable"]), "hydratable used" if s["hydratable"] else "hydratable not used"),
        "GHSA-6738-r8g5-qwp3": (bool(s["hydratable"]), "hydratable used" if s["hydratable"] else "hydratable not used"),
        "GHSA-rcqx-6q8c-2c42": (bool(s["spread_attributes"]), "attribute spreading found" if s["spread_attributes"] else "no attribute spreading found"),
        "GHSA-pr6f-5x2q-rwfp": (bool(s["spread_attributes"]), "attribute spreading found" if s["spread_attributes"] else "no attribute spreading found"),
        "GHSA-f7gr-6p89-r883": (bool(s["spread_attributes"]), "attribute spreading found" if s["spread_attributes"] else "no attribute spreading found"),
        "GHSA-crpf-4hrx-3jrp": (bool(s["spread_attributes"]), "attribute spreading found" if s["spread_attributes"] else "no attribute spreading found"),
        "GHSA-9rmh-mm8f-r9h6": (bool(s["svelte_element"]), "svelte:element found" if s["svelte_element"] else "svelte:element not found"),
        "GHSA-m56q-vw4c-c2cp": (bool(s["svelte_element"]), "svelte:element found" if s["svelte_element"] else "svelte:element not found"),
        "GHSA-phwv-c562-gvmh": (bool(s["contenteditable_bind"]), "contenteditable binding found" if s["contenteditable_bind"] else "no contenteditable binding found"),
        "GHSA-qgvg-pr8v-6rr3": (bool(s["transform_error"]), "transformError found" if s["transform_error"] else "transformError not found"),
        "GHSA-j22f-vq7h-c4qm": (bool(s["buffer_like_in_server_load"]) or None, "Buffer or typed array near a server load" if s["buffer_like_in_server_load"] else "cannot rule out without reading every server load"),
    }
    if g in table:
        return table[g]
    if adv["package"] == "devalue":
        # SvelteKit itself calls devalue.parse on client-sent data for remote functions and form actions.
        return (None, "devalue is used by SvelteKit to (de)serialise data; reachability depends on remote functions, actions and direct imports")
    return (None, "precondition not machine-checkable")




def lock_line(repo: Path, rel: str, pkg: str, version: str) -> int:
    """Best-effort line number of the package entry in a lockfile; 1 when not found."""
    p = repo / rel
    text = read_text(p) if p.is_file() else None
    if not text:
        return 1
    for needle in (f"{pkg}@{version}", f'"node_modules/{pkg}"', f"{pkg}@npm:{version}", f'"{pkg}@', f"\n{pkg}@", f'"{pkg}"'):
        i = text.find(needle)
        if i >= 0:
            return line_of(text, i)
    return 1


def version_findings(repo: Path, versions: dict, inv: dict, advisories: list[dict], id_start: int) -> tuple[list[dict], list[dict]]:
    """One finding per advisory whose precondition is detected in source (confidence likely).
    Advisories whose precondition is not detected are rolled up into one finding per package
    version (confidence possible, severity capped at medium, contract rule 5.3)."""
    findings: list[dict] = []
    matched: list[dict] = []
    n = id_start

    def locs_for(pkg: str, version: str, where: set) -> list[dict]:
        out = []
        for w in sorted(where):
            ln = lock_line(repo, w, pkg, version)
            out.append({"path": w, "line_start": ln, "line_end": ln})
        return out

    for pkg in PACKAGES:
        for version, where in sorted((versions.get(pkg) or {}).items()):
            rolled: list[tuple[dict, str]] = []
            for adv in advisories:
                if adv["package"] != pkg or not in_range(version, adv["vulnerable"]):
                    continue
                met, reason = precondition_met(adv, inv, versions)
                matched.append({"ghsa": adv["ghsa"], "package": pkg, "version": version, "precondition": reason,
                                "precondition_met": met})
                if met is not True:
                    rolled.append((adv, reason))
                    continue
                refs = [adv["ghsa"]] + ([adv["cve"]] if adv.get("cve") else []) + [
                    "CWE-1395", "OWASP A03:2025", "skills/sveltekit-security-stinger/guides/00-scoping-and-version-check.md"]
                findings.append({
                    "id": f"SEC-SVELTE-{n:03d}", "dimension": "security", "source": SOURCE,
                    "title": f"{pkg} {version} has a known security flaw that this app's code can reach: {adv['summary'].rstrip('.')}",
                    "severity": adv["severity"], "confidence": "likely",
                    "locations": locs_for(pkg, version, where),
                    "evidence": (f"Lockfile resolves {pkg}@{version} ({', '.join(sorted(where))}). {adv['ghsa']} affects "
                                 f"'{adv['vulnerable']}', first patched {adv['patched']}. Source signal: {reason}."),
                    "why_it_matters": f"{adv['condition']} Reviewed severity {adv['severity']}, maintainer severity {adv.get('maintainer_severity', adv['severity'])}.",
                    "remediation": (f"Upgrade {pkg} to {adv['patched']} or later and regenerate the lockfile. If {pkg} is "
                                    "transitive, upgrade the package that pulls it in or add a package-manager override."),
                    "effort": "S", "refs": refs,
                    "verified_by": ("Version read from the lockfile and matched to the advisory range by sveltekit_audit_scan.py; "
                                    "the precondition signal was found in source. Read the call site before raising to confirmed."),
                    "tags": ["dependency", "advisory", pkg],
                })
                matched[-1]["id"] = findings[-1]["id"]
                n += 1
            if rolled:
                top = max(rolled, key=lambda r: SEV_ORDER.index(r[0]["severity"]))[0]["severity"]
                sev = top if SEV_ORDER.index(top) <= SEV_ORDER.index("medium") else "medium"
                fixed = max((r[0]["patched"] for r in rolled), key=lambda v: (parse_version(v) or (0, 0, 0, None))[:3])
                lines = [f"{a['ghsa']} ({a['severity']}) range '{a['vulnerable']}' patched {a['patched']}" for a, _ in rolled]
                shown = lines[:12] + ([f"... and {len(lines) - 12} more"] if len(lines) > 12 else [])
                refs = [a["ghsa"] for a, _ in rolled] + [a["cve"] for a, _ in rolled if a.get("cve")] + [
                    "CWE-1395", "OWASP A03:2025", "skills/sveltekit-security-stinger/guides/00-scoping-and-version-check.md"]
                findings.append({
                    "id": f"SEC-SVELTE-{n:03d}", "dimension": "security", "source": SOURCE,
                    "title": f"{pkg} {version} is behind on security patches ({len(rolled)} published advisor{"y" if len(rolled) == 1 else "ies"})",
                    "severity": sev, "confidence": "possible",
                    "locations": locs_for(pkg, version, where),
                    "evidence": f"Lockfile resolves {pkg}@{version}. Matching advisories:\n" + "\n".join(shown),
                    "why_it_matters": ("Each advisory needs a specific feature or input pattern to be exploitable, and the scan did not "
                                       "find that pattern in this codebase. The version is still outdated, and a future code change can "
                                       "make any of these reachable."),
                    "remediation": f"Upgrade {pkg} to {fixed} or later (that clears every advisory listed) and regenerate the lockfile.",
                    "effort": "S", "refs": refs,
                    "verified_by": ("Version matched to each advisory range by sveltekit_audit_scan.py; precondition signals were not found "
                                    "in source, so confidence stays possible and severity is capped at medium."),
                    "tags": ["dependency", "advisory", "rollup", pkg],
                })
                for m in matched:
                    if m["package"] == pkg and m["version"] == version and "id" not in m:
                        m["id"] = findings[-1]["id"]
                n += 1
    return findings, matched


def main() -> int:
    ap = argparse.ArgumentParser(description="Read-only SvelteKit security inventory and advisory match.")
    ap.add_argument("--repo", required=True, help="audited repository root (never modified)")
    ap.add_argument("--out-dir", required=True, help="where to write JSON output, normally <workspace>/02-security/raw")
    ap.add_argument("--paths", nargs="*", default=[], help="repo-relative stack paths from intake.json; default whole repo")
    ap.add_argument("--advisories", default=str(Path(__file__).with_name("advisories.json")))
    ap.add_argument("--id-start", type=int, default=1, help="first NNN for SEC-SVELTE-NNN ids")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    out = Path(a.out_dir).resolve()
    if not repo.is_dir():
        print(f"repo not found: {repo}", file=sys.stderr)
        return 2
    if out == repo or repo in out.parents:
        print("refusing to write inside the audited repository; pick a workspace folder", file=sys.stderr)
        return 2
    REPO_REAL["root"] = os.path.realpath(repo)
    roots = [(repo / p).resolve() for p in a.paths] or [repo]
    for r in roots:
        if not r.exists() or (r != repo and repo not in r.parents):
            print(f"path outside repo or missing: {r}", file=sys.stderr)
            return 2
    adv_doc = json.loads(Path(a.advisories).read_text(encoding="utf-8"))
    versions, lockfiles, declared = find_versions(repo, roots)
    inv = scan(repo, roots)
    findings, matched = version_findings(repo, versions, inv, adv_doc["advisories"], a.id_start)
    next_id = a.id_start + len(findings)
    clean = []
    for pkg in ("svelte", "@sveltejs/kit", "devalue"):
        for version in sorted(versions.get(pkg) or {}):
            if not any(m["package"] == pkg and m["version"] == version for m in matched):
                clean.append({"package": pkg, "version": version, "where": sorted(versions[pkg][version])})
    out.mkdir(parents=True, exist_ok=True)
    (out / "sveltekit-version-findings.jsonl").write_text("".join(json.dumps(f) + "\n" for f in findings), encoding="utf-8")
    report = {
        "tool": "sveltekit_audit_scan.py", "advisories_generated": adv_doc.get("generated"),
        "repo": repo.name, "scope_paths": [str(r.relative_to(repo)) or "." for r in roots],
        "lockfiles": lockfiles,
        "versions": {k: {v: sorted(w) for v, w in vs.items()} for k, vs in versions.items()},
        "declared_ranges": declared,
        "versions_unresolved": [p for p in ("svelte", "@sveltejs/kit") if p in declared and p not in versions],
        "clean_core_versions": clean, "advisory_matches": matched, "next_finding_id": next_id,
        "inventory": inv,
        "caps": ([f"{STATS['symlinks']} symlink(s) skipped (never followed)"] if STATS["symlinks"] else []),
        "symlinks_skipped": STATS["symlinks"],
    }
    (out / "sveltekit-inventory.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    summary = {
        "versions": {k: sorted(v) for k, v in versions.items()},
        "advisory_findings": len(findings),
        "routes": len(inv["routes"]), "hooks": len(inv["hooks"]), "remote_functions": len(inv["remote_functions"]),
        "html_sinks": len(inv["html_sinks"]), "dom_sinks": len(inv["dom_sinks"]), "files_scanned": inv["files_scanned"],
        "next_finding_id": next_id, "symlinks_skipped": STATS["symlinks"],
    }
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
