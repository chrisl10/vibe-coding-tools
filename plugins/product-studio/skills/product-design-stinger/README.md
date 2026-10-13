# Product design stinger

Turns a Product Strategy into a complete UX package: journeys, information architecture, Mermaid task flows, screen specs with every state, content and voice, a WCAG 2.2 AA baseline, and clickable single-file HTML prototypes in light and dark. It critiques its own work against a seven-part rubric and Impeccable's detector before the owner sees it, and it runs the Claude Design round trip in both directions: a brief out, an import with provenance back in.

Part of the `product-studio` pack, between `product-strategy-stinger` (input) and `product-planning-stinger` (output). Paired Drone: `product-design-wasp-drone`.

## Guide map

| Verb | Guide | Output |
|---|---|---|
| Read the strategy, propose directions, get Gate A | [01](guides/01-read-strategy-and-set-direction.md) | `design/README.md`, `design/direction.md` |
| Map journeys and IA | [02](guides/02-map-journeys-and-ia.md) | `design/journeys/`, `design/information-architecture.md` |
| Write task flows | [03](guides/03-write-task-flows.md) | `design/flows/` |
| Specify screens and states | [04](guides/04-spec-screens-and-states.md) | `design/screens/` |
| Write content and the accessibility baseline | [05](guides/05-write-content-and-accessibility.md) | `design/content-voice.md`, `design/accessibility-baseline.md` |
| Build prototypes | [06](guides/06-build-prototypes.md) | `design/prototypes/` |
| Critique, run gates, get Gate B | [07](guides/07-critique-and-gate.md) | `design/critique/` |
| Hand off to Claude Design | [08](guides/08-hand-off-to-claude-design.md) | `design/claude-design/brief.md` |
| Import a Claude Design export | [09](guides/09-import-claude-design-export.md) | `design/claude-design/imports/<id>/` |
| Hand off to planning, design system, enforcement | [10](guides/10-hand-off-to-owners.md) | `design/planning-handoff.md` |

`design/` means `library/knowledge/private/product/design/` in the host repository. The full tree and ID scheme are in [package-layout.md](references/package-layout.md).

## Templates

[journey map](references/templates/journey-map.md), [IA and screen map](references/templates/ia-screen-map.md), [task flow](references/templates/task-flow.md), [screen spec](references/templates/screen-spec.md), [direction options](references/templates/direction-options.md), [content and voice](references/templates/content-voice.md), [accessibility baseline](references/templates/accessibility-baseline.md), [critique rubric](references/templates/critique-rubric.md), [Claude Design brief](references/templates/claude-design-brief.md), [Claude Design import checklist](references/templates/claude-design-import-checklist.md), [prototype starter HTML](references/templates/prototype-starter.html), [package README](references/templates/design-package-readme.md), [planning handoff](references/templates/planning-handoff.md).

## Script

`scripts/check-design-package.py` (Python 3.9+, stdlib only):

- `package <design-dir>`: required files, four states per screen spec, accessible Mermaid per flow, prototype rules (lang, viewport, tokens, light and dark, reduced motion, focus, no network), no em or en dashes. Exit 0 clean, 2 findings.
- `inventory <path> --out inventory.json`: sizes and SHA-256 for a Claude Design export, zip members listed without extraction, unsafe members flagged. Exit 0 clean, 2 unsafe.

## Research

[Distilled article](references/research/distilled-product-design.md) with 24 dated raw sources in [references/research/raw/](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw) and hashes in [source-ledger.json](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/source-ledger.json). Claude Design export internals (the .zip layout and the Claude Code handoff bundle) are not documented by Anthropic as of 2026-10-12; the distillation says exactly what is confirmed, what is secondary, and what is unknown.

## Related owners

| Need | Owner |
|---|---|
| Product strategy (input) | `product-strategy-stinger` |
| PRD map and wave plan (consumer) | `product-planning-stinger` |
| Build a design system from scratch | `design-system-stinger` |
| Enforce an existing system in code | `ux-ui-stinger` (React), `ux-ui-svelte-stinger` (SvelteKit) |
| Implement or polish live UI, detector gate, DESIGN.md capture | `impeccable-stinger` |
| Capture a running app and its Claude Design handoff zip | `webapp-capture-stinger` (browser-and-app-testing-tools) |
| Interviews to validate journey assumptions | `discovery-research-stinger` |

Resolve optional owners through Core's selected-plugin resolver before dispatch. A missing optional owner blocks only that handoff, not the package.

## Host support

Claude Code and Cowork use the plugin's skill and agent; Cursor uses the projected agent in `cursor-agents/`; Codex uses the generated role and skill. Without delegation, read the Drone file and run this skill directly. Browser screenshots and the Impeccable detector are used when available and reported as unavailable otherwise.
