# Maintain the local copy or fork

Copied source does not update when its original registry changes. External primitive dependencies have their own update path. Name one accountable maintainer and a review due date; this workflow schedules no autonomous job.

1. Pin original upstream revision, current local file hashes, notice records and patch history before considering an update. A missing baseline means re-establish provenance first, never overwrite the local copy.
2. Obtain candidate source and actual license/NOTICE/dependency metadata using read-only research. Compare original-to-candidate upstream changes and original-to-local modifications separately. Retain both diffs, notice deltas, dependency deltas, framework requirements and artifact hashes in update_comparison.
3. Decide per changed file whether to adopt, adapt or defer with reason. Retain local product behavior and approved tokens; ask the actual design owner when the design contract must change. Do not erase patches by re-running add --overwrite or applying presets blindly.
4. Route advisories and resolved graph changes to Dependency Audit/Security. Route license or rights changes to Software Licensing/counsel. For vendored code outside the approved component subset, return the gap to the parent; this pair owns only its approved component subset.
5. After approved changes, rerun relevant target build, SSR/hydration and interaction checks, keyboard/focus, responsive/theming checks and Impeccable detector. Record manual checks still NOT_RUN. Require Security then independent Quality then parent health before approved commit.
6. Record candidate acceptance/rejection, updated local hashes, preserved notice hashes, patch history, maintainer and next review date. Preserve the prior snapshot for rollback; any rollback mutation needs existing authorization.

Sources: editable wrapper/dependency split, changelog, Dialog behavior contract, styling.
