# 05: Lay out graphs and build sub flows

## Choose the engine

Use [references/REFERENCE.md](../references/REFERENCE.md) section 3. Neither kit ships an auto-layout engine (D10). Prefer `@dagrejs/dagre` over the unscoped `dagre` (frozen since 2022). Before adding `elkjs`, surface its `EPL-2.0 OR GPL-3.0-or-later` license to the owner and record the decision (D10).

## Feed real sizes

Layout quality depends on actual node sizes (D10):

1. Read `node.measured?.width`/`height` (React Flow 12 and Svelte Flow 1.x); fall back to explicit `width`/`height` only when you set them.
2. Run layout after nodes are measured (for example from a toolbar action, or once every node has `measured`), not on the initial empty render.
3. Convert engine output to xyflow positions. Dagre returns node centers; subtract half the size for the default top-left origin (D10).
4. Write positions immutably, then fit the view.

[examples/03-dagre-auto-layout.md](../examples/03-dagre-auto-layout.md) implements this. The official example is a one-shot layout; automatic re-layout on every change is a **derived** design that needs an explicit trigger and debouncing (G2).

Engine notes: `d3-hierarchy` assumes uniform sizes and one root; `d3-force` iterates across renders and needs rectangular collision handling; ELK is asynchronous, so await it and guard against stale results when inputs change mid-layout (D10).

## Sub flows

1. Set the child's `parentId` to the parent's id; the child's `position` becomes relative to the parent's top-left (D10).
2. Order the array so every parent precedes its children (D10).
3. Add `extent: 'parent'` to keep a child inside the parent; the parent needs dimensions, and the child needs a valid `parentId` or the flow throws (D10).
4. Use the built-in `group` type for plain containers where it fits (D10).
5. Edges on parented nodes render above siblings by default; tune with `defaultEdgeOptions={{ zIndex: 1 }}` (D10).
6. When laying out, either lay out each group's children inside the group and size the group to fit, or exclude parented nodes from a top-level Dagre pass (Dagre is weak across sub-flow boundaries). ELK handles nested layouts natively (D10). The nested strategy you choose is a derived design; record it.

## Done when

Layout places nodes without overlap for mixed sizes, sub-flow children stay attached and ordered, and the chosen engine's license is recorded.
