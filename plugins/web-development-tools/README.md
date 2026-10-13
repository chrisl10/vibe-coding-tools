# Web Development Tools

Build web interfaces and sites with React, Svelte, design systems and accessible components.

Keep the interface workflow together, with stack routing inside the pack. A developer chooses one coherent web pack instead of many tiny UI packages.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 30 skills, 30 agents and 12 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [asset-stinger](skills/asset-stinger/SKILL.md) | Maintain the Universal Asset Registry. Use to register assets, audit code-to-registry drift, or generate migrations. |
| [component-vendoring-stinger](skills/component-vendoring-stinger/SKILL.md) | Select existing UI components and prepare notice-preserving source-copy plans. Use for component reuse, exact MIT artifact provenance, authorized copies, or local fork updates. |
| [csv-xlsx-import-export-stinger](skills/csv-xlsx-import-export-stinger/SKILL.md) | Implement spreadsheet import and export in React. Use for CSV/XLSX parsing, mapping, row validation, streaming, or CSV injection. |
| [dark-mode-theming-stinger](skills/dark-mode-theming-stinger/SKILL.md) | Audits and implements dark mode for React/Next.js: CSS tokens, next-themes wiring, FOWT prevention, SSR hydration, Tailwind v4 config, multi-brand theming. Use for dark mode setup or flashing bugs. |
| [design-system-stinger](skills/design-system-stinger/SKILL.md) | Bootstrap a product design system. Use for tokens, utilities, component and screen specs, or static examples. |
| [font-loading-stinger](skills/font-loading-stinger/SKILL.md) | Fix web font loading performance. Use for FOIT/FOUT, preload, subsetting, metric-matched fallbacks, or font-swap CLS. |
| [icon-system-stinger](skills/icon-system-stinger/SKILL.md) | Design a React icon system. Use for library choice, bundle size, SVG sprites, dynamic icons, or accessibility. |
| [image-optimization-stinger](skills/image-optimization-stinger/SKILL.md) | Optimize web image delivery. Use for AVIF/WebP, responsive sizes, blur placeholders, Next image config, or image CLS. |
| [impeccable-stinger](skills/impeccable-stinger/SKILL.md) | Operate Impeccable for UI design. Use for new surfaces, redesign, polish, design capture, or anti-slop checks. |
| [localization-stinger](skills/localization-stinger/SKILL.md) | Implement locale routing, message resources, ICU/plurals, Intl formatting and RTL in a selected web framework. Use for localization changes and scoped translation review. |
| [modal-toast-dialog-stinger](skills/modal-toast-dialog-stinger/SKILL.md) | Build accessible React overlays. Use for dialog, drawer, toast, command menu, focus handling, or stacking. |
| [nextjs-stinger](skills/nextjs-stinger/SKILL.md) | Implement Next.js App Router features: server/client boundaries, reads, actions, handlers, private data, cache contracts and build/provider handoffs. |
| [nuxt-stinger](skills/nuxt-stinger/SKILL.md) | Implement Nuxt apps, SSR/data integration, Nitro routes, request state and cache/auth boundaries. Use for accepted Nuxt builds or changes. |
| [preact-stinger](skills/preact-stinger/SKILL.md) | Build Preact 11 apps and widgets. Use for signals, React compat migration, embeds, Astro islands, or Fresh. |
| [product-tour-onboarding-ui-stinger](skills/product-tour-onboarding-ui-stinger/SKILL.md) | Build in-app tours and onboarding UI. Use for tour tools, tooltips, checklists, segment triggers, or maintenance after UI changes. |
| [pwa-stinger](skills/pwa-stinger/SKILL.md) | Implement browser PWA manifest, service-worker lifecycle and bounded public offline assets. Use for scoped PWA/offline changes. |
| [react-stinger](skills/react-stinger/SKILL.md) | Review and refactor React 18/19 architecture. Use for state layers, Server Components, Suspense, Actions, data boundaries, or testing. |
| [react-to-svelte-stinger](skills/react-to-svelte-stinger/SKILL.md) | React-to-Svelte 5 porting: hooks-to-runes translation, TanStack Router to SvelteKit, RTK Query and Radix conversion, contract-first port waves. Use when porting React components or dashboards. |
| [seo-aeo-stinger](skills/seo-aeo-stinger/SKILL.md) | SEO and AEO for SvelteKit (Svelte 5) + Payload CMS + Vercel. Covers metadata, sitemap/robots, JSON-LD, Payload SEO fields, Core Web Vitals, llms.txt/AI citation, E-E-A-T, and indexation playbooks. |
| [shadcn-svelte-stinger](skills/shadcn-svelte-stinger/SKILL.md) | The shadcn-svelte library itself for any Svelte project: CLI, copy-in model, anatomy, registry, theming, forms, upgrades. Not OSPRY's design system on portal/web/wl (ux-ui-svelte-stinger owns that). |
| [svelte-stinger](skills/svelte-stinger/SKILL.md) | Svelte 5 specialist for runes, snippets, lifecycle, universal reactivity, SvelteKit 2 load/actions/remote functions, and Svelte 4 migration. Use for any .svelte, .svelte.js, or .svelte.ts work. |
| [tailwind-stinger](skills/tailwind-stinger/SKILL.md) | Tailwind CSS v4 the framework itself, CSS-first config, @theme, the Vite plugin, v3-to-v4 migration, dark mode, container queries, class ordering. Generic, any codebase, not OSPRY-specific. |
| [tanstack-stinger](skills/tanstack-stinger/SKILL.md) | TanStack libraries in SvelteKit (Svelte 5) - Query SSR/caching/mutations, Table runes state, Form snippet validation, Virtual; states plainly that Router and Start have no official Svelte support. |
| [typography-font-stinger](skills/typography-font-stinger/SKILL.md) | Build a web typography system. Use for variable fonts, font loading, fluid scales, vertical rhythm, or type tokens. |
| [ux-ui-stinger](skills/ux-ui-stinger/SKILL.md) | Enforce an existing design system. Use for component specs, token drift, library wrappers, motion rulings, or visual deltas. |
| [ux-ui-svelte-stinger](skills/ux-ui-svelte-stinger/SKILL.md) | Enforce OSPRY's SvelteKit UI standard. Use for shadcn-svelte, Tailwind token bridge, white-label branding, or markup styling. |
| [vue-stinger](skills/vue-stinger/SKILL.md) | Build Vue application slices with SFCs, composables, typed props/events, state, forms, routing and delivery evidence. Use after Vue is chosen; hand Nuxt SSR to its selected owner. |
| [web-stack-selection-stinger](skills/web-stack-selection-stinger/SKILL.md) | Recommend one web framework from product, rendering, team and hosting needs. Separate backend choices and expose implementation-owner gaps. |
| [website-stinger](skills/website-stinger/SKILL.md) | Build a SvelteKit marketing site from a brief. Use for site scaffolding, Payload CMS, Supabase, lead capture, blog, or conversion. |
| [xyflow-stinger](skills/xyflow-stinger/SKILL.md) | React Flow and Svelte Flow (xyflow) node editors: setup, state, custom nodes and edges, handles, layout, sub flows, theming, React Flow UI, SSR, tests, and migrations. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install web-development-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use react-stinger to review [React module] against its current behavior and tests. Scope any proposed implementation before editing.
```

Expected result: The requested frontend review or implementation, with checks appropriate to that change. Use a Svelte specialist for Svelte work.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/web-development-tools:build-app-search` ([procedure](commands/build-app-search.md)) | Build tenant-safe application search with an accepted query/result contract, stable pagination and measured retrieval quality. |
| `/web-development-tools:build-localization` ([procedure](commands/build-localization.md)) | Build or extend a localization app using current locale, resource, plural, formatting and RTL boundaries with explicit verification. |
| `/web-development-tools:build-nextjs-app` ([procedure](commands/build-nextjs-app.md)) | Build or extend a Next.js app using current App Router, server/client, data, mutation and cache boundaries with explicit verification. |
| `/web-development-tools:build-nuxt-app` ([procedure](commands/build-nuxt-app.md)) | Build or extend a Nuxt app using current Nuxt routing, SSR, Nitro, data and cache boundaries with explicit verification. |
| `/web-development-tools:build-pwa-app` ([procedure](commands/build-pwa-app.md)) | Build or extend a PWA app using current public asset, offline fallback, update and private-data boundaries with explicit verification. |
| `/web-development-tools:build-quick-website` ([procedure](commands/build-quick-website.md)) | Build a scoped SvelteKit marketing or lead-generation website from a brief, with explicit CMS and integration decisions. |
| `/web-development-tools:build-saas-foundation` ([procedure](commands/build-saas-foundation.md)) | Build a scoped SaaS foundation joining tenant identity, data isolation, billing entitlements and a verified user journey. |
| `/web-development-tools:build-vue-app` ([procedure](commands/build-vue-app.md)) | Build or extend a Vue app using current component, state, form, routing and asynchronous boundaries with explicit verification. |
| `/web-development-tools:build-web-app` ([procedure](commands/build-web-app.md)) | Scope and build an authorized web-app slice using an actual supported framework owner and verified boundaries. |
| `/web-development-tools:choose-web-stack` ([procedure](commands/choose-web-stack.md)) | Recommend one web framework from product, rendering, team and hosting needs, with backend boundaries and owner gaps. |
| `/web-development-tools:qualify-typography` ([procedure](commands/qualify-typography.md)) | Qualify a web typography system and font delivery using source inspection and actual browser evidence. |
| `/web-development-tools:vendor-component` ([procedure](commands/vendor-component.md)) | Select and prepare an authorized component vendoring plan with actual artifact provenance, notices, patches and update evidence. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [asset-wasp-drone](agents/asset-wasp-drone.md) | Single owner of the Universal Asset Registry: the platform-owned catalog of every Feature, Page, Route, Surface, Control, Display, Layout, NavEntry, DesignToken, Icon, MediaAsset, Font, Motion, Breakpoint, ContentEntry, Translation, FeatureFlag binding, Meter binding, and Entitlement in the codebase. | [asset-stinger](skills/asset-stinger/SKILL.md) |
| [component-vendoring-wasp-drone](agents/component-vendoring-wasp-drone.md) | Select reusable UI components, prepare exact notice-preserving copy plans, and maintain authorized local forks with artifact provenance. | [component-vendoring-stinger](skills/component-vendoring-stinger/SKILL.md) |
| [csv-xlsx-import-export-wasp-drone](agents/csv-xlsx-import-export-wasp-drone.md) | Implements and audits the "upload your spreadsheet" feature surface for React/Next.js products. | [csv-xlsx-import-export-stinger](skills/csv-xlsx-import-export-stinger/SKILL.md) |
| [dark-mode-theming-wasp-drone](agents/dark-mode-theming-wasp-drone.md) | Audits and implements the full dark-mode theming surface for React/Next.js applications. | [dark-mode-theming-stinger](skills/dark-mode-theming-stinger/SKILL.md) |
| [design-system-wasp-drone](agents/design-system-wasp-drone.md) | Bootstraps complete design systems from scratch for any product: master design brief, tokens CSS, utility layer CSS, per-component specs, per-screen specs, static HTML examples, and README. | [design-system-stinger](skills/design-system-stinger/SKILL.md) |
| [font-loading-wasp-drone](agents/font-loading-wasp-drone.md) | Production-focused web font loading specialist. | [font-loading-stinger](skills/font-loading-stinger/SKILL.md) |
| [icon-system-wasp-drone](agents/icon-system-wasp-drone.md) | Icon-system specialist for React/Next.js applications. | [icon-system-stinger](skills/icon-system-stinger/SKILL.md) |
| [image-optimization-wasp-drone](agents/image-optimization-wasp-drone.md) | Image optimization specialist for React/Next.js and HTML contexts. | [image-optimization-stinger](skills/image-optimization-stinger/SKILL.md) |
| [impeccable-wasp-drone](agents/impeccable-wasp-drone.md) | Operates the entire Impeccable design system (pbakaus/impeccable, Apache-2.0) as the Wasp Swarm's frontend-design operating system: the four-phase loop (Start -> Iterate -> Polish -> Maintain), the context contract (PRODUCT.md + DESIGN.md + surface briefs), the 23-command vocabulary, the deterministic 59-rule anti-slop detector gate, hooks, live mode, and native playbooks. | [impeccable-stinger](skills/impeccable-stinger/SKILL.md) |
| [localization-wasp-drone](agents/localization-wasp-drone.md) | Implement locale routing, resources, ICU/plurals, Intl formatting and RTL in the selected web framework. | [localization-stinger](skills/localization-stinger/SKILL.md) |
| [modal-toast-dialog-wasp-drone](agents/modal-toast-dialog-wasp-drone.md) | Accessible overlay specialist for React. | [modal-toast-dialog-stinger](skills/modal-toast-dialog-stinger/SKILL.md) |
| [nextjs-wasp-drone](agents/nextjs-wasp-drone.md) | Implement Next.js App Router features, reads, Server Actions, Route Handlers, cache/private-data isolation and build/provider handoffs. | [nextjs-stinger](skills/nextjs-stinger/SKILL.md) |
| [nuxt-wasp-drone](agents/nuxt-wasp-drone.md) | Implement accepted Nuxt apps: routing, SSR/data, Nitro routes, request state, private config and cache/auth integration. | [nuxt-stinger](skills/nuxt-stinger/SKILL.md) |
| [preact-wasp-drone](agents/preact-wasp-drone.md) | Preact 11 specialist: signals API (v2 with createModel/useModel/action), preact/compat migration from React (alias setup, known gaps, compat blockers), third-party embed widgets (shadow DOM isolation, IIFE bundle pattern, size budgeting), Astro island integration (client:* directives, require >= 5.0.1 for useId fix), and Fresh 2.x framework (Deno-native, serializable island props, cross-island signals state). | [preact-stinger](skills/preact-stinger/SKILL.md) |
| [product-tour-onboarding-ui-wasp-drone](agents/product-tour-onboarding-ui-wasp-drone.md) | In-app product tour and onboarding UI specialist. | [product-tour-onboarding-ui-stinger](skills/product-tour-onboarding-ui-stinger/SKILL.md) |
| [pwa-wasp-drone](agents/pwa-wasp-drone.md) | Implement scoped browser PWA manifest, service-worker lifecycle and public offline assets. | [pwa-stinger](skills/pwa-stinger/SKILL.md) |
| [react-to-svelte-wasp-drone](agents/react-to-svelte-wasp-drone.md) | Port-wave drone converting React surfaces to Svelte 5 against an immutable API contract - contract extraction, behavior inventory, runes/snippets port, per-row verification. | [react-to-svelte-stinger](skills/react-to-svelte-stinger/SKILL.md) |
| [react-wasp-drone](agents/react-wasp-drone.md) | React architecture specialist for React 18/19 codebases: bulletproof-react patterns, awesome-react ecosystem, React 19 idioms (Server Components, Suspense, Actions, Compiler), state layering, data-fetching boundaries, error handling, testing strategy, and performance discipline. | [react-stinger](skills/react-stinger/SKILL.md) |
| [seo-aeo-wasp-drone](agents/seo-aeo-wasp-drone.md) | SvelteKit (Svelte 5) + Payload CMS + Vercel SEO and Answer Engine Optimization specialist. | [seo-aeo-stinger](skills/seo-aeo-stinger/SKILL.md) |
| [shadcn-svelte-wasp-drone](agents/shadcn-svelte-wasp-drone.md) | shadcn-svelte library specialist for any Svelte 5 project: CLI (init/add/apply), the copy-in-your-repo model, component anatomy, the registry system, generic theming mechanics, dark mode, Superforms + Formsnap forms, customization patterns that survive upstream re-syncs, and accessibility inherited from Bits UI. | [shadcn-svelte-stinger](skills/shadcn-svelte-stinger/SKILL.md) |
| [svelte-wasp-drone](agents/svelte-wasp-drone.md) | Svelte 5 language and SvelteKit 2 runtime specialist: runes ($state, $derived, $effect, $props, $bindable, $host, $inspect), snippets and event attributes, component lifecycle, universal reactivity in .svelte.js/.svelte.ts, Svelte 4-to-5 migration, SvelteKit 2 load functions/form actions/remote functions/error boundaries, and Svelte-aware testing. | [svelte-stinger](skills/svelte-stinger/SKILL.md) |
| [tailwind-wasp-drone](agents/tailwind-wasp-drone.md) | Tailwind CSS v4 framework specialist, CSS-first configuration, @theme mechanics, utility generation, the Vite plugin, v3-to-v4 migration, dark mode variants via @custom-variant, container queries, class ordering and tooling, and Oxide-engine performance, for ANY codebase. | [tailwind-stinger](skills/tailwind-stinger/SKILL.md) |
| [tanstack-wasp-drone](agents/tanstack-wasp-drone.md) | TanStack-in-SvelteKit (Svelte 5) specialist - TanStack Query SSR/caching/prefetching/mutations, TanStack Table runes-native setup and feature registration, TanStack Form snippet-based validation, TanStack Virtual, and drawing the line on TanStack Router/Start having no official Svelte support. | [tanstack-stinger](skills/tanstack-stinger/SKILL.md) |
| [typography-font-wasp-drone](agents/typography-font-wasp-drone.md) | Typography and font-loading specialist for web products: variable fonts, Google Fonts vs Fontsource vs self-host, the FOIT/FOUT/FOFT loading story, font-display semantics, fluid type scales via clamp(), vertical rhythm, and the type-token architecture. | [typography-font-stinger](skills/typography-font-stinger/SKILL.md) |
| [ux-ui-svelte-wasp-drone](agents/ux-ui-svelte-wasp-drone.md) | Enforces and implements the OSPRY SvelteKit UI standard (ADR-007): shadcn-svelte 1.x on Bits UI v2 + Melt UI, Tailwind v4, the @theme token bridge to the PRD-071 design tokens, and the white-label brand contract. | [ux-ui-svelte-stinger](skills/ux-ui-svelte-stinger/SKILL.md) |
| [ux-ui-wasp-drone](agents/ux-ui-wasp-drone.md) | Enforces a product's design system from its source-of-truth folder (tokens, utilities, components, screens) and governs integration with shadcn/ui, Mantine, Lucide-react, and Framer Motion. | [ux-ui-stinger](skills/ux-ui-stinger/SKILL.md) |
| [vue-wasp-drone](agents/vue-wasp-drone.md) | Implement Vue SFC, composable, state, form and client-route slices after Vue is selected. | [vue-stinger](skills/vue-stinger/SKILL.md) |
| [web-stack-selection-wasp-drone](agents/web-stack-selection-wasp-drone.md) | Recommend one web framework using product, rendering, team, backend and hosting constraints. | [web-stack-selection-stinger](skills/web-stack-selection-stinger/SKILL.md) |
| [website-wasp-drone](agents/website-wasp-drone.md) | Builds production-grade SvelteKit (Svelte 5) + Payload CMS + Supabase websites end-to-end from a brief, applying a 12-phase site-template playbook (monorepo architecture, SvelteKit performance + security, SEO/AEO, analytics, Supabase backend with RLS, auth + RBAC, Payload admin, lead capture, blog, webhooks, conversion-rate optimization, and visual design tokens). | [website-stinger](skills/website-stinger/SKILL.md) |
| [xyflow-wasp-drone](agents/xyflow-wasp-drone.md) | React Flow (@xyflow/react) and Svelte Flow (@xyflow/svelte) specialist for node editors, workflow builders, and diagram canvases: setup, flow state, custom nodes, edges and handles, connection rules, Dagre or ELK layout, sub flows, theming and Tailwind v4, React Flow UI, SSR, performance, accessibility, tests, and reactflow 11 or Svelte Flow 0.x migrations. | [xyflow-stinger](skills/xyflow-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `full website with data/auth/payments` also needs `data-and-ai-tools`, `platform-and-release-tools`.
- `build-quick-website-browser` also needs `browser-and-app-testing-tools`.
- `build-web-app-data` also needs `data-and-ai-tools`.
- `build-web-app-platform` also needs `platform-and-release-tools`.
- `build-saas-foundation-data` also needs `data-and-ai-tools`.
- `build-saas-foundation-platform` also needs `platform-and-release-tools`.
- `build-saas-foundation-backend` also needs `backend-and-desktop-tools`.
- `build-app-search-data` also needs `data-and-ai-tools`.
- `build-app-search-api` also needs `backend-and-desktop-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
