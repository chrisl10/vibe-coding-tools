# 01. Version and advisory check

Goal: turn the scanner's version matches into correct, confirmed findings. Loads [../references/advisory-table.md](../references/advisory-table.md) and uses `<workspace>/02-security/raw/next-version-findings.jsonl` and `next-inventory.json`.

## Steps

1. **Read the scanner output.** Each line in `next-version-findings.jsonl` is already contract-shaped. Kinds:
   - one finding per matched critical advisory;
   - one roll-up finding for matched high advisories (each listed with its precondition status);
   - one roll-up finding for matched medium and low advisories;
   - one "no longer gets security fixes" finding for Next.js 13.x or 14.x (support policy [raw/next--support-policy.md]);
   - one `info` finding when nothing matched.

2. **Check the version source.** Open the lockfile named in `evidence` and confirm the resolved `next` version by eye (search for `node_modules/next`, `next@`). In monorepos, check that the app directory actually resolves to that entry (pnpm and yarn workspaces can hold several `next` versions; the scanner lists all it finds). If the version came from the package.json range, keep `confidence: possible`.

3. **Resolve preconditions.** For every finding tagged `needs-precondition-check`, read `advisories_matched[].preconditions` in the inventory and settle each `unknown`:
   | Precondition | How to settle |
   | --- | --- |
   | `avif_input` | Do users upload images, or do `remotePatterns` hosts serve AVIF? Check upload code and `images.formats`. If the optimizer is used at all on user or remote images, treat as met. |
   | `windows_host` | Dockerfile base image, CI deploy target, IIS or `web.config`, README. Linux containers mean unmet. |
   | `self_hosted` | `vercel.json` or Vercel project files and the owner's README; Docker or `next start` in a process manager means self-hosted. |
   | `custom_server_or_unpinned_host` | A `server.js` calling `next()` is a custom server. `next start` or standalone pin the host from 14.2 on [raw/advisory--2026-server-actions.md]. |
   | `turbopack_build` | 16.x builds use Turbopack unless `next build --webpack` [raw/next--next-16-release-proxy-rename.md]. |
   | `cache_components` | `cacheComponents: true`, `experimental.useCache`, or any `'use cache'` directive. |
   | `edge_runtime` | `export const runtime = 'edge'` in a file that defines or imports Server Actions. |
   Then rewrite the line (for a roll-up, split out any advisory whose precondition you confirm and that deserves its own line, such as a middleware bypass on an app with middleware-only auth): met and evidence shown, restore the advisory severity with `confidence: likely`; unmet, delete the line and add one sentence to `notes-nextjs-security-wasp-drone.md` under "Preconditions left open" or a "Ruled out" list; still unknown, keep it `possible` (severity capped at medium, contract rule 3) and list the question for the owner.

4. **Handle unstated fixes.** Advisories published 2026-09-30 (GHSA-h694-7cp9-m8p3, CVE-2026-94544, CVE-2026-94483, CVE-2026-94486, CVE-2026-94543, CVE-2026-94484, CVE-2026-94485) listed the patched version as `16.3.?` or `15.5.?` at research time [raw/advisory--ghsa-index-vercel-next-js.md]. If network is available, open the GHSA page; if it now names a fix and the installed version is at or above it, delete the line. Never write a fix version you did not read.

5. **Link structure to version.** A middleware bypass advisory matters most when middleware is the only gate. After guide 02, revisit these findings: if NX-PRX-01 is confirmed, keep severity; if every route also checks in-route, lower one step and say why in `verified_by`. Same for CVE-2026-64643 (action ID disclosure): it is a recon aid, so if every action authenticates inside, lower it to `low` [raw/advisory--2026-server-actions.md].

6. **Check the RSC version trap.** Do not use the `react` version in package.json to decide RSC exposure; Next.js vendors React for the App Router [raw/advisory--cve-2025-55182-react2shell-rsc-rce.md]. If the app pins `react-server-dom-*` packages directly (rare, custom setups), note it and check those versions against CVE-2025-55182 (fixed React 19.0.1, 19.1.2, 19.2.1).

7. **Check for compensating controls before downgrading.** For CVE-2025-29927, an upstream rule that strips `x-middleware-subrequest` counts (show the nginx, Cloudflare, or load balancer config). A WAF rule for React2Shell does not make an unpatched version acceptable: the advisory says there is no workaround; keep critical.

8. **Copy the final lines** into `<workspace>/02-security/findings-nextjs-security-wasp-drone.jsonl` (this file is yours alone; the orchestrator merges it with the other security Drones' files). Keep ids stable.

9. **Remediation wording.** Name the package file and the minimum version, and prefer the newest release in the line (16.3.8 or 15.5.27 at research time). For 13.x and 14.x, the fix is a major upgrade (`L` effort); suggest the official codemods, and say what to test (middleware renamed to `proxy.ts` on 16, async request APIs on 15) [raw/next--next-16-release-proxy-rename.md].

## Sources

[raw/advisory--ghsa-index-vercel-next-js.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--ghsa-index-vercel-next-js.md), [raw/next--support-policy.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--support-policy.md), [raw/advisory--cve-2025-55182-react2shell-rsc-rce.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--cve-2025-55182-react2shell-rsc-rce.md), [raw/advisory--2026-server-actions.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/advisory--2026-server-actions.md), [raw/next--next-16-release-proxy-rename.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--next-16-release-proxy-rename.md), [raw/next--npm-dist-tags-2026-09-30.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/nextjs-security-stinger/references/research/raw/next--npm-dist-tags-2026-09-30.md).
