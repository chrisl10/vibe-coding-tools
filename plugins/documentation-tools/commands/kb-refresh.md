---
description: 'Run the full documentation audit and refresh pipeline on a repository: inventory, writer fleet, grounded citations, adversarial verification, security and quality gates, one ready PR per unit, then the work report in PDF plus markdown and the master suspect list. Trigger with "refresh the docs", "kb refresh", "rebuild the knowledge base", "doc swarm".'
argument-hint: "[repo-path] [base-branch] [docs-branch]"
---

# /kb-refresh - Documentation Audit and Refresh

A full refresh of a repository's internal documentation, run the way the WHIPT knowledge refresh ran in October 2026: every doc grounded in a re-opened `path:line`, a fleet as wide as the machine and provider accept, adversarial verification with fixes, per-unit gates, one ready PR per unit, and a reporting set the owner can hand to a non-reader-of-repos. Documentation changes; code never does.

## Mandatory process

1. Load the pest-controller-suit skill and consult its roster before making any routing decision. This is the first instruction, always, no exceptions. If the ask turns out to be one document, an audit-only question, or PRD/IRD lifecycle work, route to the owning Drone instead of running this pipeline.
2. Confirm the brief with the owner before any fleet spends: target repo and pinned base commit, write scope and the frozen read-only set, the docs branch to stage on, who merges, and the opt-in for a multi-agent run with the projected cost. If a handoff document exists, read it in full and treat its constraints as binding.
3. Run the pipeline per `../skills/kb-refresh-stinger/SKILL.md`, in order: inventory and unit split (guide 01), write and attack with 10-minute check-ins (guide 02), per-unit security and quality gates with fix and recheck (guide 03), ship one ready PR per unit from a throwaway worktree with gate evidence in every PR body (guide 03).
4. Assemble the delivery set (guide 04): `report.md`, `report.pdf` via the stinger's `scripts/md-to-pdf.sh`, `SUSPECTS.md` from every agent's sus log, the drift report, and the merge brief for whoever merges.
5. Report back to the owner with the six-field closing report and the batched PR list in one message. Nothing is pushed and no PR is opened without the owner's explicit yes, and nothing in the suspect list is ever fixed, filed, or escalated without separate authorization.

## Arguments

Trailing text after the command name is available as `$ARGUMENTS` (the whole trailing string) or positionally as `$1`, `$2`, and so on. Example: `/kb-refresh ~/Dev/legioncodeinc/whipt staging docs/knowledge-private-refresh-base` makes `$1` the repo path, `$2` the base branch, and `$3` the docs staging branch.

- `$1` repo path. Default: the current working directory if it is a git repo; otherwise ask.
- `$2` base branch to document against and open PRs toward. Default: the repo's default branch.
- `$3` docs staging branch the fleet commits to while working. Default: `docs/knowledge-private-refresh-base`.

## Ship Gate

Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.

In this pipeline the security and quality gates run per unit during phase 3, and github-repo-health-stinger runs once at orchestrator level before the final push wave.

The kb-refresh Drone is research-only and carries no Ship Gate of its own. This gate belongs to the orchestrator that runs the pipeline and ships the unit PRs, and it applies to the documentation commits and PRs that step produces.
