# xyflow decision reference

Load this for the decision tables behind the guides. Every row traces to [research/distilled-xyflow.md](research/distilled-xyflow.md), whose section numbers are given in brackets as `D<n>`. Rows marked **derived** combine documented primitives into a recommendation the sources do not state directly.

## 1. Which package

| Host project | Package | Notes |
|---|---|---|
| React 17 or newer, new work | `@xyflow/react` | Named export `ReactFlow`, import `@xyflow/react/dist/style.css` [D1, D3] |
| Existing `reactflow` 11 | Migrate to `@xyflow/react` | `reactflow` is frozen at 11.11.4; security support only "depending on severity" [D1, D9] |
| Existing `react-flow-renderer` (pre-11) | Migrate through 11 to `@xyflow/react` | npm-deprecated, "renamed to reactflow"; the v10 to v11 guide is not archived, so read it live [D1] |
| Svelte 5 (5.25 or newer) or SvelteKit on Svelte 5 | `@xyflow/svelte` 1.x | Svelte 4 is not supported by 1.x [D2, D3] |
| Svelte 4 project | Upgrade Svelte first, then Svelte Flow 1.x | 0.x uses the store API that 1.0 removed [D9] |
| Anything asking for `@xyflow/svelte@2.0.0-next` or `@xyflow/system@1.0.0-next` | Stop and ask | Unreleased prereleases observed 2026-08; no stable changelog yet [D2, G5] |
| Direct `@xyflow/system` dependency | Usually remove | Framework packages pin it exactly [D1]; a separately declared range could resolve a different version (**derived** concern) |

## 2. State model

| Situation | React Flow | Svelte Flow |
|---|---|---|
| Prototype or small flow | `useNodesState` / `useEdgesState` [D5] | `$state.raw` + `bind:nodes` / `bind:edges` [D5] |
| Production, nodes edit their own data | `useReactFlow().updateNodeData` or a Zustand store with immutable actions [D5] | `useSvelteFlow().updateNodeData` [D5] |
| Other UI (sidebar, toolbar) reads flow state | Wrap both in `ReactFlowProvider` [D6] | Wrap both in `SvelteFlowProvider` [D6] |
| Two flows on one page | One provider per flow [D6] | One provider per flow [D6] |
| State must survive route changes | Provider outside the router [D6] | Provider outside the router [D6] |
| App already has a global store | Keep nodes and edges there; wire `onNodesChange`/`onEdgesChange`/`onConnect` to store actions [D5] | Function bindings with getter and setter [D5] |
| Derived value (selected ids, counts) | Narrow selector, never the whole `nodes` array [D13] | `$derived` from `.current` of a narrow hook (**derived**) |

Rules that apply to both: never mutate a node or edge in place; replace the object and its nested `data` or `position` [D5]. `useStore` is a last resort [D6].

## 3. Layout engine

| Need | Engine | Watch for |
|---|---|---|
| Directed graph, quick result | `@dagrejs/dagre` (maintained; not unscoped `dagre`) | Weak with sub flows that connect outside the sub flow [D10] |
| Single-root tree, uniform nodes | `d3-hierarchy` | Treats every node as the same size [D10] |
| Organic, non-hierarchical | `d3-force` | Iterative across renders; rectangular collision needs custom code [D10] |
| Nested sub flows, ports, edge routing, variable sizes | `elkjs` | Async; license `EPL-2.0 OR GPL-3.0-or-later`, so route the license decision to the owner before adding it [D10] |
| Edges must avoid nodes | `react-flow-smart-edge` or `libavoid-js` | Named in the React docs only [D10] |

Every engine needs measured sizes. Lay out after nodes have `measured` dimensions, or give nodes explicit `width`/`height` [D10, D12]. Official examples show a one-shot layout; a re-layout loop is **derived** [D10, G2].

## 4. Styling path

| Situation | Choice |
|---|---|
| Default look, light tweaks | `style.css` plus `--xy-*` variable overrides [D11] |
| Fully custom design system | `base.css` plus your own styles; never drop base styles [D3, D11] |
| Tailwind v4 with React Flow UI | `@import "tailwindcss";` then the xyflow stylesheet in a global CSS file [D11, C1] |
| Tailwind v4, utilities must beat library defaults | `@import '@xyflow/*/dist/style.css' layer(base);` [D11, C1] |
| Dark mode | `colorMode` `light`, `dark`, or `system`; Svelte adds `colorModeSSR` [D8] |
| Prebuilt React components | React Flow UI through the shadcn CLI; needs shadcn/ui and Tailwind; built on React 19 [D11, C4] |
| Prebuilt Svelte components | None confirmed; compose with shadcn-svelte manually (**derived**) [C2] |

## 5. Red flags

| Symptom or code smell | Cause | Fix | Source |
|---|---|---|---|
| Blank canvas | Parent has no height, or stylesheet missing | Size the container; import the stylesheet | D3 |
| Edges missing | Stylesheet missing, no handles, handle hidden with `display: none`, stale internals | Import CSS; add `Handle`; use `visibility: hidden`; call `useUpdateNodeInternals` | D7 |
| Custom nodes re-render needlessly, or Svelte warns about new `nodeTypes` | `nodeTypes`/`edgeTypes` created inside the component | Hoist to module scope or memoize | D7 |
| Node renders as default | `type` string does not match a `nodeTypes` key | Match keys exactly | D7 |
| Drag starts when typing in a node input | Missing `nodrag` | Add `nodrag` (and `nowheel` for scrollers) | D7 |
| Updates silently ignored | In-place mutation | Replace objects immutably | D5 |
| Svelte flow sluggish | `$state` instead of `$state.raw` | Use `$state.raw` | D5 |
| "Could not find a Svelte Flow context" / hook fails outside flow | Hook used outside provider | Add provider | D6 |
| Child node lands in the wrong place | Parent after child in the array, or `parentNode` used | Order parents first; use `parentId` | D10 |
| `extent: 'parent'` error | Node lacks a valid `parentId` | Set `parentId` | D10 |
| Layout overlaps | Layout ran before measurement | Wait for `measured`, or set sizes | D10 |
| `useHandleConnections` in new code | Deprecated hook | `useNodeConnections` with `handleType`/`handleId` | D6 |
| Svelte event prop ignored | React-style `onNodeClick` or legacy `on:` | Lowercase `onnodeclick` | D8 |
| Next.js server error from the flow | Flow rendered as a server component | Render inside a `"use client"` boundary | D12 |
| SSR edges missing | No handle positions on the server | Provide node `handles` and sizes | D12 |
| Tests show zero edges | jsdom lacks layout APIs | Mock the four APIs and `waitFor` edges | D13 |
| `hideAttribution: true` | Policy decision | Surface the documented terms to the owner | D14 |

## 6. Escalation

| Concern | Hand to |
|---|---|
| React component architecture, Server Components, general state strategy | `react-wasp-drone` |
| Svelte 5 runes, SvelteKit load functions, form actions | `svelte-wasp-drone` |
| Design tokens, visual design of nodes and panels | `impeccable-wasp-drone`, `ux-ui-wasp-drone`, `ux-ui-svelte-wasp-drone` |
| shadcn-svelte installs and theming | `shadcn-svelte-wasp-drone` |
| Tailwind v4 mechanics beyond the xyflow import | `tailwind-wasp-drone` |
| Persisting flows to a database, schema for saved graphs | `db-wasp-drone` or `neon-drizzle-wasp-drone` |
| Browser end-to-end tests of drag and connect | `browser-automation-wasp-drone` |
| Dependency advisories, license review of elkjs | `dependency-audit-wasp-drone`, then the owner |
| Security review (user-authored node content, saved graph import) | `security-wasp-drone` |
