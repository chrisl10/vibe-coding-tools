# Example 01: typed React Flow editor with an editable custom node

Composed from documented APIs: installation and container sizing, the change and apply utilities, `nodeTypes` hoisting, `NodeProps` generics, `useReactFlow().updateNodeData`, `Handle`, `nodrag`, and `isValidConnection` ([distillation](../references/research/distilled-xyflow.md) D3, D5, D6, D7, D7a). The self-connection rule is an application choice.

## Types

```ts
// flow/types.ts
import type { BuiltInNode, Edge, Node } from '@xyflow/react';

export type NumberNode = Node<{ value: number }, 'number'>;
export type AppNode = BuiltInNode | NumberNode;
export type AppEdge = Edge;
```

## Custom node

```tsx
// flow/NumberNode.tsx
import { memo } from 'react';
import { Handle, Position, useReactFlow, type NodeProps } from '@xyflow/react';
import type { NumberNode } from './types';

function NumberNodeView({ id, data }: NodeProps<NumberNode>) {
  const { updateNodeData } = useReactFlow();

  return (
    <div className="number-node">
      <Handle type="target" position={Position.Top} />
      <label>
        Value
        <input
          className="nodrag"
          type="number"
          value={data.value}
          onChange={(event) => updateNodeData(id, { value: Number(event.target.value) })}
        />
      </label>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export const NumberNodeComponent = memo(NumberNodeView);
```

`updateNodeData` merges a partial object into `data`, so the node object is replaced rather than mutated.

## Flow

```tsx
// flow/Flow.tsx  (add "use client" as the first line under the Next.js App Router)
import { useCallback, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  type IsValidConnection,
  type OnConnect,
  type OnEdgesChange,
  type OnNodesChange,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { NumberNodeComponent } from './NumberNode';
import type { AppEdge, AppNode } from './types';

// Module scope: the docs define nodeTypes outside the component to prevent re-renders.
const nodeTypes = { number: NumberNodeComponent };

const initialNodes: AppNode[] = [
  { id: 'a', type: 'number', position: { x: 0, y: 0 }, data: { value: 1 } },
  { id: 'b', type: 'number', position: { x: 0, y: 150 }, data: { value: 2 } },
];
const initialEdges: AppEdge[] = [{ id: 'a-b', source: 'a', target: 'b' }];

const isValidConnection: IsValidConnection = (connection) => connection.source !== connection.target;

export function Flow() {
  const [nodes, setNodes] = useState<AppNode[]>(initialNodes);
  const [edges, setEdges] = useState<AppEdge[]>(initialEdges);

  const onNodesChange: OnNodesChange<AppNode> = useCallback(
    (changes) => setNodes((snapshot) => applyNodeChanges(changes, snapshot)),
    [],
  );
  const onEdgesChange: OnEdgesChange<AppEdge> = useCallback(
    (changes) => setEdges((snapshot) => applyEdgeChanges(changes, snapshot)),
    [],
  );
  const onConnect: OnConnect = useCallback(
    (connection) => setEdges((snapshot) => addEdge(connection, snapshot)),
    [],
  );

  return (
    <div style={{ width: '100%', height: 600 }}>
      <ReactFlow<AppNode, AppEdge>
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        isValidConnection={isValidConnection}
        colorMode="system"
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
```

## Verify

- `tsc --noEmit` passes. `OnEdgesChange` and the generic `ReactFlow<AppNode, AppEdge>` form follow the documented generic pattern; if the installed version rejects either, read the live type reference rather than casting.
- The canvas renders at 600 px height, dragging a node moves it, typing in the input does not drag the node, a node cannot connect to itself.
- Run the inspector: no `inline-types` or `no-stylesheet` findings.
