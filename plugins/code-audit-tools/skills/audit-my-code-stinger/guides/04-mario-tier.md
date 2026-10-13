# 04. The Mario tier

Load this guide only for `mario`. The Mario Audit is everything in `full`, plus the remediation planning documents that turn the findings into executable work. It is the most expensive tier: expect several times the tokens of `full`, mostly in W3.

References: [audit-contract.md](../references/audit-contract.md) sections 2 and 3; [arming-lines.md](../references/arming-lines.md) (knowledge and remediation lines).

## Prerequisites (check at intake)

1. `library-stinger` and `knowledge-stinger` are installed (core Wasp Nest skills). Check with the Skill tool or a Glob for their `SKILL.md`. Missing: tell the user the Mario tier needs the Wasp Nest core, and offer `full` instead.
2. The audited repository has a `library/` folder in Library Schema v2. Missing: the Foundation Drone will already have flagged it. Offer to run the `get-started-stinger` playbook first (it asks its own consent). Without a Library, the Mario tier still writes `04-remediation/roadmap.md` and `plan.json` in the workspace, but writes nothing into the repository.

## W3 steps

1. **Draft the plan in the workspace.** Arm `remediation-planning-wasp-drone`. It reads every dimension's findings and writes `04-remediation/roadmap.md` and `plan.json`, including the exact list of proposed `library/` files (knowledge docs, PRDs, IRDs, draft CTRs).
2. **Consent gate.** Show the user the proposed file list, grouped by type, with one line per file saying what it covers and which findings it resolves. Ask for approval of the list as a whole, or edits to it. Write nothing into the repository until the user says yes to an exact list.
3. **Knowledge first.** For the approved knowledge docs, arm `knowledge-wasp-drone` with the paths and the findings that make each area worth documenting. Documenting before planning changes is deliberate: the PRDs reference these docs as the current state.
4. **Plans second.** Re-arm `remediation-planning-wasp-drone` in write mode with the approved list. It writes PRDs, IRDs, and CTR drafts through `library-stinger`'s templates.
5. **Report.** Tell the user what was written, and how to execute it: `/smoke-it` for the PRDs, `/pest-controller` for the IRDs, and a re-run of `/audit-my-code <tier>` after each wave to prove the fixes landed.

## What the Mario tier does not do

It does not fix code. Every fix goes through a PRD or IRD and the normal Ship Gate, so the audit stays an audit and the fixes stay reviewable.
