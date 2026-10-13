#!/usr/bin/env python3
"""Bundle forensic-output into a single packet archive after path preflight."""

import argparse
import os
import zipfile
from datetime import datetime
import sys
from pathlib import Path
from io import BytesIO
from private_output import write_batch, private_directory


def checked_path(path):
    path = Path(path)
    if ".." in path.parts:
        raise ValueError("packet path contains parent traversal")
    path = path.absolute()
    aliases = {'/tmp': '/private/tmp', '/var': '/private/var', '/etc': '/private/etc'}
    for entry in [*reversed(path.parents), path]:
        if entry.is_symlink():
            if sys.platform == 'darwin' and str(entry) in aliases and entry.resolve() == Path(aliases[str(entry)]):
                continue
            raise ValueError("packet path contains a symlink: " + str(entry))
    return path.resolve()


def safe_name(name):
    if not isinstance(name, str) or not name or name in {".", ".."} or any(c in name for c in ('/', '\\', ':')) or any(ord(c) < 32 or ord(c) == 127 for c in name):
        raise ValueError("packet name must be a single portable path component")
    return name


def build_archive(source, project_name, out_dir):
    source, out_dir = checked_path(source), checked_path(out_dir)
    if not source.is_dir() or not out_dir.is_dir():
        raise ValueError("packet source and output directories must exist")
    if out_dir == source or source in out_dir.parents:
        raise ValueError("packet output must be outside its source")
    slug = safe_name(project_name.replace(' ', '_'))
    safe_name(source.name)
    output = checked_path(out_dir / f"{slug}_Forensic_Packet_{datetime.now().strftime('%Y%m%d_%H%M')}.zip")
    files = []
    for path in sorted(source.rglob('*')):
        checked_path(path)
        for part in path.relative_to(source).parts:
            safe_name(part)
        if not path.is_file() and not path.is_dir():
            raise ValueError("packet member is not a regular file or directory")
        if path.is_file():
            files.append(path)
    payload = []
    for path in files:
        if '.~lock.' in path.name or '.tmp' in path.name:
            continue
        member = f"{slug}_Forensic_Packet/{source.name}/{path.relative_to(source).as_posix()}"
        payload.append((member, path.read_bytes()))
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for member, content in payload:
            archive.writestr(member, content)
    write_batch({output: buffer.getvalue()})
    return output, len(payload), sum(len(content) for _, content in payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--src', required=True, help='forensic-output directory')
    parser.add_argument('--project-name', required=True)
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    try:
        output, count, total = build_archive(args.src, args.project_name, args.out_dir)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print(f"Wrote {output}")
    print(f"Files: {count}; uncompressed: {total/1024/1024:.1f} MB; compressed: {output.stat().st_size/1024/1024:.1f} MB")


if __name__ == '__main__':
    main()
