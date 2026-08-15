# Harness Compatibility

Vibe Coding Tools preserves each capability using the format its harness actually supports. Compatibility means the behavior survives, not that every directory name is identical.

| Capability | Claude Code | Codex | Cursor |
|---|---|---|---|
| 75 agents | Markdown agents | 75 project TOML agents | Markdown agents |
| 78 core skills | Native plugin skills | Native plugin skills | Native skills |
| 2 commands | Native commands | Translated into 2 skills | Native commands |
| 4 rules | `CLAUDE.md` and `.md` rules | Project developer instructions | Native `.mdc` rules |
| Dash guard | Blocking PreToolUse hook | Blocking PreToolUse adapter parses patches | Blocking preToolUse hook |
| Component validation | Advisory PostToolUse hook | Advisory PostToolUse patch adapter | Advisory postToolUse hook |
| Package manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` | `.cursor-plugin/plugin.json` |

## Codex has two layers

The Codex plugin provides skills and hooks in the ChatGPT desktop app and Codex CLI. The Codex IDE extension does not install plugins, so the repository also ships `.codex/agents`, `.codex/config.toml`, and `.codex/hooks.json` as a project adapter.

## Source and generation

The `.claude` tree is canonical. `learn/scripts/generate-harnesses.py` removes unsupported shared agent metadata, translates active Cursor paths, creates Codex TOML agents, and refreshes the 80 Codex-facing skills.

## Honest limits

- A Codex plugin does not contain the 75 custom-agent TOMLs. The project adapter does.
- Cursor and Claude hook payloads are not interchangeable, even when they call the same script.
- A model name from one provider is not copied into another provider's configuration.
- Installed hooks require each harness's trust and reload process.
