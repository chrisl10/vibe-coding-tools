# Queen Wasp Stinger

The forge of The Wasp Nest. This skill creates every other component of the Wasp Nest agentic development system: rules, plugins, commands (Pest Controller Tools), agents (Drones), and skills (Stingers), across the four supported harnesses: Claude Code, Cursor, ChatGPT Codex, and Claude Cowork.

It replaces two earlier tools: Anthropic's original skill-creator and the Wasp Nest's stinger-forge. Where those were single-harness and research-thin, this one is grounded in a dedicated research corpus and covers all five component types on all four harnesses.

## Why it exists

Harnesses move fast and their docs disagree with each other, with community writeups, and sometimes with themselves. Authoring a component from memory produces spec drift: skills that fail Cowork upload, rules Cursor silently ignores, MCP configs Codex never loads. This skill pins every authoring decision to downloaded primary sources so the components it forges actually load where they're supposed to.

## Structure

```
queen-wasp-stinger/
├── SKILL.md                      The forge workflow and hard portability rules
├── README.md                     This file
├── guides/
│   ├── the-hive-architecture.md              System model, pairing law, Ship Gate
│   ├── pest-controller-registration.md             Registering new Drone and Stinger pairs
│   ├── vibe-coding-tools-reference-update.md Keeping repo references in sync
│   ├── harness-support-matrix.md             What each harness supports, at a glance
│   └── per-type-per-harness-specific-guide.md  Deep authoring procedures, all 20 combos
└── references/
    ├── research/
    │   ├── distilled-research-articles.md    Cited digest of all research
    │   ├── distilled-<harness>.md            Per-harness digests
    │   └── raw/                              59 archived primary sources (source repository only, not shipped)
    ├── scripts/
    │   ├── per-type-validation.py            Validate any component per harness
    │   ├── cowork-skill-packager.py          Validate and zip .skill for Cowork
    │   └── cowork-plugin-packager.py         Validate and zip plugins for Cowork
    └── templates/
        ├── skills/      Reference SKILL.md template + harness field reference
        ├── agents/      Wasp Nest Drone template + harness field reference
        ├── rules/       Reference .mdc template + harness field reference
        ├── commands/    Wasp Nest command template + harness field reference
        └── plugins/     Working plugin skeleton + harness field reference
```

## Quick start

Ask the orchestrator to forge a component and name the target harnesses. Examples:

- "Forge a new stinger for Postgres migration safety, all four harnesses"
- "Build a Drone and Stinger pair for API contract testing, register them with the pest-controller"
- "Turn this checklist into a Cursor rule and a matching CLAUDE.md section"
- "Package the marketing plugin for Cowork and tell me what breaks"

The skill walks the forge workflow: intent, support matrix, per-type guide, template, conventions, validation, registration.

## Provenance

Research window 2026-02-14 to 2026-08-14. 289 sources reviewed, 59 raw documents archived under `references/research/raw/` (source-repository research, not shipped with the plugin), every distilled claim cited back to its source file. Known conflicts between sources are flagged in the guides rather than silently resolved.

## Wasp Nest v3 source and placement

Required Core owns Queen. Canonical components live in src or the selected `packs/<plugin-id>` source root; the root plugin-catalog.json records each owner and prerequisites. Generated home trees, caches and plugin projections are consumption outputs. Registration includes updating that source catalog and validating the selected owner; it does not imply installation, registry writes, publication or push.

For the current projection, see [the layout guide](../../learn/reference/PLUGIN-LAYOUT.md). The dated research provenance above remains the original archive, not a claim that every host-format field is freshly verified.

## Wasp Nest placement

Orchestrator level. No paired Drone. The other core skills at this level are `pest-controller-suit` and `get-started-stinger`. Specialist Drones and Stingers pair; direct-use skills must declare `metadata.hive-tier: standalone` so the validator can distinguish intent from a missing agent.

Part of The Wasp Nest, curated by [Mario Aldayuz a.k.a @thenotoriousllama](https://github.com/thenotoriousllama).

## Distribution upgrades and capability overlap

Use [the lifecycle and overlap guide](guides/plugin-lifecycle-and-overlap.md) to stage exact artifact upgrades and compare competing triggers before creating another pair. Its dated primary-source digest, upgrade record, overlap worksheet and eight explicitly unexecuted cases preserve source, generated and installed evidence boundaries. Existing validators and Harness Integration supply the checks.
