# Current xyflow snapshot (dated 2026-09-23)

Every value here is an observation on 2026-09-23, not a default. Before changing a dependency or stating "latest", refresh with [../guides/09-refresh-current-xyflow.md](../guides/09-refresh-current-xyflow.md). Sources: [research/distilled-xyflow.md](research/distilled-xyflow.md) sections D2, D10, D14.

## Stable packages

| Package | Version | Published | Peers |
|---|---|---|---|
| `@xyflow/react` | 12.11.6 | 2026-09-01 | `react >=17`, `react-dom >=17`; optional `@types/react`, `@types/react-dom` |
| `@xyflow/svelte` | 1.6.6 | 2026-09-01 | `svelte ^5.25.0` |
| `@xyflow/system` | 0.0.82 | 2026-09-01 | none; pinned exactly by both framework packages |
| `reactflow` (legacy) | 11.11.4 | 2024-06-20 | legacy React Flow 11; migrate |

## Prereleases (do not adopt without a decision)

| Package | Tags | Published |
|---|---|---|
| `@xyflow/svelte` | 2.0.0-next.0 to next.3 | 2026-08-12 to 2026-08-19 |
| `@xyflow/system` | 1.0.0-next.0 to next.3 | 2026-08-11 to 2026-08-19 |

The 1.6.x Svelte line kept receiving patches after these tags. No stable changelog describes the 2.0 changes yet.

## In-window release notes (2026-03-23 to 2026-09-23)

| Date | React | Svelte | System | Notable |
|---|---|---|---|---|
| 2026-03-27 | 12.10.2 | 1.5.2 | 0.0.76 | `BuiltInNode` may omit `type`; viewport helper options passed correctly |
| 2026-06-01 | 12.11.0 | 1.6.0 | 0.0.77 | `autoPanOnSelection`; React optional `@types` peers; Svelte aria label on node elements and SSR `window` guard; touch selection fix |
| 2026-06-22 | 12.11.1 | 1.6.1 | 0.0.78 | fixes |
| 2026-07-06 | 12.11.2 | 1.6.2 | 0.0.79 | dark-mode background pattern fix; zoom pane extent cached (listed in Svelte notes) |
| 2026-08-12 | 12.11.3 | 1.6.3 | 0.0.80 | panning fixes; `extent: 'parent'` resolution; Svelte ESM and TypeScript import fixes |
| 2026-08-25 | 12.11.4, 12.11.5 | 1.6.4, 1.6.5 | 0.0.81 | development-mode log when attribution is hidden |
| 2026-09-01 | 12.11.6 | 1.6.6 | 0.0.82 | attribution warning skipped when the pane is not rendered; provider store reset on unmount; edges hidden with hidden nodes |

No breaking changes, removed APIs, or security advisories in the window.

## Layout libraries

| Package | Version | Published | License |
|---|---|---|---|
| `@dagrejs/dagre` | 3.1.1 | 2026-08-08 | MIT |
| `dagre` (legacy) | 0.8.5 | 2019-12-03 | MIT |
| `elkjs` | 0.12.0 | 2026-07-17 | EPL-2.0 OR GPL-3.0-or-later |
| `d3-hierarchy` | 3.1.2 | 2022-04-02 | ISC |
| `d3-force` | 3.0.0 | 2021-06-05 | ISC |

## Commercial facts (mutable)

Pro tiers seen on reactflow.dev at fetch time: Starter $169/month, Professional $289/month, Enterprise custom. Svelte Flow Pro and the integrated Pro Platform launched 2026-06-15. Never quote these prices as current without refreshing.
