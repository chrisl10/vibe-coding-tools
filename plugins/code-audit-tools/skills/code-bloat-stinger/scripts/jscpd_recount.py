#!/usr/bin/env python3
"""Recount duplication from a jscpd JSON report, per area and per file.

Why this exists: jscpd's own `percentage` counts each clone's lines once
(one copy). It does not give a "both copies counted" figure, per-area
figures, a big-files-versus-small-files comparison, or a check that every
file you meant to scan was scanned. jscpd's per-clone `lines` also
describes the first copy only: the second copy can span a different number
of lines, so figures built from `lines` are wrong per file. This script
takes each side's own range (its real length), repairs only invalid ranges
(missing, reversed, or past the end of the file), takes the union of
covered lines per file over both sides of every clone, and recomputes.
The both-copies denominator is every in-scope file, including files too
small to hold a clone, which jscpd 5.x leaves out of its own line count.

Works with jscpd 4.x and 5.x JSON reports. Python 3.9+ standard library only.

Example:
  python3 jscpd_recount.py --report raw/jscpd-50/jscpd-report.json \
      --coverage-report raw/jscpd-coverage/jscpd-report.json \
      --root .scratch/repo-copy --ext ts,tsx,js,jsx \
      --exclude '**/node_modules/**' --exclude '**/dist/**' \
      --area-depth 2 --area 'packages/adapters/*' \
      --big-lines 1000 --top 20 --json-out raw/jscpd-50/recount.json
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import stat
import sys
from collections import defaultdict

DEFAULT_EXT = "ts,tsx,js,jsx,mjs,cjs,mts,cts"


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


def count_lines(path: str) -> int:
    """Physical lines the way jscpd counts them: newline count, plus one
    when the file does not end with a newline."""
    data = read_regular(path)
    if not data:
        return 0
    n = data.count(b"\n")
    if not data.endswith(b"\n"):
        n += 1
    return n


def matches_any(rel: str, patterns: list[str]) -> bool:
    rel = rel.replace(os.sep, "/")
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch("/" + rel, pat):
            return True
        # Treat '**/x/**' as "any path segment named x".
        core = pat.strip("*/")
        if pat.startswith("**/") and pat.endswith("/**") and "/" not in core and "*" not in core:
            if core in rel.split("/")[:-1]:
                return True
    return False


def walk_files(root: str, exts: set[str], excludes: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    set_root(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir.replace(os.sep, "/")
        dirnames[:] = [
            d for d in filter_dirs(dirpath, dirnames)
            if d != ".git" and not matches_any((rel_dir + "/" + d).lstrip("/") + "/", excludes)
            and not matches_any((rel_dir + "/" + d + "/x").lstrip("/"), excludes)
        ]
        for name in filenames:
            ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
            if ext not in exts:
                continue
            rel = (rel_dir + "/" + name).lstrip("/")
            if matches_any(rel, excludes):
                continue
            full = os.path.join(root, rel)
            if os.path.islink(full):
                SYMLINKS_SKIPPED[0] += 1
                continue
            out[rel] = count_lines(full)
    return out


def normalize(name: str, root: str, known: dict[str, int], strip: list[str]) -> str:
    """Map a jscpd file name to a repo-relative path."""
    p = name.replace("\\", "/")
    for s in strip:
        s = s.replace("\\", "/").rstrip("/") + "/"
        if p.startswith(s):
            p = p[len(s):]
    if os.path.isabs(p):
        try:
            p = os.path.relpath(p, root).replace(os.sep, "/")
        except ValueError:
            pass
    while p.startswith("./"):
        p = p[2:]
    if p in known:
        return p
    # Strip leading ../ segments and retry by suffix match.
    q = p
    while q.startswith("../"):
        q = q[3:]
    if q in known:
        return q
    candidates = [k for k in known if k.endswith("/" + q) or k == q]
    if len(candidates) == 1:
        return candidates[0]
    # jscpd 4.x names are relative to its working directory, so the name
    # may carry extra leading folders: pick the longest known suffix.
    longer = [k for k in known if q.endswith("/" + k)]
    if longer:
        return max(longer, key=len)
    return q


def side_range(side: dict, clone: dict, file_lines: int) -> tuple[int, int, bool, bool]:
    """Return (start, end, repaired, asymmetric) for one side of a clone.

    Each side keeps its own start and end. jscpd's `lines` field describes
    the first copy only; the second copy can span fewer or more lines (the
    same tokens laid out on fewer, longer lines), so a mismatch with `lines`
    is reported as asymmetric, not repaired. Only invalid ranges are
    repaired: a missing or reversed range, or one that runs past the end of
    the file. Repairs use the clone's `lines` (or its fragment's line count).
    """
    start = (side.get("startLoc") or {}).get("line") or side.get("start")
    end = (side.get("endLoc") or {}).get("line") or side.get("end")
    length = clone.get("lines")
    if not length:
        frag = clone.get("fragment") or ""
        length = frag.count("\n") + 1 if frag else None
    repaired = False
    try:
        start = int(start)
    except (TypeError, ValueError):
        start = None
    try:
        end = int(end)
    except (TypeError, ValueError):
        end = None
    if start is None or start < 1:
        start = 1
        repaired = True
    if end is None or end < start:
        end = start + int(length) - 1 if length else start
        repaired = True
    if file_lines and end > file_lines:
        end = file_lines
        repaired = True
    if file_lines and start > file_lines:
        start = end = file_lines
        repaired = True
    asymmetric = bool(length) and not repaired and (end - start + 1) != int(length)
    return start, end, repaired, asymmetric


def union_len(intervals: list[tuple[int, int]]) -> int:
    if not intervals:
        return 0
    intervals.sort()
    total = 0
    cs, ce = intervals[0]
    for s, e in intervals[1:]:
        if s <= ce + 1:
            ce = max(ce, e)
        else:
            total += ce - cs + 1
            cs, ce = s, e
    total += ce - cs + 1
    return total


def area_of(path: str, areas: list[str], depth: int) -> str:
    best = None
    for pat in areas:
        pat_n = pat.rstrip("/")
        if "*" in pat_n:
            parts = path.split("/")
            pp = pat_n.split("/")
            if len(parts) > len(pp) and fnmatch.fnmatch("/".join(parts[: len(pp)]), pat_n):
                cand = "/".join(parts[: len(pp)])
                if best is None or len(cand) > len(best):
                    best = cand
        elif path == pat_n or path.startswith(pat_n + "/"):
            if best is None or len(pat_n) > len(best):
                best = pat_n
    if best:
        return best
    parts = path.split("/")
    if len(parts) <= depth:
        return "/".join(parts[:-1]) or "(root)"
    return "/".join(parts[:depth])


def pct(a: float, b: float) -> float:
    return round(100.0 * a / b, 2) if b else 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", required=True, help="jscpd-report.json")
    ap.add_argument("--root", required=True, help="the scanned tree (the throwaway repo copy)")
    ap.add_argument("--ext", default=DEFAULT_EXT, help="comma-separated extensions that were scanned")
    ap.add_argument("--exclude", action="append", default=[], help="glob to exclude (repeatable), same as the jscpd --ignore list")
    ap.add_argument("--strip-prefix", action="append", default=[], help="prefix to strip from jscpd file names (repeatable)")
    ap.add_argument("--area", action="append", default=[], help="area prefix or glob, for example 'packages/adapters/*' (repeatable)")
    ap.add_argument("--area-depth", type=int, default=2, help="path depth for areas not matched by --area")
    ap.add_argument("--big-lines", type=int, default=1000, help="threshold for the big-files comparison")
    ap.add_argument("--top", type=int, default=20, help="rows for top clone pairs and top files")
    ap.add_argument("--coverage-report", help="jscpd-report.json from a coverage run at --min-tokens 1 (same scope, caps lifted)")
    ap.add_argument("--json-out", help="write the full result as JSON here")
    args = ap.parse_args()

    with open(args.report, encoding="utf-8") as fh:
        report = json.load(fh)
    dups = report.get("duplicates") or []
    stats = (report.get("statistics") or {}).get("total") or {}

    exts = {e.strip().lower().lstrip(".") for e in args.ext.split(",") if e.strip()}
    if output_inside_root(args.json_out, args.root):
        print(f"refusing to write output inside the audited root: {args.json_out}", file=sys.stderr)
        return 2
    files = walk_files(args.root, exts, args.exclude)
    total_lines = sum(files.values())

    covered: dict[str, list[tuple[int, int]]] = defaultdict(list)
    repaired = 0
    asymmetric = 0
    unmatched: set[str] = set()
    pairs = []
    for c in dups:
        sides = []
        for key in ("firstFile", "secondFile"):
            side = c.get(key) or {}
            rel = normalize(side.get("name", ""), args.root, files, args.strip_prefix)
            if rel not in files:
                unmatched.add(rel)
                fl = count_lines(os.path.join(args.root, rel))
            else:
                fl = files[rel]
            s, e, rep, asym = side_range(side, c, fl)
            repaired += 1 if rep else 0
            asymmetric += 1 if asym else 0
            covered[rel].append((s, e))
            sides.append((rel, s, e))
        length = max(sides[0][2] - sides[0][1] + 1, sides[1][2] - sides[1][1] + 1)
        pairs.append({"lines": length, "tokens": c.get("tokens"), "kind": c.get("kind", "exact"),
                      "a": f"{sides[0][0]}:{sides[0][1]}-{sides[0][2]}",
                      "b": f"{sides[1][0]}:{sides[1][1]}-{sides[1][2]}"})

    per_file = {}
    for path, lines in files.items():
        dup = union_len(list(covered.get(path, [])))
        per_file[path] = {"lines": lines, "dup_lines_both": dup, "dup_pct_both": pct(dup, lines)}
    both_total = sum(v["dup_lines_both"] for v in per_file.values())

    per_area: dict[str, dict] = defaultdict(lambda: {"files": 0, "lines": 0, "dup_lines_both": 0})
    for path, v in per_file.items():
        a = area_of(path, args.area, args.area_depth)
        per_area[a]["files"] += 1
        per_area[a]["lines"] += v["lines"]
        per_area[a]["dup_lines_both"] += v["dup_lines_both"]
    areas_out = sorted(
        ({"area": k, **v, "dup_pct_both": pct(v["dup_lines_both"], v["lines"])} for k, v in per_area.items()),
        key=lambda r: (-r["dup_pct_both"], -r["lines"]))

    big = {p: v for p, v in per_file.items() if v["lines"] > args.big_lines}
    small = {p: v for p, v in per_file.items() if v["lines"] <= args.big_lines}
    big_lines = sum(v["lines"] for v in big.values())
    small_lines = sum(v["lines"] for v in small.values())

    scanned_sources = stats.get("sources")
    warnings = []
    coverage_sources = None
    if args.coverage_report:
        with open(args.coverage_report, encoding="utf-8") as fh:
            coverage_sources = ((json.load(fh).get("statistics") or {}).get("total") or {}).get("sources")
        if coverage_sources is not None and coverage_sources != len(files):
            warnings.append(
                f"Coverage run scanned {coverage_sources} files but the file walk found {len(files)}. A size or line cap "
                "skipped files (4.x: --max-lines 1000 and --max-size 100kb; 5.x: --max-size 1mb), or the format, "
                "--ignore and --exclude lists differ. Fix before reporting any figure.")
    elif scanned_sources is not None and scanned_sources < len(files):
        warnings.append(
            f"jscpd counted {scanned_sources} files; the file walk found {len(files)}. jscpd 5.x leaves files with fewer "
            "tokens than --min-tokens out of its counts, so a small gap is normal, but a cap may also have skipped files. "
            "Pass --coverage-report with a --min-tokens 1 run to tell the two apart.")
    if unmatched:
        warnings.append(f"{len(unmatched)} clone file names did not match the file walk; use --strip-prefix. Examples: {sorted(unmatched)[:5]}")

    result = {
        "jscpd_standard_pct": round(float(stats.get("percentage", 0.0)), 2),
        "jscpd_clones": stats.get("clones", len(dups)),
        "jscpd_sources": scanned_sources,
        "jscpd_lines": stats.get("lines"),
        "coverage_run_sources": coverage_sources,
        "walk_files": len(files),
        "walk_lines": total_lines,
        "both_copies_lines": both_total,
        "both_copies_pct": pct(both_total, total_lines),
        "repaired_clone_sides": repaired,
        "asymmetric_clone_sides": asymmetric,
        "big_files": {"threshold": args.big_lines, "files": len(big), "lines": big_lines,
                      "dup_pct_both": pct(sum(v["dup_lines_both"] for v in big.values()), big_lines)},
        "small_files": {"files": len(small), "lines": small_lines,
                        "dup_pct_both": pct(sum(v["dup_lines_both"] for v in small.values()), small_lines)},
        "areas": areas_out,
        "largest_files": sorted(({"path": p, **v} for p, v in per_file.items()), key=lambda r: -r["lines"])[: args.top],
        "top_clone_pairs": sorted(pairs, key=lambda r: -r["lines"])[: args.top],
        "warnings": warnings,
        "caps": coverage_caps(), "symlinks_skipped": SYMLINKS_SKIPPED[0],
    }
    if args.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)

    print(f"jscpd standard metric: {result['jscpd_standard_pct']}% ({result['jscpd_clones']} clones, {scanned_sources} files scanned by jscpd)")
    print(f"Both copies counted:   {result['both_copies_pct']}% ({both_total} of {total_lines} lines in {len(files)} in-scope files)")
    print(f"Clone sides: {repaired} repaired (invalid range), {asymmetric} asymmetric (second copy spans a different number of lines; kept as is)")
    print(f"Big files (>{args.big_lines} lines): {result['big_files']['dup_pct_both']}% dup over {big_lines} lines; "
          f"small files: {result['small_files']['dup_pct_both']}% over {small_lines} lines")
    print("\n| Area | Files | Lines | Dup (both copies) |\n| --- | --- | --- | --- |")
    for r in areas_out[: args.top]:
        print(f"| {r['area']} | {r['files']} | {r['lines']:,} | {r['dup_pct_both']}% |")
    print("\n| Lines | Copy A | Copy B |\n| --- | --- | --- |")
    for r in result["top_clone_pairs"]:
        print(f"| {r['lines']} | {r['a']} | {r['b']} |")
    for w in warnings + ["CAP: " + c for c in coverage_caps()]:
        print(f"\nWARNING: {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
