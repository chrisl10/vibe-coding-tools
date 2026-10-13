# xyflow inspection report: {project}

- Date: {YYYY-MM-DD}
- Inspector: `scripts/inspect-xyflow-project.py` (schema {n}), plus manual review
- Scope: {paths inspected}
- Knowledge cutoff used: `references/CURRENT-XYFLOW.md` dated {date}, refreshed {yes or no}

## Stack

| Item | Value |
|---|---|
| Kit | React Flow / Svelte Flow / both |
| xyflow package and range | {e.g. @xyflow/react ^12.11.0} |
| Framework and version | {React 19, Next.js 15 App Router / Svelte 5.x, SvelteKit 2} |
| Legacy packages present | {none or list} |
| Layout engine | {none, @dagrejs/dagre, elkjs, d3-hierarchy, d3-force} |
| Styling | {style.css or base.css; Tailwind version and import order} |
| State model | {useState, useNodesState, Zustand, $state.raw + bind, external store} |
| SSR | {none, Next.js client boundary, SvelteKit SSR with sizes and handles} |

## Findings

| Severity | Code | Path | Finding | Action |
|---|---|---|---|---|
| {error, warn, manual, info} | {inspector code or manual} | {path} | {what} | {fix or owner} |

## Manual-review boundaries

- Attribution: {hideAttribution present? documented terms surfaced to owner?}
- Licenses: {elkjs or other copyleft dependencies?}
- Untrusted input: {saved-flow import, user-authored node content rendered as HTML?}

## Next step

{bounded plan, or the peer Drone this goes to}
