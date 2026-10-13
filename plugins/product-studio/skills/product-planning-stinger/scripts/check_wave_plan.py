#!/usr/bin/env python3
"""check_wave_plan.py - read-only checker for a product-planning Wave Plan.

Checks a wave-plan.md written from references/templates/wave-plan.md:

  * the wave table (columns Key, Wave, Depends on) parses
  * keys are unique and every dependency names a known key
  * the dependency graph has no cycle (Kahn's algorithm)
  * every dependency sits in an EARLIER wave (end-to-start)
  * waves are numbered 1..N with no gaps
  * the Mermaid graph has the same edges as the table
  * optional --prd-map: same keys and same dependencies as the PRD Map

It also prints the fewest possible waves (Kahn levels) as a suggestion.
Grounding: references/research/raw/topological-sorting.md,
references/research/raw/linear-project-dependencies.md,
references/research/raw/mermaid-flowchart-syntax.md.

Stdlib only. Writes nothing. Exit 0 when no errors, 1 on errors, 2 on usage.
"""

import argparse
import re
import sys
from pathlib import Path

KEY_RE = re.compile(r"^F\d{2,3}$")
EDGE_RE = re.compile(r"\b(F\d{2,3})\b[^\n]*?-->\s*(?:\|[^|]*\|\s*)?(F\d{2,3})\b")


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def find_table(text, required):
    """Return list of row dicts for the first table whose header has all required columns."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        header = [h.lower() for h in split_row(line)]
        if not all(col in header for col in required):
            continue
        rows = []
        for body in lines[i + 2:]:
            if not body.strip().startswith("|"):
                break
            cells = split_row(body)
            rows.append({header[j]: cells[j] if j < len(cells) else "" for j in range(len(header))})
        return rows
    return None


def parse_deps(value):
    value = value.strip()
    if not value or value.lower() in {"none", "-", "n/a"}:
        return []
    return [d.strip() for d in re.split(r"[,\s]+", value) if d.strip()]


def kahn_levels(nodes, deps):
    """Return (levels dict, cyclic set). Level 1 = no dependencies."""
    remaining = {n: set(d for d in deps.get(n, []) if d in nodes) for n in nodes}
    levels = {}
    level = 0
    while remaining:
        ready = sorted(n for n, d in remaining.items() if not d)
        if not ready:
            return levels, set(remaining)
        level += 1
        for n in ready:
            levels[n] = level
            del remaining[n]
        for d in remaining.values():
            d.difference_update(ready)
    return levels, set()


def mermaid_edges(text):
    blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
    if not blocks:
        return None
    edges = set()
    for block in blocks:
        for line in block.splitlines():
            for a, b in EDGE_RE.findall(line):
                edges.add((a, b))
    return edges


def check(plan_path, map_path=None):
    errors, notes = [], []
    text = plan_path.read_text(encoding="utf-8")
    rows = find_table(text, ["key", "wave", "depends on"])
    if rows is None:
        return ["no wave table with columns Key, Wave, Depends on"], notes

    waves, deps = {}, {}
    for row in rows:
        key = row.get("key", "")
        if not KEY_RE.match(key):
            errors.append("row key '%s' is not an F## planning key" % key)
            continue
        if key in waves:
            errors.append("duplicate key %s" % key)
            continue
        wave = row.get("wave", "")
        if not wave.isdigit() or int(wave) < 1:
            errors.append("%s has wave '%s'; use a whole number from 1" % (key, wave))
            continue
        waves[key] = int(wave)
        deps[key] = parse_deps(row.get("depends on", ""))

    for key, ds in deps.items():
        for d in ds:
            if d not in waves:
                errors.append("%s depends on unknown key %s" % (key, d))

    levels, cyclic = kahn_levels(set(waves), deps)
    if cyclic:
        errors.append("dependency cycle: these keys are in or behind a cycle and cannot be ordered: %s (fix the PRD Map: merge PRDs or pull out a shared contract)" % ", ".join(sorted(cyclic)))

    for key, ds in deps.items():
        for d in ds:
            if d in waves and waves[d] >= waves[key]:
                errors.append("violated: %s (wave %d) depends on %s (wave %d); a dependency must be in an earlier wave" % (key, waves[key], d, waves[d]))

    used = sorted(set(waves.values()))
    if used and used != list(range(1, used[-1] + 1)):
        errors.append("wave numbers have gaps: %s" % used)

    table_edges = {(d, k) for k, ds in deps.items() for d in ds if d in waves}
    graph = mermaid_edges(text)
    if graph is None:
        errors.append("no ```mermaid dependency graph found")
    else:
        for a, b in sorted(table_edges - graph):
            errors.append("edge %s --> %s is in the table but missing from the Mermaid graph" % (a, b))
        for a, b in sorted(graph - table_edges):
            errors.append("edge %s --> %s is in the Mermaid graph but not in the table" % (a, b))
        if re.search(r"^\s*end\s*\[", text, re.M):
            errors.append("a node named lowercase 'end' breaks Mermaid")

    if map_path is not None:
        mrows = find_table(map_path.read_text(encoding="utf-8"), ["key", "depends on"])
        if mrows is None:
            errors.append("PRD Map has no table with columns Key and Depends on")
        else:
            mdeps = {r["key"]: set(parse_deps(r.get("depends on", ""))) for r in mrows if KEY_RE.match(r.get("key", ""))}
            for k in sorted(set(mdeps) - set(waves)):
                errors.append("%s is in the PRD Map but not in any wave" % k)
            for k in sorted(set(waves) - set(mdeps)):
                errors.append("%s is in the Wave Plan but not in the PRD Map" % k)
            for k in sorted(set(mdeps) & set(waves)):
                if mdeps[k] != set(deps[k]):
                    errors.append("%s dependencies differ: map %s, plan %s" % (k, sorted(mdeps[k]), sorted(deps[k])))

    if not cyclic and levels:
        fewest = max(levels.values())
        notes.append("fewest possible waves: %d (plan uses %d)" % (fewest, max(waves.values()) if waves else 0))
        for lvl in range(1, fewest + 1):
            notes.append("  suggested wave %d: %s" % (lvl, ", ".join(sorted(k for k, v in levels.items() if v == lvl))))
    status = re.search(r"\*\*Status:\*\*\s*([A-Za-z]+)", text)
    notes.append("status: %s" % (status.group(1) if status else "not stated"))
    return errors, notes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("wave_plan", type=Path)
    parser.add_argument("--prd-map", type=Path, default=None)
    args = parser.parse_args(argv)
    for p in [args.wave_plan] + ([args.prd_map] if args.prd_map else []):
        if not p.is_file():
            print("ERROR: file not found: %s" % p)
            return 2
    errors, notes = check(args.wave_plan, args.prd_map)
    for e in errors:
        print("ERROR: " + e)
    for n in notes:
        print("INFO: " + n)
    print("Summary: %d error(s)" % len(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
