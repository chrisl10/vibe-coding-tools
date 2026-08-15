# Hooks: automatic checkpoints

A hook is a small program that runs when a specific event happens. A smoke detector is a useful analogy. You do not need to remember to check for smoke every minute. The detector watches the event and responds automatically.

AI coding hooks can run before or after a tool action, when a session starts, or when a prompt is submitted. They are best for important checks that should not depend on memory.

## The two hooks in this project

### Dash guard

The dash guard runs before a write or edit. It inspects new prose in Markdown, MDX, MDC, and text files. If the edit adds an em dash or en dash, the hook blocks the tool call and explains how to replace it. Raw research archives are exempt because they preserve source material.

The same policy is translated for three input formats:

- Claude provides a file path and changed text.
- Codex provides an `apply_patch` command, so the adapter extracts paths and added lines.
- Cursor provides its own event and response fields.

The outcome is the same even though the message format differs.

### Component validator

The component validator runs after a Bee or Stinger edit. It calls the repository validator and sends problems back to the assistant. It is advisory because a file may be temporarily incomplete during a series of edits.

## Locations

| Harness | Manifest | Scripts |
|---|---|---|
| Claude project | `.claude/settings.json` | `.claude/hooks/` |
| Claude plugin | `.claude/hooks/hooks.json` | `.claude/hooks/` |
| Codex project | `.codex/hooks.json` | `.codex/hooks/` |
| Codex plugin | plugin `hooks/hooks.json` | plugin `hooks/` |
| Cursor project/plugin | `.cursor/hooks.json` | `.cursor/hooks/` |

Codex requires review and trust for changed local hooks. Use `/hooks` to inspect the exact definitions before enabling them.

## Blocking versus advisory hooks

A blocking hook prevents an unsafe action. Use it only when the policy can be checked reliably and a false block is easy to fix.

An advisory hook adds context after an action. Use it for validation findings, reminders, and information that needs judgment.

If a hook can delete data, publish externally, rotate credentials, or change production, it must not run without a clear authorization boundary.

## Testing a hook

Test both the event and the response:

1. Ordinary ASCII prose is allowed.
2. Each forbidden dash character is blocked in each prose extension.
3. Raw research is exempt.
4. Code and binary files do not trigger false blocks.
5. Codex patch parsing finds each affected file.
6. Cursor receives Cursor-shaped JSON.
7. Claude and Codex receive their supported hook output.
8. Component errors are visible but do not damage the edited file.

Never call a hook portable merely because its JavaScript file was copied. Portability includes manifest, event input, output schema, path resolution, trust, and a passing fixture.
