# ChrisL Forged

Locally forged specialist Drone+Stinger pairs: desk additions forged on the 2.x tree and ported into the version 3 plugin layout.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## What ships

Seven locally forged pairs. Each Stinger is the paired Drone's operating manual; each Drone reads its Stinger before touching anything.

| Drone | Stinger | What it does |
| --- | --- | --- |
| [before-after-wasp-drone](agents/before-after-wasp-drone.md) | [before-after-stinger](skills/before-after-stinger/SKILL.md) | PR-ready before and after screenshot pairs via the @vercel/before-and-after CLI, uploaded and appended to the pull request. |
| [code-structure-wasp-drone](agents/code-structure-wasp-drone.md) | [code-structure-stinger](skills/code-structure-stinger/SKILL.md) | Two-layer architecture discipline: actions orchestrate domain rules, services centralize reusable operational mechanics. |
| [evidence-testing-wasp-drone](agents/evidence-testing-wasp-drone.md) | [evidence-testing-stinger](skills/evidence-testing-stinger/SKILL.md) | Records verifiable proof a change works: annotated recordings, screenshot-and-probe sequences, or measured before and after numbers. |
| [unslop-wasp-drone](agents/unslop-wasp-drone.md) | [unslop-stinger](skills/unslop-stinger/SKILL.md) | Cuts AI tells from human-read prose and adds human voice against a 31-pattern catalog. |
| [effect-wasp-drone](agents/effect-wasp-drone.md) | [effect-stinger](skills/effect-stinger/SKILL.md) | Effect-TS v4 implementation, v3-to-v4 migration, and conformance review grounded in the official v4 docs. |
| [production-release-wasp-drone](agents/production-release-wasp-drone.md) | [production-release-stinger](skills/production-release-stinger/SKILL.md) | Executes the complete production release at the project's tier, from authorization to verified-shipped. |
| [production-release-build-wasp-drone](agents/production-release-build-wasp-drone.md) | [production-release-build-stinger](skills/production-release-build-stinger/SKILL.md) | Audits CI-to-deploy posture, classifies it on the tier ladder, and installs or upgrades the right release flow. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first.

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install chrisl-forged@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector.

```text
Use unslop-stinger to cut AI tells from this PR body and keep every technical fact.
```

Expected result: specialist output from the paired Stinger's procedure, with its research archive cited where claims depend on it.

## Dispatch guides

Pest Controller dispatch guides for these Drones live in [references/pest-controller-guides/](references/pest-controller-guides/). The roster in Core's `pest-controller-suit` routes to them; confirm this pack is installed before dispatch.

## Prerequisites and boundaries

- Executing or installing release flows touches live repositories and platforms: `production-release-wasp-drone` and `production-release-build-wasp-drone` act only on owner-authorized instructions.
- `before-after-stinger` needs Node and the `@vercel/before-and-after` CLI; `evidence-testing-stinger` needs a recorder or a scriptable browser for its live paths.
- Core supplies shared routing and review methods. Read the linked Stinger before work. Missing tool, browser, or account access is a reported gap.
<!-- wasp-pack-guide:end -->
