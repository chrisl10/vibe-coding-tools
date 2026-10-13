#!/usr/bin/env python3
"""check-design-package.py -- product-design-stinger

Two deterministic, stdlib-only checks. No network access, never executes
content from the files it reads.

  package <design-dir>
      Structural check of a UX package written by product-design-stinger
      (default location library/knowledge/private/product/design). Reports
      missing required files, screen specs missing any of the four states,
      task flows without a Mermaid block carrying accTitle and accDescr,
      prototypes missing the light/dark, reduced-motion, lang, viewport or
      no-network rules, and em or en dashes in authored markdown.
      Exit 0 = clean, 2 = findings, 1 = usage or read error.

  inventory <file-or-dir> [--out inventory.json]
      Lists every file of a Claude Design export with size and SHA-256.
      Zip archives are listed member by member WITHOUT extracting; members
      with absolute paths, parent-directory segments, symlink modes, or an
      oversized or extreme compression ratio (possible zip bomb) are flagged
      unsafe and not read. Files are hashed in chunks. Exit 0 = inventory written and nothing unsafe,
      2 = unsafe members or suspicious types found, 1 = error.

Grounding: references/research/distilled-product-design.md (sections 1.3,
3, 6, 8, 9) and references/package-layout.md.
"""

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

REQUIRED_FILES = [
    "README.md",
    "direction.md",
    "information-architecture.md",
    "content-voice.md",
    "accessibility-baseline.md",
    "planning-handoff.md",
]
REQUIRED_DIRS = ["journeys", "flows", "screens", "prototypes", "critique"]
STATE_HEADINGS = ["empty", "loading", "error", "success"]
DASHES = (chr(0x2014), chr(0x2013))  # em dash, en dash
SUSPICIOUS_EXT = {".exe", ".dll", ".so", ".dylib", ".sh", ".bat", ".cmd", ".ps1",
                  ".app", ".jar", ".command", ".scr", ".msi", ".pkg", ".dmg"}
MAX_MEMBER_BYTES = 512 * 1024 * 1024  # zip members larger than this are flagged, not read
MAX_RATIO = 100  # uncompressed / compressed above this is flagged as a possible zip bomb
CHUNK = 1024 * 1024
EXTERNAL_RE = re.compile(r"""<(script|link|img|iframe)\b[^>]*\b(src|href)\s*=\s*["']\s*(https?:)?//""", re.I)


class Report:
    def __init__(self):
        self.findings = []

    def add(self, where, msg):
        self.findings.append((where, msg))

    def emit(self):
        for where, msg in self.findings:
            print(f"FINDING {where}: {msg}")
        print(f"Summary: {len(self.findings)} finding(s)")
        return 2 if self.findings else 0


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def check_dashes(path, text, rep, rel):
    for n, line in enumerate(text.splitlines(), 1):
        if any(d in line for d in DASHES):
            rep.add(f"{rel}:{n}", "em or en dash in authored prose; use a comma, colon, parentheses or period")


def check_screen(path, rep, rel):
    text = read(path)
    headings = {m.group(1).strip().lower() for m in re.finditer(r"^#{2,4}\s+(.+)$", text, re.M)}
    for state in STATE_HEADINGS:
        if not any(h == state or h.startswith(state + " ") or h.startswith(state + ":") for h in headings):
            rep.add(rel, f"screen spec has no '{state.title()}' state heading")
    check_dashes(path, text, rep, rel)


def check_flow(path, rep, rel):
    text = read(path)
    blocks = re.findall(r"```mermaid\s*\n(.*?)```", text, re.S)
    if not blocks:
        rep.add(rel, "task flow has no ```mermaid block")
    for i, block in enumerate(blocks, 1):
        if "accTitle" not in block or "accDescr" not in block:
            rep.add(rel, f"mermaid block {i} lacks accTitle and accDescr")
        if re.search(r"\[\s*end\s*\]|\(\s*end\s*\)", block):
            rep.add(rel, f"mermaid block {i} uses lowercase 'end' as a label, which breaks rendering")
    check_dashes(path, text, rep, rel)


def check_prototype(path, rep, rel):
    text = read(path)
    low = text.lower()
    if not re.search(r"<html[^>]*\blang\s*=", low):
        rep.add(rel, "missing lang attribute on <html>")
    if 'name="viewport"' not in low and "name='viewport'" not in low:
        rep.add(rel, "missing viewport meta")
    if ":root" not in low or "--" not in text:
        rep.add(rel, "no :root CSS custom properties (tokens must be CSS variables)")
    if "color-scheme" not in low or not ("light-dark(" in low or "prefers-color-scheme" in low):
        rep.add(rel, "no light and dark support (color-scheme plus light-dark() or prefers-color-scheme)")
    if "prefers-reduced-motion" not in low:
        rep.add(rel, "no prefers-reduced-motion rule")
    if ":focus-visible" not in low and "outline" not in low:
        rep.add(rel, "no visible focus style")
    if EXTERNAL_RE.search(text):
        rep.add(rel, "loads an external resource; prototypes must be single-file with no network requests")
    if path.name != "index.html":
        for state in STATE_HEADINGS:
            if f'"{state}"' not in low and f"'{state}'" not in low:
                rep.add(rel, f"no '{state}' state found in the prototype")


def cmd_package(args):
    root = Path(args.design_dir)
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 1
    rep = Report()
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            rep.add(name, "required file missing")
    for name in REQUIRED_DIRS:
        if not (root / name).is_dir():
            rep.add(name + "/", "required folder missing")
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        if rel.startswith("claude-design/imports/") and "/raw/" in rel:
            continue  # owner exports are kept unmodified
        if rel.startswith("screens/"):
            check_screen(md, rep, rel)
        elif rel.startswith("flows/"):
            check_flow(md, rep, rel)
        else:
            check_dashes(md, read(md), rep, rel)
    protos = root / "prototypes"
    if protos.is_dir():
        files = sorted(protos.glob("*.html"))
        if not (protos / "index.html").is_file():
            rep.add("prototypes/index.html", "missing prototype index")
        for html in files:
            check_prototype(html, rep, html.relative_to(root).as_posix())
    return rep.emit()


def sha256_stream(fh):
    h = hashlib.sha256()
    for chunk in iter(lambda: fh.read(CHUNK), b""):
        h.update(chunk)
    return h.hexdigest()


def zip_entries(path, unsafe):
    rows = []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            name = info.filename
            pp = PurePosixPath(name)
            reasons = []
            if name.startswith("/") or re.match(r"^[A-Za-z]:", name) or "\\" in name:
                reasons.append("absolute or non-portable path")
            if ".." in pp.parts:
                reasons.append("parent-directory segment")
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode and stat.S_ISLNK(mode):
                reasons.append("symlink")
            if pp.suffix.lower() in SUSPICIOUS_EXT:
                reasons.append("executable or script type")
            if info.file_size > MAX_MEMBER_BYTES or (
                    info.file_size > 1024 * 1024
                    and info.file_size > MAX_RATIO * max(info.compress_size, 1)):
                reasons.append("oversized or extreme compression ratio (possible zip bomb)")
            digest = None
            if not info.is_dir() and not reasons:
                with zf.open(info) as fh:
                    digest = sha256_stream(fh)
            row = {"path": f"{path.name}!{name}", "size": info.file_size, "sha256": digest}
            if reasons:
                row["unsafe"] = reasons
                unsafe.append(row)
            if not info.is_dir():
                rows.append(row)
    return rows


def cmd_inventory(args):
    target = Path(args.target)
    if not target.exists():
        print(f"ERROR: {target} does not exist", file=sys.stderr)
        return 1
    files = [target] if target.is_file() else sorted(p for p in target.rglob("*"))
    rows, unsafe = [], []
    base = target.parent if target.is_file() else target
    for p in files:
        rel = p.relative_to(base).as_posix()
        if p.is_symlink():
            row = {"path": rel, "size": None, "sha256": None, "unsafe": ["symlink"]}
            rows.append(row)
            unsafe.append(row)
            continue
        if p.is_dir():
            continue
        if not p.is_file():
            row = {"path": rel, "size": None, "sha256": None, "unsafe": ["not a regular file"]}
            rows.append(row)
            unsafe.append(row)
            continue
        with p.open("rb") as fh:
            digest = sha256_stream(fh)
        row = {"path": rel, "size": p.stat().st_size, "sha256": digest, "type": p.suffix.lower() or "none"}
        if p.suffix.lower() in SUSPICIOUS_EXT:
            row["unsafe"] = ["executable or script type"]
            unsafe.append(row)
        rows.append(row)
        if zipfile.is_zipfile(p):
            try:
                rows.extend(zip_entries(p, unsafe))
            except zipfile.BadZipFile as exc:
                print(f"ERROR: {rel}: {exc}", file=sys.stderr)
                return 1
    result = {"target": target.name, "files": rows, "unsafe": unsafe}
    out = json.dumps(result, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"Wrote {args.out}: {len(rows)} file(s), {len(unsafe)} unsafe")
    else:
        sys.stdout.write(out)
    return 2 if unsafe else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p1 = sub.add_parser("package", help="check a UX package folder")
    p1.add_argument("design_dir")
    p1.set_defaults(func=cmd_package)
    p2 = sub.add_parser("inventory", help="inventory a Claude Design export")
    p2.add_argument("target")
    p2.add_argument("--out")
    p2.set_defaults(func=cmd_inventory)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
