# Sus log protocol

Every fleet agent keeps a running suspect log for the code issues it notices while doing documentation work. Reporting them is a core responsibility of the run; acting on them is forbidden. The logs concatenate into one master suspect list at the end.

## Where the logs live

In the run workspace: `sus/<unit>-<role>.md` (for example `sus/auth-1-writer.md`). One file per agent, append-only, started in the agent's first check-in even if empty.

## Entry format

```markdown
### SUS-<unit>-<nn> [P0|P1|P2|P3] [quality|security|functionality]
- Where: <path>:<line> (re-opened on <commit>)
- Observed: <what the doc work surfaced, one to two sentences>
- Why suspect: <the reasoning, one to three sentences>
- Check to confirm: <the exact command or read that would confirm or kill it>
- Suggested fix direction: <one line, NOT applied>
- Status: OPEN | CONFIRMED | REFUTED <by whom, when>
```

Severity: P0 exploitable now or exposes data; P1 broken behavior or exploitable logic flaw; P2 smell, drift, fragile pattern; P3 nit. When in doubt, round up and let the master list sort it out.

Rules:

- `Where` must be a real `path:line` the agent re-opened. An entry without it, or without `Check to confirm`, gets rejected back to the authoring agent at concatenation time.
- Category `security` entries never quote the sensitive value; describe the shape and location.
- The log is append-only: corrections are new entries that REFUTE an earlier one, never edits.
- Nothing found is still logged: `### <date> nothing found this session` as the last line before handoff.

## Handoff

Each agent hands its sus log path to the orchestrator in its final report line. The orchestrator collects them all before assembling the master.

## Master suspect list

Write `SUSPECTS.md` in the run workspace:

1. Header: repo, pinned commit, run dates, agent count, total entries.
2. Counts by severity and by category.
3. Entries sorted severity first, then category, then path. Each entry keeps its full fields plus a `Found by:` line naming the unit and role.
4. Duplicates (same path, same line region, same category) merge into one entry with all finders listed and the strongest wording kept.
5. `Unreviewed` section: any unit whose log never arrived, with the resume command to produce it.
6. Footer: the delivery rule. "This list is a report. No entry has been fixed, filed, or escalated. Triage belongs to the owner."

Rejected entries (missing Where or Check to confirm) are listed under `Rejected` with the reason, so nothing silently disappears.

The master goes into the final report and the merge brief. It is never applied: no fixes, no refactors, no GitHub issues, no PRD edits, unless the owner directs it afterward as separate, explicitly authorized work.
