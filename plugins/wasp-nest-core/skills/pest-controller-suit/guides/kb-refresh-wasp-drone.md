# kb-refresh-wasp-drone - Pest-Controller-Suit's Guide

The Pest-Controller-Suit routing skill's record of when to invoke `kb-refresh-wasp-drone`. Use this guide to decide whether a user request belongs to this Drone.

**Drone:** `kb-refresh-wasp-drone`, in the optional `documentation-tools` plugin. Confirm the pack is installed before dispatch.
**Stinger:** `kb-refresh-stinger` (same plugin)
**Prerequisites:** Core plus Documentation; full repository discovery also requires Code Audit's Swarm capability. Resolve that workflow before dispatch.
**Command:** `/documentation-tools:kb-refresh` in Claude plugin mode; `source-command-kb-refresh` from Documentation in Codex
**Trigger policy:** on-demand

---

**Plugin owner:** `documentation-tools`. **Required selection:** wasp-nest-core. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain

Full documentation refresh for a repository's internal docs (a `documentation-tools` component, invoked with `/documentation-tools:kb-refresh` in Claude plugin mode): inventory the existing knowledge base, split it into domain units, run a writer fleet as wide as the device and provider accept, verify every citation adversarially, gate each unit through security and quality with fix and recheck, ship one ready PR per unit, and close with the work report (markdown plus PDF), the drift report, and the master suspect list of code issues the fleet noticed but never fixed. The fleet is read-only against code; documentation is the only deliverable.

## Trigger phrases

Route to `kb-refresh-wasp-drone` when the user says any of:

- "refresh the docs", "kb refresh", "knowledge base refresh"
- "rebuild the knowledge base", "bring the library current"
- "doc swarm", "run the documentation fleet"
- "the docs are stale, fix that at scale"
- "track documentation freshness and missing proof" within an owner-fenced inventory

Or when the request implicitly involves rewriting a repository's `library/knowledge/` tree against the current code with receipts.

## Do NOT route when

- One document needs writing or updating: `knowledge-wasp-drone` owns single knowledge docs.
- The ask is PRD, IRD, or library scaffolding: `library-wasp-drone` owns the requirements lifecycle; kb-refresh only reports drift against it.
- The ask is an audit report with no documentation deliverable: `swarm-audit-wasp-drone` owns swarm audits.
- The ask is customer-facing help center content: `knowledge-base-help-center-wasp-drone` owns that.

If a request straddles two Drones' domains, prefer the narrower-scoped Drone and let the broader one act as backup. A full refresh that starts with "audit first, then rewrite" is still kb-refresh's; a pure audit is swarm-audit's.

## Inputs the Drone needs

Before invoking, ensure the user has provided (or you can infer):

- Target repo and the base ref to document against (default: the repo's default branch).
- Write scope and any frozen read-only set (contracts, ADRs, ledgers). Default: `library/knowledge/private/**` frozen set per the stinger.
- Opt-in for a multi-agent run with the projected cost. The Workflow tool requires it; ask, never assume.
- Optional: docs staging branch (default `docs/knowledge-private-refresh-base`), who merges, a handoff document.

If a required input is missing, do not invoke yet - ask the user to supply it.

For bounded freshness work, load kb-refresh guide 05 and use its receipt worksheet. Record source revision, exact re-opened claim, actual proof type and unchecked coverage. Age is triage only. A bounded receipt pass does not imply approval to launch a repository-wide fleet.

## Outputs the Drone produces

- The unit map (unit to disjoint file sets) and the plan the owner approved.
- One ready PR per unit against the base branch, gate evidence in every PR body.
- `report.md`, `report.pdf`, `SUSPECTS.md`, the drift report, and the merge brief in the run workspace.
- The six-field closing report.

## Multi-Drone sequences this Drone participates in

- Pre-merge documentation wave - kb-refresh runs first and hands the batched PR list and merge brief to the merge owner (TARS or the orchestrator); `github-repo-health-wasp-drone` runs once at orchestrator level before the final push wave.
- Swarm-audit follow-through - when a swarm audit surfaces "docs are stale" as a finding, the remediation is a kb-refresh run, not more audit.

## Critical directives the orchestrator should respect

- Grounding law: every claim cites a re-opened `path:line`; unverifiable claims are labeled `(unverified)`; model memory is never a source.
- The fleet is read-only against code: suspects are logged, never fixed; PRDs and issues are never edited or created.
- No push, PR, or merge without the owner's explicit yes; PRs are ready, never draft.
- No em dashes or en dashes in anything written.

(Full list lives in the Drone file's `## Critical Directive` section.)
