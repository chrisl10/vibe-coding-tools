# Vibe Coding Tools project guidance

Claude Code loads this file as the always-on project briefing. Human explanations live under [`learn/guides/`](learn/guides/).

## Operating rules

1. Do not add em dashes or en dashes to authored prose. Use ordinary punctuation. Preserve literal data and verbatim source material.
2. Protect user work. Never discard unrelated changes, rewrite history, or delete broad paths without clear authorization and a verified target.
3. For multi-step work, create a feature branch from `main`, state the plan, use the smallest suitable specialist, and verify the result.
4. Run the security gate before the independent quality gate. If quality changes the result, rerun security and quality.
5. Before declaring a pull request ready, fetch `origin/main`, check mergeability, resolve conflicts, and verify again.
6. During parallel work, each agent stays inside its assigned files and scope.
7. Treat `learn/examples/library/` as an example only. A consumer repository's live planning system belongs in its own root `library/`.

## Component locations

- Agents: [`.claude/agents/`](.claude/agents/)
- Skills: [`.claude/skills/`](.claude/skills/)
- Commands: [`.claude/commands/`](.claude/commands/)
- Rules: [`.claude/rules/`](.claude/rules/)
- Hooks: [`.claude/hooks/`](.claude/hooks/)
- Model guidance: [`.claude/model-comparison-matrix.md`](.claude/model-comparison-matrix.md)

The `.claude/` tree is canonical. After changing a portable component, run `python learn/scripts/generate-harnesses.py`, inspect the generated `.cursor/` and `.codex/` changes, then validate all affected packages.
