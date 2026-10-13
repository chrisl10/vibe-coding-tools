# 06: Style, theme, and adopt UI kits

## Stylesheets

- `style.css` for the default look; `base.css` when building a fully custom theme. Never ship with neither: base styles are required (D3, D11).
- Import once, globally.

## Theme tokens

- Override `--xy-*` variables under `.react-flow` / `.svelte-flow` or `:root`, for example `--xy-node-background-color-default`, `--xy-edge-stroke-default`, `--xy-handle-background-color-default`. The React reference lists 27 light defaults (D11); dark values were not captured, so read the live theming page before overriding dark tokens (G3).
- Map the product's design tokens onto `--xy-*` variables rather than restyling internal classes; class overrides (`.react-flow__node`, `.svelte-flow__edge`) are for what variables do not cover (D11).
- Token design itself belongs to `impeccable-wasp-drone` or the design-system owner; this Drone wires tokens into the canvas.

## Dark mode

`colorMode="light" | "dark" | "system"` (React default `light`). Svelte adds `colorModeSSR` for server output (D8). Keep custom node styles keyed to the same mode; in React Flow the root receives a class for the active mode (D11).

## Tailwind v4 (conflict C1)

Two documented orders exist:

| Setup | Global CSS |
|---|---|
| Using React Flow UI components | `@import "tailwindcss";` then `@import "@xyflow/react/dist/style.css";` |
| Tailwind utilities must override library defaults | `@import '@xyflow/react/dist/style.css' layer(base);` then `@import 'tailwindcss';` (Svelte: same with `@xyflow/svelte`) |

Pick one, state which in the report, and verify in the browser that node, edge, and control styles look right in both color modes. Tailwind mechanics beyond this go to `tailwind-wasp-drone`.

## React Flow UI (React only)

- A shadcn/ui registry of nodes, handles, edges, and controls; install with `npx shadcn@latest add https://ui.reactflow.dev/<component>` (D11). Components are copied into the repo and become your code to review and maintain.
- Prerequisites: shadcn/ui configured and Tailwind installed. Components are built on React 19 and Tailwind 4 even though `@xyflow/react` itself supports React 17 or newer (C4); confirm the host meets that bar first.
- MIT licensed, maintained by webkid GmbH (D11).
- Installing through the CLI changes files and dependencies; list them in the plan.
- The documented command runs the newest `shadcn` CLI from the registry and copies remote source into the repository. Where the repository already pins a `shadcn` version, use that version instead of `@latest`, get approval for the install as [00-authority-and-scope.md](00-authority-and-scope.md) requires, and read the copied component source before committing it.

## Svelte projects

No Svelte equivalent of React Flow UI was confirmed (C2). Build node chrome from the project's own components; for shadcn-svelte primitives coordinate with `shadcn-svelte-wasp-drone`. Label this composition as derived.

## Attribution

Leave the attribution visible unless the owner confirms the documented terms for their kit (D14, C5). Hidden attribution logs a development-mode message in current releases.
