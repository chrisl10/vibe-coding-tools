# harness-integration-wasp-drone

**Plugin owner:** `wasp-nest-core`. **Required selection:** Core itself. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain
This Drone owns cross-harness capability integration for The Wasp Nest's four target harnesses (Claude Code, Cursor, ChatGPT Codex, Claude Cowork): where each component type (rules, commands, agents, skills, plugins) lives per harness, the wiring-mechanism decision (lifecycle hooks vs MCP server vs native extension vs plain instruction file), the hook/lifecycle event surface per harness and the real shared floor across them, MCP server registration per harness (including the Codex TOML trap and Cowork's cloud-reachability requirement), capability detection and graceful degradation when a harness lacks a feature, and cross-harness portability (the Agent Skills spec-six frontmatter, AGENTS.md as the shared rules baseline, plugin manifest differences). It also owns, as a fully preserved worked example, the Wasp Nestmind six-host case study (Claude Code, Codex, Cursor, Hermes, pi, OpenClaw) this Drone was originally built around, including the hivemind_search/read/index tool contract and the OpenClaw ClawHub bundle-scanner gate.

## Paired Stinger
[harness-integration-stinger](../../harness-integration-stinger) - the decision framework, per-harness placement/hook/MCP/portability guides, worked examples, and the Wasp Nestmind six-host case study.

## Worker coordination

Route "coordinate parallel AI workers with exclusive ownership" here. Load [the coordination guide](../../harness-integration-stinger/guides/07-coordinate-parallel-workers.md), verify the actual native dispatch/status/stop surface and capacity, and resolve AppPrimer Zero before using its existing handoff validator. Unknown runtime capability permits authorized serial preparation only. Keep planned, selected, observed and integrated proof separate.

## Availability, fallback and action boundaries

Route source coverage versus installed availability (O288), missing native-agent skill fallback (O289), installed-host release proof (O300) and personal-work carrier/action boundaries (O294) here. Load paired guides 08 through 11. Use explicit selected Core resolver results, then separate native discovery/execution and account/tool access receipts. No source file, UI install or role projection proves enabled dispatch. Direct skill preparation is serial when capacity is unknown, with independent-review losses disclosed. Personal drafts never imply authorization for a send, schedule or connector write. Domain content still belongs to its selected personal/Littlebird specialist.

## Task packs, hooks and selected command coverage

Route O287, O292 and O299 here. Load paired guides 12 through 14. Select actual component owners and active workflow prerequisites; require host/version/carrier payload, trust and execution receipts for hook claims; audit flat commands, host adapters, retained resources and native discovery separately. Standalone skills and command-only compositions remain legitimate without fabricated roles. Detection changes no registry or settings.

## Trigger phrases
- "wire this capability into Claude Code and Cursor"
- "add a hook event"
- "register an MCP server across harnesses"
- "audit a harness adapter"
- "will this skill work in Cowork"
- "what happens on a harness that doesn't support this"
- "fix capability detection in install"
- "the OpenClaw bundle fails ClawHub" (Hivemind case study)

## Do NOT route when
- The question is about vector-store schema, not the adapter that calls it; that belongs to vector-store-stinger.
- The question is about the embeddings runtime itself; that belongs to embeddings-runtime-stinger.
- The question is about MCP wire-protocol internals (JSON-RPC framing, zod schemas, transport) rather than registering the server in a harness; that belongs to mcp-protocol-wasp-drone.
- The question is about the build/release CI pipeline topology; that belongs to ci-release-wasp-drone.
- The question is about retrieval ranking internals or the login token vault security audit; those are out of this Drone's scope entirely.

## Inputs the Drone needs
- Which harness(es) are in scope (or "all four" for a contract-wide change).
- The scenario type: new component placement, hook event, MCP registration, capability-detection/degradation question, portability check, distribution audit, or a Hivemind case-study question specifically.
- The relevant source files or capability description (skill/agent/hook/MCP config being wired).

## Outputs
- A component-placement or wiring-mechanism recommendation, a hook entry, an MCP server stanza per harness, or a portability fix.
- A cross-harness contract-drift finding when a tool/hook change lands on only one harness without an explicit, classified degradation for the others.
- An audit report against the harness-adapter checklist.

## Commonly sequenced with
- mcp-protocol-wasp-drone: hands off MCP wire-protocol internals once registration is wired.
- vector-store-wasp-drone: owns the schema behind an MCP-backed memory tool's data layer.
- ci-release-wasp-drone: owns the build/release pipeline that ships the harness bundles.
