# Nuxt implementation digest

Captured 2026-10-08 UTC. Official Nuxt 4.x pages and explicitly versioned Nitro v2 cache documentation. Inspect the actual project lockfile before using an API. These documents are capability guidance, not proof that a version is installed or that a host runs it.

| ID | Derived implementation instruction | Archived source |
|---|---|---|
| R1 | Nuxt universal rendering returns HTML and subsequently hydrates Vue. Rendering mode must follow content, interaction and freshness requirements; SSR is not a universal requirement. | rendering |
| R2 | Hybrid rules apply by route; generated static output cannot supply runtime server endpoints. Select actual server output when server handlers are required. | rendering |
| R3 | Module-level mutable refs can share state across server requests. Request-created useState values serialize into hydration payloads, so only client-safe DTOs belong there. | state |
| R4 | useFetch supports SSR payload transfer and relative server requests through request-aware fetching. Audit forwarded cookies/headers and destination trust rather than forwarding credentials to arbitrary URLs. | data-fetching |
| R5 | Public config is browser-visible; private runtime config is server-only unless application code serializes it. Runtime overrides require matching NUXT names; built servers do not read .env automatically. | runtime-config |
| R6 | server/api routes receive the /api prefix; server/routes do not. Server middleware and Vue route middleware have different execution surfaces. | server |
| R7 | Page middleware is navigation UX. Sensitive server routes need server session validation and additional accepted resource/tenant authorization. Nuxt Auth Utils is the recipe module, not an instruction to replace existing auth. | sessions |
| R8 | Nitro v2 cached event handlers alter header handling. Authenticated handlers must stay outside response caching by default; varies is not proof of correct authorization or partitioning. | nitro-v2-cache |
| R9 | Deployment requires an actual Nitro preset and compatible host. Static, Node and edge outputs impose different server/runtime requirements; the selected provider owner qualifies these. | deployment |

## Version disagreement and evidence limit

The unversioned standalone Nitro page now documents `defineCachedHandler`; the captured v2 page uses `defineCachedEventHandler`. Do not transpose the latest standalone Nitro API into a Nuxt app without checking its resolved Nitro/H3 versions. The official Nuxt 4.x documentation is rolling and can describe features newer than an existing project. All application build, hydration, session, cache isolation and provider behavior remains NOT_RUN in this source forge. Derived authorization and no-private-cache policy comes from accepted application contracts and Core Security, not a claim that Nuxt supplies tenant policy.
