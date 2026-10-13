# 09 - GitHub Actions job shapes for a SvelteKit app

October 2026 qualification: [guide 17](17-reduce-ci-work-with-proof.md) governs current efficiency work, unknown-input accounting, candidate proof, secret boundaries and verified action SHA pins. Dated example versions/topologies are illustrative and require target-specific confirmation. No source example authorizes workflow activation or provider effects.

Primary case: a target repository confirmed to be a SvelteKit application on Vercel. Covers pnpm install, typecheck, lint, unit test, Playwright e2e and build obligations. Use [guide 17](17-reduce-ci-work-with-proof.md) before adding or removing jobs.

## The shared setup boilerplate

This illustrative shape is not a version recommendation. Resolve and verify full action commit SHAs and the target-supported Node/pnpm versions before authoring an actual workflow. Existing dated major tags below are reference placeholders, not immutable pins:

```yaml
- uses: actions/checkout@<verified-full-commit-sha>
- uses: pnpm/action-setup@<verified-full-commit-sha>
- uses: actions/setup-node@<verified-full-commit-sha>
  with:
    node-version: <target-supported-pinned-version>
    cache: pnpm
- run: pnpm install --frozen-lockfile
```

`--frozen-lockfile` is not optional in CI: it fails the install if `pnpm-lock.yaml` drifted from `package.json`, catching an uncommitted lockfile change before it becomes a build-time surprise. `cache: pnpm` on `actions/setup-node` wraps `actions/cache` internally, keyed on the lockfile hash - see `guides/14-caching-strategy.md` for the full caching decision. Source: `references/research/distilled-ci-release.md` §1.

## Recommended job split

Inventory existing jobs and measured setup/transfer costs before splitting. The table is an illustrative obligation map, not a mandatory four-job topology. Reuse a compatible qualified producer when possible, and retain separate work where runner/environment/security or proof contracts differ. See [guide 17](17-reduce-ci-work-with-proof.md).

| Job | Runs | Gate |
|---|---|---|
| `lint-typecheck` | ESLint, then `svelte-check` (needs `$env/static/private` resolved - set CI-safe dummy values for vars a lint/typecheck pass doesn't need to be real, e.g. a dummy `DATABASE_URL`), then a Drizzle schema check if applicable | none - runs first, fails fast |
| `unit-tests` | Vitest / `@testing-library/svelte` suite. Install a browser only when the actual tests/module dependencies require one; a server-directory import alone does not establish that need | none, or `needs: [lint-typecheck]` if the team wants to save CI minutes on an already-broken PR |
| `e2e-tests` | `pnpm build` against a real ephemeral database (see `guides/12-migration-gating-drizzle-neon.md`), then Playwright | `needs: [lint-typecheck]` - do not start an expensive Playwright run against code that fails typecheck |
| `build` | Production build smoke - proves `pnpm build` succeeds independent of whatever env the e2e job used | `needs: [lint-typecheck]` |

This mirrors the pattern found in a real SvelteKit + Drizzle/Neon CI (`research/distilled-ci-release.md` §1) - gating expensive jobs behind a cheap gate is a deliberate cost control, not accidental structure. An alternative pattern (SvelteKit's and Svelte's own CI) runs every job fully in parallel with no `needs:` graph at all, accepting the extra CI minutes for faster wall-clock feedback on a fast, well-funded runner pool. Pick based on the project's actual CI-minute budget and PR volume; both are legitimate, cite whichever is chosen and why.

## The `svelte-kit sync` race condition

If `check`, `test`, and `build` targets each independently call `svelte-kit sync` (directly, or implicitly via the Vite plugin) and run in parallel against the same working directory, they can race-write `.svelte-kit/types/` and throw intermittent `ENOENT`. If a monorepo tool (Nx, Turborepo) is running these as parallel targets against one working tree, split them into sequential steps rather than one `-t check test build` invocation. Source: `research/distilled-ci-release.md` §1.

## Node version

Pin an explicit `node-version`, never a floating alias (`lts/*`, `latest`). Node 24 is current as of this research window (2026-08-14) - both SvelteKit's own CI and Svelte core's own CI use it. Re-verify currency before copying this pin into a new repo months from now; this is exactly the kind of fact that goes stale.

## Playwright e2e job specifics

See `guides/14-caching-strategy.md` for browser-binary caching and `guides/15-required-status-checks.md`'s handling of sharded jobs as required checks (job naming under a matrix). For the DB the e2e job runs against, see `guides/12-migration-gating-drizzle-neon.md` - never point an e2e job at the shared production database.

## Cross-references

- `guides/00-principles.md` - classify app-vs-package before applying this guide.
- `guides/10-vercel-integration-and-double-builds.md` - whether this workflow should also deploy, or only check.
- `guides/14-caching-strategy.md` - pnpm store and Playwright browser caching in depth.
- `svelte-stinger` - if lint/typecheck findings are about Svelte 5 idiom itself (runes misuse, stale Svelte 4 patterns), not CI wiring, hand off there; check overlap before writing Svelte-specific testing guidance here.
