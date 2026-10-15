# 00. Scoping and version detection

Run this guide first on every audit. It fixes the scope, maps the React stack in each path, runs the version check, and decides which later guides apply.

References: [finding-rules.md](../references/finding-rules.md), [advisory-table.md](../references/advisory-table.md), [detection-patterns.md](../references/detection-patterns.md) (stack markers), [checks-rsc.md](../references/checks-rsc.md) RC-01, [checks-supply-chain-and-ai.md](../references/checks-supply-chain-and-ai.md) SC-01 to SC-05.

## Procedure

1. **Read the arming line and the contract.** Note the workspace, the audited repo (read only), the throwaway copy path, `stacks` and their `paths`, and include and exclude globs. If the line says the app is Next.js, write down the overlap rule: skip Server Actions, route handlers, middleware or proxy, and `next.config`; the Next.js Drone owns them.
2. **Create your output folder only:** `<workspace>/02-security/raw/react-security-wasp-drone/`. Never write inside the audited repo, never write `02-security/findings.jsonl` or `metrics.json`.
3. **Read every `package.json` under the stack paths** and the lockfile that governs each (it may be at the monorepo root). Record the package manager and lockfile type.
4. **Run the version check** (stdlib Python, read only):
   ```bash
   python3 <skill>/scripts/react_version_check.py --repo <repo> --paths <stack paths> \
     --out <workspace>/02-security/raw/react-security-wasp-drone/version-findings.jsonl \
     --summary <workspace>/02-security/raw/react-security-wasp-drone/version-summary.json --start-id 1
   ```
   The summary lists lockfiles, resolved versions, feature flags it found by source scan, and caps. Every cap goes into your metrics `coverage.caps`.
5. **Map the stack per path** from the summary plus the markers in detection-patterns.md. Write a table in your notes:

   | Path | React | Renderer | RSC runtime | Router and mode | SSR entry | Notable libs |
   | --- | --- | --- | --- | --- | --- | --- |

   - Renderer: client-only SPA (Vite, CRA, Parcel, Rsbuild), SSR (custom `renderToPipeableStream` server, React Router Framework Mode), or RSC (`@vitejs/plugin-rsc`, Waku, rwsdk, `@parcel/rsc`, React Router RSC, hand-rolled `react-server-dom-*`).
   - React Router mode: Framework (`@react-router/dev` plus `react-router.config.*`), Data (`createBrowserRouter`, `RouterProvider`), Declarative (`<BrowserRouter>` only). Many advisories depend on it.
   - Next.js present: record it and hand Next.js-specific RSC versions to the Next.js Drone (the script adds a cap).
6. **Hand-check what the script cannot read:** bun lockfiles, prerelease React builds (`-canary`, `-experimental`), vendored copies (a `vendor/` or `packages/*/dist` that bundles React), and Git or tarball dependencies. Compare by hand with advisory-table.md. Record each as a cap or a finding.
7. **Review the script's findings before copying them.** For each, confirm the precondition the script could not prove (for example, that an RSC server is actually deployed, or that Framework Mode redirects use request data). Raise to `confirmed` only after you trace it; otherwise keep the script's confidence. Copy accepted findings into `02-security/findings-react-security-wasp-drone.jsonl` with the same ids.
8. **Decide which guides apply** and note why any is skipped:
   - 01 XSS and SSR: always (any React UI). The SSR half only when an SSR or RSC entry exists.
   - 02 RSC and Server Functions: when any RSC runtime or `'use server'` exists outside Next.js.
   - 03 Secrets and data: always.
   - 04 Auth, routing, client trust: always for apps with login; skip only for static marketing sites with no auth (say so).
   - 06 Supply chain and AI patterns: always (short when the script found nothing).
9. **Run the candidate scan once** for the later guides:
   ```bash
   python3 <skill>/scripts/sink_scan.py --repo <repo> --paths <stack paths> \
     --out <workspace>/02-security/raw/react-security-wasp-drone/sink-candidates.json
   ```
   Note any per-check caps it prints.
10. **Record measures** for metrics: React version per path, RSC runtime version, open RSC advisories count, React Router version and mode, lockfile present (yes or no).

## Done when

The stack table is in notes, version findings are reviewed and copied, every cap is recorded, and the list of guides to run is written down.

## Sources

- raw/rsc--react-blog-cve-2025-55182.md
- raw/rsc--github-react-security-advisories.md
- raw/rsc--npm-registry-react-server-dom-versions.md
- raw/rsc--vite-plugin-rsc-advisories.md
- raw/router--react-router-advisories.md
- raw/lockfile--npm-pnpm-yarn-formats.md
