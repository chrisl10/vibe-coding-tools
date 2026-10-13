# Next.js advisory table (affected and patched versions)

Generated from `next-advisories.json`, which is a normalized copy of the GitHub Security Advisories for `vercel/next.js` fetched 2026-09-30 ([raw/advisory--ghsa-index-vercel-next-js.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--ghsa-index-vercel-next-js.md)). Ranges: lower bound inclusive, upper bound exclusive (the first patched version). "not stated" means the advisory did not list a patched version at fetch time; never fill it in by guessing. "no patch in line" means the advisory lists no fix for that major line.

Newest releases at research time (npm, [raw/next--npm-dist-tags-2026-09-30.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--npm-dist-tags-2026-09-30.md)): 16.x `16.3.8`, 15.x `15.5.27`, 14.x `14.2.35` (unsupported), 13.x `13.5.11` (unsupported).

Labels: CVE-2025-29927 and everything published before 2025-09-30 is older than 12 months; it stays in the table because unpatched installs are still affected.

Preconditions are the codes the scan script evaluates (see `precondition_help` in the JSON). An advisory with an unmet precondition does not apply to the app.

| Published | GHSA | CVE | Sev | Title | Affected (lower) to first patched | Preconditions |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-30 | GHSA-h694-7cp9-m8p3 | - | medium | Cache leak across root param values in nested 'use cache' functions | 16.3.0 and later in line (patched version not stated) | cache_components |
| 2026-09-22 | GHSA-vcvr-r3jv-pc5j | CVE-2026-94545 | critical | Remote Code Execution in next/og ImageResponse (Node.js runtime) with attacker-controlled SVG values | 16.2.0 to 16.3.6 | next_og |
| 2026-09-30 | GHSA-3w37-wq28-93x7 | CVE-2026-94544 | medium | Pending 'use cache' fill can leak Draft Mode content into regular responses | 16.3.0 and later in line (patched version not stated) | cache_components, draft_mode |
| 2026-09-30 | GHSA-cjq9-62q9-8jv4 | CVE-2026-94483 | high | Server-Side Request Forgery in Image Optimization through allow-listed remote hosts | 16.0.0 and later in line (patched version not stated) | image_remote_patterns |
| 2026-09-30 | GHSA-39w2-rjm5-chcv | CVE-2026-94486 | low | Information disclosure in the development server's MCP endpoint (next dev only) | 16.0.0 and later in line (patched version not stated) | dev_only |
| 2026-09-30 | GHSA-4jqv-mc3x-m676 | CVE-2026-94543 | medium | Cache poisoning of SSG and ISR pages in self-hosted Pages Router apps | 15.0.0 and later in line (patched version not stated); 16.0.0 and later in line (patched version not stated) | pages_router, self_hosted |
| 2026-09-30 | GHSA-mcj8-r9mp-w47p | CVE-2026-94484 | medium | Cache poisoning in SSG/ISR rendering with a root-level catch-all page | 15.0.0 and later in line (patched version not stated); 16.0.0 and later in line (patched version not stated) | root_catch_all |
| 2026-09-30 | GHSA-f87g-xv8r-7p7x | CVE-2026-94485 | medium | Metadata image routes ignore dynamicParams (webpack builds) | 16.0.0 and later in line (patched version not stated) | app_router, webpack_build, metadata_image_routes |
| 2026-08-25 | GHSA-2xp9-vwfh-vxw4 | - | critical | Unauthenticated Remote Code Execution in Image Optimization API when AVIF files are optimized | 10.0.0 to 15.5.24; 16.0.0 to 16.3.3 | image_optimizer, avif_input |
| 2026-08-25 | GHSA-p293-qw3h-jr36 | CVE-2026-75604 | critical | Unauthenticated Remote Code Execution on Windows-hosted servers | 13.4.0 to 15.5.24; 16.0.0 to 16.3.3 | windows_host |
| 2026-07-21 | GHSA-p9j2-gv94-2wf4 | CVE-2026-64645 | high | SSRF in rewrites (and open redirect in redirects) via attacker-controlled destination hostname | 12.0.0 to 15.5.21; 16.0.0 to 16.2.11 | rewrites_dynamic_host |
| 2026-07-21 | GHSA-4c39-4ccg-62r3 | CVE-2026-64646 | medium | Unbounded Server Action payload in Edge runtime | 13.0.0 to 15.5.21; 16.0.0 to 16.2.11 | server_actions, edge_runtime |
| 2026-07-21 | GHSA-89xv-2m56-2m9x | CVE-2026-64649 | high | SSRF in Server Actions on custom servers when the Host header is not pinned | 14.1.1 to 15.5.21; 16.0.0 to 16.2.11 | server_actions, custom_server_or_unpinned_host |
| 2026-07-21 | GHSA-68g3-v927-f742 | CVE-2026-64648 | medium | Cache confusion of response bodies for requests with bodies | 13.0.0 to 15.5.21; 16.0.0 to 16.2.11 | - |
| 2026-07-21 | GHSA-6gpp-xcg3-4w24 | CVE-2026-64642 | high | Middleware / Proxy bypass in App Router apps built with Turbopack and a single i18n locale | 16.0.0 to 16.2.11 | app_router, middleware, i18n_single_locale, turbopack_build |
| 2026-07-21 | GHSA-m99w-x7hq-7vfj | CVE-2026-64641 | high | Denial of Service in App Router using Server Actions | 13.0.0 to 15.5.21; 16.0.0 to 16.2.11 | app_router, server_actions |
| 2026-07-21 | GHSA-4633-3j49-mh5q | CVE-2026-64647 | medium | Cache confusion of response bodies for requests with invalid UTF-8 bodies | 13.0.0 to 15.5.21; 16.0.0 to 16.2.11 | - |
| 2026-07-21 | GHSA-q8wf-6r8g-63ch | CVE-2026-64644 | medium | Denial of Service in the Image Optimization API using SVGs | 15.5.0 to 15.5.21; 16.0.0 to 16.2.11 | image_optimizer |
| 2026-07-21 | GHSA-955p-x3mx-jcvp | CVE-2026-64643 | medium | Unauthenticated disclosure of internal Server Function endpoints | 13.0.0 to 15.5.21; 16.0.0 to 16.2.11 | app_router, server_actions |
| 2026-05-07 | GHSA-26hh-7cqf-hhc6 | CVE-2026-45109 | high | Middleware / Proxy bypass via segment-prefetch routes (incomplete fix follow-up) | 15.2.0 to 15.5.18; 16.0.0 to 16.2.6 | app_router, middleware |
| 2026-05-06 | GHSA-267c-6grr-h53f | CVE-2026-44575 | high | Middleware / Proxy bypass in App Router applications via segment-prefetch routes | 15.2.0 to 15.5.16; 16.0.0 to 16.2.5 | app_router, middleware |
| 2026-05-06 | GHSA-ffhc-5mcf-pf4q | CVE-2026-44581 | medium | Cross-site scripting in App Router applications using CSP nonces behind shared caches | 13.4.0 to 15.5.16; 16.0.0 to 16.2.5 | app_router, csp_nonce |
| 2026-05-06 | GHSA-vfv6-92ff-j949 | CVE-2026-44582 | low | Cache poisoning via collisions in React Server Component cache-busting | 13.4.6 to 15.5.16; 16.0.0 to 16.2.5 | app_router |
| 2026-05-06 | GHSA-gx5p-jg67-6x7h | CVE-2026-44580 | medium | Cross-site scripting in beforeInteractive scripts with untrusted input | 13.0.0 to 15.5.16; 16.0.0 to 16.2.5 | before_interactive |
| 2026-05-06 | GHSA-mg66-mrh9-m8jx | CVE-2026-44579 | high | Denial of Service via connection exhaustion in applications using Cache Components | 15.0.0 to 15.5.16; 16.0.0 to 16.2.5 | cache_components |
| 2026-05-06 | GHSA-492v-c6pp-mqqv | CVE-2026-44574 | high | Middleware / Proxy bypass through dynamic route parameter injection | 15.4.0 to 15.5.16; 16.0.0 to 16.2.5 | middleware, dynamic_routes |
| 2026-05-06 | GHSA-h64f-5h5j-jqjh | CVE-2026-44577 | medium | Denial of Service in the Image Optimization API | 10.0.0 to 15.5.16; 16.0.0 to 16.2.5 | image_optimizer |
| 2026-05-06 | GHSA-c4j6-fc7j-m34r | CVE-2026-44578 | high | SSRF via WebSocket upgrade requests on self-hosted built-in Node server | 13.4.13 to 15.5.16; 16.0.0 to 16.2.5 | self_hosted |
| 2026-05-06 | GHSA-wfc6-r584-vfw7 | CVE-2026-44576 | medium | Cache poisoning in React Server Component responses | 14.2.0 to 15.5.16; 16.0.0 to 16.2.5 | app_router |
| 2026-05-06 | GHSA-36qx-fr4f-26g5 | CVE-2026-44573 | high | Middleware / Proxy bypass in Pages Router applications using i18n (locale-less _next/data requests) | 12.2.0 to 15.5.16; 16.0.0 to 16.2.5 | pages_router, i18n, middleware |
| 2026-05-06 | GHSA-8h8q-6873-q5fj | CVE-2026-23870 | high | Denial of Service with Server Components | 13.0.0 to 15.5.16; 16.0.0 to 16.2.5 | app_router |
| 2026-05-06 | GHSA-3g8h-86w9-wvmq | CVE-2026-44572 | low | Middleware / Proxy redirects can be cache-poisoned | 12.2.0 to 15.5.16; 16.0.0 to 16.2.5 | middleware |
| 2026-04-08 | GHSA-q4gf-8mx6-v5v3 | CVE-2026-23869 | high | Denial of Service with Server Components | 13.0.0 to 15.5.15; 16.0.0 to 16.2.3 | app_router |
| 2026-03-16 | GHSA-3x4c-7xq6-9pq8 | CVE-2026-27980 | medium | Unbounded next/image disk cache growth can exhaust storage | 10.0.0 to 15.5.14; 16.0.0 to 16.1.7 | image_optimizer, self_hosted |
| 2026-03-16 | GHSA-mq59-m269-xvcx | CVE-2026-27978 | medium | Origin null can bypass Server Actions CSRF checks | 16.0.1 to 16.1.7 | server_actions |
| 2026-03-16 | GHSA-jcc7-9wpm-mj36 | CVE-2026-27977 | medium | Origin null can bypass allowedDevOrigins for internal dev endpoints (next dev only) | 16.0.1 to 16.1.7 | dev_only |
| 2026-03-16 | GHSA-h27x-g6w4-24gq | CVE-2026-27979 | medium | Unbounded postponed resume buffering can lead to DoS | 16.1.0 to 16.1.7 | cache_components |
| 2026-03-16 | GHSA-ggv3-7p47-pfv8 | CVE-2026-29057 | medium | HTTP request smuggling in rewrites | 9.5.0 to 15.5.13; 16.0.0 to 16.1.7 | rewrites |
| 2026-01-26 | GHSA-9g9p-9gw9-jx7f | CVE-2025-59471 | medium | Denial of Service in Image Optimizer | 10.0.0 to 15.0.0 (no patch in line); 15.0.0 to 15.5.10; 16.0.0 to 16.1.5 | image_optimizer |
| 2026-01-26 | GHSA-5f7q-jpqc-wp7h | CVE-2025-59472 | medium | Denial of Service in Partial Pre Rendering | 16.1.0 to 16.1.5 | cache_components |
| 2026-01-26 | GHSA-h25m-26qc-wcjf | CVE-2026-23864 | high | Denial of Service with Server Components | 13.0.0 to 15.0.0 (no patch in line); 15.0.0 to 15.0.8; 15.1.0 to 15.1.12; 15.2.0 to 15.2.9; 15.3.0 to 15.3.9; 15.4.0 to 15.4.11; 15.5.0 to 15.5.10; 16.0.0 to 16.0.11; 16.1.0 to 16.1.5 | app_router |
| 2025-12-11 | GHSA-5j59-xgg2-r9c4 | CVE-2025-67779 | high | Denial of Service with Server Components (incomplete fix follow-up) | 13.3.0 to 14.0.0 (no patch in line); 14.0.0 to 14.2.35; 15.0.0 to 15.0.7; 15.1.0 to 15.1.11; 15.2.0 to 15.2.8; 15.3.0 to 15.3.8; 15.4.0 to 15.4.10; 15.5.0 to 15.5.9; 16.0.0 to 16.0.10 | app_router |
| 2025-12-11 | GHSA-w37m-7fhw-fmv9 | CVE-2025-55183 | medium | Server Actions source code exposure | 15.0.0 to 15.0.6; 15.1.0 to 15.1.10; 15.2.0 to 15.2.7; 15.3.0 to 15.3.7; 15.4.0 to 15.4.9; 15.5.0 to 15.5.8; 16.0.0 to 16.0.9 | app_router, server_actions |
| 2025-12-11 | GHSA-mwv6-3258-q52c | CVE-2025-55184 | high | Denial of Service with Server Components | 13.3.0 to 14.0.0 (no patch in line); 14.0.0 to 14.2.34; 15.0.0 to 15.0.6; 15.1.0 to 15.1.10; 15.2.0 to 15.2.7; 15.3.0 to 15.3.7; 15.4.0 to 15.4.9; 15.5.0 to 15.5.8; 16.0.0 to 16.0.9 | app_router |
| 2025-12-03 | GHSA-9qr9-h5gf-34mp | CVE-2025-55182 | critical | Remote code execution in React Server Components (React2Shell); Next.js alias CVE-2025-66478 (rejected as duplicate) | 15.0.0 to 15.0.5; 15.1.0 to 15.1.9; 15.2.0 to 15.2.6; 15.3.0 to 15.3.6; 15.4.0 to 15.4.8; 15.5.0 to 15.5.7; 16.0.0 to 16.0.7 | app_router |
| 2025-08-29 | GHSA-4342-x723-ch2f | CVE-2025-57822 | medium | Improper middleware redirect handling leads to SSRF | 0.0.0 to 14.2.32; 15.0.0 to 15.4.7 | middleware |
| 2025-08-29 | GHSA-xv57-4mr9-wg8v | CVE-2025-55173 | medium | Content injection for Image Optimization | 0.0.0 to 14.2.31; 15.0.0 to 15.4.5 | image_optimizer |
| 2025-08-29 | GHSA-g5qg-72qw-gw5v | CVE-2025-57752 | medium | Cache key confusion for Image Optimization API routes | 0.0.0 to 14.2.31; 15.0.0 to 15.4.5 | image_optimizer |
| 2025-07-03 | GHSA-r2fc-ccr8-96c4 | CVE-2025-49005 | low | Cache poisoning due to omission of Vary header | 15.3.0 to 15.3.3 | app_router |
| 2025-07-03 | GHSA-67rr-84xm-4c7r | CVE-2025-49826 | high | DoS via cache poisoning | 15.0.5 to 15.2.0 | - |
| 2025-05-14 | GHSA-qpjv-v59x-3qc4 | CVE-2025-32421 | low | Race condition to cache poisoning | 0.0.0 to 14.2.24; 15.0.1 to 15.1.6 | - |
| 2025-04-02 | GHSA-223j-4rm8-mrmf | CVE-2025-30218 | low | x-middleware-subrequest-id may be leaked to external hosts | 12.0.0 to 12.3.6; 13.0.0 to 13.5.10; 14.0.0 to 14.2.26; 15.0.0 to 15.2.4 | middleware |
| 2025-03-21 | GHSA-f82v-jwr5-mffw | CVE-2025-29927 | critical | Authorization bypass in Next.js Middleware via the x-middleware-subrequest header | 11.1.4 to 12.3.5; 13.0.0 to 13.5.9; 14.0.0 to 14.2.25; 15.0.0 to 15.2.3 | middleware |
| 2025-05-28 | GHSA-3h52-269p-cp9r | CVE-2025-48068 | low | Information exposure in dev server due to lack of origin verification (next dev only) | 13.0.0 to 14.2.30; 15.0.0 to 15.2.2 | dev_only |
| 2025-01-03 | GHSA-7m27-7ghc-44w9 | CVE-2024-56332 | medium | Denial of Service with Server Actions | 13.0.0 to 13.5.8; 14.0.0 to 14.2.21; 15.0.0 to 15.1.1 | server_actions |
| 2024-12-17 | GHSA-7gfc-8cq8-jh5f | CVE-2024-51479 | high | Authorization bypass in Next.js | 9.5.5 to 14.2.15 | middleware |
| 2024-10-14 | GHSA-g77x-44xx-532m | CVE-2024-47831 | medium | Denial of Service in image optimization | 10.0.0 to 14.2.7 | image_optimizer |
| 2024-09-17 | GHSA-gp8f-8m3g-qvj9 | CVE-2024-46982 | high | Cache poisoning | 13.5.1 to 13.5.7; 14.0.0 to 14.2.10 | - |
| 2024-07-10 | GHSA-fq54-2j52-jc42 | CVE-2024-39693 | high | Denial of Service condition | 13.3.1 to 13.5.0 | - |
| 2024-05-09 | GHSA-77r5-gw3j-2mpf | CVE-2024-34350 | high | HTTP request smuggling | 13.4.0 to 13.5.1 | rewrites |
| 2024-05-09 | GHSA-fr5h-rqp8-mj6g | CVE-2024-34351 | high | SSRF in Server Actions | 13.4.0 to 14.1.1 | server_actions |

## Reading the table quickly

- On 16.x: anything below 16.3.6 is exposed to at least one critical advisory (next/og RCE needs Node `ImageResponse`; AVIF and Windows RCEs are fixed in 16.3.3). 16.3.8 still matches the 2026-09-30 advisories whose fix version was not stated.
- On 15.x: anything below 15.5.24 is exposed to the AVIF optimizer RCE and the Windows RCE; anything below 15.5.7 (or its per-minor equivalent) is exposed to React2Shell (CVE-2025-55182); anything below 15.2.3 is exposed to CVE-2025-29927.
- On 14.x and 13.x: the 2026 advisories list no patch. The fix is a major upgrade.

Sources: [raw/advisory--ghsa-index-vercel-next-js.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--ghsa-index-vercel-next-js.md), [raw/next--npm-dist-tags-2026-09-30.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--npm-dist-tags-2026-09-30.md), [raw/next--support-policy.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--support-policy.md).
