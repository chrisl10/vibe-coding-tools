# 04: Build custom nodes, edges, and handles

## Custom nodes

1. Define the node's data type and add it to the app union: `Node<Data, 'kind'>`, unioned with `BuiltInNode` when default types remain (D7a).
2. Write the component. React: a function taking `NodeProps<MyNode>`, wrapped in `memo` for large graphs (D13). Svelte: `let { id, data }: NodeProps = $props()` (D7).
3. Register it in `nodeTypes` at module scope (React) or once in the instance script (Svelte); the key must equal the node's `type` exactly, or it falls back to `default` (D7).
4. Put `nodrag` on inputs, buttons, and sliders; `nowheel` on scrollable regions; `nopan` on overlays (D7).
5. Update data with `updateNodeData`, never by mutating `data` (D5).

## Handles

1. Add `<Handle type="source|target" position={Position.X} />`; a node needs at least one to be connectable (D7).
2. Give every additional handle of the same type a unique `id`; edges choose it with `sourceHandle`/`targetHandle` (D7).
3. Hide a handle with `visibility: hidden` or `opacity: 0`, never `display: none` (D7).
4. After adding, removing, or moving handles at runtime, call the function returned by `useUpdateNodeInternals()` with the node id (D6).
5. Read a node's connections with `useNodeConnections({ handleType, handleId })`; do not use the deprecated `useHandleConnections` in new code (D6).
6. `<Handle>` must render inside a custom node; outside one, Svelte Flow reports "Handle: No node id found" (D7).

## Connection rules

- `connectionMode`: `ConnectionMode.Strict` (default, source to target) or `ConnectionMode.Loose` (D7, C6).
- React Flow: `isValidConnection: (edge: Edge | Connection) => boolean` on `<ReactFlow>` rejects a connection before it becomes an edge (D7). Svelte Flow: the `isValidConnection` prop exists, typed `IsValidConnection<Edge>`; confirm its parameter shape in the live type reference (G7). Keep validators pure and cheap (**derived** advice).
- Svelte `onbeforeconnect` (renamed from `onEdgeCreate`) runs when a connection is about to become an edge. Its type is `(connection) => false | void | null | EdgeType | Connection`; the docs state it "can prevent the connection or modify it by returning `false` or a modified connection". Return `false` to cancel or a modified connection to adjust it; the effect of `null` is typed but not described. Keep reusable validation in `isValidConnection`, which also drives the connection-line feedback (D8, G7).
- Drop-to-create: combine connect-start and connect-end events with `screenToFlowPosition` (D7).

## Custom edges

1. Compute the path with `getBezierPath`, `getSmoothStepPath`, `getStraightPath` (React also `getSimpleBezierPath`); in Svelte compute inside `$derived` (D7).
2. Render `<BaseEdge id path />` and register the component in `edgeTypes` (D7).
3. Labels with HTML: React `<EdgeLabelRenderer>` with an absolutely positioned div translated to `labelX`/`labelY`, `pointerEvents: 'all'` when interactive; Svelte `<EdgeLabel x y>` (D7). Interactive label content carries `nodrag nopan`.
4. Fully custom shapes: build an SVG path from `sourceX, sourceY` to `targetX, targetY` (D7).

## Done when

Each custom type renders from a typed node object, interactive controls do not drag the canvas, handles connect to the intended ids, invalid connections are refused, and the inspector shows no `inline-types` or `handle-connections-hook` finding.
