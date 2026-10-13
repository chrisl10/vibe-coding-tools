# Next.js implementation

Paired specialist: nextjs-wasp-drone. Development source owner: web-development-tools. Build a bounded App Router feature in an existing authorized application, with framework-specific reads/actions/routes, rendering and cache boundaries. This pair fills the Next.js implementation gap; it does not change React's component ownership or turn security auditing into implementation.

## Guide map

| Task | Load |
| --- | --- |
| Build server/client route boundaries | [Guide01](guides/01-build-server-client-boundaries.md) |
| Implement reads, actions and HTTP handlers | [Guide02](guides/02-implement-loads-actions-and-routes.md) |
| Isolate private data and caching | [Guide03](guides/03-isolate-cache-and-private-data.md) |
| Qualify build and prepare provider handoff | [Guide04](guides/04-qualify-build-and-provider-handoff.md) |

[Source digest](references/research/distillation.md), [boundary record](templates/boundary-record.md), [bounded starter](templates/starter/README.md), [negative cases](examples/negative-cases.md), [reference index](references/REFERENCE.md).

## Related owners and host support

Resolve names through Core's selected-plugin registry before delegation. Use direct skill loading only when supported and report the absence of a native role. Never invent a callable agent from this source file. React owns component composition/state/testing; Impeccable owns UI design; existing selected auth/data/backend owners implement provider protocols and persistence. NextJS Security in code-audit-tools owns the framework audit; Core Security owns Ship Gate security. Provider deployment belongs to the selected Vercel/Cloudflare/platform owner. Provider absence is a handoff gap, not authority to configure one. SEO-AEO's Svelte scope is not a Next.js SEO capability; stop for an actual scoped owner when requested.

Skill spec-six and Claude/Cowork plugin-agent fields follow Queen's source format references. Cursor uses its curated name/description/model fields and does not enforce Claude tool allowlists. Codex needs parent-generated role wiring; these source files alone do not establish installed dispatch.

## Qualification limits

The pure policy exercise checks input/DTO mechanics only. Starter Next execution, TSX/typecheck/build, browser behavior, authorization and cache isolation remain NOT_RUN until observed in a real compatible application. Source packaging is not application delivery. Installation, accounts, credentials, settings, provider writes, deployment, publication and commit/push require their own task authorization.
