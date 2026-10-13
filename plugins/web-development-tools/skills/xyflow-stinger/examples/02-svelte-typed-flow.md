# Example 02: typed Svelte Flow editor with an editable custom node

The Svelte 5 counterpart of Example 01, composed from documented APIs: installation, `$state.raw` with `bind:nodes`/`bind:edges`, `$props()` with `NodeProps`, `useSvelteFlow().updateNodeData`, `Handle`, `nodrag`, and the type-union pattern ([distillation](../references/research/distilled-xyflow.md) D3, D5, D7, D7a).

## Types

```ts
// flow/types.ts
import type { BuiltInNode, Node } from '@xyflow/svelte';

export type NumberNode = Node<{ value: number }, 'number'>;
export type AppNode = BuiltInNode | NumberNode;
```

## Custom node

```svelte
<!-- flow/NumberNode.svelte -->
<script lang="ts">
  import { Handle, Position, useSvelteFlow, type NodeProps } from '@xyflow/svelte';
  import type { NumberNode } from './types';

  let { id, data }: NodeProps<NumberNode> = $props();
  const { updateNodeData } = useSvelteFlow();
</script>

<div class="number-node">
  <Handle type="target" position={Position.Top} />
  <label>
    Value
    <input
      class="nodrag"
      type="number"
      value={data.value}
      oninput={(event) => updateNodeData(id, { value: Number(event.currentTarget.value) })}
    />
  </label>
  <Handle type="source" position={Position.Bottom} />
</div>
```

## Flow

```svelte
<!-- flow/Flow.svelte -->
<script lang="ts">
  import { SvelteFlow, Background, Controls, type Edge } from '@xyflow/svelte';
  import '@xyflow/svelte/dist/style.css';
  import NumberNode from './NumberNode.svelte';
  import type { AppNode } from './types';

  // The instance script runs once, so this object stays stable across updates.
  const nodeTypes = { number: NumberNode };

  let nodes = $state.raw<AppNode[]>([
    { id: 'a', type: 'number', position: { x: 0, y: 0 }, data: { value: 1 } },
    { id: 'b', type: 'number', position: { x: 0, y: 150 }, data: { value: 2 } },
  ]);
  let edges = $state.raw<Edge[]>([{ id: 'a-b', source: 'a', target: 'b' }]);
</script>

<div style:width="100%" style:height="600px">
  <SvelteFlow bind:nodes bind:edges {nodeTypes} colorMode="system" fitView>
    <Background />
    <Controls />
  </SvelteFlow>
</div>
```

To change nodes from outside the canvas, reassign the whole array (`nodes = nodes.map(...)`) or call `updateNode`; never assign into `nodes[i]` (D5).

## Verify

- `svelte-check` passes. The Svelte TypeScript guide documents the node union but not `NodeProps<NumberNode>` explicitly (gap G6); if the installed version types it differently, follow `svelte-check` and the live type reference.
- Event attributes are lowercase (`oninput`, and `onnodeclick` on the flow), never `on:input` (D8).
- Run the inspector: no `svelte-state-not-raw`, `svelte-writable-store`, or `no-stylesheet` findings.
