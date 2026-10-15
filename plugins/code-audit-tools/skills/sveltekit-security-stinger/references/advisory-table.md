# Advisory table: svelte, @sveltejs/kit, devalue, adapters

Generated 2026-09-30 from `scripts/advisories.json`, which `scripts/sveltekit_audit_scan.py` reads. Sources: raw/advisory--github-advisory-db-svelte-ecosystem.md, raw/advisory--kit-repo-advisories.md, raw/advisory--svelte-repo-advisories.md, raw/advisory--devalue-repo-advisories.md.

Rules for using this table:

- Compare the version resolved in the lockfile, never the range in `package.json`.
- Ranges are exactly as published. "Severity" is the GitHub-reviewed value where one exists; "Maint." is the maintainer's value on the repository advisory.
- "Precondition" is what the app must do for the flaw to be reachable. A version match without the precondition is reported at `possible` confidence, capped at `medium` (contract rule 5.3).
- If the audit date is more than 30 days after 2026-09-30, refresh: `gh api /repos/sveltejs/kit/security-advisories` (and svelte, devalue) plus `gh api '/advisories?ecosystem=npm&affects=<pkg>'`, then update `scripts/advisories.json`. Never add an entry you did not fetch.
- Adapters with no published advisories on 2026-09-30: adapter-cloudflare, adapter-netlify, adapter-static, adapter-auto; also vite-plugin-svelte and mdsvex.

## @sveltejs/kit

| GHSA | CVE | Severity | Maint. | Published | Affected | Patched | Precondition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GHSA-29g2-3rmr-qm68 | CVE-2026-66062 | medium | medium | 2026-08-07 | <= 2.70.1 | 2.70.2 | Any app; crafted Accept header causes CPU exhaustion when platform header-length limits are raised or absent. |
| GHSA-866w-xmhq-wj7x |  | medium | medium | 2026-07-24 | <= 2.69.0 | 2.69.1 | Uses remote form functions with a file input and accepts user-controlled field path names. |
| GHSA-wqjv-9729-c5q2 |  | medium | medium | 2026-07-24 | <= 2.69.0 | 2.69.1 | Uses remote form functions; very large payloads can crash the Node process. |
| GHSA-hgv7-v322-mmgr |  | medium | medium | 2026-05-21 | >= 2.38.0, <= 2.60.0 | 2.60.1 | Uses query.batch; rare timing can merge concurrent requests from different users (cross-user data disclosure). |
| GHSA-3f6h-2hrp-w5wx | CVE-2026-40074 | medium | medium | 2026-04-10 | <= 2.57.0 | 2.57.1 | Calls redirect() inside the handle hook with a location containing characters invalid in an HTTP header, worst when the location is user input. |
| GHSA-2crg-3p73-43xp | CVE-2026-40073 | high | medium | 2026-04-10 | <= 2.57.0 | 2.57.1 | Runs on adapter-node and relies on BODY_SIZE_LIMIT (chunked requests could bypass it). Limits enforced at WAF, gateway, or platform are unaffected. |
| GHSA-fpg4-jhqr-589c |  | low | low | 2026-02-28 | >= 2.49.0, <= 2.53.2 | 2.53.3 | experimental.remoteFunctions plus form, and processes the files array without checking count or size. |
| GHSA-88qp-p4qg-rqm6 |  | medium | medium | 2026-02-19 | >= 2.49.0, <= 2.52.1 | 2.52.2 | experimental.remoteFunctions plus form. |
| GHSA-vrhm-gvg7-fpcf |  | medium | medium | 2026-02-19 | >= 2.49.0, <= 2.52.1 | 2.52.2 | experimental.remoteFunctions plus form. |
| GHSA-j2f3-wq62-6q46 | CVE-2026-22803 | high | high | 2026-01-15 | >= 2.49.0, <= 2.49.4 | 2.49.5 | Uses the experimental form remote function (binary application/x-sveltekit-formdata payload). |
| GHSA-j62c-4x62-9r35 | CVE-2025-67647 | high | high | 2026-01-15 | >= 2.19.0, <= 2.49.4 | 2.49.5 | At least one prerendered route (DoS from 2.44.0). DoS plus SSRF from 2.19.0 when also on adapter-node without ORIGIN set and without a proxy that validates Host. |
| GHSA-6q87-84jw-cjhp | CVE-2025-32388 | medium | medium | 2025-04-14 | >= 2.0.0, < 2.20.6 | 2.20.6 | A server load function iterates over all entries of event.url.searchParams. |
| GHSA-rjjv-87mx-6x3h | CVE-2024-53261 | low | low | 2024-11-25 | < 2.8.3 | 2.8.3 | Dev server only (dev mode 404 page). |
| GHSA-mh2x-fcqh-fmqv | CVE-2024-53262 | low | low | 2024-11-25 | < 2.8.3 | 2.8.3 | App passes user-controlled content into error() messages that reach the static error.html fallback. |
| GHSA-g5m6-hxpp-fc49 | CVE-2024-23641 | high | high | 2024-01-24 | >= 2.0.0, < 2.4.3 | 2.4.3 | adapter-node or preview; a GET or HEAD request with a body crashes the server. |
| GHSA-gv7g-x59x-wf8f | CVE-2023-29008 | high | medium | 2023-04-07 | < 1.15.2 | 1.15.2 | SvelteKit 1 CSRF check bypass with upper-cased Content-Type. |
| GHSA-5p75-vc5g-8rv2 | CVE-2023-29003 | high | critical | 2023-04-04 | < 1.15.1 | 1.15.1 | SvelteKit 1 CSRF check bypass with a different Content-Type (text/plain, PUT, PATCH, DELETE). |

## @sveltejs/adapter-node

| GHSA | CVE | Severity | Maint. | Published | Affected | Patched | Precondition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GHSA-j62c-4x62-9r35 | CVE-2025-67647 | high | high | 2026-01-15 | >= 5.4.1, <= 5.5.0 | 5.5.1 | At least one prerendered route (DoS from 2.44.0). DoS plus SSRF from 2.19.0 when also on adapter-node without ORIGIN set and without a proxy that validates Host. |
| GHSA-g5m6-hxpp-fc49 | CVE-2024-23641 | high | high | 2024-01-24 | >= 2.0.0, < 2.1.2 | 2.1.2 | adapter-node or preview; a GET or HEAD request with a body crashes the server. |
| GHSA-g5m6-hxpp-fc49 | CVE-2024-23641 | high | high | 2024-01-24 | >= 3.0.0, < 3.0.3 | 3.0.3 | adapter-node or preview; a GET or HEAD request with a body crashes the server. |
| GHSA-g5m6-hxpp-fc49 | CVE-2024-23641 | high | high | 2024-01-24 | = 4.0.0 | 4.0.1 | adapter-node or preview; a GET or HEAD request with a body crashes the server. |

## @sveltejs/adapter-vercel

| GHSA | CVE | Severity | Maint. | Published | Affected | Patched | Precondition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GHSA-9pq4-5hcf-288c | CVE-2026-27118 | medium | medium | 2026-02-19 | < 6.3.2 | 6.3.2 | Deployed with adapter-vercel; an internal ISR query parameter on all routes lets an attacker get user-specific responses cached for others. Victim must click an attacker link while signed in. |

## svelte

| GHSA | CVE | Severity | Maint. | Published | Affected | Patched | Precondition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GHSA-f3cj-j4f6-wq85 |  | medium | medium | 2026-05-14 | >= 5.46.0, <= 5.55.6 | 5.55.7 | Uses experimental hydratable with attacker-controlled input where a synchronous value is hydrated, then a promise value. |
| GHSA-rcqx-6q8c-2c42 | CVE-2026-42573 | medium | medium | 2026-05-14 | <= 5.55.6 | 5.55.7 | Attribute spreading on a form element plus spreading or a dynamic name on an input or button inside it, both user-controllable. |
| GHSA-9rmh-mm8f-r9h6 | CVE-2026-42567 | medium | medium | 2026-05-14 | >= 5.51.5, <= 5.55.6 | 5.55.7 | svelte:element with a tag of unconstrained length. |
| GHSA-pr6f-5x2q-rwfp | CVE-2026-42599 | medium | medium | 2026-05-14 | <= 5.55.6 | 5.55.7 | Spreads user-controlled or external data as element attributes (SSR); event handler props reach HTML. |
| GHSA-qgvg-pr8v-6rr3 | CVE-2026-27902 | medium | medium | 2026-02-26 | >= 5.53.0, < 5.53.5 | 5.53.5 | Attacker-controlled content returned from transformError (error boundaries). |
| GHSA-phwv-c562-gvmh | CVE-2026-27901 | medium | medium | 2026-02-26 | <= 5.53.4 | 5.53.5 | contenteditable with bind:innerText or bind:textContent initialised from untrusted data on the server. |
| GHSA-crpf-4hrx-3jrp | CVE-2026-27125 | medium | medium | 2026-02-19 | <= 5.51.4 | 5.51.5 | SSR attribute spreading when Object.prototype is already polluted elsewhere. |
| GHSA-m56q-vw4c-c2cp | CVE-2026-27122 | medium | medium | 2026-02-19 | <= 5.51.4 | 5.51.5 | svelte:element this={tag} with an untrusted tag string (SSR). |
| GHSA-f7gr-6p89-r883 | CVE-2026-27121 | medium | medium | 2026-02-19 | <= 5.51.4 | 5.51.5 | Spreads untrusted data as element attributes during SSR. |
| GHSA-h7h7-mm68-gmrc | CVE-2026-27119 | medium | medium | 2026-02-19 | >= 5.39.3, < 5.51.5 | 5.51.5 | SSR of an option element whose content is untrusted. |
| GHSA-gw32-9rmw-qwww |  | high | high | 2026-01-16 | >= 3.0.0, < 3.59.2 | 3.59.2 | Svelte 3 SSR textarea bind:value filled by user content. |
| GHSA-6738-r8g5-qwp3 | CVE-2025-15265 | medium | medium | 2026-01-15 | >= 5.46.0, <= 5.46.3 | 5.46.4 | hydratable keys built from untrusted input. |
| GHSA-8266-84wp-wv5c | CVE-2024-45047 | medium | medium | 2024-08-30 | < 4.2.19 | 4.2.19 | Svelte 4 SSR attribute escaping (mXSS) with untrusted values. |
| GHSA-wv8q-r932-8hc7 | CVE-2022-25875 | medium | medium | 2022-07-13 | < 3.49.0 | 3.49.0 | Svelte 3 SSR with objects in attributes. |

## devalue

| GHSA | CVE | Severity | Maint. | Published | Affected | Patched | Precondition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GHSA-9rgm-9g3h-6x36 | CVE-2026-81176 | medium | medium | 2026-09-17 | < 5.9.1 | 5.9.2 | devalue.parse called on untrusted data. |
| GHSA-77vg-94rm-hx3p | CVE-2026-42570 | high | high | 2026-05-14 | >= 5.6.3, <= 5.8.0 | 5.8.1 | devalue.parse called on untrusted data (sparse arrays). |
| GHSA-mwv9-gp5h-frr4 |  | low | low | 2026-03-12 | >= 4.0.0, < 5.6.4 | 5.6.4 | Downstream code merges devalue.parse output with Object.assign or similar. |
| GHSA-cfw5-2vxh-hr84 | CVE-2026-30226 | medium | medium | 2026-03-12 | < 5.6.4 | 5.6.4 | devalue.parse or unflatten on untrusted data. |
| GHSA-33hq-fvwr-56pm |  | low | low | 2026-02-19 | <= 5.6.2 | 5.6.3 | Sparse arrays reach uneval or stringify on the server (hard to exploit). |
| GHSA-8qm3-746x-r74r |  | low | low | 2026-02-19 | <= 5.6.2 | 5.6.3 | uneval of untrusted data that is later evaluated. |
| GHSA-g2pg-6438-jwpf | CVE-2026-22775 | high | high | 2026-01-15 | >= 5.1.0, < 5.6.2 | 5.6.2 | devalue.parse on untrusted data (ArrayBuffer hydration). |
| GHSA-vw5p-8cq8-m7mv | CVE-2026-22774 | high | high | 2026-01-15 | >= 5.3.0, <= 5.6.1 | 5.6.2 | devalue.parse on untrusted data (typed array hydration). |
| GHSA-vj54-72f3-p5jv | CVE-2025-57820 | high | high | 2025-08-26 | < 5.3.2 | 5.3.2 | devalue.parse on untrusted data with __proto__ keys. |
| GHSA-4q55-j62x-fr9h |  | low | low | 2026-09-18 | <= 5.9.2 | 5.9.3 | devalue.parse on untrusted data; defensive fix, very unlikely to matter. |
| GHSA-x5rw-q4pp-hg5g |  | low | low | 2026-09-18 | >= 5.8.0, <= 5.9.2 | 5.9.3 | stringifyAsync with request-influenced promise timing; mostly a developer bug. |
| GHSA-r9w8-h9r3-54w4 |  | low | low | 2026-09-18 | <= 5.9.2 | 5.9.3 | parse with a malformed custom ArrayBuffer reviver. |
| GHSA-wf3x-273g-mvxv |  | low | low | 2026-09-18 | >= 1.0.0, <= 5.9.2 | 5.9.3 | Evaluating uneval output of very large sparse arrays. |
| GHSA-mcm9-63f2-9j32 |  | medium | medium | 2026-09-18 | <= 5.9.2 | 5.9.3 | Data parsed then passed to uneval. |
| GHSA-hx4r-w6wj-j8fg |  | medium | medium | 2026-09-18 | <= 5.9.2 | 5.9.3 | Attacker-influenced sparse values passed to uneval. |
| GHSA-j22f-vq7h-c4qm | CVE-2026-92708 | high | high | 2026-09-18 | >= 5.1.0, <= 5.9.2 | 5.9.3 | A server load (or other serialised data) returns a Node Buffer or typed array; up to 64 KB of shared process memory, including other users request data, can be shipped to the client. |

## Fixes without an advisory that change audit results

| Package | Version | Change | Source |
| --- | --- | --- | --- |
| @sveltejs/kit | 2.70.0 | CSRF and remote-function origin checks no longer compiled out of builds with a non-production NODE_ENV (PR 16313). Below 2.70.0, a staging-style build has no origin checks. | raw/kit-source--csrf-implementation-and-prs.md |
| @sveltejs/kit | 2.58.0 | `requested()` requires a `limit` (refresh-list DoS). | raw/kit-source--csrf-implementation-and-prs.md |
| @sveltejs/kit | 2.36.0 / 2.36.2 | `csrf.trustedOrigins` added; `csrf.checkOrigin` deprecated. | raw/kit-source--csrf-implementation-and-prs.md |
| @sveltejs/kit | 2.0.0 | `dangerZone.trackServerFetches` removed; cookie `path` required. | raw/kit-docs--cookies-api-reference.md |
