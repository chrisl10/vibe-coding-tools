# Rules: guidance that stays active

A rule is a standard the assistant should follow throughout its work. Think of classroom rules such as "wear goggles during experiments" or "show your work on the test." A command starts one named routine. A rule applies whenever its condition is relevant.

## The four policies

### No em or en dashes

New prose uses ordinary punctuation. Literal data, code, regex, and verbatim quotations can preserve the characters. The dash guard hook enforces file edits mechanically.

### Plan construction protocol

Multi-step work starts from a feature branch, assigns the smallest capable specialist, records risk and validation, and does not claim completion before the ship gate passes.

### Pull request conflict check

Before handoff, fetch `origin/main`, check mergeability, resolve conflicts, push the clean branch, and verify again.

### Respect agent work boundaries

Parallel workers stay inside their assigned files and scope. One agent does not delete, overwrite, or "clean up" another agent's active work.

## Different harnesses, same intent

| Harness | Representation |
|---|---|
| Claude Code | Root `CLAUDE.md` plus `.claude/rules/*.md` |
| Codex | `.codex/config.toml` plus project instructions |
| Cursor | `.cursor/rules/*.mdc` |

The file formats differ. The policy should not.

## Rule versus hook

Use a rule when the standard requires judgment. Use a hook when a narrow part can be checked mechanically. For example, "protect user work" needs judgment, while "block these two Unicode dash characters in new Markdown text" can be deterministic.

## Writing a good rule

- State the required behavior in one sentence.
- Explain the reason in plain language.
- Name exceptions.
- Give good and bad examples.
- Avoid impossible promises such as "never make a bug."
- Connect mechanical parts to tests or hooks.
- Translate the rule into each supported harness.

Too many always-on rules compete for attention. Keep only standards that are broadly important, and put detailed procedures in skills.
