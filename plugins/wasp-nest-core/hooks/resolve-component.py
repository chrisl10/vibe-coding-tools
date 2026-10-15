#!/usr/bin/env python3
"""Resolve one installed capability from the user's plugin registry.

The Wasp Nest registry (~/.wasp-nest/installed-plugins.json, written by the local
installer) wins. Without it, Claude Code's own marketplace install record is used.
"""

import argparse
import json
import os
from pathlib import Path


def claude_selection(core_root, claude_registry=None):
    """Read Claude Code's own install record when no Wasp Nest registry exists.

    A Claude marketplace install (`/plugin install`) records each installed plugin in
    `<CLAUDE_CONFIG_DIR or ~/.claude>/plugins/installed_plugins.json`, keyed
    `name@marketplace`. Only plugins from Core's marketplace that the catalog knows
    are selected; cached siblings that Claude does not list stay unselected.
    """
    claude_home = Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude')
    path = Path(claude_registry or os.environ.get('WASP_NEST_CLAUDE_REGISTRY') or claude_home / 'plugins/installed_plugins.json')
    if not path.is_file():
        return {}
    known = {p['name'] for p in json.loads((core_root / 'plugin-catalog.json').read_text())['plugins']}
    version = json.loads((core_root / 'plugin.json').read_text()).get('version')
    cwd = Path.cwd().resolve()
    # installed_plugins.json lists installs; a plugin switched off in any Claude
    # settings file (enabledPlugins: false) is not selected.
    disabled = set()
    for settings in [claude_home / 'settings.json', cwd / '.claude/settings.json', cwd / '.claude/settings.local.json']:
        try:
            enabled = json.loads(settings.read_text()).get('enabledPlugins', {}) if settings.is_file() else {}
            disabled |= {key for key, value in enabled.items() if value is False}
        except (ValueError, AttributeError, OSError):
            continue
    try:
        listed = json.loads(path.read_text()).get('plugins', {})
        listed = listed if isinstance(listed, dict) else {}
    except (ValueError, AttributeError):
        return {}
    entries = {}
    for key, installs in listed.items():
        if key in disabled:
            continue
        name, _, marketplace = key.partition('@')
        for install in installs if isinstance(installs, list) else [installs]:
            if not isinstance(install, dict):
                continue
            root = install.get('installPath')
            if name not in known or not isinstance(root, str) or not root or not Path(root).is_absolute():
                continue
            project = install.get('projectPath')
            if install.get('scope', 'user') != 'user' and not (isinstance(project, str) and project and (cwd == Path(project).resolve() or Path(project).resolve() in cwd.parents)):
                continue
            entries.setdefault(marketplace, {}).setdefault(name, []).append((install.get('version'), Path(root).resolve()))
    # Core's own entry names the marketplace to trust; never mix marketplaces.
    marketplaces = [m for m, plugins in entries.items() if any(root == core_root for _, root in plugins.get('wasp-nest-core', []))]
    if len(marketplaces) != 1:
        return {}
    selection = {}
    for name, candidates in entries[marketplaces[0]].items():
        matching = [root for found, root in candidates if found == version]
        selection[name] = str((matching or [root for _, root in candidates])[0])
    return selection


def installed_roots(core_root=None, registry=None, claude_registry=None):
    core_root = Path(core_root or os.environ.get('PLUGIN_ROOT') or Path(__file__).resolve().parents[1]).resolve()
    registry = Path(registry or os.environ.get('WASP_NEST_PLUGIN_REGISTRY') or Path.home() / '.wasp-nest/installed-plugins.json')
    roots = {}
    if registry.is_file():
        selection = json.loads(registry.read_text())['plugins']
    elif (core_root / 'plugin-catalog.json').is_file() and (core_root / 'plugin.json').is_file():
        selection = claude_selection(core_root, claude_registry)
    else:
        selection = {}
    for name, value in selection.items():
        path = Path(value).resolve()
        if not Path(value).is_absolute():
            raise ValueError('registry root must be absolute: ' + name)
        manifest = path / 'plugin.json'
        if not manifest.is_file() or json.loads(manifest.read_text()).get('name') != name:
            raise ValueError('installed plugin identity mismatch: ' + name)
        roots[name] = path
    manifest = core_root / 'plugin.json'
    if manifest.is_file() and json.loads(manifest.read_text()).get('name') == 'wasp-nest-core':
        roots['wasp-nest-core'] = core_root
    if 'wasp-nest-core' not in roots:
        raise ValueError('required plugin is not installed: wasp-nest-core')
    return roots


def resolve(name, kind='skill', workflow=None, core_root=None, registry=None, claude_registry=None):
    roots = installed_roots(core_root, registry, claude_registry)
    data = json.loads((roots['wasp-nest-core'] / 'plugin-catalog.json').read_text())
    plugins = {p['name']: p for p in data['plugins']}
    unknown = set(roots) - set(plugins)
    if unknown:
        raise ValueError('unknown installed plugin: ' + ', '.join(sorted(unknown)))
    matches = [p for p in plugins.values() if name in p[kind + 's']]
    if len(matches) != 1:
        raise ValueError('component needs exactly one owner: ' + name)
    owner = matches[0]
    seen = set()

    def require(plugin):
        if plugin in seen:
            return
        seen.add(plugin)
        if plugin not in roots:
            raise ValueError('required plugin is not installed: ' + plugin)
        if json.loads((roots[plugin] / 'plugin.json').read_text()).get('version') != data['version']:
            raise ValueError('installed plugin version differs from Core: ' + plugin)
        for dependency in plugins[plugin]['requires']:
            require(dependency)

    require('wasp-nest-core')
    require(owner['name'])
    if workflow:
        requirements = owner['optional_workflow_requirements']
        if workflow not in requirements:
            raise ValueError('unknown workflow prerequisite key: ' + workflow)
        for dependency in requirements[workflow]:
            require(dependency)
    relative = 'skills/' + name + '/SKILL.md' if kind == 'skill' else kind + 's/' + name + '.md'
    package = roots[owner['name']]
    path = package / relative
    if path.is_symlink() or not path.is_file():
        raise ValueError('installed component is missing: ' + name)
    if any(parent.is_symlink() for parent in path.parents if parent != package and package in parent.parents):
        raise ValueError('installed component has a symlink ancestor: ' + name)
    if package not in path.resolve().parents:
        raise ValueError('installed component escapes its plugin root: ' + name)
    return {'plugin': owner['name'], 'kind': kind, 'name': name, 'path': str(path), 'checked_plugins': sorted(seen)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--kind', choices=['skill', 'agent', 'command'], default='skill')
    parser.add_argument('--workflow')
    parser.add_argument('--registry', type=Path)
    parser.add_argument('--core-root', type=Path)
    parser.add_argument('--claude-registry', type=Path, help='Claude installed_plugins.json, used only when the Wasp Nest registry is absent')
    args = parser.parse_args()
    try:
        print(json.dumps(resolve(args.name, args.kind, args.workflow, args.core_root, args.registry, args.claude_registry)))
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(1, str(error) + '\n')
