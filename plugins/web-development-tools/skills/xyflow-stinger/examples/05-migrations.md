# Example 05: migration diffs

Before and after snippets taken from the official migration guides (D9). The React guide says it is not exhaustive and the Svelte archive captures only the main changes; re-read the live page for the version you are leaving.

## React Flow 11 (`reactflow`) to 12 (`@xyflow/react`)

```diff
- import ReactFlow, { addEdge, updateEdge } from 'reactflow';
- import 'reactflow/dist/style.css';
+ import { ReactFlow, addEdge, reconnectEdge } from '@xyflow/react';
+ import '@xyflow/react/dist/style.css';
```

```diff
- const width = node.width;               // was the measured size
+ const width = node.measured?.width;     // measured size now lives here
```

```diff
- { id: 'child', parentNode: 'group', position: { x: 10, y: 10 }, data: {} }
+ { id: 'child', parentId: 'group', position: { x: 10, y: 10 }, data: {} }
```

```diff
- setNodes((nds) => { nds[0].hidden = true; return nds; });
+ setNodes((nds) => nds.map((n, i) => (i === 0 ? { ...n, hidden: true } : n)));
```

Renames to sweep for: `onEdgeUpdate` to `onReconnect`, `updateEdge()` to `reconnectEdge()`, `edgeUpdaterRadius` to `reconnectRadius`, `edge.updatable` to `edge.reconnectable`, `xPos`/`yPos` to `positionAbsoluteX`/`positionAbsoluteY`, `getNodesBounds(nodes, nodeOrigin)` to `getNodesBounds(nodes, { nodeOrigin })`, store `nodeInternals` to `nodeLookup`. Removed: `getTransformForBounds`, `getRectOfNodes`, `project`, `getMarkerEndId`, `updateEdge`. Also replace deprecated `useHandleConnections({ type, id })` with `useNodeConnections({ handleType, handleId })` (D6).

Search commands:

```text
rg -n "from 'reactflow'|reactflow/dist|parentNode|onEdgeUpdate|updateEdge|edgeUpdaterRadius|updatable|xPos|yPos|getRectOfNodes|project\(|nodeInternals|useHandleConnections" src
```

## Svelte Flow 0.x to 1.0 (Svelte 5)

```diff
- const nodes = writable([...]);
- const edges = writable([...]);
+ let nodes = $state.raw([...]);
+ let edges = $state.raw([...]);
```

```diff
- <SvelteFlow {nodes} {edges} />
+ <SvelteFlow bind:nodes bind:edges />
```

```diff
- type $$Props = NodeProps;
- export let data: $$Props['data'];
+ let { data, position, selected }: NodeProps = $props();
```

```diff
- nodes[0].position.x = 100;
+ nodes = nodes.map((node) => node.id === '1' ? { ...node, position: { ...node.position, x: 100 } } : node);
```

Also: hooks return `.current` objects instead of stores; `onEdgeCreate` becomes `onbeforeconnect`; `<EdgeLabelRenderer>` becomes `<EdgeLabel x y>`; slot-based connection lines become `connectionLineComponent`; viewport uses `$state<Viewport>` plus `bind:viewport`.

```text
rg -n 'writable\(|\$\$Props|export let|EdgeLabelRenderer|onEdgeCreate|on:[a-z]+' src
```

## Verify

- The inspector reports no `legacy-package`, `mixed-generations`, `parent-node-field`, `svelte-writable-store`, or `svelte-flow-0x` findings.
- Type check (`tsc --noEmit` or `svelte-check`) passes without new casts.
- Manual pass: drag, connect, reconnect, delete, sub-flow drag, save and restore behave as before.
