#!/usr/bin/env python3
"""Assemble <workspace>/evidence-index.md from every Drone's notes files.

Usage:
    python3 build_evidence_index.py <workspace>

Drones never write evidence-index.md (contract section 9). Each lists its raw artifacts under an
`## Evidence` heading in its own notes file. This script collects those lines per dimension, adds
any raw file nobody listed (so nothing is silently missing), and rewrites the index. Run it after
each wave; it is idempotent.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

FOLDERS = ["00-foundation", "01-bloat", "02-security", "03-quality", "04-remediation"]
HEADING = re.compile(r"^##\s+Evidence\s*$", re.I | re.M)
NEXT_HEADING = re.compile(r"^#{1,2}\s+\S", re.M)
PATH_IN_LINE = re.compile(r"`([^`]+)`")


def evidence_lines(notes: Path) -> list[str]:
    """Bullet lines under the first `## Evidence` heading of one notes file."""
    text = notes.read_text(encoding="utf-8", errors="replace")
    m = HEADING.search(text)
    if not m:
        return []
    rest = text[m.end():]
    end = NEXT_HEADING.search(rest)
    block = rest[: end.start()] if end else rest
    return [l.rstrip() for l in block.splitlines() if l.lstrip().startswith(("-", "*"))]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    ws = Path(sys.argv[1]).resolve()
    out = ["# Evidence index", "", "Every raw artifact behind a number in the brief, by dimension.", ""]
    total = 0
    for folder in FOLDERS:
        d = ws / folder
        if not d.is_dir():
            continue
        lines: list[str] = []
        for notes in sorted(d.glob("notes*.md")):
            if notes.name == "notes.md" and any(d.glob("notes-*.md")):
                continue  # the merged security notes repeat the per-source sections
            lines += evidence_lines(notes)
        listed = {p for l in lines for p in PATH_IN_LINE.findall(l)}
        raw = d / "raw"
        unlisted = []
        if raw.is_dir():
            for f in sorted(p for p in raw.rglob("*") if p.is_file() and not p.is_symlink()):
                rel = f.relative_to(ws).as_posix()
                if rel not in listed and f.relative_to(d).as_posix() not in listed:
                    unlisted.append(f"- `{rel}` - not described by its Drone")
        if not lines and not unlisted:
            continue
        out += [f"## {folder}", "", *lines, *unlisted, ""]
        total += len(lines) + len(unlisted)
    (ws / "evidence-index.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {ws / 'evidence-index.md'} ({total} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
