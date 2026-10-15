# Guide 03: Gates and ship

Per unit: security gate, then quality gate, each with fix and recheck. Then ship from a throwaway worktree so live writers are never disturbed.

## Security gate (per unit)

Scan, in order:

1. The unit's docs: any secret-shaped string (token, key, password, connection string, private hostname, customer data). Environment variable names are fine; values never.
2. The planned PR body: same scan. Gate summaries quote findings, so the summary must already be clean.
3. Cross-references: doc quotes of config snippets must be redacted shapes, not real values.

A hit is fixed in the doc (redact or remove), then the whole scan re-runs. The gate result is written to the run workspace as a per-unit markdown summary; that file is what the PR body embeds. Report to the library directory per the Ship Gate: `library/requirements/reports/<domain>/`.

## Quality gate (per unit)

1. Completeness: every file in the unit's plan exists, has the standard header (`knowledge-stinger` format), and is in the right domain folder.
2. Citation sweep: every behavioral claim carries `path:line`; spot-check a sample by re-opening on the pinned commit; any claim the verifier marked unverifiable is labeled `(unverified)` in the doc, not silently dropped.
3. Dash sweep: no U+2014 or U+2013 anywhere in the unit's files.
4. Cross-links: every Related link resolves.

Fix, then re-run the gate. Medium or above findings must be resolved before shipping the unit; residuals that genuinely cannot be fixed inside scope are labeled in the gate summary and travel to the PR body.

## Ship (per unit)

The rule: never ship from a worktree a writer can touch. The reference scripts live in `references/research/raw/` (source-repository research, not shipped) (`kb-refresh--script--ship-unit-2026-10-04.sh` is the superseded pattern; `kb-refresh--script--ship-shard-2026-10-04.sh` is the working one).

```
1. git worktree add --detach <tmp>/ship-wt <pinned-base-commit>
2. in ship-wt: git checkout -B docs/kb-refresh/<unit> <pinned-base-commit>
3. git checkout <docs-branch> -- <unit files>     # unit files from the committed docs branch
4. git add -A -- <unit files>                     # explicit paths only, never -A bare
5. git commit -m "docs(knowledge): refresh <unit> ..."
6. run the repo's validation script; record PASS or FAIL in the PR body either way
7. git push -u origin docs/kb-refresh/<unit>
8. gh pr create --base <base-branch> --head docs/kb-refresh/<unit> \
     --title "docs(knowledge): refresh <unit> domain" --body-file <gate summary + repo health + tools + model>
```

Notes that burned the reference run:

- `.gitignore` can swallow new docs (a `data/` rule ate a whole domain's files once). If step 4 refuses ignored paths, `git add -f` exactly those paths and say so in the PR body; never edit the ignore rules as a side effect.
- Commits on the shared docs branch while other shards still write must use explicit file paths, never `git add -A` bare.
- Never push the docs branch itself unless the owner says so; it is the fleet's staging surface.

PRs are ready, never draft. The gate summary in the body means the merge owner never has to trust the pipeline's word.

## Close the wave

1. github-repo-health-stinger at orchestrator level, once, before the final push wave (Ship Gate order).
2. Owner reviews the reports and gives the explicit yes; nothing leaves the machine without it.
3. Send the merge owner one batched message: the full PR list, merge-order notes (root unit last), the merge brief file, and the drift report. Whoever merges merges; the pipeline never merges into a shared branch itself.
