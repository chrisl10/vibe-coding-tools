#!/usr/bin/env python3
"""Make the throwaway copy of the audited repository, portably.

Usage:
  python3 make_scratch_copy.py <repo> <dest> [--ref HEAD] [--working-tree]

One method on every platform (macOS, Linux, Windows with Git for Windows):
`git archive` streamed into Python's tarfile, so neither rsync nor a `tar`
binary is needed. `git archive` only reads the repository; nothing is written
into the audited repository or its `.git` (unlike `git worktree add`).

Default mode copies the committed tree at `--ref` (HEAD). `--working-tree`
copies tracked and untracked-but-not-ignored files instead, for a user who
asked to audit uncommitted work. Either way:

- Secret-shaped files are left out even if committed: `.env`, `.env.*`
  (except `.env.example`), `*.pem`, `*.key`, `.npmrc`, `*.tfstate*`, SSH private
  keys (`id_rsa*`, `id_ed25519*`, `id_ecdsa*`), `*.p12`, `*.pfx`, `.netrc`, `credentials.json`.
- Symlinks that point outside the copy, hard links and special files are
  skipped, so no tool run in the copy can follow a link back into the host.
- Submodule contents are never included; their presence is reported.

Prints a JSON summary (files written, excluded and skipped paths, submodule
flag). Record every excluded or skipped path as a coverage cap.
Exit codes: 0 copied, 1 git failed, 2 usage error (bad paths).
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath

EXCLUDE = (".env", ".env.*", "*.pem", "*.key", ".npmrc", "*.tfstate*", "id_rsa*", "id_ed25519*", "id_ecdsa*", "*.p12", "*.pfx", ".netrc", "credentials.json")
KEEP = (".env.example",)


def git_env() -> dict:
    """Neutral git environment: no system or global config, no prompts, no optional locks."""
    env = {k: v for k, v in os.environ.items() if k.upper() in {"PATH", "SYSTEMROOT", "COMSPEC", "PATHEXT", "TEMP", "TMP"}}
    env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0", "LANG": "C",
                # The audited repo's own .git/config is untrusted: never start its fsmonitor.
                "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false"})
    return env


def excluded(rel: str) -> bool:
    name = PurePosixPath(rel).name
    if name in KEEP:
        return False
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in EXCLUDE)


def safe_rel(rel: str) -> PurePosixPath | None:
    p = PurePosixPath(rel.replace("\\", "/"))
    if p.is_absolute() or not p.parts or ".." in p.parts or ":" in p.parts[0]:
        return None
    return p


def inside(dest: Path, target: Path) -> bool:
    try:
        Path(os.path.normpath(target)).relative_to(dest)
        return True
    except ValueError:
        return False


class Copier:
    def __init__(self, dest: Path):
        self.dest = dest
        self.files = 0
        self.excluded: list[str] = []
        self.skipped: list[dict] = []
        self.links: list[tuple[str, Path]] = []

    def skip(self, rel: str, reason: str) -> None:
        self.skipped.append({"path": rel, "reason": reason})

    def target(self, rel: str) -> Path | None:
        p = safe_rel(rel)
        if p is None:
            self.skip(rel, "unsafe path")
            return None
        if excluded(rel):
            self.excluded.append(rel)
            return None
        out = self.dest.joinpath(*p.parts)
        # Never write through a link created earlier in this copy (or onto one).
        probe = out
        while probe != self.dest:
            if probe.is_symlink():
                self.skip(rel, "path passes through a symlink")
                return None
            probe = probe.parent
        return out

    def link(self, rel: str, out: Path, linkname: str) -> None:
        resolved = out.parent / linkname
        if os.path.isabs(linkname) or not inside(self.dest, resolved):
            self.skip(rel, "symlink points outside the copy")
            return
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(linkname, out)
            self.links.append((rel, out))
        except OSError:
            self.skip(rel, "symlink could not be created on this platform")

    def contain_links(self) -> None:
        """The lexical check above cannot see chains (`a/up -> ..`, `b -> a/up/..`).
        Once every link exists, resolve each for real and drop any that leave the copy."""
        real_dest = Path(os.path.realpath(self.dest))
        removed = True
        while removed:
            removed = False
            for rel, out in list(self.links):
                if not inside(real_dest, Path(os.path.realpath(out))):
                    out.unlink()
                    self.links.remove((rel, out))
                    self.skip(rel, "symlink points outside the copy")
                    removed = True

    def write(self, out: Path, data, mode: int) -> None:
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "wb") as fh:
            shutil.copyfileobj(data, fh)
        if mode & 0o111:
            os.chmod(out, 0o755)
        self.files += 1


def copy_ref(repo: Path, ref: str, copier: Copier) -> int:
    cmd = ["git", "-C", str(repo), "archive", "--format=tar", ref]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=git_env())
    try:
        with tarfile.open(fileobj=proc.stdout, mode="r|") as tar:
            for member in tar:
                if member.name in ("pax_global_header",) or member.type == tarfile.XGLTYPE:
                    continue
                out = copier.target(member.name)
                if out is None:
                    continue
                if member.isdir():
                    out.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    copier.write(out, tar.extractfile(member), member.mode)
                elif member.issym():
                    copier.link(member.name, out, member.linkname)
                else:
                    copier.skip(member.name, "hard link or special file")
    except tarfile.TarError as exc:
        proc.kill()
        print(f"git archive output unreadable: {exc}", file=sys.stderr)
        return 1
    finally:
        err = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
        proc.wait()
    if proc.returncode != 0:
        print(f"git archive failed: {err.strip()}", file=sys.stderr)
        return 1
    return 0


def copy_working_tree(repo: Path, copier: Copier) -> int:
    r = subprocess.run(["git", "-C", str(repo), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                       capture_output=True, env=git_env())
    if r.returncode != 0:
        print(f"git ls-files failed: {r.stderr.decode('utf-8', 'replace').strip()}", file=sys.stderr)
        return 1
    for rel in sorted(set(filter(None, r.stdout.decode("utf-8", "replace").split("\0")))):
        out = copier.target(rel)
        if out is None:
            continue
        src = repo.joinpath(*PurePosixPath(rel).parts)
        if not inside(repo, Path(os.path.realpath(src.parent))):
            copier.skip(rel, "parent directory is a symlink leaving the repository")
        elif src.is_symlink():
            copier.link(rel, out, os.readlink(src))
        elif src.is_file():
            with open(src, "rb") as fh:
                copier.write(out, fh, src.stat().st_mode)
        elif not src.exists():
            copier.skip(rel, "tracked but missing from the working tree")
        else:
            copier.skip(rel, "not a regular file (submodule or special file)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("repo", type=Path)
    ap.add_argument("dest", type=Path)
    ap.add_argument("--ref", default="HEAD", help="commit to copy (default HEAD)")
    ap.add_argument("--working-tree", action="store_true", help="copy tracked and untracked, non-ignored files instead")
    args = ap.parse_args(argv)

    repo = args.repo.resolve()
    dest = args.dest.resolve()
    if not (repo / ".git").exists():
        print(f"not a git repository root: {repo}", file=sys.stderr)
        return 2
    if inside(repo, dest):
        print("refusing to write the copy inside the audited repository", file=sys.stderr)
        return 2
    if args.ref.startswith("-"):
        print("--ref must name a commit, not an option", file=sys.stderr)
        return 2
    if dest.exists() and any(dest.iterdir()):
        print(f"destination is not empty: {dest}", file=sys.stderr)
        return 2
    dest.mkdir(parents=True, exist_ok=True)

    copier = Copier(dest)
    code = copy_working_tree(repo, copier) if args.working_tree else copy_ref(repo, args.ref, copier)
    copier.contain_links()
    if code:
        return code
    print(json.dumps({
        "mode": "working-tree" if args.working_tree else "ref",
        "ref": None if args.working_tree else args.ref,
        "dest": str(dest),
        "files": copier.files,
        "excluded_patterns": list(EXCLUDE),
        "excluded": copier.excluded,
        "skipped": copier.skipped,
        "submodules_not_copied": (repo / ".gitmodules").is_file(),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
