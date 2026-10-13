# Example 03: Dagre auto layout on demand (derived)

**Derived design.** The official Dagre example lays out once and does not re-run on change; the reusable auto-layout example is Pro-gated (D10, G2). This example composes the documented dagre API (center coordinates, `rankdir`) with xyflow's measured dimensions and immutable updates. It is framework-neutral; only the import of `Node` and `Edge` changes. graphlib reads (`hasNode`, `node`) follow the graphlib API reference (D10).

## Layout function

```ts
// flow/layout.ts
import dagre from '@dagrejs/dagre'; // verify the entry point of the installed version (wiki shows CommonJS only)
import type { Edge, Node } from '@xyflow/react'; // or '@xyflow/svelte'

type Direction = 'TB' | 'BT' | 'LR' | 'RL';

function sizeOf(node: Node): { width: number; height: number } {
  const width = node.measured?.width ?? node.width;
  const height = node.measured?.height ?? node.height;
  if (width == null || height == null) {
    throw new Error(`node ${node.id} has no size yet; run layout after measurement or set width and height`);
  }
  return { width, height };
}

export function layoutWithDagre<N extends Node>(nodes: N[], edges: Edge[], rankdir: Direction = 'TB'): N[] {
  const graph = new dagre.graphlib.Graph();
  graph.setGraph({ rankdir, nodesep: 50, ranksep: 50 });
  graph.setDefaultEdgeLabel(() => ({}));

  // Top-level nodes only: dagre is weak with sub flows connected outside the sub flow (D10).
  const topLevel = nodes.filter((node) => !node.parentId);
  for (const node of topLevel) graph.setNode(node.id, sizeOf(node));
  for (const edge of edges) {
    if (graph.hasNode(edge.source) && graph.hasNode(edge.target)) graph.setEdge(edge.source, edge.target);
  }

  dagre.layout(graph);

  return nodes.map((node) => {
    if (node.parentId) return node;
    const placed = graph.node(node.id); // undefined only if the node was never added
    if (!placed) return node;
    const { x, y } = placed;
    const { width, height } = sizeOf(node);
    // dagre returns centers; xyflow positions are top-left with the default node origin.
    return { ...node, position: { x: x - width / 2, y: y - height / 2 } };
  });
}
```

## Wiring

React Flow, from a toolbar button rendered inside the flow or under a `ReactFlowProvider`:

```tsx
const { getNodes, getEdges, setNodes, fitView } = useReactFlow();
const onLayout = () => {
  setNodes(layoutWithDagre(getNodes(), getEdges(), 'LR'));
  requestAnimationFrame(() => void fitView());
};
```

Svelte Flow, inside the component that owns the bound arrays:

```ts
function onLayout() {
  nodes = layoutWithDagre(nodes, edges, 'LR');
}
```

## Verify

- Layout on a graph with mixed node sizes: no overlaps, ranks follow `rankdir`.
- Running layout before first render throws the explicit size error rather than stacking nodes at the origin.
- If automatic re-layout on every change is required, decide the trigger explicitly (after `measured` is present on all nodes) and debounce it; that loop is an application design, not a documented xyflow feature.
