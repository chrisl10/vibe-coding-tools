# 05 Handoff: how the user runs the plan

Goal: end the engagement with a clear next action. This Drone plans; it does not implement.

## What to tell the user

1. Where the outputs are: `04-remediation/roadmap.md` and `plan.json` in the workspace, and the list of `library/` files written (if approved).
2. The one thing to do first: the first Now item, its owner Drone, and its first step.
3. How to execute:
   - To drive a set of PRDs to done: run `/smoke-it` and name the PRD folders for one wave. /smoke-it reads each PRD end to end, builds an acceptance-criteria ledger, checks contract dependencies (a Draft CTR blocks the affected criteria until the user accepts it), routes each criterion to a Drone through the roster, runs security then quality, and ships through a PR. [smoke-it command, core]
   - To run one package or a single IRD: `/pest-controller` with the PRD or IRD path, which routes it to the owner Drone named in the roadmap.
   - Suggested batching: one /smoke-it run per wave, Now first. Packages with `depends_on` run after their dependency is verified.
4. What needs the user: accepting any CTR drafts; opening GitHub issues if IRDs were wanted and no numbers existed; confirming Draft knowledge docs; any Now package marked "needs confirmation".
5. What proves it worked: re-run `/audit-my-code mario` (or the single dimension) after the wave; the finding ids in the PRDs should disappear and no new medium-or-higher finding should appear in touched paths.

## Make PRDs executable by /smoke-it

Check each written PRD before handing off:

- Acceptance criteria are binary, testable, and each names a finding id and a check.
- `## Contract dependencies` is present (pin or "None").
- The Overview states owner Drone and wave.
- The first step of any structural PRD is the safety net (characterization tests).
- The last criterion is the audit re-run.
- The folder has an empty `qa/` subfolder.

## Never

Never start implementation. Never commit or push. Never mark a PRD in-work or completed (lifecycle moves belong to /smoke-it and the Library Drone). Never edit `library/notes/`.

## References and sources

- [owner-routing.md](../references/owner-routing.md): which Drone each work package routes to
- [roadmap-template.md](../templates/roadmap-template.md): the roadmap shape the handoff points the user at
- `src/commands/smoke-it.md` (core command)
- `pest-controller-suit` (core skill) roster and dispatch contract
