# Example 04: save and restore a flow, treating imports as untrusted

`toObject()` returning nodes, edges, and viewport, and the explicit save-action pattern, are documented (D5). Validating a restored document before handing it to the canvas is a **derived** safety step: saved flows often come from storage, files, or other users, and node `type` strings and `data` drive which components render.

## Shape and validation

```ts
// flow/persistence.ts
import type { Edge, Node, Viewport } from '@xyflow/react'; // or '@xyflow/svelte'

export type SavedFlow = { nodes: Node[]; edges: Edge[]; viewport: Viewport };

// Add every custom type here as well as to parseNodeData or parseEdgeData: unknown types are rejected first.
const KNOWN_NODE_TYPES = new Set(['default', 'input', 'output', 'group', 'number']);
const KNOWN_EDGE_TYPES = new Set(['default', 'straight', 'step', 'smoothstep', 'simplebezier']); // built-in edge types (D4)
const MAX_ELEMENTS = 5000;
const MAX_RAW_CHARS = 5_000_000;

type Json = Record<string, unknown>;
const isObject = (value: unknown): value is Json =>
  typeof value === 'object' && value !== null && !Array.isArray(value);
const isFiniteNumber = (value: unknown): value is number => typeof value === 'number' && Number.isFinite(value);
const isId = (value: unknown): value is string => typeof value === 'string' && value.length > 0 && value.length <= 200;
const optionalId = (value: unknown): string | undefined => {
  if (value === undefined || value === null) return undefined;
  if (!isId(value)) throw new Error('bad handle or parent id');
  return value;
};

// Replace with a per-type schema (for example zod) for every custom node type.
function parseNodeData(type: string, data: unknown): Json {
  if (!isObject(data)) throw new Error('node data must be an object');
  if (type === 'number') {
    if (!isFiniteNumber(data.value)) throw new Error('number node needs a numeric value');
    return { value: data.value };
  }
  return typeof data.label === 'string' ? { label: data.label.slice(0, 500) } : {};
}

// Same contract for edges: return only the fields each edge type is allowed to carry.
function parseEdgeData(type: string, data: unknown): Json | undefined {
  if (data === undefined) return undefined;
  if (!isObject(data)) throw new Error('edge data must be an object');
  return typeof data.label === 'string' ? { label: data.label.slice(0, 500) } : {};
}

export function parseSavedFlow(raw: string): SavedFlow {
  if (raw.length > MAX_RAW_CHARS) throw new Error('flow too large');
  const doc: unknown = JSON.parse(raw);
  if (!isObject(doc) || !Array.isArray(doc.nodes) || !Array.isArray(doc.edges)) throw new Error('not a saved flow');
  if (doc.nodes.length + doc.edges.length > MAX_ELEMENTS) throw new Error('flow too large');

  // Rebuild every element from allowlisted fields. Never pass the parsed objects through:
  // fields such as style, className, and domAttributes reach the DOM.
  const ids = new Set<string>();
  const nodes: Node[] = doc.nodes.map((input: unknown) => {
    if (!isObject(input) || !isId(input.id) || ids.has(input.id)) throw new Error('bad or duplicate node id');
    const type = input.type ?? 'default';
    if (typeof type !== 'string' || !KNOWN_NODE_TYPES.has(type)) throw new Error('unknown node type');
    const position = input.position;
    if (!isObject(position) || !isFiniteNumber(position.x) || !isFiniteNumber(position.y)) throw new Error('bad position');
    const parentId = optionalId(input.parentId);
    if (parentId !== undefined && !ids.has(parentId)) throw new Error('parent must precede child');
    ids.add(input.id);
    return {
      id: input.id,
      type,
      position: { x: position.x, y: position.y },
      data: parseNodeData(type, input.data),
      ...(parentId !== undefined ? { parentId } : {}),
    };
  });

  const edgeIds = new Set<string>();
  const edges: Edge[] = doc.edges.map((input: unknown) => {
    if (!isObject(input) || !isId(input.id) || edgeIds.has(input.id)) throw new Error('bad or duplicate edge id');
    if (!isId(input.source) || !isId(input.target) || !ids.has(input.source) || !ids.has(input.target)) {
      throw new Error('dangling edge');
    }
    const type = input.type ?? 'default';
    if (typeof type !== 'string' || !KNOWN_EDGE_TYPES.has(type)) throw new Error('unknown edge type');
    edgeIds.add(input.id);
    const sourceHandle = optionalId(input.sourceHandle);
    const targetHandle = optionalId(input.targetHandle);
    if (input.label !== undefined && typeof input.label !== 'string') throw new Error('edge label must be text');
    const label = typeof input.label === 'string' ? input.label.slice(0, 500) : undefined;
    const data = parseEdgeData(type, input.data);
    return {
      id: input.id,
      type,
      source: input.source,
      target: input.target,
      ...(sourceHandle !== undefined ? { sourceHandle } : {}),
      ...(targetHandle !== undefined ? { targetHandle } : {}),
      ...(label !== undefined ? { label } : {}),
      ...(data !== undefined ? { data } : {}),
    };
  });

  const vp = doc.viewport ?? { x: 0, y: 0, zoom: 1 };
  if (!isObject(vp) || !isFiniteNumber(vp.x) || !isFiniteNumber(vp.y) || !isFiniteNumber(vp.zoom) || vp.zoom <= 0) {
    throw new Error('bad viewport');
  }
  return { nodes, edges, viewport: { x: vp.x, y: vp.y, zoom: vp.zoom } };
}
```

The parent check enforces the documented ordering rule that parents precede children (D10). Rebuilding each node and edge from an allowlist of fields is part of the same **derived** safety step: nodes accept a `domAttributes` field that attaches arbitrary DOM attributes (D13), and `style` and `className` also reach the DOM, so a parsed document is never handed to the canvas as-is. Add fields to the allowlist deliberately, one at a time, with their own checks: for every custom node or edge type, add the type to `KNOWN_NODE_TYPES` or `KNOWN_EDGE_TYPES` and extend `parseNodeData` or `parseEdgeData`, so the type is accepted and its `data` survives a round trip.

## Save and restore

```ts
// React Flow
const { toObject, setNodes, setEdges, setViewport } = useReactFlow();
const save = () => localStorage.setItem('flow', JSON.stringify(toObject()));
const restore = () => {
  const raw = localStorage.getItem('flow');
  if (!raw) return;
  const flow = parseSavedFlow(raw);
  setNodes(flow.nodes);
  setEdges(flow.edges);
  void setViewport(flow.viewport);
};
```

In Svelte Flow, `toObject()` comes from `useSvelteFlow()`; restore by reassigning the bound `nodes` and `edges` and the bound viewport (D5).

## Verify

- Round trip: save, reload, restore gives the same nodes, edges, and viewport for every allowlisted field (ids, types, positions, `parentId`, per-type node `data`, edge handles, edge `label`, per-type edge `data`). Fields outside the allowlist are dropped by design; if a flow relies on one, add it to the allowlist with a check before claiming a full round trip.
- Rejected inputs: unknown node or edge `type`, duplicate id, child before parent, dangling edge, non-numeric position, non-object `data`, oversized input.
- Dropped fields: a document carrying `style`, `className`, or `domAttributes` restores without them.
- Custom nodes render `data` as text; any node that renders `data` as HTML (`dangerouslySetInnerHTML`, `{@html}`) goes to `security-wasp-drone` before shipping.
- `setViewport` on the React instance is not in the captured instance excerpt; confirm it in the live `ReactFlowInstance` reference, or restore the viewport through `fitView` instead.
