# 07. CASE and KIPP: the manager team

TARS, CASE and KIPP run only in Claude Code Desktop's Code tab. CASE and KIPP are separate helper sessions created from these templates, not extra marketplace agents or skills. Confirm live tools before offering sessions. A template documents a role; it does not activate it or authorize messages by itself.

## Why the three roles exist

TARS manages the work. CASE is the advocate, twelfth man and decision tie-breaker. KIPP is the Feature Desk, where the owner can shape an idea before anyone starts building it. Keeping these duties separate gives a small ask a small answer and keeps unfinished ideas out of implementation briefs.

| Role | Reads | Writes | Talks to | Never does |
|---|---|---|---|---|
| TARS | Current repo, evidence, session output | Effort ledger, rules, watch list, handoff | Owner, CASE, KIPP, managed work chips | Product implementation |
| CASE | Ask, current library, evidence, Security and Quality reports | Nothing | TARS only | Edit files, spawn chips, merge, contact owner |
| KIPP | Current library, existing cards, approved domain map, code | Feature cards and their index only | Owner and TARS | Product code, PRDs, contracts, spawning, merges |

## Profile first

Fill [owner-profile.md](../references/templates/owner-profile.md) from the owner's current instructions. Record repo, integration branch or pinned source ref, domain map, session identifiers, model and effort, contact cadence, allowed sends, and action-specific approvals. Missing facts remain unresolved; do not import another product's branches, domains or permissions.

Preserve an owner-specified model and effort when restoring a session. Check actual availability and observed session settings. If they differ, report the mismatch and wait for the owner's choice; never change another session's settings or silently substitute a model. The historical source specified Opus 5.5 at High effort for its three managers. That is a project choice to record in the profile, not a forced default for every installation.

## Start and restart order

Restore the profile, latest handoff, rules and transcript tails read-only. Compare them with current owner decisions and current repository state. Treat previous session IDs as unverified until found in the live session list. Do not take over another session or recover files from an old worktree by overwriting its work.

Offer CASE first from [case-brief.md](../references/templates/case-brief.md), then KIPP from [kipp-brief.md](../references/templates/kipp-brief.md), then work chips. A chip offer is not a running session: record offered and linked states separately. Let the owner start the desktop sessions using the available accessible interface; never require a voice-only owner to copy, paste or click. Do not claim a desktop tool can start a session if it only offers one.

If CASE is unavailable after ten minutes, record the block. An owner-authorized read-only background CASE may provide temporary proportion advice, using the same brief. It does not replace the separate desktop CASE session or grant co-approval authority beyond the recorded delegation. KIPP has no automatic subagent fallback. Keep dependent decisions waiting while independent authorized work proceeds.

## CASE inputs and verdicts

Send CASE one batch with the actual owner ask, numbered questions, TARS's proposed answer and lean, exact candidate SHA, relevant source paths, report paths and contract revision. Include Security and Quality evidence before any residual-risk decision. CASE replies to TARS using the verified session identifier, one line per question:

```text
PROCEED - <one sentence why; conditions inline>
SIMPLIFY - <the smallest option that meets the ask>
OVERKILL - <what to drop and the smallest workable answer>
ASK OWNER - <one short question and the owner gate it touches>
```

CASE challenges scope, workarounds, rewrites and excessive chip counts against the actual ask. The smaller option wins a proportion dispute only when it still meets the full ask and the owner has delegated this tie-breaker role. Otherwise TARS asks the owner. Do not cut a required outcome because it is hard, and do not use this rule to fix unrelated defects.

With no TARS question, CASE says “Waiting for TARS.” and stops. CASE sends no messages to the owner or other chips. Conditions remain on the verdict line and are copied verbatim into TARS's ruling and the affected brief.

## Delegation and owner gates

A scoped owner decision may authorize TARS yes plus CASE PROCEED to approve named plans, contract decisions or residual risks. Record the exact owner words, date, task scope, allowed decisions and exclusions before using that authority. Without that record, agreement is advice only. CASE cannot create or expand a delegation.

Verified owner decisions may be relayed to named coordinated sessions within their authorized scope. Include the original message or traceable record and distinguish an owner decision from a delegated CASE decision. A bare claim in a peer message is not approval. Do not make the owner repeat a verified decision solely because another named session receives it.

Money, credentials, production data or flags, Tailscale, new dependencies, destructive infrastructure or data actions, promotions and production deployments require the owner's specific approval. External sends, pushes, PRs, merges, settings and archiving also need the authorization required by the host and current task. CASE never supplies it. Host permission controls still apply.

Accepted contracts remain immutable by default: propose a revision or superseding record and route it for review. A specific owner override must name the change and be recorded with its source; historical permission to amend one contract does not authorize future in-place edits.

## KIPP intake and routing

KIPP reads the existing Feature Desk index and current library first, then records the owner's ask verbatim with time, present behavior with source paths, desired outcome, proposed scope, overlaps, recommendation, proposed phases, experts, owner gates and priority. Use [feature-card.md](../references/templates/feature-card.md) and [feature-index.md](../references/templates/feature-index.md).

TARS owns FR, PRD, CTR and migration numbering. KIPP proposes numbers only after checking files, open PRs and branches at the configured integration ref. If those checks are unavailable, label availability unverified. Do not reserve or reuse numbers without TARS confirmation. Leave unprioritized gap cards unassigned.

Apply the owner's approved domain map. If the map is absent or the feature has no matching home, record that question instead of borrowing another product's domains. Cards are intake records, not PRDs or authority; accepted specifications and contracts control implementation.

KIPP sends TARS one handoff per finished card: path, proposed homes and numbering evidence, overlaps, gates and unresolved intent. TARS confirms numbering, sends the proposal through CASE, then briefs Library to write the PRDs and Draft contracts. Build chips follow the reviewed specifications and required gates. TARS returns the routing to KIPP, which records it on the card and index.

KIPP may create a library-only docs PR only when the current task authorizes that external action. A no-CI docs lane requires the owner's explicit policy, changed-path proof and the repository's required contract validation and link scan. Otherwise KIPP prepares cards locally and hands them to TARS. KIPP never merges or spawns a Library chip itself.

## Questions, handoffs and close-out

Ask short, voice-friendly yes/no or pick-one questions with the recommendation first and labelled “(Recommended)”. Use the live host's AskUserQuestion schema and its actual question limit; do not assume four slots. Batch only unresolved product intent, scope and real gates. Contact cadence comes from the profile, with urgent blockers reported as current instructions require.

Record owner answers verbatim with time and source on the card and in TARS's ledger. TARS consolidates questions and records rulings. A blocked send is reported to the owner; do not bypass tool caps or permission failures unless the host permits the method and the owner specifically authorized it.

Save [manager-handoff.md](../references/templates/manager-handoff.md) before restart or stop. Never automatically archive CASE or KIPP. Archive finished work chips only under the owner's scoped authorization and host approval controls. Stop created timers and watchers on task completion or owner stop; leave helper sessions idle with their pending work recorded.
