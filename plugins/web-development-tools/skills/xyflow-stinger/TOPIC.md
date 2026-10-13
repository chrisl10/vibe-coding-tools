# xyflow Stinger Topic Record

- Component type: Stinger, paired with `xyflow-wasp-drone`
- Domain: node-based editors and diagrams built with the xyflow libraries: React Flow (`@xyflow/react`) and Svelte Flow (`@xyflow/svelte`), both running on the shared `@xyflow/system` core
- Why one pair covers both kits: the two libraries share one monorepo, one core package, one conceptual model (nodes, edges, handles, viewport), and mostly parallel APIs. Only the reactivity layer differs (React state and a Zustand store versus Svelte 5 runes), so one Stinger with a React and Svelte crosswalk avoids two near-duplicate Drones
- Trigger boundary: use for flow canvases, node editors, workflow builders, diagram UIs, custom nodes, edges and handles, flow state, layout engines wired into a flow, sub flows, theming, React Flow UI components, SSR of a flow, performance on large graphs, accessibility of the canvas, testing flow components, and migrations between xyflow generations
- Exclusions: general React architecture (react-stinger), Svelte 5 language and SvelteKit runtime (svelte-stinger), design-system tokens and visual design (impeccable-stinger, ux-ui-stinger, ux-ui-svelte-stinger), shadcn-svelte library mechanics (shadcn-svelte-stinger), Tailwind v4 framework mechanics (tailwind-stinger), backend persistence of saved flows (db-stinger), and formal security or quality acceptance (security-stinger, quality-stinger)
- Harness targets: Claude Code, Cursor, ChatGPT Codex, and Claude Cowork
- Focus: development-focused, so the exact Queen Wasp Critical Directive and Ship Gate are required
- Research window: 2026-03-23 through 2026-09-23, retrieval at the cutoff
- Source policy: official reactflow.dev, svelteflow.dev, and xyflow.com documentation, the official xyflow/xyflow repository and changelogs, and the npm registry. Community material is excluded unless no primary source exists, and is labeled when used
- Currency policy: versions are dated observations, never timeless defaults. Runtime work inspects the target project and refreshes current releases before changing dependencies
- Derived-pattern policy: auto-layout pipelines, persistence shapes, and editor architectures assembled from documented primitives are labeled as derived designs

## Outcomes

The Stinger must equip its paired Drone to:

1. Inspect an existing flow project without changing it and identify the xyflow generation, framework, and risky patterns.
2. Install and render a flow correctly in React, Next.js, Svelte, or SvelteKit, including stylesheet and container sizing.
3. Choose and implement a state model (controlled, uncontrolled, store-backed) that stays immutable and performant.
4. Build typed custom nodes, edges, and handles with connection validation.
5. Wire an automatic layout engine and sub flows without fighting measured dimensions.
6. Theme the canvas, adopt React Flow UI components where appropriate, and keep dark mode coherent.
7. Keep large graphs fast, the canvas accessible, and flow components testable.
8. Migrate legacy `reactflow` v11 and Svelte Flow 0.x projects to the current generation.
9. Respect the MIT license and the documented attribution terms.
10. Refresh the dated version snapshot from primary sources before making currency claims.
