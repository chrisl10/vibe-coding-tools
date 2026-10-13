#!/usr/bin/env python3
"""Size profile: share of code in files over N lines, largest files, per area.

Inputs, in order of preference:
  --cloc FILE   output of `cloc --by-file --json ...`
  --scc FILE    output of `scc --by-file -f json ...`
  --root DIR    fallback line counter (no tool): physical and non-blank lines

The threshold is applied to a file's physical lines (code plus comments plus
blanks), because "a file over 1,000 lines" means what a reader sees in an
editor. The share is reported two ways: by code lines (cloc or scc `code`)
and by physical lines. The fallback counter has no comment detection, so its
"code" figure is non-blank lines; say so in the report.

Python 3.9+ standard library only.

Example:
  python3 size_profile.py --cloc raw/cloc-by-file.json --threshold 1000 \
      --exclude '**/vendor/**' --area-depth 2 --top 20 --json-out raw/size-profile.json
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import stat
import sys
from collections import defaultdict

DEFAULT_EXT = "ts,tsx,js,jsx,mjs,cjs,mts,cts,py,go,rs,rb,php,java,kt,swift,cs,svelte,vue,astro"
# cloc and scc count prose and data too. These are not code for a bloat audit.
DEFAULT_EXCLUDE_LANG = ("Markdown,JSON,JSON5,JSONL,Text,Plain Text,YAML,XML,CSV,TSV,SVG,TOML,INI,"
                        "reStructuredText,AsciiDoc,License,Org,diff,Properties File,Jupyter Notebook")


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


def from_cloc(path: str) -> dict[str, dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = {}
    for k, v in data.items():
        if k in ("header", "SUM") or not isinstance(v, dict) or "code" not in v:
            continue
        code, comment, blank = int(v.get("code", 0)), int(v.get("comment", 0)), int(v.get("blank", 0))
        out[k] = {"code": code, "lines": code + comment + blank, "language": v.get("language", "")}
    return out


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


def from_scc(path: str) -> dict[str, dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = {}
    for lang in data:
        for f in lang.get("Files") or []:
            out[f.get("Location")] = {"code": int(f.get("Code", 0)), "lines": int(f.get("Lines", 0)),
                                      "language": f.get("Language", lang.get("Name", ""))}
    return out


def from_root(root: str, exts: set[str], excludes: list[str]) -> dict[str, dict]:
    out = {}
    set_root(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir.replace(os.sep, "/")
        dirnames[:] = [d for d in filter_dirs(dirpath, dirnames) if d not in (".git", "node_modules")
                       and not matches_any((rel_dir + "/" + d + "/x").lstrip("/"), excludes)]
        for name in filenames:
            ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
            if ext not in exts:
                continue
            rel = (rel_dir + "/" + name).lstrip("/")
            if matches_any(rel, excludes):
                continue
            data = read_regular(os.path.join(root, rel))
            if data is None:
                continue
            text = data.decode("utf-8", "replace")
            lines = text.splitlines()
            out[rel] = {"code": sum(1 for ln in lines if ln.strip()), "lines": len(lines), "language": ext}
    return out


def strip_prefix(files: dict[str, dict], prefixes: list[str]) -> dict[str, dict]:
    out = {}
    for k, v in files.items():
        p = k.replace("\\", "/")
        for s in prefixes:
            s = s.replace("\\", "/").rstrip("/") + "/"
            if p.startswith(s):
                p = p[len(s):]
        while p.startswith("./"):
            p = p[2:]
        out[p] = v
    return out


def area_of(path: str, areas: list[str], depth: int) -> str:
    for pat in sorted(areas, key=len, reverse=True):
        pat_n = pat.rstrip("/")
        if "*" in pat_n:
            n = len(pat_n.split("/"))
            head = "/".join(path.split("/")[:n])
            if len(path.split("/")) > n and fnmatch.fnmatch(head, pat_n):
                return head
        elif path == pat_n or path.startswith(pat_n + "/"):
            return pat_n
    parts = path.split("/")
    return "/".join(parts[:depth]) if len(parts) > depth else ("/".join(parts[:-1]) or "(root)")


def pct(a: float, b: float) -> float:
    return round(100.0 * a / b, 2) if b else 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--cloc", help="cloc --by-file --json output")
    src.add_argument("--scc", help="scc --by-file -f json output")
    src.add_argument("--root", help="fallback: count lines under this directory")
    ap.add_argument("--ext", default=DEFAULT_EXT, help="extensions for --root mode")
    ap.add_argument("--exclude", action="append", default=[], help="glob to exclude (repeatable), applied in every mode")
    ap.add_argument("--strip-prefix", action="append", default=[], help="prefix to strip from tool paths (repeatable)")
    ap.add_argument("--include-lang", help="comma-separated languages to keep (cloc or scc names); overrides --exclude-lang")
    ap.add_argument("--exclude-lang", default=DEFAULT_EXCLUDE_LANG,
                    help="comma-separated languages to drop (default: prose and data formats); pass '' to keep all")
    ap.add_argument("--threshold", type=int, action="append", help="physical-line threshold (repeatable, default 1000)")
    ap.add_argument("--area", action="append", default=[], help="area prefix or glob (repeatable)")
    ap.add_argument("--area-depth", type=int, default=2)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--json-out")
    args = ap.parse_args()
    thresholds = args.threshold or [1000]
    if args.root and output_inside_root(args.json_out, args.root):
        print(f"refusing to write output inside the audited root: {args.json_out}", file=sys.stderr)
        return 2

    if args.cloc:
        files, source = from_cloc(args.cloc), "cloc"
    elif args.scc:
        files, source = from_scc(args.scc), "scc"
    else:
        exts = {e.strip().lower().lstrip(".") for e in args.ext.split(",") if e.strip()}
        files, source = from_root(args.root, exts, args.exclude), "fallback line counter (code = non-blank lines)"
    files = strip_prefix(files, args.strip_prefix)
    files = {k: v for k, v in files.items() if not matches_any(k, args.exclude)}
    if args.cloc or args.scc:
        if args.include_lang:
            keep = {x.strip().lower() for x in args.include_lang.split(",") if x.strip()}
            files = {k: v for k, v in files.items() if str(v.get("language", "")).lower() in keep}
        elif args.exclude_lang:
            drop = {x.strip().lower() for x in args.exclude_lang.split(",") if x.strip()}
            files = {k: v for k, v in files.items() if str(v.get("language", "")).lower() not in drop}
    langs: dict[str, int] = defaultdict(int)
    for v in files.values():
        langs[v.get("language") or "?"] += v["code"]

    total_code = sum(v["code"] for v in files.values())
    total_lines = sum(v["lines"] for v in files.values())
    bands = []
    for t in sorted(thresholds):
        over = {k: v for k, v in files.items() if v["lines"] > t}
        bands.append({
            "threshold": t,
            "files_over": len(over),
            "code_in_files_over": sum(v["code"] for v in over.values()),
            "share_by_code_pct": pct(sum(v["code"] for v in over.values()), total_code),
            "share_by_lines_pct": pct(sum(v["lines"] for v in over.values()), total_lines),
        })

    per_area: dict[str, dict] = defaultdict(lambda: {"files": 0, "code": 0, "lines": 0, "code_in_big": 0})
    t0 = sorted(thresholds)[0]
    for k, v in files.items():
        a = per_area[area_of(k, args.area, args.area_depth)]
        a["files"] += 1
        a["code"] += v["code"]
        a["lines"] += v["lines"]
        if v["lines"] > t0:
            a["code_in_big"] += v["code"]
    areas = sorted(({"area": k, **v, "big_share_pct": pct(v["code_in_big"], v["code"])} for k, v in per_area.items()),
                   key=lambda r: -r["code"])

    largest = sorted(({"path": k, **v} for k, v in files.items()), key=lambda r: -r["lines"])[: args.top]
    result = {"source": source, "files": len(files), "code_lines": total_code, "physical_lines": total_lines,
              "languages": dict(sorted(langs.items(), key=lambda kv: -kv[1])),
              "bands": bands, "areas": areas, "largest_files": largest,
              "caps": coverage_caps() + (["fallback line counter: comments counted as code (no cloc or scc output)"]
                                         if args.root else []),
              "symlinks_skipped": SYMLINKS_SKIPPED[0]}
    if args.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)

    for cap in coverage_caps():
        print(f"CAP: {cap}", file=sys.stderr)
    print(f"Source: {source}. {len(files):,} files, {total_code:,} code lines, {total_lines:,} physical lines.")
    print("Languages (code lines): " + ", ".join(f"{k} {v:,}" for k, v in list(result["languages"].items())[:8]))
    for b in bands:
        print(f"Files over {b['threshold']:,} lines: {b['files_over']:,}, holding {b['share_by_code_pct']}% of code "
              f"({b['share_by_lines_pct']}% of physical lines)")
    print("\n| File | Lines | Code |\n| --- | --- | --- |")
    for r in largest:
        print(f"| {r['path']} | {r['lines']:,} | {r['code']:,} |")
    print(f"\n| Area | Files | Code | Share in files over {t0:,} lines |\n| --- | --- | --- | --- |")
    for r in areas[: args.top]:
        print(f"| {r['area']} | {r['files']:,} | {r['code']:,} | {r['big_share_pct']}% |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
