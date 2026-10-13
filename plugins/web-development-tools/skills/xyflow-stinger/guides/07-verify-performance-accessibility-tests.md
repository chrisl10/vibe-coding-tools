# 07: Verify performance, accessibility, and tests

## Performance

React Flow (D13):

1. `memo` custom nodes and edges; keep `nodeTypes`/`edgeTypes` at module scope.
2. `useCallback` every handler passed to `<ReactFlow>`; `useMemo` object and array props.
3. Never subscribe to the whole `nodes` array for a derived value; select a narrow slice (for example selected ids).
4. Collapse large subtrees with `hidden`; simplify shadows, gradients, and animations at scale.
5. Consider `onlyRenderVisibleElements` for very large graphs; it trades per-frame visibility work for fewer DOM elements, so measure both ways.

Svelte Flow (D13): `$state.raw` for nodes and edges; read narrow hooks (`useNodesData`, `useNodeConnections`) rather than the whole array; current 1.6.x releases cache the zoom pane extent to avoid synchronous layout during pan and pinch. No Svelte-specific performance guide exists (G1); apply the shared rules above where they translate and label them derived.

Measure with the browser profiler on a graph of the target size (drag, pan, zoom, select-all). Report node and edge counts with the timings.

## Accessibility

1. Keep keyboard support on: `disableKeyboardA11y` false; `nodesFocusable` and `edgesFocusable` true unless a node is purely decorative (D13).
2. Know the model: Tab focuses, Enter or Space selects, Escape clears, arrows move selected draggable nodes (Shift for larger steps); `autoPanOnNodeFocus` keeps focused nodes in view (D13).
3. Translate or tailor announcements with `ariaLabelConfig` (keys such as `node.a11yDescription.default`, controls, minimap, handle labels) (D13). Read the live type page for the full key list (G3).
4. React Flow: give nodes meaningful roles and labels through `ariaRole` and `domAttributes` when the default is not descriptive. These were not confirmed for Svelte Flow; check the live docs there (D13).
5. Controls inside nodes remain real buttons and inputs with labels; `nodrag` does not change their semantics.
6. Check contrast of node, edge, and handle colors in both color modes.

## Tests

Unit and component tests in jsdom (D13):

1. Mock `ResizeObserver`, `DOMMatrixReadOnly`, `HTMLElement` `offsetHeight`/`offsetWidth`, and `SVGElement.prototype.getBBox` in the test setup. Copy the mock implementation from the live React Flow testing page; the archive records the list, not the code.
2. Wait for edges with `waitFor` until `.react-flow__edge` (Svelte: `.svelte-flow__edge`) elements exist; edges render after node measurement.
3. For clicks inside custom nodes, render with `nodesDraggable={false}` and `panOnDrag={false}`.
4. Test pure logic (layout functions, validators, import parsers, store actions) without rendering the canvas at all; that is where most regressions live.

Svelte Flow has no official testing page (G1): apply the same mock list in Vitest with a jsdom or happy-dom environment and label it derived. Real drag and connect gestures belong in browser tests; coordinate with `browser-automation-wasp-drone`.

## Done when

The report lists graph size, profiler observations, keyboard walkthrough results, and test commands with outcomes. Do not claim performance or accessibility you did not measure.
