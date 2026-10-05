---
name: "source-command-smoke-it"
description: "Drive a set of PRDs to 100% completion using the Wasp Swarm. Spawns armed wasp-drone sub-agents in waves, tracks every acceptance criterion to zero open items, runs the security/quality close-out, and ships via commit-push-PR-CI. Trigger with \"run the PRDs\", \"execute the PRDs\", \"smoke it\", \"complete the acceptance criteria\", \"finish everything in the PRD\"."
license: "AGPL-3.0-or-later"
---

# source-command-smoke-it

Use this skill when the user asks to run the migrated source command `smoke-it`.

Read [the command procedure](../../commands/smoke-it.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.
