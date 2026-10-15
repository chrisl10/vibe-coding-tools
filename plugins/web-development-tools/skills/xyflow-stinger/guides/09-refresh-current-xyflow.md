# 09: Refresh current xyflow facts

Run this before stating a current version, bumping a dependency, or migrating across a major. The snapshot in [references/CURRENT-XYFLOW.md](../references/CURRENT-XYFLOW.md) is dated 2026-09-23.

## Sources, in authority order

1. npm registry (read-only):

   ```text
   npm view @xyflow/react version time peerDependencies --json
   npm view @xyflow/svelte version time peerDependencies --json
   npm view @xyflow/system version time --json
   ```

2. Package changelogs on `main`: `packages/react/CHANGELOG.md`, `packages/svelte/CHANGELOG.md`, `packages/system/CHANGELOG.md` in `xyflow/xyflow` (D15).
3. GitHub releases and the repository security page for advisories (D1, D2).
4. Official docs, including the machine-readable `/llms.txt`, `/llms-medium.txt`, and `/llms-full.txt` on reactflow.dev and svelteflow.dev (D15). These are the fastest way to load current API detail into context.
5. The xyflow blog for product changes (Pro, new kits) (D15).

The svelteflow.dev "what's new" page has lagged the registry (C3); prefer the registry and changelog.

## Procedure

1. Record the date and the exact commands or URLs used.
2. Compare against the snapshot: new stable versions, peer range changes, breaking changes, deprecations, advisories, and whether any `-next` line went stable.
3. If a major changed or a prerelease went stable, stop and report before touching the consumer project.
4. When the task authorizes maintaining this Stinger: archive each new source under `references/research/raw/` (source-repository research, not shipped) with the standard header, update `distilled-xyflow.md` with citations, then update `CURRENT-XYFLOW.md` and any guide row that changed. Never hand-edit a version without its source.
5. In consumer work, report the refreshed facts in the task report instead of editing this Stinger.
