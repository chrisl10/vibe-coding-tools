@AGENTS.md

## Claude Code

The shared project briefing lives in [`AGENTS.md`](AGENTS.md) and is imported above. Everything in it applies here.

Claude Code specifics:

- Slash commands: `/the-beekeeper` to route a task, `/the-smoker` to drive PRDs to verified completion.
- Load the whole colony locally with `claude --plugin-dir .claude`.
- Hooks in [`.claude/hooks/`](.claude/hooks/) enforce the no-dash rule on writes and validate components after edits.
