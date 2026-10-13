# 02: Install and render a flow

## React Flow

1. Install `@xyflow/react` with the repository's package manager (D3).
2. Import `@xyflow/react/dist/style.css` once, in a global stylesheet or entry file. With Tailwind v4, follow [06-style-theme-and-ui-kits.md](06-style-theme-and-ui-kits.md) for import order (C1).
3. Render `<ReactFlow>` inside a parent with explicit width and height (D3).
4. Under the Next.js App Router, render the flow inside a `"use client"` component; the official example marks its page that way (D12). Keep data fetching in server components and pass plain nodes and edges down.
5. Start from [examples/01-react-typed-flow.md](../examples/01-react-typed-flow.md).

## Svelte Flow

1. Confirm Svelte 5.25 or newer, then install `@xyflow/svelte` (D2, D3).
2. Import `@xyflow/svelte/dist/style.css` (D3).
3. Declare `let nodes = $state.raw([...])` and `let edges = $state.raw([...])`, and pass them with `bind:nodes bind:edges` (D5).
4. Wrap `<SvelteFlow>` in a sized container (D3).
5. Start from [examples/02-svelte-typed-flow.md](../examples/02-svelte-typed-flow.md).

## Server rendering

Only when the flow must render on the server (D12):

- Give every node `width`/`height` (fixed) or `initialWidth`/`initialHeight` (may change after hydration).
- Give every node a `handles` array with `type`, `position`, `x`, `y` so edges can be drawn.
- Svelte: pass `width` and `height` to `<SvelteFlow>`; consider `colorModeSSR` for dark mode (D8). React: pass `initialNodes`, `initialEdges`, `initialWidth`, `initialHeight` to `<ReactFlowProvider>`.
- Static images or docs diagrams: React `renderToStaticMarkup()`, Svelte `render(Flow, { props })`.

If SSR is not required, keep the flow client-only; SSR adds the sizing and handle data above, so only take it on when the task needs server output.

## Done when

The canvas renders at the intended size, nodes drag, and the inspector reports no `no-stylesheet` or `next-client-boundary` finding for the new files.
