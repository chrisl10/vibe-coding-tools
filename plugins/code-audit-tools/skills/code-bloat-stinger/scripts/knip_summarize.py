#!/usr/bin/env python3
"""Summarize a knip JSON report into category counts by workspace.

Accepts the knip 6.x shape ({"issues": [{"file", "<type>": [{"name", ...}]}]})
and the 5.x shape (same, plus a root "files" array of unused file paths).

What it adds on top of knip:
  - counts per category, overall and per workspace (workspaces read from
    package.json "workspaces" and pnpm-workspace.yaml "packages")
  - a core-only filter (--exclude globs: vendor, tests, fixtures, examples)
  - non-blank line totals for unused files (--root), so flagged files can be
    turned into flagged lines
  - "used in own file" counts for unused exports and types: the name appears
    more than once in its own file, the same idea as knip's
    ignoreExportsUsedInFile option
  - a seeded, stratified spot-check sample (--sample N) to classify by hand

Python 3.9+ standard library only.

Example:
  python3 knip_summarize.py --report raw/knip.json --root .scratch/repo-copy \
      --exclude '**/vendor/**' --exclude '**/*.test.*' --sample 12 \
      --json-out raw/knip-summary.json --sample-out raw/spot-check.md
"""
from __future__ import annotations

import argparse
import fnmatch
import glob
import json
import os
import random
import re
import stat
import sys
from collections import defaultdict

CATEGORIES = [
    ("files", "Unused files"),
    ("exports", "Unused exports"),
    ("nsExports", "Unused exports in namespaces"),
    ("types", "Unused types"),
    ("nsTypes", "Unused types in namespaces"),
    ("duplicates", "Duplicate exports"),
    ("enumMembers", "Unused enum members"),
    ("namespaceMembers", "Unused namespace members"),
    ("classMembers", "Unused class members (knip 5 only)"),
    ("dependencies", "Unused dependencies"),
    ("devDependencies", "Unused devDependencies"),
    ("optionalPeerDependencies", "Unused optional peers"),
    ("unlisted", "Unlisted dependencies"),
    ("binaries", "Unlisted binaries"),
    ("unresolved", "Unresolved imports"),
    ("catalog", "Unused catalog entries"),
    ("catalogReferences", "Unresolved catalog references"),
    ("cycles", "Circular dependencies"),
]


def matches_any(rel: str, patterns: list[str]) -> bool:
    rel = rel.replace(os.sep, "/")
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch("/" + rel, pat):
            return True
        core = pat.strip("*/")
        if pat.startswith("**/") and pat.endswith("/**") and "/" not in core and "*" not in core:
            if core in rel.split("/")[:-1]:
                return True
    return False


# ---- symlink-safe reads (audit M3): never follow symlinks, regular files only, 2 MB cap, must stay inside root
MAX_FILE_BYTES = 2_000_000
SYMLINKS_SKIPPED = [0]
OVERSIZE_SKIPPED = [0]
ROOT_REAL = [""]


def set_root(root: str) -> None:
    ROOT_REAL[0] = os.path.realpath(root) if root else ""


def _inside_root(path: str) -> bool:
    root = ROOT_REAL[0]
    if not root:
        return True
    real = os.path.realpath(path)
    return real == root or real.startswith(root + os.sep)


def is_safe_file(path: str) -> bool:
    """True for a regular, non-symlink file inside the root. Counts skipped symlinks."""
    try:
        if os.path.islink(path):
            SYMLINKS_SKIPPED[0] += 1
            return False
        if not stat.S_ISREG(os.lstat(path).st_mode):
            return False
    except OSError:
        return False
    if not _inside_root(path):
        SYMLINKS_SKIPPED[0] += 1
        return False
    return True


def read_regular(path: str, limit: int = MAX_FILE_BYTES):
    """Bytes of a safe file under the size cap, else None."""
    if not is_safe_file(path):
        return None
    try:
        if os.lstat(path).st_size > limit:
            OVERSIZE_SKIPPED[0] += 1
            return None
        with open(path, "rb") as fh:
            data = fh.read(limit + 1)
    except OSError:
        return None
    if len(data) > limit:
        OVERSIZE_SKIPPED[0] += 1
        return None
    return data


def filter_dirs(dirpath: str, dirnames: list) -> list:
    """Drop symlinked directories (counted) from an os.walk dirnames list."""
    kept = []
    for d in dirnames:
        if os.path.islink(os.path.join(dirpath, d)):
            SYMLINKS_SKIPPED[0] += 1
        else:
            kept.append(d)
    return kept


def output_inside_root(out: str, root: str) -> bool:
    """True when the output path lies inside the audited root (refuse to write there)."""
    if not out or not root:
        return False
    o, r = os.path.realpath(os.path.abspath(out)), os.path.realpath(root)
    return o == r or o.startswith(r + os.sep)


def coverage_caps() -> list:
    caps = []
    if SYMLINKS_SKIPPED[0]:
        caps.append(f"{SYMLINKS_SKIPPED[0]} symlink(s) skipped (never followed)")
    if OVERSIZE_SKIPPED[0]:
        caps.append(f"{OVERSIZE_SKIPPED[0]} file(s) over {MAX_FILE_BYTES:,} bytes skipped")
    return caps


def read_pnpm_packages(path: str) -> list[str]:
    """Minimal reader for the `packages:` list in pnpm-workspace.yaml."""
    pats, inside = [], False
    try:
        data = read_regular(path)
        if data is None:
            return pats
        for raw in data.decode("utf-8", "replace").splitlines():
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            if re.match(r"^packages\s*:", line):
                inside = True
                continue
            if inside:
                m = re.match(r"^\s+-\s*['\"]?([^'\"]+)['\"]?\s*$", line)
                if m:
                    pats.append(m.group(1).strip())
                elif not line.startswith((" ", "\t")):
                    inside = False
    except OSError:
        pass
    return pats


def workspace_dirs(root: str) -> list[str]:
    pats: list[str] = []
    try:
        pj = read_regular(os.path.join(root, "package.json"))
        pkg = json.loads(pj.decode("utf-8", "replace")) if pj is not None else {}
        ws = pkg.get("workspaces")
        if isinstance(ws, dict):
            ws = ws.get("packages")
        if isinstance(ws, list):
            pats.extend(ws)
    except (OSError, ValueError):
        pass
    pats.extend(read_pnpm_packages(os.path.join(root, "pnpm-workspace.yaml")))
    dirs = set()
    for pat in pats:
        if pat.startswith("!"):
            continue
        for d in glob.glob(os.path.join(root, pat)):
            if os.path.islink(d):
                SYMLINKS_SKIPPED[0] += 1
                continue
            if os.path.isfile(os.path.join(d, "package.json")) and is_safe_file(os.path.join(d, "package.json")):
                dirs.add(os.path.relpath(d, root).replace(os.sep, "/"))
    return sorted(dirs, key=len, reverse=True)


def workspace_of(path: str, dirs: list[str]) -> str:
    for d in dirs:
        if path == d + "/package.json" or path.startswith(d + "/"):
            return d
    return "."


def nonblank_lines(path: str) -> int:
    data = read_regular(path)
    if data is None:
        return 0
    return sum(1 for ln in data.decode("utf-8", "replace").splitlines() if ln.strip())


def used_in_own_file(root: str, rel: str, name: str, cache: dict) -> bool | None:
    if not root or not name:
        return None
    if rel not in cache:
        data = read_regular(os.path.join(root, rel))
        cache[rel] = data.decode("utf-8", "replace") if data is not None else None
    text = cache[rel]
    if text is None:
        return None
    return len(re.findall(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])", text)) > 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", required=True, help="knip --reporter json output")
    ap.add_argument("--root", help="the analyzed tree (throwaway copy); enables workspaces, line counts, in-file checks")
    ap.add_argument("--exclude", action="append", default=[], help="glob for non-core paths to drop (repeatable)")
    ap.add_argument("--strip-prefix", action="append", default=[], help="prefix to strip from knip paths (repeatable)")
    ap.add_argument("--sample", type=int, default=12, help="spot-check sample size (minimum 12 is the protocol)")
    ap.add_argument("--seed", type=int, default=20260930)
    ap.add_argument("--json-out")
    ap.add_argument("--sample-out", help="write the spot-check worksheet (Markdown) here")
    args = ap.parse_args()
    if args.root:
        set_root(args.root)
        for o in (args.json_out, args.sample_out):
            if output_inside_root(o, args.root):
                print(f"refusing to write output inside the audited root: {o}", file=sys.stderr)
                return 2

    with open(args.report, encoding="utf-8") as fh:
        text = fh.read().strip()
    # knip prints one JSON line; tolerate stray log lines before it.
    start = text.find("{")
    report = json.loads(text[start:]) if start >= 0 else {"issues": []}

    issues = list(report.get("issues") or [])
    for f in report.get("files") or []:  # knip 5.x root list
        issues.append({"file": f, "files": [{"name": f}]})

    dirs = workspace_dirs(args.root) if args.root else []
    counts = defaultdict(int)
    by_ws: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    dep_names: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    unused_files = []
    in_file = {"exports": [0, 0], "types": [0, 0]}
    cache: dict = {}
    pool = []
    dropped = 0
    seen_files = set()

    for it in issues:
        rel = (it.get("file") or "").replace("\\", "/")
        for s in args.strip_prefix:
            s = s.rstrip("/") + "/"
            if rel.startswith(s):
                rel = rel[len(s):]
        if matches_any(rel, args.exclude):
            dropped += sum(len(v) for v in it.values() if isinstance(v, list))
            continue
        ws = workspace_of(rel, dirs)
        for key, _label in CATEGORIES:
            items = it.get(key)
            if not isinstance(items, list) or not items:
                continue
            if key == "files":
                if rel in seen_files:
                    continue
                seen_files.add(rel)
                items = items[:1]
            counts[key] += len(items)
            by_ws[ws][key] += len(items)
            for x in items:
                name = x.get("name") if isinstance(x, dict) else str(x)
                if key in ("dependencies", "devDependencies", "optionalPeerDependencies", "unlisted", "unresolved", "binaries"):
                    dep_names[ws][key].append(name)
                if key == "files":
                    lines = nonblank_lines(os.path.join(args.root, rel)) if args.root else None
                    unused_files.append({"path": rel, "workspace": ws, "nonblank_lines": lines})
                if key in in_file:
                    u = used_in_own_file(args.root, rel, name, cache)
                    if u is not None:
                        in_file[key][0] += 1
                        in_file[key][1] += 1 if u else 0
                loc = f"{rel}:{x.get('line')}" if isinstance(x, dict) and x.get("line") else rel
                pool.append({"category": key, "workspace": ws, "name": name, "location": loc})

    rng = random.Random(args.seed)
    by_cat = defaultdict(list)
    for p in pool:
        by_cat[p["category"]].append(p)
    sample = []
    priority = ["files", "dependencies", "exports", "devDependencies", "types", "unlisted", "unresolved", "duplicates"]
    cats = [c for c in priority if by_cat.get(c)] + [c for c in by_cat if c not in priority]
    for c in cats:
        rng.shuffle(by_cat[c])
    while len(sample) < args.sample and any(by_cat[c] for c in cats):
        for c in cats:
            if by_cat[c] and len(sample) < args.sample:
                sample.append(by_cat[c].pop())

    unused_files.sort(key=lambda r: -(r["nonblank_lines"] or 0))
    flagged_lines = sum(r["nonblank_lines"] or 0 for r in unused_files)
    result = {
        "totals": {k: counts.get(k, 0) for k, _ in CATEGORIES if counts.get(k)},
        "dropped_as_non_core": dropped,
        "unused_file_nonblank_lines": flagged_lines if args.root else None,
        "exports_used_in_own_file": {"checked": in_file["exports"][0], "used_in_file": in_file["exports"][1]},
        "types_used_in_own_file": {"checked": in_file["types"][0], "used_in_file": in_file["types"][1]},
        "by_workspace": {ws: dict(v) for ws, v in sorted(by_ws.items())},
        "dependency_names": {ws: dict(v) for ws, v in dep_names.items()},
        "unused_files": unused_files,
        "spot_check_sample": sample,
        "caps": coverage_caps(), "symlinks_skipped": SYMLINKS_SKIPPED[0],
    }
    if args.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)

    print("| Category | Core | Note |\n| --- | --- | --- |")
    for key, label in CATEGORIES:
        n = counts.get(key)
        if not n:
            continue
        note = ""
        if key == "files" and args.root:
            note = f"{flagged_lines:,} non-blank lines"
        if key in in_file and in_file[key][0]:
            note = f"{in_file[key][1]:,} used inside their own file"
        print(f"| {label} | {n:,} | {note} |")
    for cap in coverage_caps():
        print(f"CAP: {cap}", file=sys.stderr)
    print(f"\nDropped as non-core: {dropped:,} issues")
    cols = ["files", "exports", "types", "dependencies", "devDependencies"]
    print("\n| Workspace | Files | Exports | Types | Deps | Dev deps |\n| --- | --- | --- | --- | --- | --- |")
    for ws, v in sorted(by_ws.items(), key=lambda kv: -sum(kv[1].values())):
        print(f"| {ws} | " + " | ".join(str(v.get(c, 0)) for c in cols) + " |")

    if args.sample_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.sample_out)), exist_ok=True)
        with open(args.sample_out, "w", encoding="utf-8") as fh:
            fh.write("# Spot-check worksheet\n\nClassify each row as Dead, False alarm, or Partial, and give the reason "
                     "(see guides/05-spot-check-and-false-positives.md).\n\n")
            fh.write("| # | Category | Workspace | Finding | Verdict | Why |\n| --- | --- | --- | --- | --- | --- |\n")
            for i, s in enumerate(sample, 1):
                fh.write(f"| {i} | {s['category']} | {s['workspace']} | `{s['name']}` at {s['location']} |  |  |\n")
        print(f"\nSpot-check worksheet: {args.sample_out} ({len(sample)} rows)")
    if len(sample) < 12:
        print(f"\nNOTE: only {len(sample)} findings available to sample; the protocol asks for at least 12.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
