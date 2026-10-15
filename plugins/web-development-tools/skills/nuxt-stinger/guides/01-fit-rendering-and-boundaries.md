# Fit, rendering and boundaries

1. Confirm the accepted Nuxt choice or obtain Web Stack Selection's decision. Nuxt fits a Vue team needing routed content, server data and a server deployment; content alone does not mandate request-time SSR.
2. Record Nuxt/Nitro/H3/Vue versions from the actual package and lockfile, current app structure, and server preset. Do not upgrade/install as part of discovery.
3. Make a route inventory: public stable content may prerender; changing public content may use SSR or narrowly scoped revalidation; interaction-heavy private views may use CSR or SSR according to actual UX. Hybrid means a justified route-by-route mix.
4. Resolve the accepted backend/API/DTO/tenant/session contracts. Preserve auth/data providers and external services. Impeccable owns PRODUCT.md, DESIGN.md and surface direction; Vue owns component/reactivity architecture. Nuxt owns routing, SSR integration, data composables and Nitro glue. Do not rewrite contracts to fit a starter.
5. Use the rendering worksheet and request tests before calling the model appropriate. Keep server endpoints out of a static-only promise.

Grounding: [R1/R2](../references/research/distilled-nuxt.md), rendering, deployment. Selection, contract preservation and ownership are workflow policy.
