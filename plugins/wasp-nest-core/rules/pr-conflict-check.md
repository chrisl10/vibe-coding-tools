# PR Conflict Check

Before opening an authorized PR or declaring a branch ready, inspect the actual PR base, current branch and worktree ownership. Preserve the project's merge policy and the user's instructions.

## Check against the actual base

Read the PR's base/head and merge state when a PR exists. Otherwise use the task's requested integration base. An authorized remote fetch can refresh that exact base; if network refresh is not authorized, report the age and limits of the local reference. Do not assume `origin/main` for every project.

With the correct local references, `git merge-tree $(git merge-base HEAD <base-ref>) HEAD <base-ref>` can inspect a proposed merge without changing the checkout. A remote mergeability state or a local merge-tree result is evidence at its observed revisions, not a promise about a later candidate.

## Resolve only within approved ownership

For conflicts, identify the involved files and consult their owners before editing another task's active work. Follow the project's approved merge-versus-rebase policy. A rebase rewrites commit history; do not perform it, or a force-push, without explicit authorization covering that action. A normal push also needs task-specific authorization. Never force-push a shared base.

After an authorized repair, check the resulting candidate once. Repeat a passing check only if relevant bytes or base/head changed. Apply the current work-unit and retry limits to failures; do not poll until an uncertain merge state changes by chance.

## Report before handoff

Record the exact base/head, method, conflicts, observed result and verification limits. If unresolved, save a coherent handoff and report the specific blocker. A requested check does not automatically authorize repair, push or PR creation.
