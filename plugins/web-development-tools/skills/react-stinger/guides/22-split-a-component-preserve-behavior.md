# Split a giant component while preserving behavior

Use size as a navigation signal, not proof of a defect. Start with the existing characterization baseline and [comparison record](../templates/outcome-comparison-record.md). Grounding

1. Inventory visible states, inputs, forms, focus, accessible names, keys, draft persistence, selection, URL behavior, requests, analytics and effect setup/cleanup. Record source lines and actual existing checks. Missing critical characterization blocks a claim of preserved behavior.
2. Pick one coherent presentation seam. Extract a module-level component with explicit props/events. Keep state and side effects in the existing owner for the first step. Do not define a new component type inside its parent's render. Keep DOM hierarchy, keys and controlled/uncontrolled input contracts; changing type, position or key may reset state.
3. Lift pure formatting/selectors separately with before/after outputs. Do not move event-time actions into Effects. Keep mutation ordering, subscriptions, ref forwarding, error/Suspense placement and server/client boundaries unchanged unless separately requested.
4. Move state only after documenting who owns it and what resets it. A new wrapper can change reconciliation identity; manual browser checks must cover typing a draft, parent rerender, reorder, tab change, close/reopen and pending request completion. Preserve any intentional reset.
5. Compare characterization traces, request payload/order and rendered interactions. Use the installed RTL/browser setup for focus, accessible names and draft survival. A pure selector equality exercise does not prove React reconciliation. Require Security then Quality for the actual change.

[Worked extraction](../examples/outcome-modernization.md#component-extraction) gives an explicitly unmounted React example and exercised pure outputs. Never certify behavior preservation from line count, snapshots alone or static example compilation.
