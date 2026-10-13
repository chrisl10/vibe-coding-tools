# xyflow Stinger

`xyflow-stinger` is the React Flow and Svelte Flow knowledge package for `xyflow-wasp-drone`. Both libraries come from the `xyflow/xyflow` monorepo and share the `@xyflow/system` core, so one Stinger covers them with a crosswalk for the places where React state and Svelte 5 runes diverge.

The root `SKILL.md` is intentionally lean. Detailed work lives here:

- `guides/` holds one procedure per major verb: scope, inspect, install and render, manage state, build nodes and edges, lay out, style, verify, migrate, refresh.
- `references/REFERENCE.md` holds decision tables, red flags, and escalation.
- `references/API-CROSSWALK.md` maps every captured React Flow name to its Svelte Flow counterpart.
- `references/CURRENT-XYFLOW.md` is the dated version and release snapshot.
- `references/research/raw/` archives one note per primary source; `references/research/distilled-xyflow.md` cites every claim to that archive and lists conflicts and gaps.
- `examples/` holds a typed React flow, a typed Svelte flow, a Dagre layout, save and restore with import validation, and migration diffs.
- `templates/` holds an inspection report, an architecture decision record, and a migration plan.
- `scripts/inspect-xyflow-project.py` performs a deterministic, read-only first pass over a project and emits JSON.

## Research posture

The release sweep covers 2026-03-23 through 2026-09-23. Documentation pages fetched at the cutoff are living baseline references. Current stable releases at the cutoff: `@xyflow/react` 12.11.6, `@xyflow/svelte` 1.6.6, `@xyflow/system` 0.0.82, all published 2026-09-01. Prereleases `@xyflow/svelte` 2.0.0-next and `@xyflow/system` 1.0.0-next appeared in August 2026 and are not treated as current.

Recorded conflicts include the two documented Tailwind v4 import orders, whether React Flow UI serves Svelte (unconfirmed), and differing attribution wording between the React and Svelte docs. Derived patterns (automatic re-layout, saved-flow validation, Svelte composition in place of React Flow UI) are labeled wherever they appear.

## Inspector

Run from the Stinger directory:

```text
python scripts/inspect-xyflow-project.py <project-root> --pretty
python scripts/inspect-xyflow-project.py --self-test --pretty
```

It performs no network requests, project commands, or writes. It skips `node_modules` and build output, parses `package.json` files, and applies regex heuristics to source files. Every heuristic finding names the distillation section it depends on; operational findings (unreadable file, invalid `package.json`, truncated scan, skipped symlinks) carry an empty `basis`.

## Validation

From the repository root:

```text
python src/skills/queen-wasp-stinger/references/scripts/per-type-validation.py packs/web-development-tools/skills/xyflow-stinger --type skill --harness all
python scripts/validate.py
```

The bar is zero validation errors, six-field portable frontmatter, no dynamic shell injection, no broken internal links, no unmarked mutable version claims, and no em or en dash characters in authored prose.

## Scope boundary

This Stinger owns the xyflow-specific layer. React architecture, Svelte runtime behavior, design systems, database persistence, and security or quality acceptance stay with their own Stingers, listed in `references/REFERENCE.md` section 6.
