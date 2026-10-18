#!/usr/bin/env python3
"""Register packaged Codex agent roles after the plugin's hook is trusted."""

from __future__ import annotations

import json
import importlib.util
import os
import re
import shutil
import sys
import tempfile

if sys.version_info < (3, 11):
    # SessionStart must not prevent the user's Codex session from starting, so report and exit 0.
    print("Wasp Nest Codex agent registration skipped: register-codex-agents.py needs Python 3.11 or newer "
          "(it reads TOML with tomllib). Install Python 3.11+ and rerun; on Windows use `py -3.11`.", file=sys.stderr)
    sys.exit(0)

import tomllib  # noqa: E402  (imported after the version check so older Python fails clearly)
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

# Loading a trusted packaged helper must not mutate the plugin cache.
sys.dont_write_bytecode = True


def checked_path(path):
    path = Path(path)
    if ".." in path.parts:
        raise ValueError('registration path contains parent traversal')
    path = path.absolute()
    aliases = {'/tmp': '/private/tmp', '/var': '/private/var', '/etc': '/private/etc'}
    for entry in [*reversed(path.parents), path]:
        if entry.is_symlink():
            if sys.platform == 'darwin' and str(entry) in aliases and entry.resolve() == Path(aliases[str(entry)]):
                continue
            raise ValueError('registration path contains a symlink: ' + str(entry))
    return path.resolve()


FENCE = re.compile(r'^( {0,3})(`{3,}|~{3,}).*?^\1\2[ \t]*$', re.M | re.S)
CODE_SPAN = re.compile(r'(`+)(?!`).+?(?<!`)\1(?!`)', re.S)


def without_code(content, inline=True):
    blank = lambda match: re.sub(r'[^\n]', ' ', match.group(0))
    visible = FENCE.sub(blank, content)
    return CODE_SPAN.sub(blank, visible) if inline else visible


def installed_role_content(source):
    """Translate documentary resources when a role leaves its selected package."""
    content = source.read_text(encoding='utf-8')
    config = tomllib.loads(content)
    body = config['developer_instructions']
    package = source.parent.parent
    pattern = re.compile(r'(\]\()([^\s)]+)(\))')
    def replace(match):
        raw = match[2]
        if raw.startswith(('http:', 'https:', 'mailto:', '#', 'data:')):
            return match[0]
        relative, separator, anchor = raw.partition('#')
        # Resolve the lexical reference within the checked package, then inspect
        # every actual ancestor before reading or exposing that resource path.
        resource = Path(os.path.abspath(source.parent / unquote(relative)))
        if package not in resource.parents:
            raise ValueError('agent resource escapes selected package: ' + relative)
        checked_path(resource)
        if not resource.exists():
            raise ValueError('agent resource is missing from selected package: ' + relative)
        absolute = resource.as_posix()
        if any(c.isspace() for c in absolute):
            absolute = '<' + absolute + separator + anchor + '>'
        else:
            absolute += separator + anchor
        return match[1] + absolute + match[3]
    visible = without_code(body)
    for match in reversed(list(pattern.finditer(visible))):
        original = pattern.match(body, match.start())
        body = body[:match.start()] + replace(original) + body[match.end():]
    # Body prose also names the paired skill root in code spans. Keep those
    # references usable after registration, while preserving all TOML metadata.
    visible = without_code(body, inline=False)
    # Inline examples that contain Markdown links are documentary syntax, while
    # the plain paired-path code span is a real instruction resource.
    for span in reversed(list(CODE_SPAN.finditer(visible))):
        if '](' in span.group(0):
            visible = visible[:span.start()] + re.sub(r'[^\n]', ' ', span.group(0)) + visible[span.end():]
    for match in reversed(list(re.finditer(r'\.\./skills/', visible))):
        body = body[:match.start()] + (package / 'skills').as_posix() + '/' + body[match.end():]
    field = re.compile(r'(?ms)^developer_instructions\s*=\s*(?:""".*?"""|"(?:\\.|[^"\\])*"|\x27\x27\x27.*?\x27\x27\x27|\x27[^\x27]*\x27)')
    rewritten, count = field.subn(lambda _: 'developer_instructions = ' + json.dumps(body, ensure_ascii=False), content, count=1)
    if count != 1:
        raise ValueError('agent instruction field cannot be projected safely')
    projected = tomllib.loads(rewritten)
    if {k: v for k, v in projected.items() if k != 'developer_instructions'} != {k: v for k, v in config.items() if k != 'developer_instructions'}:
        raise ValueError('agent metadata changed during resource projection')
    return rewritten.encode('utf-8')


def register() -> dict[str, int] | None:
    plugin_root = os.environ.get("PLUGIN_ROOT")
    if not plugin_root:
        return None
    root = checked_path(plugin_root)
    checked_path(root / "plugin.json")
    checked_path(root / "plugin-catalog.json")
    registry = checked_path(os.environ.get("WASP_NEST_PLUGIN_REGISTRY") or Path.home() / ".wasp-nest/installed-plugins.json")
    if registry.is_file():
        for selected in json.loads(registry.read_text())["plugins"].values():
            selected_root = checked_path(selected)
            checked_path(selected_root / "plugin.json")
    resolver_path = checked_path(root / 'hooks/resolve-component.py')
    spec = importlib.util.spec_from_file_location('wasp_installed_components', resolver_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    roots = module.installed_roots(root)
    data = json.loads((roots['wasp-nest-core'] / 'plugin-catalog.json').read_text())
    owners = {p['name']: p for p in data['plugins']}
    agents = []
    projected_contents = {}
    for name, package in roots.items():
        if name not in owners:
            raise ValueError('unknown installed plugin: ' + name)
        for requirement in owners[name]['requires']:
            if requirement not in roots:
                raise ValueError('required plugin is not installed: ' + requirement)
        if json.loads((package / 'plugin.json').read_text()).get('version') != data['version']:
            raise ValueError('installed plugin version differs from Core: ' + name)
        for agent_name in owners[name]['agents']:
            agent = package / 'codex-agents' / (agent_name + '.toml')
            if (package / 'codex-agents').is_symlink() or not agent.is_file() or agent.is_symlink():
                raise ValueError('declared agent role is missing: ' + agent_name)
            if tomllib.loads(agent.read_text()).get('name') != agent_name:
                raise ValueError('agent role identity mismatch: ' + agent_name)
            projected_contents[agent] = installed_role_content(agent)
            agents.append(agent)
    if not agents:
        return None

    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    target_dir = codex_home / "agents"
    for ancestor in [target_dir, *target_dir.parents]:
        if ancestor == home:
            break
        if ancestor.is_symlink():
            raise ValueError('Codex agent target has a symlink ancestor: ' + str(ancestor))
    backup_dir = home / ".wasp-nest" / "backups" / "codex-agents" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    for ancestor in [backup_dir, *backup_dir.parents]:
        if ancestor == home:
            break
        if ancestor.is_symlink():
            raise ValueError('Codex agent backup has a symlink ancestor: ' + str(ancestor))
    target_dir = checked_path(target_dir)
    backup_dir = checked_path(backup_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    installed = backed_up = 0

    for source in agents:
        if source.is_symlink() or not source.is_file():
            continue
        target = target_dir / source.name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            continue
        # Global roles point to the selected package's actual paired resources.
        content = projected_contents[source]
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
