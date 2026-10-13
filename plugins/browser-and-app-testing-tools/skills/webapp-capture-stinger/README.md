# Webapp Capture

Capture a scoped running app as screenshots, masked-frame demos, measured component inventories, candidate tokens, audits and a checked Claude Design handoff. Version 1.2 uses guarded requests, private outputs and explicit coverage.

Start with [SKILL.md](SKILL.md), then [Foundation](guides/00-foundation.md). The [reference](references/REFERENCE.md) maps every script and config field. A human handles real login; a seeded local account is preferred. No installed dependency or provider access is assumed.

| Need | Route |
| --- | --- |
| Screenshots, demo and script | [Demo guide](guides/01-demo-video-screenshots-script.md) |
| Observed components and tokens | [Inventory guide](guides/02-component-library-capture.md) |
| UI/source drift and bounded contrast | [Audit guide](guides/03-inconsistency-audit.md) |
| Component/theme migration map | [shadcn guide](guides/04-shadcn-map.md) |

The scripts produce measured evidence; describe/merge/theme decisions still need review. Rendered HTML is not original React/Svelte source. Masking protects selected pixels, not every unknown sensitive region. Incomplete coverage, unknown paint and missing inputs remain explicit gaps.
