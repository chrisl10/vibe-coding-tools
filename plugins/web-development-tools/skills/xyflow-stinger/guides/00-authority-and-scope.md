# 00: Establish authority and scope

Read this first on every task. It decides what you may touch and which facts you may state.

## Before planning

1. Read the repository's instructions (`AGENTS.md`, `CLAUDE.md`), the authorizing PRD, IRD, or task, its acceptance criteria, and any accepted contract (`CTR-###`) the flow depends on.
2. Record the exact paths you own. Other agents may be working in the same repository; never edit, move, or delete files outside your assignment.
3. Identify the kit (React Flow, Svelte Flow, or both) and the host framework (React, Next.js, Svelte, SvelteKit). If the task names neither and the code does not settle it, ask.
4. Note external effects the task might imply (installing packages, publishing, paid Pro content). Installing dependencies changes the lockfile: say so in the plan and get approval where the repository requires it.

## What counts as a fact

- Domain facts come from [references/research/distilled-xyflow.md](../references/research/distilled-xyflow.md), which cites a raw source for every row. Cite the section (`D5`, `D10`) in plans and reports.
- Versions are dated observations (see [references/CURRENT-XYFLOW.md](../references/CURRENT-XYFLOW.md)). Before saying "latest" or bumping a dependency, run [09-refresh-current-xyflow.md](09-refresh-current-xyflow.md).
- Patterns marked **derived** (auto re-layout loops, import validation, Svelte composition of shadcn-svelte in place of React Flow UI) are application designs built from documented primitives. Label them as such in code comments and reports.
- Where the distillation lists a conflict (C1 to C6) or gap (G1 to G7), state it rather than picking silently.

## Scope boundary

This Stinger owns xyflow-specific work: canvas setup, flow state wiring, custom nodes, edges, and handles, connection rules, layout-engine integration, sub flows, theming of the canvas, React Flow UI adoption, SSR of the flow, canvas performance, accessibility, tests, and xyflow migrations. Hand off general React architecture, Svelte runes and SvelteKit internals, design systems, database persistence, and security acceptance to the peers listed in [references/REFERENCE.md](../references/REFERENCE.md) section 6.

## Attribution and licensing

`proOptions.hideAttribution` is governed by documented terms that differ in wording between the React and Svelte docs (D14, C5). Never enable or remove it on your own judgment; surface the documented position to the owner. Treat an `elkjs` addition as a license decision for the owner (`EPL-2.0 OR GPL-3.0-or-later`, D10).
