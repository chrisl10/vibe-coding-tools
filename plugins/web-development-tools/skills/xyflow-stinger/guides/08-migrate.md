# 08: Migrate between xyflow generations

## Plan first

1. Inspect ([01-inspect-and-align.md](01-inspect-and-align.md)) and fill [templates/migration-plan.md](../templates/migration-plan.md).
2. Re-read the live migration guide for the exact source version; the archived React guide says it is not exhaustive, and the Svelte archive captures only its main changes (D9).
3. Migrate in slices, each ending with a type check and a manual interaction pass. Do not delete compatibility code until behavior is proven.

## React Flow 10 (`react-flow-renderer`)

The package is npm-deprecated as "renamed to reactflow" (D1). Migrate to 11 with the live v11 guide (not archived), then continue below.

## React Flow 11 to 12

1. Swap `reactflow` for `@xyflow/react`; switch default import to named `{ ReactFlow }`; update the stylesheet path (D9).
2. Replace reads of `node.width`/`height` for rendered size with `node.measured?.width`/`height`; keep `width`/`height` only as intentional sizing (D9).
3. Rename `parentNode` to `parentId`, `xPos`/`yPos` to `positionAbsoluteX`/`positionAbsoluteY`, and the reconnection API (`onReconnect`, `reconnectEdge`, `reconnectRadius`, `reconnectable`) (D9).
4. Replace the removed helpers (`getTransformForBounds`, `getRectOfNodes`, `project`, `getMarkerEndId`, `updateEdge`) using the replacements named in the live migration guide; the archive records the removals, not every replacement. Current candidates in the documented API are `screenToFlowPosition` for coordinate conversion and `getNodesBounds` (now `getNodesBounds(nodes, { nodeOrigin })`) for bounds; confirm before substituting (D9, D6).
5. Remove every in-place mutation (D9).
6. Replace `useHandleConnections` with `useNodeConnections` (D6).
7. Remove `reactflow` from the manifest once nothing imports it; two generations must not coexist (D1).

The search command and diffs are in [examples/05-migrations.md](../examples/05-migrations.md).

## Svelte Flow 0.x to 1.x

1. Upgrade to Svelte 5 first (with `svelte-wasp-drone` if the app is large) (D9).
2. Replace `writable` nodes and edges with `$state.raw`, props with `bind:nodes bind:edges`, and `export let` node props with `$props()` (D9).
3. Replace store reads with `.current` hook results (D9).
4. Rename `onEdgeCreate` to `onbeforeconnect`, `<EdgeLabelRenderer>` to `<EdgeLabel x y>`, slot connection lines to `connectionLineComponent`, and `on:` events to lowercase attributes (D8, D9).
5. Replace in-place mutation with reassignment or `updateNode` (D9).
6. Review new defaults you now get (keyboard accessibility, elevation on select) against the product's expectations (D9).

## Svelte Flow 2.0 and xyflow system 1.0

Prereleases exist (2026-08) with no stable changelog (D2, G5). Do not migrate to them unless the owner asks; then run a fresh research sweep ([09-refresh-current-xyflow.md](09-refresh-current-xyflow.md)) before planning.
