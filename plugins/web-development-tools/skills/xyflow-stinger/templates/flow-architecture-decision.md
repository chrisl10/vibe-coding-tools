# Flow architecture decision: {feature}

- Date: {YYYY-MM-DD}
- Status: proposed | accepted
- Kit: React Flow | Svelte Flow

## Context

{What the canvas is for, expected graph size, who edits it, where it is saved.}

## Decisions

| Area | Choice | Why | Source row |
|---|---|---|---|
| State model | {e.g. Zustand store with immutable actions} | {reason} | REFERENCE.md section 2 |
| Provider placement | {around flow and sidebar, outside router} | {reason} | D6 |
| Node and edge types | {list with data shapes, one union type} | {reason} | D7a |
| Connection rules | {connectionMode, isValidConnection rule} | {reason} | D7 |
| Layout | {none, dagre on demand, elkjs (license accepted by owner on date)} | {reason} | REFERENCE.md section 3 |
| Styling | {style.css or base.css, Tailwind order, colorMode} | {reason} | REFERENCE.md section 4, C1 |
| Persistence | {toObject to API, validation rules} | {reason} | examples/04 |
| SSR | {client-only, sized SSR} | {reason} | D12 |
| Accessibility | {keyboard on, ariaLabelConfig translations} | {reason} | D13 |
| Attribution | {visible, or hidden under documented terms confirmed by owner} | {reason} | D14 |

## Derived designs used

{List any derived pattern (re-layout loop, import validation) and the primitives it composes.}

## Consequences

{Performance limits, migration exposure (for example Svelte Flow 2.0), open questions.}
