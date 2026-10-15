---
description: "Build a scoped SaaS foundation joining tenant identity, data isolation, billing entitlements and a verified user journey."
argument-hint: "[product/repository] [outcome and constraints]"
---

# /build-saas-foundation

## Mandatory process

1. Load the installed `pest-controller-suit` Core skill and consult its roster before making any routing decision. This is the first instruction, always, no exceptions. Source work resolves component ownership from root `plugin-catalog.json`; installed work uses Core's explicit selected-plugin registry and resolver. Missing Core blocks routing. Load each selected pair's Stinger and required guides before work, and verify actual host tools/delegation. Cached files do not prove selection. Dispatch registered Drones at top level only when delegation is authorized; otherwise execute the selected paired procedure directly and report that fallback truthfully. No invented roles or nested dispatch.

2. Confirm the accepted first-version PRD, chosen frontend/backend/provider architecture, tenant and membership model, billing unit, plan/entitlement rules, environment and authorized local implementation scope. Existing stack decisions are inputs; do not silently migrate them. Price changes, live resources and deployment remain owner actions.
3. Resolve UI/runtime implementation owners from actual selected skills. svelte-wasp-drone handles Svelte/SvelteKit behavior; react-wasp-drone handles React architecture; nextjs-wasp-drone handles Next.js server, client, data and cache boundaries; nuxt-wasp-drone handles Nuxt/Nitro; vue-wasp-drone handles Vue components and routing. For other stacks require a real scoped backend/runtime owner. WorkOS and Neon/Drizzle pairs activate only for those chosen providers. A chosen stack whose owner is not selected is an explicit dependency, not a role invented by this command.
4. Have library-wasp-drone specify the tenant/account/member/subscription/entitlement lifecycle and one complete onboarding-to-paid-feature path. contract-writing-wasp-drone defines actor/tenant authorization, billing-event projection, entitlement transitions, errors and replay semantics. Library pins identical accepted CTR revisions for provider and consumer requirements before dependent work.
5. Sequence schema/data isolation with db-wasp-drone (neon-drizzle-wasp-drone for chosen Neon/Drizzle depth), identity with auth-wasp-drone (WorkOS depth conditional), and billing with payments-wasp-drone only within its verified SvelteKit/Stripe scope. A non-Svelte Stripe adapter needs an actual implementer; payments expertise does not silently supply it. Use separate ownership for these providers and the UI consumer.
6. Implement tenant-scoped persistence and server-enforced entitlements. Verify denied cross-tenant access for read/write/search, role removal, anonymous access and privileged service scope. For billing verify raw-body signature validation, duplicate/reordered/retried events, durable deduplication, customer-to-tenant mapping, and entitlement grant/revoke/failure reconciliation. A client return page is not a payment grant. Use approved test environment and fixtures; do not create live products/prices or charge money.
7. Join providers to the user journey after their contract checks pass. Verify failed checkout, pending payment, membership loss and webhook delay visibly and honestly. Keep billing records and actor authority distinct; a paid customer cannot choose another tenant in the client request.
8. Run affected implementation checks, then Security, then Quality against the PRD and contract pins, then orchestrator Repository Health. Deliver source paths, schema/auth/billing/UI ownership, exact evidence, unresolved dependencies and environment/provider limitations. No green-shard or browser mock alone proves end-to-end SaaS readiness.

## Selected-owner map

| Capability | Catalog owner | Activation |
|---|---|---|
| `pest-controller-suit` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `library-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `contract-writing-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `security-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `quality-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `github-repo-health-stinger` | `wasp-nest-core` | Required Core procedure/review where applicable |
| `svelte-stinger` | `web-development-tools` | Required for its chosen branch; do not imply sibling selection |
| `react-stinger` | `web-development-tools` | Required for its chosen branch; do not imply sibling selection |
| `nextjs-stinger` | `web-development-tools` | Required for its chosen branch; do not imply sibling selection |
| `nuxt-stinger` | `web-development-tools` | Required for its chosen branch; do not imply sibling selection |
| `vue-stinger` | `web-development-tools` | Required for its chosen branch; do not imply sibling selection |
| `auth-stinger` | `platform-and-release-tools` | Required for its chosen branch; do not imply sibling selection |
| `workos-stinger` | `platform-and-release-tools` | Required for its chosen branch; do not imply sibling selection |
| `payments-stinger` | `platform-and-release-tools` | Required for its chosen branch; do not imply sibling selection |
| `db-stinger` | `data-and-ai-tools` | Required for its chosen branch; do not imply sibling selection |
| `neon-drizzle-stinger` | `data-and-ai-tools` | Required for its chosen branch; do not imply sibling selection |

## Inputs and host qualification

Use trailing invocation text exposed by the actual host; `$ARGUMENTS` is supported only where documented. Reuse answered inputs and accepted decisions. Ask one concrete batch for unresolved material inputs before dependent work, while continuing independent authorized work. Claude/Cowork uses the owner flat command, Cursor its generated command projection, and Codex the owner's generated `source-command-build-saas-foundation` skill. Source generation is not installation, role discovery, or runtime proof. Resolve all resources against the selected carrier root. A missing required owner blocks its dependent boundary and is named in the report; optional branches require only their own selected dependencies.

## Output contract

Write advisory evidence to the receiving repository's `library/requirements/reports/build-saas-foundation/<date>-report.md` when local artifact writing is authorized, or return the same fields in the response. Library owns any PRD at its current Schema v2 path; never create a competing plan folder or overwrite another agent's active artifact.

Report status, selected owner/version and paired procedure, concrete artifacts, accepted contract pins, actual checks and their results, evidence limits, unfinished boundaries and the smallest unresolved user decision. Keep source/static checks, mock/browser behavior, native execution, packaged artifacts and provider evidence separate. Permission to create a source workflow does not authorize installation, provider writes, credentials, spend, commits, push or publication.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
