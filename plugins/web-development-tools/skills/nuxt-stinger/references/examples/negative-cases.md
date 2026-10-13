# Negative cases and required rejection

These are source review cases, not executed app tests.

| Case | Required outcome | App evidence |
|---|---|---|
| Static-only deployment with private Nitro API | Flag missing server runtime, require accepted host/model | NOT_RUN |
| SSR chosen for every page because content exists | Require per-route product/freshness rationale | NOT_RUN |
| Module-scoped ref holds current account | Reject cross-request mutable state | NOT_RUN |
| Same async key returns differing locale/tenant DTO | Require distinct identity, permissions and principal-change eviction | NOT_RUN |
| Route middleware guards page, API lacks session check | Reject direct API exposure | NOT_RUN |
| Valid session accesses another tenant by query parameter | Require server-derived tenant and resource authorization | NOT_RUN |
| /** swr rule includes account or login | Disable private scope caching; audit exact roots and descendants | NOT_RUN |
| private,no-store header wraps defineCachedEventHandler | Reject blanket safety claim; inspect wrapper storage/CDN | NOT_RUN |
| runtimeConfig.public contains backendSecret | Reject browser secret exposure; inspect payload/build | NOT_RUN |
| useFetch forwards cookies to arbitrary upstream | Use accepted trusted adapter and owner review | NOT_RUN |
| Latest Nitro API copied into older Nuxt lockfile | Verify resolved major and correct API | NOT_RUN |
| Passing Node syntax means app hydration/auth is verified | Reject evidence substitution | NOT_RUN |
