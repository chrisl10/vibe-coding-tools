#!/usr/bin/env python3
"""Deterministic Next.js security inventory and version-advisory scanner.

Part of nextjs-security-stinger (Legion Code Inc., AGPL-3.0-or-later).
Python 3.9+ standard library only. Read-only: never writes inside the
audited repository.

What it does:
  1. Finds every Next.js app in the repo (package.json files that depend on
     `next`), and resolves the installed version from the nearest lockfile
     (package-lock.json, npm-shrinkwrap.json, pnpm-lock.yaml, yarn.lock,
     bun.lock). Falls back to the package.json range.
  2. Compares each version to references/next-advisories.json and writes
     contract-shaped findings (audit-contract.md section 5) to
     <out>/next-version-findings.jsonl.
  3. Writes an inventory for manual review to <out>/next-inventory.json:
     'use server' files and their exported actions, Route Handlers, Pages
     API routes, middleware and proxy files with matchers, next.config
     security keys, 'use client' files, 'use cache' and unstable_cache use,
     NEXT_PUBLIC_ variable names, auth libraries, and hint flags.

Usage:
  python3 next_audit_scan.py --repo PATH --out DIR [--paths apps/web ...]
         [--id-start 1] [--advisories FILE]

Exit code 0 on success, 2 on bad arguments.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

SOURCE = "nextjs-security-wasp-drone"
SKIP_DIRS = {
    "node_modules", ".git", ".next", "dist", "build", "out", ".turbo",
    ".vercel", "coverage", ".cache", ".output", "vendor", ".scratch",
}
CODE_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts"}
MAX_FILE_BYTES = 2_000_000

HERE = Path(__file__).resolve().parent
DEFAULT_ADVISORIES = HERE.parent / "references" / "next-advisories.json"

# ---------------------------------------------------------------- versions

VER_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?")


def parse_ver(s):
    """Return a comparable tuple for a semver string, or None."""
    if not s:
        return None
    m = VER_RE.search(str(s))
    if not m:
        return None
    major, minor, patch, pre = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
    if pre is None:
        pre_key = (1,)
    else:
        parts = []
        for p in pre.split("."):
            parts.append((0, int(p), "") if p.isdigit() else (1, 0, p))
        pre_key = (0, tuple(parts))
    return (major, minor, patch, pre_key)


def ver_str(t):
    return "%d.%d.%d" % t[:3] if t else "?"


def in_range(v, rng):
    lo = parse_ver(rng.get("introduced") or "0.0.0")
    hi = parse_ver(rng.get("fixed")) if rng.get("fixed") else None
    if lo and v < lo:
        return False
    if hi and v >= hi:
        return False
    if not hi and rng.get("fix_status") == "unknown":
        # Unknown fix: treat as affected only within the same major line.
        return v[0] == lo[0] if lo else True
    return True


# ---------------------------------------------------------------- file walk


STATS = {"symlinks": 0}
REPO_REAL = {"root": ""}


def _inside(path, root_real: str) -> bool:
    real = os.path.realpath(path)
    return real == root_real or real.startswith(root_real + os.sep)


def walk(root: Path, scopes):
    """Yield regular, non-symlink files inside the repo; symlinks (files and dirs) are counted and skipped."""
    bases = [root / s for s in scopes] if scopes else [root]
    seen = set()
    for base in bases:
        if os.path.islink(base):
            STATS["symlinks"] += 1
            continue
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            kept = []
            for d in dirnames:
                if d in SKIP_DIRS or d.startswith(".git"):
                    continue
                if os.path.islink(os.path.join(dirpath, d)):
                    STATS["symlinks"] += 1
                    continue
                kept.append(d)
            dirnames[:] = kept
            for fn in filenames:
                p = Path(dirpath) / fn
                if p in seen:
                    continue
                if os.path.islink(p):
                    STATS["symlinks"] += 1
                    continue
                try:
                    if not stat.S_ISREG(os.lstat(p).st_mode):
                        continue
                except OSError:
                    continue
                if REPO_REAL["root"] and not _inside(p, REPO_REAL["root"]):
                    STATS["symlinks"] += 1
                    continue
                seen.add(p)
                yield p


def read_text(p: Path):
    try:
        if os.path.islink(p):
            STATS["symlinks"] += 1
            return None
        st = os.lstat(p)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_FILE_BYTES:
            return None
        if REPO_REAL["root"] and not _inside(p, REPO_REAL["root"]):
            STATS["symlinks"] += 1
            return None
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def rel(root: Path, p: Path) -> str:
    try:
        return p.relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


# ---------------------------------------------------------------- lockfiles


def version_from_package_lock(text, importer=""):
    try:
        data = json.loads(text)
    except ValueError:
        return None
    pk = data.get("packages") or {}
    for key in ([importer.rstrip("/") + "/node_modules/next"] if importer else []) + ["node_modules/next"]:
        if key in pk:
            return pk[key].get("version")
    deps = data.get("dependencies") or {}
    if "next" in deps and isinstance(deps["next"], dict):
        return deps["next"].get("version")
    return None


def versions_from_pnpm(text, importer=None):
    """Prefer the importer entry for this package dir (pnpm workspaces)."""
    if importer is not None and re.search(r"(?m)^importers:\s*$", text):
        block = re.search(r"(?ms)^importers:\s*\n(.*?)(?=^\S)", text + "\nEND\n")
        if block:
            key = importer or "."
            m = re.search(r"(?ms)^  ['\"]?" + re.escape(key) + r"['\"]?:\s*\n(.*?)(?=^  \S|\Z)", block.group(1))
            if not m:
                return []
            sub = m.group(1)
            vm = re.search(r"(?m)^\s+next:\s*\n\s+specifier:[^\n]*\n\s+version:\s*['\"]?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)", sub)
            vm = vm or re.search(r"(?m)^\s+next:\s*['\"]?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)", sub)
            return [vm.group(1)] if vm else []
    found = set(re.findall(r"(?m)^\s{2}/?next@(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)", text))
    found |= set(re.findall(r"(?m)^\s+next:\s*\n\s+specifier:[^\n]*\n\s+version:\s*['\"]?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)", text))
    found |= set(re.findall(r"(?m)^\s+next:\s*['\"]?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)", text))
    return sorted(found)


def versions_from_yarn(text):
    out = set()
    for m in re.finditer(r'(?m)^"?next@[^\n]*:\s*\n((?:[ \t]+[^\n]*\n)+)', text):
        vm = re.search(r'version:?\s*"?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)', m.group(1))
        if vm:
            out.add(vm.group(1))
    return sorted(out)


def versions_from_bun(text):
    return sorted(set(re.findall(r'"next":\s*\[\s*"next@(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)', text)))


def resolve_next_version(root: Path, pkg_dir: Path):
    """Walk up from pkg_dir to root looking for a lockfile that pins next."""
    d = pkg_dir
    while True:
        importer = pkg_dir.relative_to(d).as_posix() if pkg_dir != d else ""
        for name in ("package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock"):
            lf = d / name
            if not lf.exists():
                continue
            text = read_text(lf)
            if not text:
                continue
            if name in ("package-lock.json", "npm-shrinkwrap.json"):
                v = version_from_package_lock(text, importer)
                vs = [v] if v else []
            elif name == "pnpm-lock.yaml":
                vs = versions_from_pnpm(text, importer if importer else ".")
            elif name == "yarn.lock":
                vs = versions_from_yarn(text)
            else:
                vs = versions_from_bun(text)
            if vs:
                return vs, rel(root, lf)
        if d == root or d.parent == d or root not in d.parents:
            break
        d = d.parent
    return [], None


# ---------------------------------------------------------------- code scans

DIRECTIVE_TOP = re.compile(r"""\A(?:\s|//[^\n]*\n|/\*.*?\*/)*['"]use (server|client|cache(?::\s*\w+)?)['"]""", re.S)
INLINE_USE_SERVER = re.compile(r"""['"]use server['"]""")
INLINE_USE_CACHE = re.compile(r"""['"]use cache(?::\s*\w+)?['"]""")
EXPORT_FN = re.compile(
    r"export\s+(?:default\s+)?(?:async\s+)?function\s*\*?\s*(\w*)\s*\(|"
    r"export\s+const\s+(\w+)\s*(?::[^=]+)?=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*=>"
)
AUTH_TOKENS = re.compile(
    r"\b(auth\s*\(|getServerSession|currentUser\s*\(|getAuth\s*\(|auth\.protect|getUser\s*\(|getClaims\s*\(|"
    r"verifySession|requireUser|requireAuth|requireAdmin|getSession\s*\(|getCurrentUser|withAuth|validateRequest|"
    r"getIronSession|getKindeServerSession|stackServerApp|withSession|checkAuth|ensureAuth|assertAuth|session\s*=)"
)
VALIDATION_TOKENS = re.compile(r"\.(safeParse|parse|parseAsync|safeParseAsync)\s*\(|\bv\.parse\s*\(|\bparse\(\s*\w+Schema|\.validate\s*\(")
DB_TOKENS = re.compile(r"\b(prisma|db|drizzle|sql`|supabase|knex|mongoose|sequelize|kysely|pool\.query|\.from\(['\"])")
HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")
ROUTE_METHOD = re.compile(r"export\s+(?:async\s+)?(?:function\s+|const\s+)(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\b")
NEXT_PUBLIC = re.compile(r"\bNEXT_PUBLIC_[A-Z0-9_]+")
SENSITIVE_NAME = re.compile(r"(SECRET|SERVICE_ROLE|PRIVATE|PASSWORD|PASSWD|_TOKEN|SK_LIVE|WEBHOOK|DATABASE_URL|DB_URL|ADMIN)", re.I)
SAFE_PUBLIC_NAME = re.compile(r"(PUBLISHABLE|ANON_KEY|_URL$|SITE_URL|APP_URL|POSTHOG_KEY|GA_|GTM|SENTRY_DSN|MEASUREMENT_ID|_ID$)", re.I)
SECRET_LITERAL = re.compile(r"\b(sk_live_[0-9A-Za-z]{8,}|rk_live_[0-9A-Za-z]{8,}|ghp_[0-9A-Za-z]{20,}|AKIA[0-9A-Z]{16}|sk-ant-[0-9A-Za-z_-]{20,}|sk-proj-[0-9A-Za-z_-]{20,}|xox[bp]-[0-9A-Za-z-]{10,})")
PROCESS_ENV = re.compile(r"process\.env\.([A-Z0-9_]+)")


def extract_body(text: str, start: int, limit: int = 20000) -> str:
    """Crude brace matcher from the first '{' after start."""
    i = text.find("{", start)
    if i < 0:
        return ""
    depth = 0
    end = min(len(text), i + limit)
    j = i
    while j < end:
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i : j + 1]
        j += 1
    return text[i:end]


def redact(s: str) -> str:
    return s[:4] + "****" if len(s) > 4 else "****"


def scan_code(root: Path, files):
    inv = {
        "use_server_files": [],
        "inline_use_server": [],
        "use_client_files": [],
        "use_cache": [],
        "unstable_cache": [],
        "route_handlers": [],
        "pages_api_routes": [],
        "middleware_proxy": [],
        "server_only_imports": 0,
        "client_only_imports": 0,
        "taint_api_uses": [],
        "next_public_vars": {},
        "client_files_reading_private_env": [],
        "client_files_importing_db": [],
        "hardcoded_secret_candidates": [],
        "next_og_image_response": [],
        "draft_mode_uses": [],
        "before_interactive_scripts": [],
        "edge_runtime_files": [],
        "generate_static_params_files": [],
        "metadata_image_routes": [],
        "dynamic_route_dirs": 0,
        "root_catch_all": [],
        "custom_server_files": [],
        "dangerously_set_inner_html": [],
        "get_session_server_use": [],
        "unsafe_metadata_use": [],
        "service_role_refs": [],
    }
    for p in files:
        rp = rel(root, p)
        parts = Path(rp).parts
        if "[" in rp and p.suffix in CODE_EXT and p.stem in ("page", "route", "layout"):
            inv["dynamic_route_dirs"] += 1
        if p.suffix not in CODE_EXT:
            if p.name.startswith(".env"):
                text = read_text(p) or ""
                for m in re.finditer(r"(?m)^\s*(NEXT_PUBLIC_[A-Z0-9_]+)\s*=", text):
                    inv["next_public_vars"].setdefault(m.group(1), []).append(rp)
            continue
        text = read_text(p)
        if text is None:
            continue
        stem = p.stem
        top = DIRECTIVE_TOP.match(text)
        top_kind = top.group(1) if top else None

        # middleware / proxy
        mw_base = p.parent.parent if p.parent.name == "src" else p.parent
        if stem in ("middleware", "proxy") and (mw_base / "package.json").exists():
            mm = re.search(r"matcher\s*:\s*(\[[^\]]*\]|'[^']*'|\"[^\"]*\")", text, re.S)
            inv["middleware_proxy"].append({
                "path": rp,
                "kind": stem,
                "matcher": re.sub(r"\s+", " ", mm.group(1))[:400] if mm else None,
                "auth_call_seen": bool(AUTH_TOKENS.search(text)),
                "auth_libs": sorted(set(re.findall(r"(clerkMiddleware|withAuth|updateSession|NextAuth|auth as (?:middleware|proxy)|authMiddleware|authkitMiddleware)", text))),
                "sets_csp_nonce": bool(re.search(r"nonce", text)) and "Content-Security-Policy" in text,
                "reads_x_middleware_subrequest": "x-middleware-subrequest" in text.lower(),
            })

        # use server
        if top_kind == "server":
            actions = []
            for m in EXPORT_FN.finditer(text):
                name = m.group(1) or m.group(2) or "default"
                body = extract_body(text, m.end() - 1)
                actions.append({
                    "name": name,
                    "line": line_of(text, m.start()),
                    "auth_call_seen": bool(AUTH_TOKENS.search(body)),
                    "validation_seen": bool(VALIDATION_TOKENS.search(body)),
                    "touches_db": bool(DB_TOKENS.search(body)),
                    "returns_db_call": bool(re.search(r"return\s+(?:await\s+)?(?:prisma|db|drizzle|supabase)\b", body)),
                })
            inv["use_server_files"].append({
                "path": rp,
                "imports_server_only": "server-only" in text,
                "file_level_auth_helper_imported": bool(re.search(r"import[^;]*\b(auth|verifySession|getCurrentUser|currentUser|getServerSession)\b", text)),
                "actions": actions,
            })
        elif INLINE_USE_SERVER.search(text):
            lines = [line_of(text, m.start()) for m in INLINE_USE_SERVER.finditer(text)]
            inv["inline_use_server"].append({"path": rp, "lines": lines[:50], "auth_call_seen_in_file": bool(AUTH_TOKENS.search(text))})

        # use client
        if top_kind == "client":
            priv = sorted({v for v in PROCESS_ENV.findall(text) if not v.startswith("NEXT_PUBLIC_") and v != "NODE_ENV"})
            entry = {"path": rp}
            inv["use_client_files"].append(entry)
            if priv:
                inv["client_files_reading_private_env"].append({"path": rp, "vars": priv})
            dbm = re.search(r"from\s+['\"](@prisma/client|drizzle-orm[^'\"]*|pg|mysql2|mongoose|@neondatabase/serverless|@vercel/postgres|[^'\"]*/(?:db|prisma|drizzle)(?:/[^'\"]*)?)['\"]", text)
            if dbm:
                inv["client_files_importing_db"].append({"path": rp, "import": dbm.group(1), "line": line_of(text, dbm.start())})

        # use cache
        if top_kind and top_kind.startswith("cache"):
            inv["use_cache"].append({"path": rp, "scope": "file", "directive": top_kind})
        elif INLINE_USE_CACHE.search(text):
            inv["use_cache"].append({"path": rp, "scope": "inline", "lines": [line_of(text, m.start()) for m in INLINE_USE_CACHE.finditer(text)][:50],
                                     "reads_cookies_or_headers_in_file": bool(re.search(r"\b(cookies|headers)\s*\(", text))})
        if "unstable_cache" in text:
            inv["unstable_cache"].append({"path": rp, "lines": [line_of(text, m.start()) for m in re.finditer(r"unstable_cache\s*\(", text)][:50]})

        # route handlers and pages api
        if stem == "route" and ("app" in parts):
            methods = sorted(set(ROUTE_METHOD.findall(text)))
            inv["route_handlers"].append({
                "path": rp,
                "methods": methods,
                "auth_call_seen": bool(AUTH_TOKENS.search(text)),
                "validation_seen": bool(VALIDATION_TOKENS.search(text)),
                "touches_db": bool(DB_TOKENS.search(text)),
                "reads_cookies": bool(re.search(r"\bcookies\s*\(|request\.cookies|req\.cookies", text)),
                "origin_check_seen": bool(re.search(r"headers\.get\(\s*['\"](origin|sec-fetch-site)['\"]|\bverifyOrigin|\bcsrf", text, re.I)),
                "webhook_signature_seen": bool(re.search(r"(constructEvent|verifySignature|svix|webhook.*verify|x-hub-signature|stripe-signature)", text, re.I)),
                "cors_wildcard": bool(re.search(r"Access-Control-Allow-Origin['\"]?\s*[:,]\s*['\"]\*", text)),
                "generate_static_params": "generateStaticParams" in text,
            })
        if "pages" in parts and "api" in parts and stem != "_middleware":
            inv["pages_api_routes"].append({
                "path": rp,
                "auth_call_seen": bool(AUTH_TOKENS.search(text)),
                "touches_db": bool(DB_TOKENS.search(text)),
                "method_check_seen": bool(re.search(r"req\.method", text)),
            })

        # misc hints
        if re.search(r"""import\s+['"]server-only['"]""", text):
            inv["server_only_imports"] += 1
        if re.search(r"""import\s+['"]client-only['"]""", text):
            inv["client_only_imports"] += 1
        for m in re.finditer(r"experimental_taint(ObjectReference|UniqueValue)", text):
            inv["taint_api_uses"].append({"path": rp, "line": line_of(text, m.start())})
        for m in NEXT_PUBLIC.finditer(text):
            inv["next_public_vars"].setdefault(m.group(0), [])
            if rp not in inv["next_public_vars"][m.group(0)] and len(inv["next_public_vars"][m.group(0)]) < 20:
                inv["next_public_vars"][m.group(0)].append(rp)
        for m in SECRET_LITERAL.finditer(text):
            inv["hardcoded_secret_candidates"].append({"path": rp, "line": line_of(text, m.start()), "value_redacted": redact(m.group(0))})
        if re.search(r"""from\s+['"]next/og['"]""", text) and "ImageResponse" in text:
            inv["next_og_image_response"].append({"path": rp, "edge_runtime": bool(re.search(r"runtime\s*=\s*['\"]edge", text)),
                                                  "reads_request_input": bool(re.search(r"searchParams|params|request\.url|req\.url", text))})
        if re.search(r"\bdraftMode\s*\(", text):
            inv["draft_mode_uses"].append(rp)
        if re.search(r"""strategy\s*=\s*\{?\s*['"]beforeInteractive""", text):
            inv["before_interactive_scripts"].append(rp)
        if re.search(r"""export\s+const\s+runtime\s*=\s*['"]edge['"]""", text):
            inv["edge_runtime_files"].append(rp)
        if "generateStaticParams" in text:
            inv["generate_static_params_files"].append(rp)
        if stem in ("opengraph-image", "twitter-image"):
            inv["metadata_image_routes"].append(rp)
        if re.search(r"dangerouslySetInnerHTML", text):
            inv["dangerously_set_inner_html"].append({"path": rp, "lines": [line_of(text, m.start()) for m in re.finditer(r"dangerouslySetInnerHTML", text)][:20]})
        if re.search(r"auth\.getSession\s*\(", text) and top_kind != "client":
            inv["get_session_server_use"].append({"path": rp, "lines": [line_of(text, m.start()) for m in re.finditer(r"auth\.getSession\s*\(", text)][:20]})
        if "unsafeMetadata" in text:
            inv["unsafe_metadata_use"].append({"path": rp, "lines": [line_of(text, m.start()) for m in re.finditer(r"unsafeMetadata", text)][:20]})
        if re.search(r"SERVICE_ROLE", text):
            inv["service_role_refs"].append({"path": rp, "client_file": top_kind == "client", "next_public": "NEXT_PUBLIC_SUPABASE_SERVICE_ROLE" in text})
        if p.name in ("server.js", "server.ts", "server.mjs") and re.search(r"""require\(['"]next['"]\)|from\s+['"]next['"]""", text) and "createServer" in text:
            inv["custom_server_files"].append(rp)
        if stem in ("page", "index") and (p.parent.name.startswith("[...") or p.parent.name.startswith("[[...")) and p.parent.parent.name in ("app", "pages"):
            inv["root_catch_all"].append(rp)
        if p.parent.name == "pages" and (stem.startswith("[...") or stem.startswith("[[...")):
            inv["root_catch_all"].append(rp)

    # Annotate sensitive NEXT_PUBLIC names
    inv["suspicious_next_public_names"] = sorted(
        n for n in inv["next_public_vars"] if SENSITIVE_NAME.search(n) and not SAFE_PUBLIC_NAME.search(n)
    )
    return inv


# ---------------------------------------------------------------- next.config


def scan_next_config(root: Path, app_dir: Path):
    for name in ("next.config.ts", "next.config.mjs", "next.config.js", "next.config.cjs", "next.config.mts"):
        p = app_dir / name
        if p.exists():
            text = read_text(p) or ""
            out = {"path": rel(root, p)}
            def has(rx):
                return bool(re.search(rx, text, re.S))
            out["remote_patterns_present"] = has(r"remotePatterns")
            out["remote_hostnames"] = sorted(set(re.findall(r"hostname\s*:\s*['\"]([^'\"]+)['\"]", text)))[:50]
            out["remote_hostname_wildcards"] = [h for h in out["remote_hostnames"] if "*" in h]
            out["remote_url_objects"] = re.findall(r"new\s+URL\(\s*['\"]([^'\"]+)['\"]", text)[:50]
            out["images_domains_deprecated"] = has(r"\bdomains\s*:\s*\[")
            out["dangerously_allow_svg"] = has(r"dangerouslyAllowSVG\s*:\s*true")
            out["images_csp_set"] = has(r"images\s*:\s*\{[^}]*contentSecurityPolicy")
            out["content_disposition_inline"] = has(r"contentDispositionType\s*:\s*['\"]inline")
            out["dangerously_allow_local_ip"] = has(r"dangerouslyAllowLocalIP\s*:\s*true")
            out["images_unoptimized"] = has(r"unoptimized\s*:\s*true")
            out["production_browser_source_maps"] = has(r"productionBrowserSourceMaps\s*:\s*true")
            out["powered_by_header_disabled"] = has(r"poweredByHeader\s*:\s*false")
            out["headers_fn"] = has(r"\bheaders\s*\(\s*\)|async\s+headers\b|headers\s*:\s*async")
            out["csp_in_config"] = has(r"Content-Security-Policy")
            out["hsts_in_config"] = has(r"Strict-Transport-Security")
            out["rewrites_fn"] = has(r"\brewrites\s*\(|async\s+rewrites\b|rewrites\s*:\s*async")
            out["redirects_fn"] = has(r"\bredirects\s*\(|async\s+redirects\b|redirects\s*:\s*async")
            out["dynamic_host_destinations"] = re.findall(r"destination\s*:\s*['\"](https?://[^'\"/]*:[A-Za-z_][^'\"/]*[^'\"]*)['\"]", text)[:20]
            out["server_actions_allowed_origins"] = re.findall(r"allowedOrigins\s*:\s*(\[[^\]]*\])", text)[:5]
            out["server_actions_body_size_limit"] = re.findall(r"bodySizeLimit\s*:\s*['\"]?([^'\",}\s]+)", text)[:5]
            out["taint_enabled"] = has(r"taint\s*:\s*true")
            out["cache_components"] = has(r"cacheComponents\s*:\s*true") or has(r"useCache\s*:\s*true")
            out["output"] = (re.findall(r"output\s*:\s*['\"](\w+)['\"]", text) or [None])[0]
            locales = re.search(r"locales\s*:\s*\[([^\]]*)\]", text)
            out["i18n"] = has(r"\bi18n\s*:")
            out["i18n_locale_count"] = len(re.findall(r"['\"][^'\"]+['\"]", locales.group(1))) if locales else 0
            out["typescript_ignore_build_errors"] = has(r"ignoreBuildErrors\s*:\s*true")
            out["eslint_ignore_during_builds"] = has(r"ignoreDuringBuilds\s*:\s*true")
            out["allowed_dev_origins"] = has(r"allowedDevOrigins")
            return out
    return None


# ---------------------------------------------------------------- findings


def fmt_ranges(adv):
    bits = []
    for r in adv["ranges"]:
        hi = r.get("fixed")
        if r.get("fix_status") == "no-fix-in-line":
            bits.append(">= %s (no patch in this line)" % r["introduced"])
        elif hi:
            bits.append(">= %s < %s" % (r["introduced"], hi))
        else:
            bits.append(">= %s (patched version not stated)" % r["introduced"])
    return "; ".join(bits)


def eval_preconditions(adv, facts):
    """Return ('met'|'unmet'|'unknown', details)."""
    status = "met"
    details = []
    for pre in adv.get("preconditions", []):
        val = facts.get(pre)
        details.append("%s=%s" % (pre, "unknown" if val is None else str(val).lower()))
        if val is False:
            return "unmet", details
        if val is None:
            status = "unknown"
    return status, details


SEV_ORDER = ["info", "low", "medium", "high", "critical"]


def cap(sev, maxsev):
    return sev if SEV_ORDER.index(sev) <= SEV_ORDER.index(maxsev) else maxsev


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="path to the audited repository (read-only)")
    ap.add_argument("--out", required=True, help="output directory, normally <workspace>/02-security/raw")
    ap.add_argument("--paths", nargs="*", default=[], help="repo-relative scope paths from intake.json stacks[].paths")
    ap.add_argument("--advisories", default=str(DEFAULT_ADVISORIES))
    ap.add_argument("--id-start", type=int, default=1, help="first NNN for SEC-NEXT-NNN ids")
    args = ap.parse_args(argv)

    root = Path(args.repo).resolve()
    out = Path(args.out).resolve()
    if not root.is_dir():
        print("repo not found: %s" % root, file=sys.stderr)
        return 2
    if out == root or root in out.parents:
        print("refusing to write inside the audited repository: %s" % out, file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    adv_doc = json.loads(Path(args.advisories).read_text(encoding="utf-8"))
    advisories = adv_doc["advisories"]
    latest = adv_doc.get("known_latest", {})

    REPO_REAL["root"] = os.path.realpath(root)
    files = list(walk(root, args.paths))

    # Find Next.js apps
    apps = []
    for p in files:
        if p.name != "package.json":
            continue
        try:
            pkg = json.loads(read_text(p) or "{}")
        except ValueError:
            continue
        deps = {}
        for k in ("dependencies", "devDependencies", "peerDependencies"):
            deps.update(pkg.get(k) or {})
        if "next" not in deps:
            continue
        vs, lock = resolve_next_version(root, p.parent)
        auth_libs = sorted(k for k in deps if k in {
            "next-auth", "@auth/core", "@auth/nextjs", "@clerk/nextjs", "@supabase/ssr", "@supabase/auth-helpers-nextjs",
            "@supabase/supabase-js", "better-auth", "iron-session", "jose", "@workos-inc/authkit-nextjs", "lucia",
            "@kinde-oss/kinde-auth-nextjs", "@stackframe/stack", "@auth0/nextjs-auth0", "firebase", "firebase-admin"})
        apps.append({
            "package_json": rel(root, p),
            "dir": rel(root, p.parent) or ".",
            "declared_range": deps["next"],
            "resolved_versions": vs,
            "lockfile": lock,
            "react_declared": deps.get("react"),
            "auth_libraries": {k: deps[k] for k in auth_libs},
            "has_server_only_pkg": "server-only" in deps,
            "scripts": {k: v for k, v in (pkg.get("scripts") or {}).items() if k in ("build", "dev", "start")},
        })

    code_inv = scan_code(root, files)

    findings = []
    nnn = args.id_start
    per_app = []
    for app in apps:
        app_dir = root / app["dir"]
        cfg = scan_next_config(root, app_dir)
        rd = app_dir
        router = {
            "app_router": any((rd / d).is_dir() for d in ("app", "src/app")),
            "pages_router": any((rd / d).is_dir() for d in ("pages", "src/pages")),
        }
        prefix = "" if app["dir"] == "." else app["dir"].rstrip("/") + "/"
        def in_app(path):
            return path.startswith(prefix)
        mw = [m for m in code_inv["middleware_proxy"] if in_app(m["path"])]
        facts = {
            "app_router": router["app_router"],
            "pages_router": router["pages_router"],
            "middleware": bool(mw),
            "server_actions": any(in_app(f["path"]) for f in code_inv["use_server_files"] + code_inv["inline_use_server"]),
            "image_optimizer": (not cfg["images_unoptimized"]) if cfg else None,
            "image_remote_patterns": (cfg["remote_patterns_present"] or cfg["images_domains_deprecated"]) if cfg else False,
            "cache_components": (cfg and cfg["cache_components"]) or any(in_app(u["path"]) for u in code_inv["use_cache"]) or None,
            "draft_mode": any(in_app(x) for x in code_inv["draft_mode_uses"]),
            "next_og": any(in_app(x["path"]) and not x["edge_runtime"] for x in code_inv["next_og_image_response"]),
            "dev_only": True,
            "rewrites": cfg["rewrites_fn"] if cfg else False,
            "rewrites_dynamic_host": bool(cfg and cfg["dynamic_host_destinations"]) or (None if cfg and (cfg["rewrites_fn"] or cfg["redirects_fn"]) else False),
            "edge_runtime": any(in_app(x) for x in code_inv["edge_runtime_files"]) or None,
            "custom_server_or_unpinned_host": True if any(in_app(x) for x in code_inv["custom_server_files"]) else None,
            "i18n": cfg["i18n"] if cfg else False,
            "i18n_single_locale": (cfg["i18n"] and cfg["i18n_locale_count"] == 1) if cfg else False,
            "turbopack_build": None,
            "webpack_build": True if "--webpack" in json.dumps(app["scripts"]) else None,
            "metadata_image_routes": any(in_app(x) for x in code_inv["metadata_image_routes"]),
            "csp_nonce": any(m["sets_csp_nonce"] for m in mw),
            "before_interactive": any(in_app(x) for x in code_inv["before_interactive_scripts"]),
            "dynamic_routes": code_inv["dynamic_route_dirs"] > 0 or None,
            "root_catch_all": any(in_app(x) for x in code_inv["root_catch_all"]),
            "avif_input": None,
            "windows_host": None,
            "self_hosted": None,
        }
        if facts["cache_components"] is None and cfg is not None:
            facts["cache_components"] = False
        matched, not_applicable = [], []
        versions = app["resolved_versions"]
        version_source = app["lockfile"]
        confidence_base = "likely"
        if not versions:
            m = VER_RE.search(app["declared_range"] or "")
            versions = [m.group(0)] if m else []
            version_source = app["package_json"] + " (declared range, no lockfile pin found)"
            confidence_base = "possible"
        for vs in versions:
            v = parse_ver(vs)
            if not v:
                continue
            line = str(v[0])
            line_latest = latest.get(line)
            for adv in advisories:
                hit = next((r for r in adv["ranges"] if in_range(v, r)), None)
                if not hit:
                    continue
                pre_status, pre_details = eval_preconditions(adv, facts)
                rec = {"ghsa": adv["ghsa"], "cve": adv["cve"], "severity": adv["severity"], "version": vs,
                       "range": hit, "preconditions": pre_details, "precondition_status": pre_status}
                if pre_status == "unmet":
                    not_applicable.append(rec)
                    continue
                matched.append((adv, hit, pre_status, pre_details, vs))
            # Unsupported major
            if v[0] < 15:
                findings.append({
                    "id": "SEC-NEXT-%03d" % nnn, "dimension": "security", "source": SOURCE,
                    "title": "This app runs Next.js %d, which no longer gets security fixes" % v[0],
                    "severity": "high" if confidence_base == "likely" else "medium",
                    "confidence": confidence_base,
                    "locations": [{"path": app["package_json"], "line_start": 1, "line_end": 1}],
                    "evidence": "next %s resolved from %s. Next.js support policy (fetched 2026-09-30): 16.x Active LTS, 15.x Maintenance LTS, 14.x and older unsupported." % (vs, version_source),
                    "why_it_matters": "Security advisories published in 2026 list ranges such as '>=13.0.0 < 15.5.21' with no patch for 13.x or 14.x, so this app keeps those holes until it moves to a supported major version.",
                    "remediation": "Plan an upgrade of next in %s to the 16.x line (newest at research time: %s) or at minimum 15.5.x (newest at research time: %s), using the official codemods." % (app["package_json"], latest.get("16"), latest.get("15")),
                    "effort": "L",
                    "refs": ["OWASP A03:2025", "CWE-1104", "guides/01-version-and-advisory-check.md"],
                    "verified_by": "Version read from the lockfile and compared to the Next.js support policy table.",
                    "tags": ["nextjs", "version", "unsupported"],
                })
                nnn += 1

        # Emit one finding per critical advisory; roll up high, and medium/low, separately
        groups = {"high": [], "lower": []}
        for adv, hit, pre_status, pre_details, vs in matched:
            v = parse_ver(vs)
            sev = adv["severity"]
            conf = confidence_base
            if "dev_only" in adv.get("preconditions", []):
                sev = "low" if sev in ("critical", "high", "medium") else sev
            if pre_status == "unknown" or hit.get("fix_status") == "unknown":
                conf = "possible"
            if conf == "possible":
                sev = cap(sev, "medium")
            fixed = hit.get("fixed")
            if hit.get("fix_status") == "no-fix-in-line":
                fix_txt = "No patch exists for the %d.x line; upgrade to a supported line (16.x newest at research time: %s)." % (v[0], latest.get("16"))
            elif hit.get("fix_status") == "unknown":
                fix_txt = "The advisory did not state a patched version at research time; check %s and upgrade to the newest %d.x release (at research time: %s), then re-run this scan." % (adv["ghsa"], v[0], latest.get(str(v[0])))
            else:
                fix_txt = "Upgrade next to %s or later in this line (newest %d.x at research time: %s)." % (fixed, v[0], latest.get(str(v[0])))
            rec = (adv, hit, pre_status, pre_details, vs, sev, conf, fix_txt)
            dev = "dev_only" in adv.get("preconditions", [])
            if adv["severity"] == "critical" and not dev:
                refs = [x for x in [adv["cve"], adv["ghsa"]] if x] + adv.get("cwe", []) + ["CWE-1395", "OWASP " + adv.get("owasp", "A03:2025"), "guides/01-version-and-advisory-check.md"]
                findings.append({
                    "id": "SEC-NEXT-%03d" % nnn, "dimension": "security", "source": SOURCE,
                    "title": "The installed Next.js version (%s) is affected by: %s" % (vs, adv["title"]),
                    "severity": sev, "confidence": conf,
                    "locations": [{"path": app["package_json"], "line_start": 1, "line_end": 1}],
                    "evidence": "next %s resolved from %s. %s affected ranges: %s. Preconditions: %s." % (
                        vs, version_source, adv["ghsa"], fmt_ranges(adv), ", ".join(pre_details) or "none stated"),
                    "why_it_matters": "This is a published, framework-level security flaw (%s, rated critical by the Next.js team). Anyone who knows the advisory can target it without access to your code." % adv["ghsa"],
                    "remediation": fix_txt + " Package: %s." % app["package_json"],
                    "effort": "S" if hit.get("fix_status") == "fixed" else "M",
                    "refs": refs,
                    "verified_by": "Version from lockfile matched against the GHSA range in references/next-advisories.json; preconditions evaluated from repo inventory (%s)." % pre_status,
                    "tags": ["nextjs", "version", "advisory"] + (["needs-precondition-check"] if pre_status == "unknown" else []),
                })
                nnn += 1
            elif adv["severity"] == "high" and not dev:
                groups["high"].append(rec)
            else:
                groups["lower"].append(rec)
        for gname, rollup in groups.items():
            if not rollup:
                continue
            top = max((r[5] for r in rollup), key=SEV_ORDER.index)
            conf = "likely" if any(r[6] == "likely" for r in rollup) else "possible"
            if conf == "possible":
                top = cap(top, "medium")
            lines = ["%s %s (%s, preconditions %s): %s" % (r[0]["ghsa"], r[0]["cve"] or "", r[0]["severity"], r[2], r[0]["title"]) for r in rollup[:12]]
            if len(rollup) > 12:
                lines.append("... and %d more (see next-inventory.json)" % (len(rollup) - 12))
            fixes = sorted({r[1]["fixed"] for r in rollup if r[1].get("fixed") and r[1].get("fix_status") == "fixed"}, key=parse_ver)
            label = "high-severity" if gname == "high" else "medium or low"
            cwes = sorted({c for r in rollup for c in r[0].get("cwe", [])})[:6]
            findings.append({
                "id": "SEC-NEXT-%03d" % nnn, "dimension": "security", "source": SOURCE,
                "title": "The installed Next.js version (%s) is missing fixes for %d %s published advisories" % (rollup[0][4], len(rollup), label),
                "severity": top, "confidence": conf,
                "locations": [{"path": app["package_json"], "line_start": 1, "line_end": 1}],
                "evidence": "next %s resolved from %s. Matching advisories:\n%s" % (rollup[0][4], version_source, "\n".join(lines)),
                "why_it_matters": ("These are known framework flaws (middleware bypasses, denial of service, server-side request forgery, cache poisoning and similar). Each one applies only when its precondition holds, and all are closed by upgrading." if gname == "high"
                                   else "Each is a lower-risk known weakness (denial of service, cache confusion, dev-server leaks and similar). Together they show the framework is behind on security patches."),
                "remediation": "Upgrade next in %s to at least %s (the highest patched version among these), ideally the newest release in your line. Check each precondition listed in the evidence to decide urgency." % (app["package_json"], fixes[-1] if fixes else "the newest release in your line"),
                "effort": "S",
                "refs": [x for r in rollup[:10] for x in [r[0]["cve"] or r[0]["ghsa"]]] + cwes + ["CWE-1395", "OWASP A03:2025", "guides/01-version-and-advisory-check.md"],
                "verified_by": "Version from lockfile matched against GHSA ranges in references/next-advisories.json; per-advisory precondition status listed in evidence and in next-inventory.json.",
                "tags": ["nextjs", "version", "advisory-rollup"] + (["needs-precondition-check"] if any(r[2] == "unknown" for r in rollup) else []),
            })
            nnn += 1
        if not matched and versions and parse_ver(versions[0]) and parse_ver(versions[0])[0] >= 15:
            findings.append({
                "id": "SEC-NEXT-%03d" % nnn, "dimension": "security", "source": SOURCE,
                "title": "Next.js %s has no matching published advisory in the research table" % versions[0],
                "severity": "info", "confidence": confidence_base,
                "locations": [{"path": app["package_json"], "line_start": 1, "line_end": 1}],
                "evidence": "next %s resolved from %s; 0 of %d advisories matched." % (versions[0], version_source, len(advisories)),
                "why_it_matters": "No action needed for known framework advisories as of 2026-09-30. New advisories appear often, so re-check on each audit.",
                "remediation": "None. Keep next on the newest release in its line.",
                "effort": "S",
                "refs": ["guides/01-version-and-advisory-check.md"],
                "verified_by": "Version from lockfile compared to every advisory range in references/next-advisories.json.",
                "tags": ["nextjs", "version"],
            })
            nnn += 1
        per_app.append({
            **app,
            "router": router,
            "next_config": cfg,
            "facts_for_preconditions": facts,
            "advisories_matched": [{"ghsa": a["ghsa"], "cve": a["cve"], "severity": a["severity"], "version": vs,
                                     "precondition_status": ps, "preconditions": pd, "fixed": h.get("fixed"), "fix_status": h.get("fix_status")}
                                    for a, h, ps, pd, vs in matched],
            "advisories_not_applicable": not_applicable,
            "middleware_proxy": mw,
            "deployment_hints": {
                "vercel_json": (app_dir / "vercel.json").exists() or (root / "vercel.json").exists(),
                "dockerfile": (app_dir / "Dockerfile").exists() or (root / "Dockerfile").exists(),
                "netlify_toml": (app_dir / "netlify.toml").exists() or (root / "netlify.toml").exists(),
                "open_next": (app_dir / "open-next.config.ts").exists() or (app_dir / "wrangler.toml").exists() or (app_dir / "wrangler.jsonc").exists(),
                "custom_server_files": [x for x in code_inv["custom_server_files"] if in_app(x)],
                "output": cfg["output"] if cfg else None,
            },
        })

    inventory = {
        "schema": "next-inventory/1",
        "generated_by": "nextjs-security-stinger/scripts/next_audit_scan.py",
        "repo": str(root.name),
        "scope_paths": args.paths,
        "advisory_table": {"count": len(advisories), "known_latest": latest},
        "apps": per_app,
        "files_scanned": len(files),
        "symlinks_skipped": STATS["symlinks"],
        "caps": ([f"{STATS['symlinks']} symlink(s) skipped (never followed)"] if STATS["symlinks"] else []),
        **code_inv,
        "summary": {
            "apps": len(per_app),
            "use_server_files": len(code_inv["use_server_files"]),
            "server_actions_exported": sum(len(f["actions"]) for f in code_inv["use_server_files"]),
            "server_actions_without_auth_hint": sum(1 for f in code_inv["use_server_files"] for a in f["actions"] if not a["auth_call_seen"]),
            "inline_use_server_files": len(code_inv["inline_use_server"]),
            "route_handlers": len(code_inv["route_handlers"]),
            "route_handlers_mutating_without_auth_hint": sum(1 for r in code_inv["route_handlers"] if set(r["methods"]) & {"POST", "PUT", "PATCH", "DELETE"} and not r["auth_call_seen"] and not r["webhook_signature_seen"]),
            "pages_api_routes": len(code_inv["pages_api_routes"]),
            "middleware_proxy_files": len(code_inv["middleware_proxy"]),
            "use_client_files": len(code_inv["use_client_files"]),
            "findings_written": len(findings),
        },
        "notes": [
            "auth_call_seen, validation_seen and similar flags are regex hints only. They are not findings. Read every flagged file before writing a finding.",
            "React is vendored inside next for the App Router, so RSC advisories follow the next version, not the react version in package.json.",
        ],
    }

    fpath = out / "next-version-findings.jsonl"
    with fpath.open("w", encoding="utf-8") as fh:
        for f in findings:
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    ipath = out / "next-inventory.json"
    ipath.write_text(json.dumps(inventory, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"findings_file": str(fpath), "inventory_file": str(ipath), **inventory["summary"],
                      "next_versions": {a["dir"]: a["resolved_versions"] or a["declared_range"] for a in per_app},
                      "next_id": nnn}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
