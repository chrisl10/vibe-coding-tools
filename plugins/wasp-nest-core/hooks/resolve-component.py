#!/usr/bin/env python3
"""Resolve one installed capability from the user's explicit plugin registry."""

import argparse
import json
import os
from pathlib import Path


def installed_roots(core_root=None, registry=None):
    core_root = Path(core_root or os.environ.get('PLUGIN_ROOT') or Path(__file__).resolve().parents[1]).resolve()
    registry = Path(registry or os.environ.get('WASP_NEST_PLUGIN_REGISTRY') or Path.home() / '.wasp-nest/installed-plugins.json')
    roots = {}
    if registry.is_file():
        for name, value in json.loads(registry.read_text())['plugins'].items():
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


def resolve(name, kind='skill', workflow=None, core_root=None, registry=None):
    roots = installed_roots(core_root, registry)
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
    args = parser.parse_args()
    try:
        print(json.dumps(resolve(args.name, args.kind, args.workflow, args.core_root, args.registry)))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, str(error) + '\n')
