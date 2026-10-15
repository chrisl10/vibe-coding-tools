# 14 - Caching strategy in GitHub Actions

October 2026 qualification: [guide 17](17-reduce-ci-work-with-proof.md) governs current efficiency work, unknown-input accounting, candidate proof, secret boundaries and verified action SHA pins. Dated example versions/topologies are illustrative and require target-specific confirmation. No source example authorizes workflow activation or provider effects.

Primary case. pnpm store caching, Playwright browser caching, and Turborepo remote cache if the repo becomes a monorepo.

## pnpm store caching

Default: `actions/setup-node`'s built-in `cache: pnpm` input - lowest-maintenance path, wraps `actions/cache` internally, keyed on the lockfile hash.

```yaml
- uses: actions/setup-node@<verified-full-commit-sha>
  with:
    node-version: <target-supported-pinned-version>
    cache: pnpm
```

**pnpm's own docs say this caching is not required and not guaranteed to make install faster** - "feel free to not cache the pnpm store in your job." Measure before assuming it's a win, especially on a small project where cache-restore overhead can rival a cold install. Source: `research/distilled-ci-release.md` §6.

**Security caveat:** never let an untrusted job (one running against fork-PR code, e.g. via `pull_request_target`) write to a store cache that a trusted, secret-bearing job later restores from - a poisoned cache entry is a supply-chain injection vector, not a theoretical one. Source: `research/distilled-ci-release.md` §6.

## Playwright browser caching: fresh installation is the default

Official Playwright docs recommend against browser-binary caching because restoration can take comparable time and OS dependencies still need installation. Start with fresh browser installation. Adopt the historical illustrative cache pattern below only when target-specific cold/hit/miss measurements support it and security boundaries remain intact. Prior community claims do not establish this target's savings. Source: October Playwright capture, [guide 17](17-reduce-ci-work-with-proof.md). Example action tags must be replaced by verified full SHAs.

```yaml
- name: Get Playwright version
  id: playwright-version
  run: echo "version=$(npm ls @playwright/test --json | jq -r '.dependencies["@playwright/test"].version')" >> "$GITHUB_OUTPUT"
- name: Cache Playwright browsers
  uses: actions/cache@<verified-full-commit-sha>
  id: playwright-cache
  with:
    path: ~/.cache/ms-playwright
    key: playwright-${{ runner.os }}-${{ steps.playwright-version.outputs.version }}
- name: Install Playwright browsers
  if: steps.playwright-cache.outputs.cache-hit != 'true'
  run: pnpm exec playwright install --with-deps
- name: Install Playwright system deps only
  if: steps.playwright-cache.outputs.cache-hit == 'true'
  run: pnpm exec playwright install-deps
```

Key on the **Playwright version**, not the lockfile hash - a version bump should invalidate the cache, an unrelated lockfile change shouldn't force a re-download. The single most-repeated mistake across sources: caching binaries but skipping `install-deps` on a cache hit, which restores the binaries fine but leaves them unable to launch because system libraries outside the cached path are missing on the fresh runner.

**GitHub's 10GB per-repo cache limit** can evict an active feature branch's cache (or even the default branch's) when many short-lived branches each cache a slightly different Playwright version. Mitigate with a shared fallback cache key across branches rather than a fully branch-unique one. Source: `research/distilled-ci-release.md` §6.

## Turborepo remote cache (archived for future use - not applicable today)

This source repository distributes components. Determine whether the target repository actually uses Turborepo before applying this material. For a qualifying target, the documented path is Vercel Remote Cache via OIDC (`vercel/setup-turborepo-remote-cache-action`, requires `permissions: id-token: write`), preferred over a long-lived Personal Access Token. Only task **outputs** are cached remotely, never source. Full detail: `references/research/raw/turborepo-remote-cache-github-actions.md` (source-repository research, not shipped). Do not present this section's guidance as an immediate requirement for the current single-app layout.

## Severity framing

- **Must-fix:** an untrusted job with write access to a cache a trusted job restores from.
- **Should-refactor:** Playwright browser cache present but missing the `install-deps` cache-hit fallback; a cache key that includes something that changes every run (defeating caching entirely) or something that never changes (never invalidating a genuinely stale cache).
- **Style:** cache key naming convention, missing a comment on why caching was skipped for a given job.

## Cross-references

- `guides/09-github-actions-job-shapes-sveltekit.md` - the jobs this caching strategy applies to.
- `devops-stinger` - general Actions caching architecture patterns (`guides/08-caching-strategies.md`) for Docker/Depot-based pipelines; this repo doesn't build containers, so that guide's Docker-layer caching content doesn't apply here, but its general "cache is a first-class architectural concern" framing is consistent with this guide.
