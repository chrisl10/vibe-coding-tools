# 04. Data exposure and caching

Goal: find private data that reaches the browser or reaches the wrong user, through props, bundles, static output, or caches. Loads [../references/checks-data-exposure-and-caching.md](../references/checks-data-exposure-and-caching.md) (NX-DATA-01 to 05, NX-CACHE-01 to 04).

## Steps

1. **Secrets first (NX-DATA-03).** Review `suspicious_next_public_names[]`, `hardcoded_secret_candidates[]`, `service_role_refs[]`, and tracked env files (`git ls-files | rg '\.env'`). `NEXT_PUBLIC_` values are inlined into the client bundle at build time [raw/next--source-maps-powered-by-env-vars.md]. If a `.next/` build directory already exists in the repo checkout, grep `.next/static` read-only for the same names and key prefixes: that is what ships. Redact every value to its first 4 characters plus `****` (contract rule 2). Separate public-by-design keys (Supabase publishable or anon, Stripe `pk_`, analytics ids) from real secrets.

2. **Server to client props (NX-DATA-01).** For each `'use client'` component that takes an object prop named like a model (`user`, `account`, `order`), find the Server Component that renders it and the query feeding it. Confirm which columns reach the prop. The docs call passing the whole row "EXPOSED" [raw/next--data-security-guide.md].

3. **Server-only boundaries (NX-DATA-02).** Check `client_files_importing_db[]`, `client_files_reading_private_env[]`, and whether DAL modules import `server-only` (`server_only_imports` count versus number of data modules).

4. **Source maps (NX-DATA-04).** `next_config.production_browser_source_maps` [raw/next--source-maps-powered-by-env-vars.md].

5. **Taint (NX-DATA-05).** If taint APIs are used, look for spreads or clones of tainted objects passed to clients [raw/react--taint-apis.md].

6. **Caches (NX-CACHE-01).** For each entry in `use_cache[]` and `unstable_cache[]`, read the function: does its result depend on the user, and is the user (or tenant) an argument or a captured variable that changes per user? `use cache` output is reused across requests and cannot read cookies or headers inside [raw/next--use-cache-and-unstable-cache.md]. For `unstable_cache`, check that every closure that identifies the user is in `keyParts`. Also check `fetch(..., { cache: 'force-cache' })` and `next: { revalidate }` calls that send per-user cookies or Authorization headers.

7. **Static output (NX-CACHE-02).** For `generate_static_params_files[]`, `force-static` pages, `revalidate` exports, and Pages Router `getStaticProps`, check what data the build fetches. Static output is the same for every visitor [raw/next--generate-static-params-and-dynamic-params.md] [raw/next--authentication-guide.md]. Note `dynamicParams` settings; metadata image routes ignored `dynamicParams` on webpack builds before the 2026-09-30 fix (CVE-2026-94485) [raw/advisory--2026-rewrites-ssrf-and-other.md].

8. **Open cache advisories (NX-CACHE-03)** when Cache Components or Draft Mode are in use on 16.3.x [raw/advisory--2026-cache-poisoning-and-cache-leaks.md].

9. **Shared cache headers (NX-CACHE-04).** Grep for `Cache-Control` with `public` or `s-maxage` on responses that vary by user.

10. **Sweep AI patterns** AI-04, AI-06, AI-07, AI-20 from [../references/ai-failure-patterns.md](../references/ai-failure-patterns.md), then write findings per guide 06.

## Sources

[raw/next--data-security-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--data-security-guide.md), [raw/next--source-maps-powered-by-env-vars.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--source-maps-powered-by-env-vars.md), [raw/react--taint-apis.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/react--taint-apis.md), [raw/next--use-cache-and-unstable-cache.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--use-cache-and-unstable-cache.md), [raw/next--generate-static-params-and-dynamic-params.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--generate-static-params-and-dynamic-params.md), [raw/next--authentication-guide.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--authentication-guide.md), [raw/advisory--2026-cache-poisoning-and-cache-leaks.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-cache-poisoning-and-cache-leaks.md), [raw/advisory--2026-rewrites-ssrf-and-other.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-rewrites-ssrf-and-other.md).
