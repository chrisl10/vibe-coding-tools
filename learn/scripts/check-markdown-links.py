#!/usr/bin/env python3
"""Report broken local Markdown links in files or directories."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "#")


def markdown_files(values: list[str]) -> list[Path]:
    result: set[Path] = set()
    for value in values:
        path = Path(value)
        if path.is_dir():
            result.update(path.rglob("*.md"))
        elif path.suffix.lower() in {".md", ".mdc"} and path.exists():
            result.add(path)
    return sorted(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Markdown files or directories")
    args = parser.parse_args()
    failures = []
    files = markdown_files(args.paths)
    for file in files:
        text = file.read_text(encoding="utf-8")
        if "references/research/raw" in file.as_posix():
            continue
        for match in LINK.finditer(text):
            raw = match.group(1).strip().strip("<>")
            target = raw.split("#", 1)[0].strip()
            if not target or target.startswith(SKIP_PREFIXES):
                continue
            if any(marker in target for marker in ("<", ">", "{", "}", "*", "$")):
                continue
            target = unquote(target.split(' "', 1)[0])
            resolved = (file.parent / target).resolve()
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{file.as_posix()}:{line}: {raw}")
    if failures:
        print("Broken local Markdown links:")
        print("\n".join(failures))
        print(f"FAIL: {len(failures)} broken links across {len(files)} files")
        return 1
    print(f"PASS: 0 broken links across {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
