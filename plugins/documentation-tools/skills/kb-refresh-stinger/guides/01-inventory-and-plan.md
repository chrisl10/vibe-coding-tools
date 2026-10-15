# Guide 01: Inventory and plan

Everything before the first writer spawns. Get this wrong and the fleet writes fiction fast.

## Intake

1. Read the assignment or handoff in full. It defines: the target repo, the base ref to document against, the write scope, any frozen read-only set, the merge owner, and any extra gates. If there is no handoff, derive these from the owner in one batched question set before proceeding; do not guess scope.
2. Pin the ref. Fetch and record the exact commit of the base branch (for example `git fetch origin staging && git rev-parse origin/staging`). Every citation in every doc points at this commit. If the base moves mid-run, finish on the pinned commit and note the delta in the report.
3. Confirm the opt-in for a multi-agent run with the owner, per the Workflow tool's requirement. State the projected cost and get the explicit yes before launching anything.

## Scout

Read-only, inline, no fleet needed:

- Library tree: every file under `library/knowledge/private/**` and the requirements tree, with sizes and last-modified commits (`git log -1 --format=%cs -- <path>` per file is enough).
- Code facts: top-level layout, package manifests, toolchains, entry points. The writer fleet will do the deep reading; the scout only needs the map.
- History facts: commit count, PR count, branch list, recent release tags. These feed the "how far behind are the docs" number in the plan.
- Hazards: generated directories that must never be documented as hand-written, files with secrets-shaped names, giant files that need chunking.

## Classify every existing doc

Per doc, exactly one of:

- **keep**: current and grounded; the fleet re-verifies citations but rewrites nothing.
- **update**: right topic, wrong or stale content; the fleet rewrites in place.
- **write**: missing; the fleet creates it.

At inventory time, commit-age comparison is a cheap triage signal. Before choosing keep or update, re-open the material claim sources at the pinned revision and record their receipts using guide 05. Changed bytes, a new date or a moved path alone do not establish semantic drift. Record missing and unchecked proof separately; the inventory still reports N keep / N update / N write, plus unread or unresolved rows.

## Split into units

- Group by domain (auth, data, integrations, operations, and so on), matching the repo's existing domain folders. `knowledge-stinger`'s domain taxonomy is the default when the repo has none.
- Each unit is a disjoint set of file paths. Disjoint is non-negotiable: two units touching one file means two agents writing one file, which means clobbered work and unreadable diffs.
- Include a root or overview unit last if shared files (README, index, cross-domain overview) need touching. It merges after the domain units so its links resolve.
- Write the unit-to-files map to disk as JSON (the reference run's map, `raw/kb-refresh--evidence--unit-split-2026-10-04.json`, is source-repository research, not shipped; do not require it: one entry per unit naming its domain and its non-overlapping file list is enough). Every later stage reads units from that file, never from memory.

## Plan presentation

Give the owner one message with: unit count and list, shard layout (how many workflows, units per shard), the doc split numbers, the projected token and wall-clock cost from measured medians, and a smaller alternative (fewer shards, verify rounds capped at 2, or update-only). Get the explicit yes on the plan before launching. Record the choice; the closing report states which plan ran.

## Out of scope, always

No code changes, no dependency installs, no config changes, no issue creation, no PRD or IRD edits. Anything the scout notices as broken goes in the plan as a sus-list seed, not a fix.
