#!/usr/bin/env python3
"""Create reproducible public marketplace and per-plugin release archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)


def checked_path(path: Path) -> Path:
    path = Path(path)
    if ".." in path.parts:
        raise ValueError("archive path contains parent traversal")
    if any("\\" in part or ":" in part or any(ord(c) < 32 or ord(c) == 127 for c in part) for part in path.parts if part != path.anchor):
        raise ValueError("path contains a non-portable member name")
    path = path.absolute()
    aliases = {'/tmp': '/private/tmp', '/var': '/private/var', '/etc': '/private/etc'}
    for entry in [*reversed(path.parents), path]:
        if entry.is_symlink():
            if sys.platform == 'darwin' and str(entry) in aliases and entry.resolve() == Path(aliases[str(entry)]):
                continue
            raise ValueError("archive path contains a symlink: " + str(entry))
    return path.resolve()


def checked_files(root: Path) -> list[Path]:
    root = checked_path(root)
    if not root.is_dir():
        raise ValueError("archive source must be a directory")
    files = []
    for source in sorted(root.rglob("*")):
        checked_path(source)
        if source.is_file():
            files.append(source)
        elif not source.is_dir():
            raise ValueError("archive source is not a regular file or directory")
    return files


def archive(path: Path, files: list[Path], root: Path) -> None:
    root, path = checked_path(root), checked_path(path)
    payload = []
    for source in sorted(files):
        source = checked_path(source)
        if root not in source.parents or not source.is_file():
            raise ValueError("archive member escapes its source root")
        payload.append((source.relative_to(root).as_posix(), source.read_bytes()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for name, content in payload:
            item = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o644 << 16
            output.writestr(item, content)


def package(root: Path, out: Path) -> list[Path]:
    root, out = checked_path(root), checked_path(out)
    if root == Path(root.anchor) or root == Path.home().resolve():
        raise ValueError("release source must be a dedicated publication tree")
    if out in {root, Path(out.anchor), Path.home().resolve()}:
        raise ValueError("release output must be a dedicated directory")
    if root / "plugins" == out or root / "plugins" in out.parents:
        raise ValueError("release output must be outside plugin payloads")
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError(f"release output is not empty: {out}")
    files = checked_files(root)
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must be a plain semantic version")
    market = root / ".claude-plugin" / "marketplace.json"
    if not market.is_file():
        raise ValueError("Claude marketplace catalog is missing")
    publication_manifest = root / "PUBLICATION-MANIFEST.json"
    if not publication_manifest.is_file():
        raise ValueError("publication manifest is required before release packaging")
    manifest = json.loads(publication_manifest.read_text())
    actual = {f.relative_to(root).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f != publication_manifest and root / ".git" not in f.parents and out not in f.parents}
    if manifest.get("version") != version or manifest.get("files") != actual:
        raise ValueError("publication manifest does not match release payload")
    entries = json.loads(market.read_text(encoding="utf-8"))["plugins"]
    names = [entry["name"] for entry in entries]
    if len(set(names)) != len(names) or any(not isinstance(n, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n) for n in names):
        raise ValueError("marketplace plugin names must be unique kebab-case identifiers")
    plans = []
    for name in names:
        folder = root / "plugins" / name
        manifest = folder / ".claude-plugin" / "plugin.json"
        if not manifest.is_file() or json.loads(manifest.read_text()).get("name") != name:
            raise ValueError(f"plugin not found or identity differs: {name}")
        archive_name = f"wasp-nest-core-{version}.zip" if name == "wasp-nest-core" else f"wasp-nest-pack-{name}-{version}.zip"
        target = checked_path(out / archive_name)
        plans.append((target, [f for f in files if folder in f.parents]))
    plans.append((checked_path(out / f"wasp-nest-marketplace-{version}.zip"), [f for f in files if root / ".git" not in f.parents and out not in f.parents]))
    checked_path(out / "SHA256SUMS")
    out.mkdir(parents=True, exist_ok=True)
    archives = []
    for target, members in plans:
        archive(target, members, root)
        archives.append(target)
    checksums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in sorted(archives))
    (out / "SHA256SUMS").write_text(checksums, encoding="utf-8")
    return archives


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    archives = package(args.root, args.out)
    print(f"packed {len(archives)} public archives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
