# Worked web-stack decisions

Fictional product/team inputs exercise the decision contract. No application was created and no rendering, hosting, auth or native-runtime behavior was tested.

## A: quick public site

Input: six stable public pages, no login/database/payments/admin, small team already knows Svelte, static hosting accepted. Recommendation: SvelteKit with qualified prerender/static delivery. The team's familiarity and stable content favor this track; the official page-options source supports the rendering shape. Do not add a CMS/DB simply because the framework permits one.

Handoff: selected Svelte owner plus appropriate visual/content/hosting owners. Acceptance requests: actual public HTML/deep-link/asset behavior from the resulting static deployment, approved content and accessibility review. Missing: exact version/adapter/content/hosting evidence. No performance or ranking guarantee.

Failure: "Svelte is fastest, so replace every backend." Reject popularity/performance speculation and scope expansion. Retain the supplied small content scope and one justified framework decision.

## B: signed-in SPA with existing API

Input: existing React19 browser components, private dashboard, established separate backend/API contract, browser-heavy controls, no public SEO pages; existing router/data conventions accepted by the team. Recommendation: React19/Vite SPA composition retaining the API. Vite supports the build shape; this deliberate choice keeps existing UI/contracts rather than pretending Vite supplies server/auth/routing semantics by itself.

Handoff: selected React owner, accepted router/data owners and actual backend/auth/security owners. Acceptance requests: refresh/deep-link routing, login/tenant-denial, API failure/loading states, browser-state behavior and hosting fallback. Backend language remains the existing qualified choice. Native mobile UI reuse is not promised.

Failure: "React19/Vite handles every Server Component and production API requirement automatically." Reject. The selected composition needs its actual router/server framework and owner evidence; React UI does not establish every full-stack behavior.

## C: public SSR and paid application

Input: team experienced in React, public frequently updated product routes need request-produced HTML, paid signed-in routes, integrated React server/client boundary accepted, Node/container hosting available. Recommendation: React/Next.js App Router, conditional on exact framework/version/deployment and qualified server ownership. Official Next sources support the architecture/deployment distinction; they do not establish payment/tenant security.

Handoff: `nextjs-stinger` for the Next server/client/data/cache boundaries, React UI owner for component architecture, data/auth/payments/security owners. If the pack that ships `nextjs-stinger` is not selected, record delivery blocked pending a selected owner and authorized scope; the Next.js security auditor cannot silently fill it. Acceptance requests: initial public HTML, server/client secret boundary, mutation errors, auth/tenant denial, cache/private data behavior and actual host mode. No code or vertical slice is generated here.

Failure: "A Next security Drone exists, therefore full Next implementation is ready." Reject the owner substitution. A recommendation can be supported while delivery capability is missing.

## D: existing Vue team

Input: maintained Vue components, Vue-skilled team, public dynamic pages plus interactive signed-in routes, accepted Nuxt-compatible host. Recommendation: Vue/Nuxt with qualified universal/hybrid route delivery. Existing skills/code and rendering need are the decisive discriminator. Do not rewrite to React merely because its agent is already installed.

Handoff: `vue-stinger` for Vue component work and `nuxt-stinger` for Nuxt rendering and Nitro; if the pack that ships them is not selected, name the gap and hold implementation. Component/design/backend owners retain their domains. Acceptance requests: initial HTML/hydration, browser-only API boundaries, direct navigation, mutations/access denial and host compatibility.

Failure: "Nuxt will automatically reuse every Vue web component as native iOS UI." Reject unsupported target equivalence; actual native targets, contracts, platform features and owners require separate qualification.

## E: unsupported implementation request

Input: user accepts C's Next recommendation and asks this advisory workflow to scaffold, install packages and deploy. Result: selection record can be delivered, but no implementation begins. Route the new requested work through Core, expose any unselected owner (`nextjs-stinger` for this case) and required action authority, and preserve the original decision. Do not manufacture a build-web-app role or treat a source command name as a registered tool.

## Exercise standard

For each case recover one recommendation, rendering/deployment shape, retained backend, actual owner graph, acceptance evidence and unimplemented state. Encoded checks cover one recommendation, source grounding, explicit missing implementation owners and refusal to turn selection into runtime proof. They do not assess framework performance or model-generated recommendations.
