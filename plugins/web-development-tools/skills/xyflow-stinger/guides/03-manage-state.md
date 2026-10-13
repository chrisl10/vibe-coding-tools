# 03: Manage flow state

The reactivity layer is where React Flow and Svelte Flow differ most. Use [references/API-CROSSWALK.md](../references/API-CROSSWALK.md) for names and [references/REFERENCE.md](../references/REFERENCE.md) section 2 to pick a model.

## Invariants for both kits

1. Nodes and edges are immutable. Replace the node object and any nested `data` or `position` object you change (D5). In-place mutation is silently ignored.
2. Keep `nodeTypes` and `edgeTypes` stable (D7).
3. Use dedicated hooks before `useStore` (D6).
4. Hooks used outside the flow component need a provider; each flow gets its own; put it outside the router to keep state across routes (D6).
5. Persist explicitly with `toObject()` or your own nodes and edges state (D5); validate anything restored ([examples/04-save-and-restore.md](../examples/04-save-and-restore.md)).

## React Flow

- Controlled flow: hold `nodes` and `edges` in state; wire `onNodesChange` to `applyNodeChanges`, `onEdgesChange` to `applyEdgeChanges`, `onConnect` to `addEdge`; wrap handlers in `useCallback` with functional setters (D5).
- `useNodesState`/`useEdgesState` are documented as prototyping conveniences; for production, prefer a store (D5).
- Store: Zustand is the documented recommendation (React Flow uses it internally); Redux, Recoil, and Jotai are viable. Keep node updates immutable inside actions (D5).
- From inside a custom node: `useReactFlow().updateNodeData(id, partial)` or a store action (D5).
- `useReactFlow()` does not re-render on changes; read state on demand in handlers (D6).
- Derived UI (selection counts, toolbars): select narrow slices, never the whole `nodes` array (D13).

## Svelte Flow

- `$state.raw` arrays plus `bind:nodes bind:edges`; the component writes interactions back (D5). Plain `$state` adds deep reactivity cost.
- Update from code by reassigning the array or calling `updateNode`/`updateNodeData` from `useSvelteFlow()` (D5).
- Hooks return objects with `.current`; read `.current` inside `$derived`, `$effect`, or markup (D5).
- External store: function bindings with getter and setter (D5).
- Viewport: `$state<Viewport>` plus `bind:viewport` (D5).
- Svelte 5 rune questions beyond this (effects, universal reactivity) go to `svelte-wasp-drone`.

## Done when

No in-place mutation remains (search for `.position.x =`, `.data.` assignments, `nodes[`), handlers are stable, and state survives the navigation paths the task requires.
