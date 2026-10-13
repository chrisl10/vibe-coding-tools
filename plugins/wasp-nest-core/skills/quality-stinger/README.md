# quality-stinger

The skill that equips the `quality-wasp-drone` Drone to audit completed implementations against their source plan documentation. It encodes the canonical audit procedure (Locate plan -> Inventory changes -> Cross-reference -> Five-axis evaluation -> Severity classification -> Report) plus the findings-report template, the severity rubric, and a library of worked examples.

This Stinger is the final checkpoint in the `library-wasp-drone` (plan) -> implementer -> `security-wasp-drone` (security) -> `quality-wasp-drone` (QA) loop. It runs after `security-wasp-drone` and before work is marked done. See `SKILL.md` for the entry point and `guides/00-principles.md` for scope, ordering, and cross-Drone handoffs.

## Plans and report locations

Library Schema v2 uses `requirements/{backlog,in-work,completed}/prd-NNN-slug/prd-NNN-slug-index.md` and `issues/{backlog,in-work,completed}/ird-NNN-slug/ird-NNN-slug-index.md` under `library/`. PRD indexes can carry `-ck-<clickupId>` after `-index`; optional sub-PRDs stay beside the index.

Save a plan audit in that plan's `qa/` folder. Standalone audits use `library/requirements/reports/<domain>/`. Honor observed legacy plan names and report locations without moving existing evidence. See [Locate the plan](guides/01-locate-plan.md) and [Report writing](guides/06-report-writing.md).

The canonical [paired Drone](../../agents/quality-wasp-drone.md) lives in Core's src/agents tree. The builder projects it into the supported installed carriers.

## Verification artifact companion

[Bind verification to the exact candidate](guides/08-verification-artifacts.md), use the [packet template](templates/verification-artifacts.md) alongside the existing QA report, and inspect [constructed cases](examples/04-verification-artifact-cases.md). Current primary captures and claim limits are in [the research digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/quality-stinger/references/research/verification-artifacts/distillation.md).

## Current plugin owner

This capability stays in required Wasp Nest Core. Its canonical source is src/skills, with canonical ownership recorded in the root [plugin catalog](../../../plugin-catalog.json). Its SKILL.md metadata declares any standalone/orchestrator exception; specialist agents keep their actual paired Stinger. Host home/plugin files are generated carriers. Use [the layout and selection guide](../../../docs/PLUGIN-LAYOUT.md) when a workflow calls an optional specialist; source references alone do not enable an installed plugin.
