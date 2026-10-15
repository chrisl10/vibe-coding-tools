# dependency-audit-stinger

Supply-chain hygiene for the actual target repository. Start with [target repository audit](guides/05-target-repository-audit.md), choose tools from the observed ecosystem and keep changes inside the authorized scope. The retained Hivemind guides, templates and examples are a concrete npm case, not a mandatory toolchain for every project.

See `SKILL.md` for the full guide map. Start with the target repository audit; `guides/00-scanner-decision-matrix.md` remains the npm worked-example tool reference.

For a beginner explanation of actual manifests and lockfiles, read [guide 06](guides/06-explain-manifest-and-lockfile.md), use the [preservation ledger](templates/manifest-reading-ledger.md) and compare the [worked fixture](examples/read-manifest-fixture.md). Distinguish requested declarations, recorded resolutions, actual installed/runtime evidence and security results. Explanation alone performs no installation or dependency changes. The update has its own pinned source digest.

**Research Summary:** `research/research-summary.md`

## Current plugin owner

This capability stays in required Wasp Nest Core. Its canonical source is src/skills, with canonical ownership recorded in the root [plugin catalog](../../plugin-catalog.json). Its SKILL.md metadata declares any standalone/orchestrator exception; specialist agents keep their actual paired Stinger. Host home/plugin files are generated carriers. Use [the layout and selection guide](../../learn/reference/PLUGIN-LAYOUT.md) when a workflow calls an optional specialist; source references alone do not enable an installed plugin.

For release qualification, use [artifact-bound SBOM evidence](guides/07-bind-sbom-to-release-artifact.md) and [safe major-upgrade contracts](guides/08-upgrade-major-dependency-safely.md). The fresh digest distinguishes project graphs, final bytes, schema validation, coverage and signed identity. Rendered [artifact cases](examples/release-artifact-evidence-cases.md) and [upgrade cases](examples/major-upgrade-contract-cases.md) are synthetic exercises with explicit limits.
