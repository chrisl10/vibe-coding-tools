#!/usr/bin/env python3
"""Read-only, deterministic inspection of a React Flow or Svelte Flow project.

The script uses only the Python standard library, performs no network calls,
executes no project commands, and writes nothing. It never follows symbolic
links and reads only regular files, each capped at MAX_TEXT_BYTES, so a hostile
checkout cannot point it at devices, pipes, or files outside the target. JSON
is the only stdout format. Exit code 0 means no error findings and no manual-review boundary.
Exit code 1 means an error finding or a manual-review boundary was found.
Exit code 2 means a usage or environment error.

Every heuristic finding carries a `basis` naming the distilled research row it
depends on, so a maintainer can re-check it when xyflow changes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCHEMA_VERSION = 1
MAX_TEXT_BYTES = 2 * 1024 * 1024
MAX_SOURCE_FILES = 5000
MAX_DIRECTORIES = 20000
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", ".svelte-kit", ".next", ".nuxt",
    ".turbo", ".vercel", ".output", "coverage", "out", ".cache",
}
SOURCE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".svelte", ".css"}
VERSION_RE = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")

CURRENT = {"@xyflow/react", "@xyflow/svelte", "@xyflow/system"}
LEGACY = {"reactflow", "react-flow-renderer"}
LEGACY_PREFIX = "@reactflow/"
LAYOUT = {"@dagrejs/dagre", "dagre", "elkjs", "d3-hierarchy", "d3-force"}
FRAMEWORK = {"react", "react-dom", "svelte", "@sveltejs/kit", "next", "tailwindcss", "zustand"}

IMPORT_RE = re.compile(r"""(?:from|import)\s*['"](@xyflow/(?:react|svelte)|reactflow|react-flow-renderer)(/[^'"]*)?['"]""")
STYLE_RE = re.compile(r"""['"(]\s*(@xyflow/(?:react|svelte))/dist/(?:style|base)\.css\s*['")]""")
KITS = ("@xyflow/react", "@xyflow/svelte")
INLINE_NODE_TYPES_RE = re.compile(r"\b(?:nodeTypes|edgeTypes)\s*=\s*\{\s*\{")
# An optional TypeScript annotation (`let nodes: Node[] = ...`) sits between the name and `=`.
TYPE_ANNOTATION = r"(?:\s*:\s*[^=;\n]+?)?"
STATE_NOT_RAW_RE = re.compile(r"\b(?:nodes|edges)" + TYPE_ANNOTATION + r"\s*=\s*\$state\s*(?:<[^>]*>)?\s*\(")
WRITABLE_RE = re.compile(r"\b(?:nodes|edges)" + TYPE_ANNOTATION + r"\s*=\s*writable\s*(?:<[^>]*>)?\s*\(")
HIDE_ATTR_RE = re.compile(r"hideAttribution\s*:\s*true")
PARENT_NODE_RE = re.compile(r"\bparentNode\s*:")
HANDLE_CONN_RE = re.compile(r"\buseHandleConnections\b")
USE_CLIENT_RE = re.compile(r"""^\s*['"]use client['"]""", re.MULTILINE)
URL_CREDENTIALS_RE = re.compile(r"(://)[^/@\s]+@")


def emit(payload: Dict[str, Any], pretty: bool = False) -> None:
    print(json.dumps(payload, indent=2 if pretty else None, sort_keys=True))


def read_text(path: Path) -> str:
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode):
        raise ValueError("not a regular file; symbolic links, devices, and pipes are skipped")
    if st.st_size > MAX_TEXT_BYTES:
        raise ValueError(f"file exceeds {MAX_TEXT_BYTES} byte inspection limit")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            raise ValueError("not a regular file")
        data = handle.read(MAX_TEXT_BYTES + 1)
    if len(data) > MAX_TEXT_BYTES:
        raise ValueError(f"file exceeds {MAX_TEXT_BYTES} byte inspection limit")
    return data.decode("utf-8", errors="replace")


def redact_spec(spec: Any) -> str:
    """Drop URL credentials (git+https://user:token@host/...) before echoing a spec."""
    return URL_CREDENTIALS_RE.sub(r"\1***@", str(spec))[:200]


def majors(spec: Optional[str]) -> Optional[List[int]]:
    """Major version of each `||` alternative in an npm range; None when any alternative is unresolvable."""
    if not spec:
        return None
    found: List[int] = []
    for alternative in spec.split("||"):
        match = VERSION_RE.search(alternative)
        if not match:
            return None
        found.append(int(match.group(1)))
    return found or None


def finding(findings: List[Dict[str, str]], severity: str, code: str, message: str,
            path: str = "", basis: str = "") -> None:
    findings.append({"severity": severity, "code": code, "message": message, "path": path, "basis": basis})


def relevant_dependencies(package_data: Dict[str, Any]) -> Dict[str, str]:
    found: Dict[str, str] = {}
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        block = package_data.get(section) or {}
        if not isinstance(block, dict):
            continue
        for name, spec in block.items():
            if name in CURRENT | LEGACY | LAYOUT | FRAMEWORK or name.startswith(LEGACY_PREFIX):
                found.setdefault(name, redact_spec(spec))
    return found


def package_findings(rel: str, deps: Dict[str, str], findings: List[Dict[str, str]]) -> None:
    legacy = sorted(n for n in deps if n in LEGACY or n.startswith(LEGACY_PREFIX))
    if legacy:
        finding(findings, "warn", "legacy-package",
                f"legacy React Flow package(s) {', '.join(legacy)}; plan the migration to @xyflow/react",
                rel, "distilled D1, D9")
    if legacy and "@xyflow/react" in deps:
        finding(findings, "error", "mixed-generations",
                "legacy and @xyflow/react packages are installed together; two stores and two stylesheets can diverge",
                rel, "distilled D1, D9")
    if "@xyflow/system" in deps:
        finding(findings, "info", "direct-system-dependency",
                "@xyflow/system is normally consumed transitively; confirm the direct dependency is intentional and version-aligned",
                rel, "distilled D1")
    svelte_flow = majors(deps.get("@xyflow/svelte"))
    svelte = majors(deps.get("svelte"))
    if svelte_flow is not None and max(svelte_flow) >= 1 and "svelte" in deps:
        if svelte is None:
            finding(findings, "manual", "svelte-range-unresolved",
                    "@xyflow/svelte 1.x requires Svelte 5; the svelte range could not be resolved from the manifest, check the lockfile",
                    rel, "distilled D2, D3")
        elif max(svelte) < 5:
            finding(findings, "error", "svelte-peer",
                    "@xyflow/svelte 1.x requires Svelte 5; no alternative in this svelte range allows Svelte 5",
                    rel, "distilled D2, D3")
    if svelte_flow is not None and max(svelte_flow) == 0:
        finding(findings, "warn", "svelte-flow-0x",
                "@xyflow/svelte 0.x uses the store-based API; plan the Svelte Flow 1.0 migration before new work",
                rel, "distilled D9")
    if "dagre" in deps and "@dagrejs/dagre" not in deps:
        finding(findings, "info", "legacy-dagre",
                "the unscoped dagre package is frozen at 0.8.5; @dagrejs/dagre is the maintained distribution",
                rel, "distilled D10")


def source_findings(rel: str, text: str, is_next_app: bool, findings: List[Dict[str, str]]) -> Dict[str, Any]:
    imports = sorted({m.group(1) for m in IMPORT_RE.finditer(text)})
    info: Dict[str, Any] = {"imports": imports, "styles": sorted({m.group(1) for m in STYLE_RE.finditer(text)})}
    if not imports:
        return info
    if INLINE_NODE_TYPES_RE.search(text):
        finding(findings, "warn", "inline-types",
                "nodeTypes or edgeTypes is passed as an inline object literal; define it once outside the component",
                rel, "distilled D7")
    if "@xyflow/svelte" in imports or rel.endswith(".svelte"):
        if STATE_NOT_RAW_RE.search(text):
            finding(findings, "warn", "svelte-state-not-raw",
                    "nodes or edges use $state(...); Svelte Flow documents $state.raw(...) to avoid deep reactivity cost",
                    rel, "distilled D5")
        if WRITABLE_RE.search(text):
            finding(findings, "warn", "svelte-writable-store",
                    "nodes or edges are created with writable(); this is the pre-1.0 store API",
                    rel, "distilled D9")
    if PARENT_NODE_RE.search(text):
        finding(findings, "warn", "parent-node-field",
                "a parentNode field appears near xyflow code; the current field name is parentId",
                rel, "distilled D9, D10")
    if HANDLE_CONN_RE.search(text):
        finding(findings, "info", "handle-connections-hook",
                "useHandleConnections appears; it is deprecated; use useNodeConnections({ handleType, handleId })",
                rel, "distilled D6")
    if HIDE_ATTR_RE.search(text):
        finding(findings, "manual", "attribution-hidden",
                "hideAttribution is enabled; confirm the project meets the documented attribution terms",
                rel, "distilled D14")
    if is_next_app and "@xyflow/react" in imports and rel.endswith((".tsx", ".jsx", ".ts", ".js")) \
            and not USE_CLIENT_RE.search(text):
        finding(findings, "manual", "next-client-boundary",
                "a Next.js app/ file imports @xyflow/react without a 'use client' directive; confirm it renders inside a client boundary",
                rel, "distilled D12")
    return info


def walk(root: Path, state: Dict[str, Any]) -> Iterable[Path]:
    count = 0
    dirs = 0
    def on_error(exc: OSError) -> None:
        state.setdefault("walk_errors", []).append(getattr(exc, "filename", None) or str(exc))

    for dirpath, dirnames, filenames in os.walk(root, onerror=on_error, followlinks=False):
        dirs += 1
        if dirs > MAX_DIRECTORIES:
            state["truncated"] = f"directory limit {MAX_DIRECTORIES} reached"
            return
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".") or d == ".storybook")
        for name in sorted(filenames):
            path = Path(dirpath) / name
            if name == "package.json" or path.suffix in SOURCE_SUFFIXES:
                if path.is_symlink():
                    state["symlinks"] = state.get("symlinks", 0) + 1
                    continue
                count += 1
                if count > MAX_SOURCE_FILES:
                    state["truncated"] = f"candidate file limit {MAX_SOURCE_FILES} reached"
                    return
                yield path


def inspect_project(target: Path) -> Dict[str, Any]:
    findings: List[Dict[str, str]] = []
    packages: List[Dict[str, Any]] = []
    files: List[Dict[str, Any]] = []
    limitations = [
        "regex heuristics over source text, not a type-aware parse",
        "lockfiles are not resolved; manifest ranges are reported as written",
        f"scan stops after {MAX_SOURCE_FILES} candidate files or {MAX_DIRECTORIES} directories",
        "symbolic links are never followed",
    ]
    walk_state: Dict[str, Any] = {}
    styled_kits: set = set()
    imported_kits: set = set()
    any_import = False
    next_packages: set = set()
    package_dirs: set = set()
    # Manifests first, so each source file can be judged against the package that owns it.
    paths = sorted(walk(target, walk_state), key=lambda p: (p.name != "package.json", str(p)))
    for path in paths:
        rel = str(path.relative_to(target))
        try:
            text = read_text(path)
        except (OSError, ValueError) as exc:
            finding(findings, "manual", "unreadable", f"could not read file: {exc}", rel)
            continue
        if path.name == "package.json":
            package_dirs.add(path.parent)
            try:
                data = json.loads(text)
            except json.JSONDecodeError as exc:
                finding(findings, "error", "bad-package-json", f"invalid JSON: {exc.msg}", rel)
                continue
            except RecursionError:
                finding(findings, "error", "bad-package-json", "JSON nesting exceeds the parser limit", rel)
                continue
            deps = relevant_dependencies(data if isinstance(data, dict) else {})
            if deps:
                packages.append({"path": rel, "dependencies": deps})
                if "next" in deps:
                    next_packages.add(path.parent)
                package_findings(rel, deps, findings)
            continue
        owner = next((d for d in [path.parent, *path.parents] if d in package_dirs), None)
        in_app = owner is not None and "app" in path.relative_to(owner).parts
        is_next_app = in_app and owner in next_packages
        info = source_findings(rel, text, is_next_app, findings)
        styled_kits.update(info["styles"])
        imported_kits.update(k for k in info["imports"] if k in KITS)
        if info["imports"]:
            any_import = True
            files.append({"path": rel, **info})
    if walk_state.get("truncated"):
        finding(findings, "manual", "scan-truncated",
                f"scan incomplete: {walk_state['truncated']}; inspect the remaining tree by hand", "")
    if walk_state.get("symlinks"):
        finding(findings, "info", "symlinks-skipped",
                f"{walk_state['symlinks']} symbolic link(s) with candidate names were skipped, not followed", "")
    if walk_state.get("walk_errors"):
        errors = walk_state["walk_errors"]
        finding(findings, "manual", "unreadable-directory",
                f"{len(errors)} director(ies) could not be read, so the scan is incomplete: {', '.join(map(str, errors[:5]))}", "")
    for kit in sorted(imported_kits - styled_kits):
        finding(findings, "warn", "no-stylesheet",
                f"{kit} is imported but no {kit}/dist/style.css or base.css import was found",
                "", "distilled D3")
    if not packages and not any_import:
        finding(findings, "info", "not-an-xyflow-project", "no xyflow packages or imports were found", "")
    blocking = any(f["severity"] in {"error", "manual"} for f in findings)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "review" if blocking else "ok",
        "target": str(target),
        "packages": packages,
        "files": files,
        "findings": findings,
        "limitations": limitations,
    }


def self_test() -> Dict[str, Any]:
    checks: List[Tuple[str, bool]] = []
    f: List[Dict[str, str]] = []
    package_findings("package.json", {"reactflow": "^11.11.0", "@xyflow/react": "^12.0.0"}, f)
    codes = {x["code"] for x in f}
    checks.append(("legacy and mixed detected", {"legacy-package", "mixed-generations"} <= codes))
    f = []
    package_findings("package.json", {"@xyflow/svelte": "^1.0.0", "svelte": "^4.2.0"}, f)
    checks.append(("svelte peer mismatch", any(x["code"] == "svelte-peer" for x in f)))
    f = []
    info = source_findings("Flow.tsx", "import { ReactFlow } from '@xyflow/react';\n"
                           "import '@xyflow/react/dist/style.css';\n"
                           "<ReactFlow nodeTypes={{ a: A }} />", False, f)
    checks.append(("react import and style", info["imports"] == ["@xyflow/react"] and info["styles"] == ["@xyflow/react"]))
    checks.append(("inline nodeTypes", any(x["code"] == "inline-types" for x in f)))
    f = []
    source_findings("Flow.svelte", "import { SvelteFlow } from '@xyflow/svelte';\nlet nodes = $state([]);", False, f)
    checks.append(("svelte $state without raw", any(x["code"] == "svelte-state-not-raw" for x in f)))
    f = []
    source_findings("Flow.svelte", "import { SvelteFlow } from '@xyflow/svelte';\nlet nodes = $state.raw([]);", False, f)
    checks.append(("svelte $state.raw accepted", not f))
    f = []
    source_findings("Flow.svelte", "import { SvelteFlow } from '@xyflow/svelte';\nlet edges: Edge[] = $state([]);", False, f)
    checks.append(("typed svelte $state without raw", any(x["code"] == "svelte-state-not-raw" for x in f)))
    f = []
    source_findings("Flow.svelte", "import { SvelteFlow } from '@xyflow/svelte';\nlet nodes: Node[] = $state.raw([]);", False, f)
    checks.append(("typed svelte $state.raw accepted", not f))
    f = []
    source_findings("app/page.tsx", "import { ReactFlow } from '@xyflow/react';", True, f)
    checks.append(("next client boundary", any(x["code"] == "next-client-boundary" for x in f)))
    f = []
    source_findings("app/page.tsx", "'use client';\nimport { ReactFlow } from '@xyflow/react';", True, f)
    checks.append(("next client boundary satisfied", not f))
    f = []
    package_findings("package.json", {"@xyflow/svelte": "^1.0.0", "svelte": "^4.2.0 || ^5.0.0"}, f)
    checks.append(("range allowing svelte 5 accepted", not any(x["code"] == "svelte-peer" for x in f)))
    f = []
    package_findings("package.json", {"@xyflow/svelte": "^1.0.0", "svelte": "workspace:*"}, f)
    checks.append(("unresolvable range reported, not asserted",
                   {x["code"] for x in f} == {"svelte-range-unresolved"}))
    deps = relevant_dependencies({"dependencies": {"reactflow": "git+https://user:tok3n@github.com/x/y.git"}})
    checks.append(("url credentials redacted", "tok3n" not in deps["reactflow"] and "***@" in deps["reactflow"]))
    failed = [name for name, ok in checks if not ok]
    return {"schema_version": SCHEMA_VERSION, "status": "ok" if not failed else "error",
            "checks": len(checks), "failed": failed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a React Flow or Svelte Flow project without modifying it.")
    parser.add_argument("target", nargs="?", help="project root to inspect")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    parser.add_argument("--self-test", action="store_true", help="run deterministic in-memory checks")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
        emit(result, args.pretty)
        return 0 if result["status"] == "ok" else 1
    if not args.target:
        emit({"schema_version": SCHEMA_VERSION, "status": "error", "message": "target is required unless --self-test is used"}, args.pretty)
        return 2
    target = Path(args.target).resolve()
    if not target.is_dir():
        emit({"schema_version": SCHEMA_VERSION, "status": "error", "message": "target is not a directory"}, args.pretty)
        return 2
    result = inspect_project(target)
    emit(result, args.pretty)
    return 1 if result["status"] != "ok" else 0


if __name__ == "__main__":
    sys.exit(main())
