# React Flow and Svelte Flow API crosswalk

Load this when porting between the kits, reviewing code in the less familiar kit, or answering "what is the Svelte name for X". Both kits share `@xyflow/system`, so concepts match; names and reactivity differ. Every row traces to [research/distilled-xyflow.md](research/distilled-xyflow.md) (section in brackets). A dash means the sources did not capture an equivalent; check the live docs before assuming one exists.

## Setup

| Concept | React Flow (`@xyflow/react`) | Svelte Flow (`@xyflow/svelte`) |
|---|---|---|
| Root component | `<ReactFlow />` (named export) [D1] | `<SvelteFlow />` [D3] |
| Stylesheet | `@xyflow/react/dist/style.css` or `base.css` [D3] | `@xyflow/svelte/dist/style.css` or `base.css` [D3] |
| Provider | `<ReactFlowProvider>` [D6] | `<SvelteFlowProvider>` [D6] |
| Root CSS class | `.react-flow`, element classes `react-flow__*` [D11] | `.svelte-flow`, element classes `svelte-flow__*` [D11] |
| Framework floor | React peer `>=17` [D2] | Svelte `^5.25.0` [D2] |

## State

| Concept | React Flow | Svelte Flow |
|---|---|---|
| Declare nodes | `useState(initial)` or `useNodesState(initial)` [D5] | `let nodes = $state.raw(initial)` [D5] |
| Feed the component | `nodes={nodes} edges={edges}` plus change handlers [D5] | `bind:nodes bind:edges` [D5] |
| Apply interaction changes | `onNodesChange` + `applyNodeChanges`; `onEdgesChange` + `applyEdgeChanges` [D5] | Automatic through the binding [D5] |
| New connection | `onConnect` + `addEdge` [D5] | Automatic; observe with `onconnect`; `onbeforeconnect` can cancel (return `false`) or modify the connection [D8] |
| Imperative instance | `useReactFlow()` returns `ReactFlowInstance` [D6] | `useSvelteFlow()` [D6] |
| Update node data | `updateNodeData(id, partialOrFn)` [D5] | `updateNodeData(id, update)` [D5] |
| Update a node | `updateNode(id, partialOrFn)` [D6] | `updateNode(id, update)` [D6] |
| Read nodes reactively | `useNodes()` returns an array [D6] | `useNodes()` returns `{ current, update, set }` [D5] |
| Node data of other nodes | `useNodesData(ids)` [D6] | `useNodesData(ids)` with `.current` [D6] |
| Connections of a node | `useNodeConnections({ handleType, handleId })` returns an array [D6] | same params, `.current` array [D6] |
| Deprecated connections hook | `useHandleConnections` (deprecated) [D6] | - |
| Re-measure handles | `useUpdateNodeInternals()(id)` [D6] | `useUpdateNodeInternals()(id or ids)` [D6] |
| Raw store | `useStore(selector, equalityFn?)`, `useStoreApi()` [D6] | `useStore()` [D6] |
| Serialize | `toObject()` [D5] | `toObject()` [D5] |
| Viewport binding | - | `bind:viewport` with `$state<Viewport>` [D5] |

## Custom nodes and edges

| Concept | React Flow | Svelte Flow |
|---|---|---|
| Node props | `NodeProps<MyNode>` function props [D7a] | `let { id, data }: NodeProps = $props()` [D7] |
| Register types | `nodeTypes` / `edgeTypes` outside the component or memoized [D7] | same rule [D7] |
| Handle | `<Handle type position id? />`, `Position` enum [D7] | same [D7] |
| Edge body | `<BaseEdge id path />` [D7] | `<BaseEdge {id} path={edgePath} />` [D7] |
| Path helpers | `getBezierPath`, `getSimpleBezierPath`, `getSmoothStepPath`, `getStraightPath` [D7] | `getBezierPath`, `getSmoothStepPath`, `getStraightPath` (compute in `$derived`) [D7] |
| Edge label portal | `<EdgeLabelRenderer>` + absolute div, `pointerEvents: 'all'` for interaction [D7] | `<EdgeLabel x y selectEdgeOnClick?>` [D7] |
| Handle state classes | `connecting`, `valid` [D11] | `connectingfrom`, `connectingto`, `valid` [D11] |
| Opt-out classes | `nodrag`, `nopan`, `nowheel` [D7] | same, renamable with `noDragClass`, `noPanClass`, `noWheelClass` [D7] |
| Custom connection line | - | `connectionLineComponent` prop [D9] |
| Reconnect edges | `onReconnect`, `reconnectEdge()`, `edge.reconnectable` [D9] | `<EdgeReconnectAnchor />` [D9] |

## Component props and events

| Concept | React Flow | Svelte Flow |
|---|---|---|
| Event naming | camelCase: `onNodeClick`, `onNodeDrag`, `onConnect` [D8] | lowercase: `onnodeclick`, `onnodedrag`, `onconnect` [D8] |
| Reject a connection | `isValidConnection: (edge: Edge \| Connection) => boolean` [D7] | `isValidConnection` prop typed `IsValidConnection<Edge>` [D7, G7] |
| Adjust or cancel a new edge | build it in `onConnect` before `addEdge`, or skip `addEdge` [D5] | `onbeforeconnect` (renamed from `onEdgeCreate`): return a modified connection, or `false` to cancel [D8] |
| Delete key | `deleteKeyCode` [D8] | `deleteKey` [D8] |
| Grid snapping | `snapToGrid` boolean; React also uses a `snapGrid` value in options [D8] | `snapGrid` typed `SnapGrid`; no `snapToGrid` prop listed. Not a rename: check each kit's type before porting [D8] |
| Zoom bounds | `minZoom` 0.5, `maxZoom` 2 [D8] | same [D8] |
| Color mode | `colorMode` [D8] | `colorMode`, `colorModeSSR` [D8] |
| Attribution | `proOptions={{ hideAttribution: true }}` [D14] | same [D14] |
| Keyboard a11y | `nodesFocusable`, `edgesFocusable`, `disableKeyboardA11y`, `ariaLabelConfig`, node `ariaRole`, `domAttributes` [D13] | `disableKeyboardA11y`, `AriaLabelConfig`; others unconfirmed [D13] |
| Visible-only rendering | `onlyRenderVisibleElements` [D13] | - |

## Server rendering

| Concept | React Flow | Svelte Flow |
|---|---|---|
| Node sizes | `width`/`height` or `initialWidth`/`initialHeight` [D12] | same [D12] |
| Handle positions | per-node `handles` array [D12] | same [D12] |
| Flow size | `initialWidth`/`initialHeight` on `ReactFlowProvider` [D12] | `width`/`height` on `SvelteFlow` [D12] |
| Static HTML | `renderToStaticMarkup()` [D12] | Svelte `render(Flow, { props })` [D12] |
