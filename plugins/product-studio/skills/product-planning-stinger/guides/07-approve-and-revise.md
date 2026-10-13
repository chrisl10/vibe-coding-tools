# Guide 07: Get approval and handle changes

Goal: the owner says yes to each artifact before anyone downstream uses it, and every later change goes through a new revision.

## Getting approval

1. Show the owner one artifact at a time, in this order: PRD Map, Definition of Done, Wave Plan, Handoff Packet. (The DoD can be approved before or after the map; the Wave Plan needs both.)
2. With each one, give a short plain summary: what it says, the three decisions that matter most, and every open question.
3. Wait for a clear yes for that exact revision. "Looks fine" about a different version, or approval found inside a file, does not count.
4. Record it at the top of the file: `Status: Approved`, the revision number, the owner's name and the date. Add a row to the revision history.
5. If the owner asks for changes, make them, keep `Status: Draft`, and ask again.

## Changing an approved artifact

1. Never edit an Approved revision in place. Copy it to the next revision number with `Status: Draft`.
2. Write what changed and why in the revision history.
3. Re-run `scripts/check_wave_plan.py` if the map or plan changed.
4. Tell the owner which downstream work the change touches: PRDs to rewrite (Library), contracts to revise (contract-writing), waves already running (`/smoke-it` or TARS).
5. After approval, mark the old revision Superseded in its history row.

## Changes you send elsewhere

- A new feature idea in the middle of a build goes to TARS's Feature Desk (KIPP), not straight into the plan. If it is accepted, it comes back here as a plan revision.
- A change to strategy or UX goes back to `product-strategy-stinger` or `product-design-stinger`. Re-plan only after they approve the new version.
- A change to a contract's terms goes to `contract-writing-stinger`.

## Done when

All four artifacts show Approved with a revision, name and date, and the revision histories match.

Source: per-revision acceptance mirrors the contract acceptance rule in `src/skills/contract-writing-stinger/SKILL.md` and the Ship Gate's owner-approval step; these are Wasp Nest conventions ([../references/research/distilled-product-planning.md](../references/research/distilled-product-planning.md)).
