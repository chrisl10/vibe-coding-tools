# Release Packages

These archives are generated from the operational harness directories at repository root.

| Archive | Installable root | Contents |
|---|---|---|
| `vibe-coding-tools-claude-code-1.0.0.zip` | `.claude/` | Claude Code agents, skills, commands, rules, and hooks |
| `vibe-coding-tools-codex-1.0.0.zip` | `.codex/plugins/vibe-coding-tools/` | Codex plugin with 80 skills and hooks |
| `vibe-coding-tools-cursor-1.0.0.zip` | `.cursor/` | Cursor agents, skills, commands, rules, and hooks |

The Codex archive is the plugin layer. Native Codex project agents remain under `.codex/agents/` because Codex plugins do not install custom project-agent TOMLs.

Before publishing a new version:

1. Run `python learn/scripts/generate-harnesses.py`.
2. Validate Claude and Codex manifests.
3. Validate every component.
4. Rebuild all three archives.
5. Extract them into an empty temporary folder.
6. Check for absolute paths, parent traversal, `.git`, `.env`, and secrets.
7. Run security before quality.
