# ux-ui-svelte-stinger

The Svelte 5 + SvelteKit UI enforcement and implementation skill. Owns the
shadcn-svelte 1.x + Tailwind v4 standard for a SvelteKit project, including the
`@theme` token bridge to the project's design tokens and any brand or
white-label contract preservation. It applies the project's own UI decision
record when one exists. The guides use OSPRY (ADR-007, PRD-071 tokens, and the
`apps/portal`, `apps/web` and `apps/wl` apps) as the worked example.

## Why this skill exists

SvelteKit apps drift into bespoke `<style>` blocks and ad-hoc button and control
classes scattered across routes. A UI standard of shadcn-svelte plus Tailwind v4,
rolled out in phases, fixes that, and this skill is the procedural arsenal that
enforces and implements it. In OSPRY the starting point was 199 `.svelte` files
in the portal alone, 66 with bespoke `<style>` blocks, and ADR-007 adopted the
standard.

## Source documents

- **Decision:** the project's UI decision record (OSPRY example: `library/knowledge/private/architecture/ADR-007-shadcn-svelte-and-tailwind-v4-as-ui-standard.md` in the OSPRY repository)
- **Research manifest:** [`research/research-summary.md`](research/research-summary.md)
- **Existing token system:** the project's token files (OSPRY example: `apps/portal/src/lib/styles/{tokens,brand,base,shell}.css`)

## Structure

```
ux-ui-svelte-stinger/
├── SKILL.md                       # the index + when-to-use (read first)
├── guides/                        # the procedural instruction set
│   ├── 00-principles.md
│   ├── 01-installation-phase-0.md
│   ├── 02-token-bridge.md         # the load-bearing guide
│   ├── 03-component-anatomy.md
│   ├── 04-dark-mode-inversion.md
│   ├── 05-white-label-preservation.md
│   ├── 06-surface-migration.md
│   └── 07-violations-and-guardrails.md
├── examples/                      # worked before/after
│   ├── phase-0-app-css.md
│   └── button-surface-migration.md
├── templates/                     # fill-in stubs
│   ├── phase-0-done-checklist.md
│   └── ui-review-output.md
├── reports/                       # past review runs (audit trail)
└── research/                      # raw primary-source dumps (READ-ONLY)
```

## Paired Drone

`ux-ui-svelte-wasp-drone` (at `packs/web-development-tools/agents/ux-ui-svelte-wasp-drone.md`) wields
this Stinger. The Drone is the persona + guardrails; this Stinger is the
procedural arsenal.

## Maintenance

Researched against the versions in `research/library-versions.md` (source-repository research, not shipped with the plugin). When a major
version of shadcn-svelte, Tailwind, or Bits UI ships:

1. Write a fresh `research/YYYY-MM-DD-<library>-vX-migration.md` (source-repository research, not shipped with the plugin) note.
2. Update the affected guide(s).
3. Update `research/library-versions.md` (source-repository research, not shipped with the plugin).
