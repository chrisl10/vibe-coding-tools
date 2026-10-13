# Guide 04: Capability Detection and Graceful Degradation

**Sources:** `research/distilled-harness-integration.md` §4; `research/external/2026-08-14-skills-compat-capability-detection.md`; `research/external/2026-08-14-hookbridge-loss-report-pattern.md`; `research/external/2026-08-14-cross-host-compiler-degradation-model.md`; `research/external/2026-08-14-mcp-capability-negotiation.md`

---

## Current selected availability and fallback

For current Wasp Nest dispatch, use [selected-availability proof](08-prove-selected-availability.md), [direct skill fallback](09-use-skill-fallback.md) and [installed-host qualification](10-qualify-installed-host-release.md). These procedures supersede the historical static capability and unattended-remediation readings below. A filesystem probe proves presence only; native tools, network access, permission and capacity require current session evidence.

## Detect first, wire second

Before wiring a capability into a harness, decide whether that harness is even present and what it supports. Two working patterns, in order of preference:

### 1. Prefer a live capability signal over a hardcoded table

MCP's own handshake carries this information when the harness offers it: "Platform detection happens automatically via the MCP handshake (`clientInfo.name`)... if your agent platform supports self-reporting via `capabilities.experimental[...]` in the MCP initialize handshake, its capabilities are used directly and take priority over the static profile" (`research/external/2026-08-14-skills-compat-capability-detection.md`). Whenever a harness can self-report what it supports, trust that signal over an assumption baked into your integration ahead of time - harness capabilities change between releases, and a live signal stays correct without a code update.

### 2. Fall back to cheap, side-effect-free filesystem probing

When no live signal exists, detection should cost nothing and change nothing: check for the harness's home directory or config file, never write, never spawn a process. This is the one part of the old Hivemind-specific installer pattern that generalizes unchanged - see `examples/case-study-hivemind-six-host-installer.md` §2 for six concrete, working detection probes.

```typescript
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

function isHarnessInstalled(): boolean {
  return existsSync(join(homedir(), ".some-harness"));
}
```

A detection step that mutates state runs on every check and corrupts idempotency the moment two runs disagree about what's already wired. Keep detection and wiring as two separate steps.

---

## Historical static profiles are not current capability evidence

The August 2026 third-party scanner snapshot in `research/external/2026-08-14-skills-compat-capability-detection.md` is retained as historical research. Its static table and statement that Codex has no built-in web search must not control current dispatch. Inspect the actual session's exposed tools, permissions, version and selected resources. [Fresh official/source evidence](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/harness-integration-stinger/references/research/availability-proof/distilled-availability.md) supports separate skill, subagent and permission surfaces; it does not certify this session's network access or native role activation.

A home/config directory proves presence, not selection or successful discovery. MCP handshake fields describe a negotiated connection and declared capabilities, not every host-local skill, role, account permission or free worker slot.

---

## When a harness genuinely lacks a feature: classify the gap before deciding what to do

Two compatible vocabularies - pick whichever fits the moment the gap is discovered.

### Build-time / authoring-time gap

From two independent cross-host compiler projects (`research/external/2026-08-14-hookbridge-loss-report-pattern.md`, `research/external/2026-08-14-cross-host-compiler-degradation-model.md`):

| Outcome | Meaning |
|---|---|
| **Preserve** | The target harness has a close native equivalent - no loss |
| **Translate** | The harness has a *different* native surface that can express the same intent |
| **Degrade** | The harness can't express the full intent, but the workflow's user-facing meaning survives in a weaker form |
| **Drop** | Unsupported, and not worth emulating |

Worked example, straight from the research: a `commands`-shaped capability "compile[s] natively for Claude, Cursor, OpenCode; degrade[s] into skills plus instruction routing for Codex" - because Codex has no native commands surface at all (see `guides/01-component-placement.md`), the only faithful move is re-expressing the capability as a skill for Codex specifically, not skipping it or forcing a commands-shaped file Codex won't load.

### Run-time gap, discovered mid-session

From a working MCP-based capability scanner (`research/external/2026-08-14-skills-compat-capability-detection.md`): **OK** / **DEGRADED** / **BLOCKED**, surfaced to the agent as a structured delta before the capability's own instructions load, so the agent or user can decide how to proceed rather than the capability silently misbehaving:

```
Status: DEGRADED
Proceed with caution - optional deps missing
```

Use build-time classification when you're authoring or reviewing an integration ahead of shipping it; use the run-time three-state model when a capability needs to self-report a gap it discovers live, inside a session.

---

## Remediation classification does not authorize effects

A scanner's SAFE/MANUAL or agent_or_user/user_only label is advisory evidence, not task authority. Preserve the requested approach and scope. Installation, activation, configuration changes, sends, account access and spend require their own applicable user authorization and host permissions. Do not install a package merely because a scanner says SAFE. A permitted local draft or read-only check may proceed within existing authorization. Use [the personal-action sheet](../templates/personal-work-action-sheet.md) for exact target, payload, tool access and action-specific authority.

---

## Idempotency is part of graceful degradation

A capability that wires itself into a harness must converge on re-run, not accumulate duplicate entries or diverge from what's actually on disk. The patterns that generalize cleanly:

- **Marker blocks** in a plain-text instruction file (`AGENTS.md`-style): wrap injected content in begin/end markers, replace the block on re-run rather than appending.
- **Config keys** in a structured config file: upsert by key, never append a duplicate.
- **Config-file entries in a list** (hooks, servers): recognize a prior entry by a stable identifier (a bundle path, a name), filter it out, then re-add the current set - never blindly append.

See `examples/case-study-hivemind-six-host-installer.md` §2 for all three patterns worked concretely across six real installers.

---

*See also:* `guides/03-mcp-registration.md` for how capability negotiation works specifically for MCP servers, and `guides/05-portability-and-contracts.md` for the frontmatter/format choices that reduce how often you need to degrade at all.
