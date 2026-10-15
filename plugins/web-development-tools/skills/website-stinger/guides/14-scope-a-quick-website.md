# 14: Scope a quick website

Use for O062 and the existing `/build-quick-website` entry. Read this after principles and before legacy Phase 1. This guide supersedes full-app assumptions for the accepted quick-site branch. Supported implementer: SvelteKit Website owner. Another required framework needs its actual selected implementer, not a renamed template.

1. Record audience, pages, one conversion, supplied copy/brand/assets, editing owner, accessibility target, existing folder ownership, intended hosting and deadline in [scope worksheet](../templates/website-scope.md). Ask one batch only for decisions that change implementation. Do not invent a testimonial, form destination or approval.
2. Decide whether pages can be static. A brochure with owner-edited content can use build-time content. A server form action, authenticated route or per-request data needs a server runtime. Choose the adapter from the installed framework version and intended host; inspect manifest and lockfile before a version-sensitive command. See static and page options.
3. Apply the requirement matrix below. No managed editors means no CMS. No persisted business data means no Supabase or app_settings. An anonymous enquiry needs no end-user login. No accepted measurement goal means no GA4, attribution storage or experiment framework. No event consumer means no webhook. A static site using a provided contact link needs no fake lead endpoint. Provider destinations awaiting authorization remain explicitly unconnected.
4. Select phases in the canonical order `1 → 2 → 5 → 6 → 7 → 3 → 4 → 8 → 9 → 10 → 12 → 11`, retaining only applicable work. Mark each omitted phase with rationale and downstream effect. A quick static website can be a single SvelteKit application; apps/web remains an allowed folder, but pnpm workspace, apps/cms, database and auth are not required merely to produce one page.
5. Implement accepted pages with resolved Svelte/Impeccable/SEO specialists and disjoint ownership where host dispatch is available. Existing project scripts and approved dependencies govern checks. Source examples are not permission to install, commit or deploy.
6. Observe local build/check results, page links, mobile/desktop, keyboard, content/asset provenance and any actual form success/failure. Log pending browser/provider checks honestly. For static output, verify all accepted routes exist and publish latency is understood. Run Security then Quality and repository gate before an authorized commit.

| Requirement | Add | Exclude when absent |
|---|---|---|
| Non-developer editing | Payload branch, guide15 | CMS admin, CMS storage |
| Real persisted submission | Authorized destination, server action when required | DB, auth and mocked collection claims |
| Private visitor account | Auth owner and protected runtime | Login, account table |
| Accepted analytics goal | Selected provider, retention/consent decision | Tracking, attribution, A/B scaffolding |
| Blog with code-owned content | Static content/routes if requested | Upload admin, storage bucket |

Deliver local website, build report and scope worksheet. The duration depends on accepted pages, assets, integrations and checks; there is no guaranteed 45-minute finish. [Worked examples](../examples/scoped-website-outcomes.md).
