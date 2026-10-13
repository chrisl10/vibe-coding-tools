# website-stinger

The Stinger that equips `website-wasp-drone` to build production-grade SvelteKit + Payload CMS + Supabase websites from a brief.

## Choose the accepted outcome

- [Quick website](guides/14-scope-a-quick-website.md): one public SvelteKit application, add only required runtime services.
- [Independent Payload CMS](guides/15-build-an-independent-payload-cms.md): CMS content/access/API contract before product schema.
- [Scope worksheet](templates/website-scope.md), [CMS contract](templates/payload-content-contract.md), [constructed cases](examples/scoped-website-outcomes.md).
- [Fresh primary-source distillation](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/web-development-tools/skills/website-stinger/references/research/scoped-website/distilled.md): grounding and version conflicts.

The stack below describes the historical full-template branch. These outcome guides supersede unconditional database/auth/analytics and copied CMS access examples. Phase excludes require accepted rationale; absent proof stays pending or fail. No fixed build duration is promised.

## Stack

| Layer | Technology |
|---|---|
| Public site | SvelteKit (Svelte 5), Vercel |
| CMS (default) | Payload 3.x, self-hosted as Next.js on Vercel |
| CMS (fallback) | TypeScript-as-CMS data objects (no Payload) |
| Database | Supabase Postgres (dual namespace: `payload` + `public`) |
| Auth (end-users) | Supabase Auth + `hooks.server.ts` route guard |
| Auth (CMS editors) | Payload built-in auth |
| Styling | Tailwind v4 + shadcn-svelte + CSS custom properties |
| Animation | `svelte/transition`, `svelte/animate`, Svelte animation libraries |
| Dark mode | `mode-watcher` |
| Forms | superforms + Zod + SvelteKit form actions |
| Analytics | `@vercel/analytics`, GA4, Web Vitals |
| SEO | `seo-aeo-wasp-drone` (SvelteKit track) |

## Monorepo structure

```
<project-root>/
├── apps/
│   ├── web/          ← SvelteKit public site
│   └── cms/          ← Next.js + Payload admin (Payload-mode only)
├── packages/
│   └── payload-types/ ← shared generated types (optional)
├── supabase/          ← migrations and seed
├── pnpm-workspace.yaml
└── build-report.md
```

## Key architectural commitments (details in guides/00-principles.md)

1. **CMS mode is chosen once, at input time.** Payload default for content-heavy sites; TypeScript-as-CMS fallback for one-page lead-gen sites.
2. **Payload requires a Next.js host.** `apps/cms` is always a separate Vercel project, never embedded in SvelteKit.
3. **SvelteKit consumes Payload over REST only.** No Local API from SvelteKit.
4. **Dual Postgres namespace.** Payload owns `payload.*` tables; business data lives in `public.*`. Both share one Supabase project.
5. **RLS-first for public schema.** Every table in `public` has RLS enabled. The `payload` schema is not exposed to Supabase RLS (Payload uses server-side access control).
6. **Settings-driven configuration.** Runtime config lives in `app_settings` (Supabase). No deploys for config changes.
7. **Token-based design system.** All visual decisions as CSS custom properties. Dark mode via `mode-watcher` + `.dark` token inversion.

## Source PRDs

`research/source-prds/` contains the 12-phase source PRDs. Every guide traces claims back to these files.

For current scoped-outcome research, see [the local archive](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/web-development-tools/skills/website-stinger/references/research/scoped-website/distilled.md).

## Maintenance

- Every guide cites its source PRD.
- The 3 Svelte animation library sources referenced in guide 12: sv-animations.vercel.app, aceternity.sveltekit.io, animation-svelte.vercel.app.
- refresh-cadence: review source PRDs whenever SvelteKit, Payload, or Supabase ships a major version.
