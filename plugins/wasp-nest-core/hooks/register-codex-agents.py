#!/usr/bin/env python3
"""Register packaged Codex agent roles after the plugin's hook is trusted."""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def register() -> dict[str, int] | None:
    plugin_root = os.environ.get("PLUGIN_ROOT")
    if not plugin_root:
        return None
    source_dir = Path(plugin_root) / "codex-agents"
    if not source_dir.is_dir():
        return None
    agents = sorted(source_dir.glob("*-wasp-drone.toml"))
    if not agents:
        return None

    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    target_dir = codex_home / "agents"
    target_dir.mkdir(parents=True, exist_ok=True)
    backup_dir = home / ".wasp-nest" / "backups" / "codex-agents" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    installed = backed_up = 0

    for source in agents:
        if source.is_symlink() or not source.is_file():
            continue
        target = target_dir / source.name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            continue
        content = source.read_bytes()
        previous = target.read_bytes() if target.is_file() else None
        if previous == content:
            continue
        if previous is not None:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_dir / source.name)
            backed_up += 1
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{source.name}.", suffix=".tmp", dir=target_dir)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as output:
                output.write(content)
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
        installed += 1

    return {"installed": installed, "backedUp": backed_up, "total": len(agents)}


if __name__ == "__main__":
    try:
        result = register()
        if result is not None and "--report" in sys.argv:
            print(json.dumps(result))
    except Exception as error:
        # SessionStart must not prevent the user's Codex session from starting.
        print(f"Wasp Nest Codex agent registration skipped: {error}", file=sys.stderr)
