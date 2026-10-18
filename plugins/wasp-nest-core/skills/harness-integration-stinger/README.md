# harness-integration-stinger

The cross-harness capability integration playbook for `harness-integration-wasp-drone`. Covers wiring one capability across The Wasp Nest's four harnesses (Claude Code, Cursor, ChatGPT Codex, Claude Cowork) - per-harness component placement, the wiring-mechanism decision (hooks, MCP, native extension, plain instruction file), hook/lifecycle events per harness, MCP registration per harness, capability detection and graceful degradation, and cross-harness portability (spec-six skill frontmatter, AGENTS.md baseline, plugin manifest differences) - with research-backed, opinionated guidance on the top integration failure modes. Includes a fully preserved worked case study of a real six-host integration (Hivemind: Claude Code, Codex, Cursor, Hermes, pi, OpenClaw), the product this stinger was originally built around.

## Start here

- [Select task packs](guides/12-select-task-packs.md), [prove hook contracts](guides/13-prove-hook-contract.md) and [audit selected commands](guides/14-audit-selected-command-coverage.md) cover O287, O292 and O299 with reusable receipts and source cases.

- [Prove selected availability](guides/08-prove-selected-availability.md), with source/selection/native/access receipts.
- [Use direct skill fallback](guides/09-use-skill-fallback.md), preserving constraints and reporting independent-review loss.
- [Qualify installed-host release claims](guides/10-qualify-installed-host-release.md), with a four-host receipt matrix.
- [Prepare personal work](guides/11-prepare-personal-work.md), with scoped sources, draft-only artifacts and action-specific authority.
- Fresh availability research, topic locks and raw source hashes.

Read [the Drone identity](../../agents/harness-integration-wasp-drone.md) and [its routing guide](../pest-controller-suit/guides/harness-integration-wasp-drone.md) for scope and handoffs.

- [Coordinate parallel workers](guides/07-coordinate-parallel-workers.md) adds live capacity, exclusive ownership and stop/handoff evidence using the selected AppPrimer Zero helper.
- [Component placement](guides/01-component-placement.md) maps the host surfaces.
- [Wiring mechanism](guides/00-decision-framework.md) chooses the integration boundary.
- [Portability and contracts](guides/05-portability-and-contracts.md) separates shared content from host-specific adapters.
- [Six-host case study](examples/case-study-hivemind-six-host-installer.md) preserves the original worked example.

## Source and installed locations

Harness Integration stays in required Core. Its canonical source is src/skills/harness-integration-stinger, with the paired Drone in src/agents.
The root plugin-catalog.json assigns ownership; the source builder produces host projections. Installed Core has its own skill/agent directories and an explicit selected-plugin resolver. Do not edit an installed cache as canonical source or treat a cached optional plugin as enabled.
