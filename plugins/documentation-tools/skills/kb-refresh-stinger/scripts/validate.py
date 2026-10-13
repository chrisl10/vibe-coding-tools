#!/usr/bin/env python3
"""
validate.py - deterministic self-check for kb-refresh-stinger.

Checks the stinger's own files: six-spec frontmatter on SKILL.md, no em or
en dashes in authored files (raw research archive exempt), relative links
resolve, and required sections exist.

JSON on stdout; exit 0 pass, 1 fail, 2 usage or environment error.
"""

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
RAW = "references" + "/research/raw/"


def dash_check() -> list:
    hits = []
    for md in SKILL_DIR.rglob("*.md"):
        rel = md.relative_to(SKILL_DIR).as_posix()
        if rel.startswith(RAW):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for ch, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
            if ch in text:
                hits.append({"file": rel, "violation": name})
    return hits


def frontmatter_check() -> dict:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {"ok": False, "error": "no frontmatter block"}
    fields = set(re.findall(r"^([a-z-]+):", match.group(1), re.M))
    extra = fields - SPEC_FIELDS
    if extra:
        return {"ok": False, "error": f"non-spec fields: {sorted(extra)}"}
    name_match = re.search(r'^name:\s*"([^"]+)"', match.group(1), re.M)
    if not name_match or name_match.group(1) != SKILL_DIR.name:
        return {"ok": False, "error": "name field missing or != folder name"}
    return {"ok": True, "fields": sorted(fields)}


def link_check() -> list:
    broken = []
    for md in SKILL_DIR.rglob("*.md"):
        rel_dir = md.parent
        for target in re.findall(r"\]\(([^)#]+?\.md)\)", md.read_text(encoding="utf-8", errors="replace")):
            if target.startswith("http"):
                continue
            resolved = (rel_dir / target.replace("../../", SKILL_DIR.parent.parent.as_posix() + "/")).resolve()
            if not resolved.exists() and not (rel_dir / target).resolve().exists():
                broken.append({"file": md.relative_to(SKILL_DIR).as_posix(), "link": target})
    return broken


def section_check() -> list:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    missing = [s for s in ("## Purpose", "## Procedure", "## Critical Directive", "## Ship Gate") if s not in text]
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate kb-refresh-stinger files")
    parser.add_argument("target", nargs="?", default=str(SKILL_DIR))
    args = parser.parse_args()
    if Path(args.target).resolve() != SKILL_DIR:
        print(json.dumps({"status": "usage-error", "error": "this validator checks its own skill directory"}))
        return 2

    fm = frontmatter_check()
    dashes = dash_check()
    broken = link_check()
    missing_sections = section_check()
    ok = fm.get("ok") and not dashes and not broken and not missing_sections

    print(json.dumps({
        "status": "pass" if ok else "fail",
        "frontmatter": fm,
        "dash_violations": dashes,
        "broken_links": broken,
        "missing_sections": missing_sections,
        "files_checked": len(list(SKILL_DIR.rglob("*.md"))),
    }))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
