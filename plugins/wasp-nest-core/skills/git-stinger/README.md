# git-stinger

The procedural arsenal for `git-wasp-drone`, the Wasp Nest's Git mastery specialist.

## Current plugin owner

This capability stays in required Wasp Nest Core. Its canonical source is src/skills, with canonical ownership recorded in the root [plugin catalog](../../../plugin-catalog.json). Its SKILL.md metadata declares any standalone/orchestrator exception; specialist agents keep their actual paired Stinger. Host home/plugin files are generated carriers. Use [the layout and selection guide](../../../docs/PLUGIN-LAYOUT.md) when a workflow calls an optional specialist; source references alone do not enable an installed plugin.


## What this stinger covers

- **Interactive rebase** - squash, fixup, reword, autosquash workflows
- **History rewriting** - `git filter-repo`, BFG Repo Cleaner, secrets removal
- **Conflict resolution** - merge/rebase conflicts, rerere, mergetool setup
- **Reflog recovery** - undoing destructive operations, recovering deleted branches
- **Worktrees** - parallel branch work without stash overhead
- **Hooks** - pre-commit, commit-msg, pre-push; Husky and lefthook setup
- **Large files** - Git LFS, partial clone, sparse checkout
- **Submodules vs subtrees** - decision matrix and lifecycle

## Reading order

1. Read `SKILL.md` - master index, critical directives, quick-reference tables
2. Read `guides/00-principles.md` - the five non-negotiable rules
3. Open the guide matching your task (see Eight-action playbook table in SKILL.md)
4. Reference research/ if you need authoritative sources for a claim

## Key rule

**Always show the escape hatch before a destructive operation.** Before `git reset --hard`, show `git reflog`. Before `filter-repo`, show `git bundle create backup.bundle --all`. The developer may not get a second chance to read the chat.

## Beginner practice

Start with [the disposable-repository lesson](guides/09-beginner-disposable-practice.md) and [worksheet](templates/beginner-git-worksheet.md). The [optional runner](scripts/practice-git.py) demonstrates status, diff, stage, commit, branch, byte-backed fixture restore, and reflog recovery in its own temporary repository. It does not commit to the user's repository or change global identity. [Fresh official command research](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/git-stinger/references/research/beginner-practice/distillation.md) grounds the lesson. Read the [worked output limits](examples/beginner-git-practice.md) before treating an exercise as recovery proof.
