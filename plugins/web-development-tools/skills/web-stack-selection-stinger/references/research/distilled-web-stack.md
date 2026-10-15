# Web stack selection digest

Fresh official retrieval October 7, 2026. Source pages describe current capabilities; versions, adapters and host limits still need project-specific verification. No popularity ranking, universal performance advantage or implementation benchmark is asserted.

| Finding | Selection implication | Source |
|---|---|---|
| React recommends frameworks for new apps and describes the extra routing/data decisions in a from-scratch build. | React/Vite is a deliberate composition, not automatically a full-stack application framework. | React app choices |
| Vite is a development/build tool with framework templates. | Vite does not alone decide production routing, mutation/auth or API ownership. | Vite |
| SvelteKit supplies app-level routing and configurable rendering on top of Svelte components. | Distinguish Svelte UI from SvelteKit application behavior. | SvelteKit |
| SvelteKit supports per-route prerender/server/client options; fully prerenderable apps can use static output. | Quick content and dynamic app routes can have different delivery requirements. | Page options |
| Next App Router distinguishes Server and Client Components; interactive/browser behavior belongs across explicit boundaries. | React UI expertise alone does not qualify all Next server/data/cache/mutation behavior. | Next components |
| Next deploys through Node, Docker, static export or adapters; feature support differs. | A framework recommendation needs a compatible deployment mode, not a Vercel-only assumption. | Next deployment |
| Vue supports progressive enhancement and SPA/full-stack usage patterns; Nuxt describes universal/client/hybrid rendering. | Existing Vue team knowledge is a material discriminator; Vue and Nuxt are separate scope choices. | Vue, Nuxt |
| Go docs cover its tool/language ecosystem, Python asyncio covers concurrent I/O, and Rust's book describes systems programming and tooling. | Backend language follows libraries/runtime/operations/team requirements; none of these sources establishes a universal advanced-language ranking or speed multiplier. | Go, Python, Rust |

## Contract and evidence limits

The interview, single-recommendation rule, qualification ledger, owner-availability gate and component/license handoffs derive from the approved topic, not a vendor's endorsement. Browser retrieval of Nuxt returned `Internal Error`; direct official HTML retrieval succeeded and is archived. No guessed SSR/SEO guarantees: rendering can make content available, but indexing/ranking and a usable/auth-safe product require their own evidence.

The Web Development Tools pack ships implementation owners for React, Svelte, Preact, Next.js (`nextjs-stinger`), Nuxt (`nuxt-stinger`) and Vue (`vue-stinger`). The read-only Next.js security audit owner (`nextjs-security-stinger`) ships in Code Audit Tools. Which of them is available in a given installation depends on the plugins actually selected, so runtime must resolve the selected owners and report gaps. A security audit owner is not an implementation owner.
