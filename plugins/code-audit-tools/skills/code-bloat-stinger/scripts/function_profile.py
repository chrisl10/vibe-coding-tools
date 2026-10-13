#!/usr/bin/env python3
"""Largest functions and closure-heavy factory files.

Primary input: `lizard --csv` output (lizard 1.24, any of its ~27 languages).
lizard prints no header and 11 columns per function:
  NLOC, CCN, token, PARAM, length, location, file, function, long_name, start, end
Nested functions are separate rows, and an outer function's start-end span
includes them, so span = end - start + 1 measures closure size and rows
inside another row's range are its inner functions.

Fallback (--heuristic DIR): a brace-matching scan for JS/TS when lizard is not
available. It finds lines that open a function (function declarations,
methods, arrow functions with a block body) and matches braces while skipping
strings, template literals and comments. It is approximate: regex literals
and unusual syntax can shift spans. Label its numbers "heuristic".

Python 3.9+ standard library only.

Examples:
  lizard --csv -l typescript -l javascript .scratch/repo-copy > raw/lizard.csv
  python3 function_profile.py --lizard-csv raw/lizard.csv --strip-prefix .scratch/repo-copy \
      --top 20 --closure-min 1000 --json-out raw/functions.json
  python3 function_profile.py --heuristic .scratch/repo-copy --exclude '**/node_modules/**'
  python3 function_profile.py --lizard-csv raw/lizard.csv --strip-prefix .scratch/repo-copy \
      --cross-check .scratch/repo-copy    # flags spans lizard got wrong (seen near regex literals)
"""
from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import os
import re
import stat
import sys
from collections import defaultdict


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


def norm(path: str, prefixes: list[str]) -> str:
    p = path.replace("\\", "/")
    for s in prefixes:
        s = s.replace("\\", "/").rstrip("/") + "/"
        if p.startswith(s):
            p = p[len(s):]
    while p.startswith("./"):
        p = p[2:]
    return p


def read_lizard(path: str, prefixes: list[str], excludes: list[str]) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8", errors="replace", newline="") as fh:
        for rec in csv.reader(fh):
            if len(rec) < 11 or not rec[0].strip().isdigit():
                continue  # header or malformed
            try:
                start, end = int(rec[9]), int(rec[10])
            except ValueError:
                continue
            f = norm(rec[6], prefixes)
            if matches_any(f, excludes):
                continue
            rows.append({"file": f, "name": rec[7], "start": start, "end": end,
                         "span": end - start + 1, "nloc": int(rec[0]), "ccn": int(rec[1])})
    return rows


FUNC_START = re.compile(
    r"(\bfunction\b[\s*]*[\w$]*\s*\(|"            # function foo( / function* foo(
    r"=>\s*\{|"                                   # arrow with block body
    r"^\s*(?:(?:public|private|protected|static|async|get|set|override|readonly)\s+)*"
    r"[\w$]+\s*(?:<[^>]*>)?\s*\([^;]*\)\s*(?::[^={]+)?\{)"  # method shorthand
)
NAME_HINT = re.compile(r"(?:function\s*\*?\s*([\w$]+))|(?:(?:const|let|var)\s+([\w$]+)\s*=)|(?:^\s*(?:async\s+)?([\w$]+)\s*\()")
KEYWORDS = {"if", "for", "while", "switch", "catch", "with", "return", "else", "do", "try"}


def strip_code(text: str) -> str:
    """Replace string, template, and comment contents with spaces, keeping
    newlines and braces outside them, so brace counting is meaningful."""
    out = []
    i, n = 0, len(text)
    state = None
    tmpl_depth = []
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if state is None:
            if c == "/" and nxt == "/":
                state = "line"; out.append("  "); i += 2; continue
            if c == "/" and nxt == "*":
                state = "block"; out.append("  "); i += 2; continue
            if c in "'\"":
                state = c; out.append(" "); i += 1; continue
            if c == "`":
                state = "`"; out.append(" "); i += 1; continue
            if c == "}" and tmpl_depth and tmpl_depth[-1] == 0:
                tmpl_depth.pop(); state = "`"; out.append(" "); i += 1; continue
            if tmpl_depth:
                if c == "{":
                    tmpl_depth[-1] += 1
                elif c == "}":
                    tmpl_depth[-1] -= 1
            out.append(c); i += 1; continue
        if state == "line":
            if c == "\n":
                state = None; out.append("\n")
            else:
                out.append(" ")
            i += 1; continue
        if state == "block":
            if c == "*" and nxt == "/":
                state = None; out.append("  "); i += 2; continue
            out.append("\n" if c == "\n" else " "); i += 1; continue
        if state in ("'", '"'):
            if c == "\\":
                out.append("  "); i += 2; continue
            if c == state or c == "\n":
                state = None
            out.append("\n" if c == "\n" else " "); i += 1; continue
        if state == "`":
            if c == "\\":
                out.append("  "); i += 2; continue
            if c == "`":
                state = None; out.append(" "); i += 1; continue
            if c == "$" and nxt == "{":
                tmpl_depth.append(0); state = None; out.append("  "); i += 2; continue
            out.append("\n" if c == "\n" else " "); i += 1; continue
    return "".join(out)


def heuristic_scan(root: str, excludes: list[str], exts: set[str]) -> list[dict]:
    rows = []
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
            raw = data.decode("utf-8", "replace")
            code = strip_code(raw)
            raw_lines = raw.splitlines()
            lines = code.split("\n")
            # Offsets of each line start.
            offsets, pos = [], 0
            for ln in lines:
                offsets.append(pos)
                pos += len(ln) + 1
            for idx, ln in enumerate(lines):
                m = FUNC_START.search(ln)
                if not m:
                    continue
                head = ln[: m.end()]
                word = re.match(r"^\s*([\w$]+)", ln)
                if word and word.group(1) in KEYWORDS and "function" not in head and "=>" not in head:
                    continue
                search_from = offsets[idx] + m.start()
                paren_at = code.find("(", search_from)
                if paren_at >= 0 and "=>" not in m.group(0) and paren_at < offsets[idx] + m.end():
                    # Skip the parameter list: destructured params contain braces.
                    depth, j = 0, paren_at
                    while j < len(code):
                        if code[j] == "(":
                            depth += 1
                        elif code[j] == ")":
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1
                    search_from = j
                brace_at = code.find("{", search_from)
                if brace_at < 0:
                    continue
                depth, j = 0, brace_at
                while j < len(code):
                    ch = code[j]
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                end_line = code.count("\n", 0, j) + 1
                start_line = idx + 1
                hint = NAME_HINT.search(raw_lines[idx] if idx < len(raw_lines) else ln)
                fname = next((g for g in (hint.groups() if hint else ()) if g), "(anonymous)")
                rows.append({"file": rel, "name": fname, "start": start_line, "end": end_line,
                             "span": end_line - start_line + 1, "nloc": None, "ccn": None})
    return rows


def profile(rows: list[dict], top: int, closure_min: int) -> dict:
    by_file = defaultdict(list)
    for r in rows:
        by_file[r["file"]].append(r)
    factories = []
    for f, fr in by_file.items():
        fr.sort(key=lambda r: (r["start"], -r["end"]))
        for r in fr:
            if r["span"] < closure_min:
                continue
            inner = [x for x in fr if x is not r and x["start"] >= r["start"] and x["end"] <= r["end"]]
            if not inner:
                continue
            inner_sorted = sorted(inner, key=lambda x: -x["span"])
            factories.append({"file": f, "name": r["name"], "start": r["start"], "end": r["end"], "span": r["span"],
                              "inner_functions": len(inner),
                              "largest_inner": [{"name": x["name"], "span": x["span"], "start": x["start"]} for x in inner_sorted[:5]]})
    # Keep only outermost factories per file (drop factories nested in a bigger one).
    outer = []
    for fac in sorted(factories, key=lambda x: -x["span"]):
        if not any(o["file"] == fac["file"] and o["start"] <= fac["start"] and o["end"] >= fac["end"] for o in outer):
            outer.append(fac)
    largest = sorted(rows, key=lambda r: -r["span"])[:top]
    return {"functions": len(rows), "largest_functions": largest, "closure_factories": outer[:top],
            "functions_over_threshold": sum(1 for r in rows if r["span"] > closure_min)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--lizard-csv", help="lizard --csv output")
    src.add_argument("--heuristic", metavar="DIR", help="brace-matching fallback scan for JS/TS under DIR")
    ap.add_argument("--ext", default="ts,tsx,js,jsx,mjs,cjs,mts,cts", help="extensions for --heuristic")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--strip-prefix", action="append", default=[])
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--closure-min", type=int, default=1000, help="span (lines) for a function to count as a large closure")
    ap.add_argument("--cross-check", metavar="DIR",
                    help="with --lizard-csv: rescan JS/TS under DIR with the heuristic and flag large functions whose spans disagree")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    if args.lizard_csv:
        rows, method = read_lizard(args.lizard_csv, args.strip_prefix, args.exclude), "lizard"
    else:
        exts = {e.strip().lower() for e in args.ext.split(",") if e.strip()}
        rows, method = heuristic_scan(args.heuristic, args.exclude, exts), "heuristic brace matching (approximate)"
    result = {"method": method, **profile(rows, args.top, args.closure_min)}
    disagreements = []
    if args.lizard_csv and args.cross_check:
        exts = {e.strip().lower() for e in args.ext.split(",") if e.strip()}
        heur = {(h["file"], h["start"]): h["span"] for h in heuristic_scan(args.cross_check, args.exclude, exts)}
        for row in result["largest_functions"] + result["closure_factories"]:
            hs = heur.get((row["file"], row["start"]))
            if hs is None:
                continue
            row["heuristic_span"] = hs
            if abs(hs - row["span"]) > max(5, 0.1 * row["span"]):
                disagreements.append({"file": row["file"], "name": row["name"], "start": row["start"],
                                      "lizard_span": row["span"], "heuristic_span": hs})
    result["span_disagreements"] = disagreements
    result["caps"] = coverage_caps()
    result["symlinks_skipped"] = SYMLINKS_SKIPPED[0]
    for root_arg in (args.heuristic, args.cross_check):
        if root_arg and output_inside_root(args.json_out, root_arg):
            print(f"refusing to write output inside the audited root: {args.json_out}", file=sys.stderr)
            return 2
    if args.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)

    for cap in result["caps"]:
        print(f"CAP: {cap}", file=sys.stderr)
    print(f"Method: {method}. {result['functions']:,} functions; {result['functions_over_threshold']:,} span more than {args.closure_min:,} lines.")
    print("\n| Function | File | Lines (span) | Start |\n| --- | --- | --- | --- |")
    for r in result["largest_functions"]:
        print(f"| {r['name']} | {r['file']} | {r['span']:,} | {r['start']} |")
    for d in disagreements:
        print(f"WARNING: {d['name']} in {d['file']} at line {d['start']}: lizard says {d['lizard_span']:,} lines, "
              f"the heuristic says {d['heuristic_span']:,}. Read the file and use the real end line.", file=sys.stderr)
    print("\n| Factory closure | File | Span | Inner functions | Largest inner |\n| --- | --- | --- | --- | --- |")
    for f in result["closure_factories"]:
        li = ", ".join(f"{x['name']} {x['span']:,}" for x in f["largest_inner"][:3])
        print(f"| {f['name']} | {f['file']} | {f['span']:,} | {f['inner_functions']:,} | {li} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
