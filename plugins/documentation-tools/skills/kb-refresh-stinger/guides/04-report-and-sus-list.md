# Guide 04: Report and sus list

The run is not done when the PRs are open. It is done when the owner can read what happened, what it cost, and what the fleet noticed without fixing.

## Work-accomplished report (markdown)

Write `report.md` per the structure in `references/report-spec.md`: header, scope, numbers (docs written, updated, kept; inspections; tokens; working hours vs wall clock), what changed per unit, how it was verified (the gauntlet with real counts), findings (suspect summary and drift count), handoff (PR list, merge order, brief location), limitations (unverified counts, anything skipped and why). Pull every number from the run's own artifacts (gate summaries, unit map, coverage ledger), never from memory.

## PDF render

1. Write `report.html`: a single print-styled sheet, Legion Code Inc. branding per `references/report-spec.md` (verified symbol SVG paths from the brand kit, mono labels, stat boxes).
2. Run `scripts/md-to-pdf.sh report.html report.pdf`. It uses headless Chrome; no dependencies to install. It finds the browser from `CHROME_PATH`, then Chrome, Chromium or Edge on `PATH`, then the macOS `/Applications` copies, then Program Files under Git Bash. Set `CHROME_PATH` for any other install.
3. Keep the markdown as the canonical backup. The PDF is the artifact for people who do not read repos.

## Master suspect list

1. Collect every agent sus log (path convention in `references/sus-log-protocol.md`). An agent with no findings still contributes its dated "nothing found" line.
2. Concatenate and dedupe by location plus category. Sort by severity. Write `SUSPECTS.md` with the header, counts by severity and category, one entry per suspect with its provenance (which unit and agent), and an "unreviewed" section for any unit whose logs never arrived.
3. Reject back to the authoring agent any entry missing `file:line` or a check-to-confirm. The master list is evidence-grade or it is noise.
4. Deliver, never apply. The sus list goes to the owner (and the merge owner's brief) as a report. No fixes, no refactors, no GitHub issues unless the owner says so afterward.

## Drift report

Doc claims that contradict PRDs, IRDs, or ADRs go in a drift report (the reference run's list, `raw/kb-refresh--evidence--sus-list-whipt-2026-10-04.md`, is source-repository research, not shipped; follow `references/report-spec.md` instead). Report only: no PRD edits, no IRD edits, no new issues. Link it from the report and the merge brief.

## Close

1. Record the run's lessons in the project memory note (thresholds measured, provider pacing observed, anything the next run should do differently).
2. Deliver the six-field closing report: Status, Delivered, Verified, Not done, Questions for the owner, Out of scope noticed only.
