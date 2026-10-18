# Guide 05: Set the Definition of Done

Goal: one project-level Definition of Done (DoD) at `library/knowledge/private/standards/definition-of-done.md` that every PRD inherits, plus a short PRD-level checklist that Library copies into each PRD.

Template: [../references/templates/definition-of-done.md](../references/templates/definition-of-done.md).

## Why one shared list

Work that does not meet the Definition of Done does not count and cannot ship. When several teams or agents build one product, they all use the same Definition of Done. Scrum Guide Without a saved, approved list, "done" means whatever the last agent said.

## Steps

1. **Check for an existing DoD.** If an Approved one exists, reuse it. Propose changes as a new revision; never edit an Approved revision in place.
2. **Keep the five core items.** These are fixed for every Wasp Nest project:
   1. Acceptance criteria verified by a separate pass (not by the builder).
   2. Tests: new behavior has tests and the full suite passes.
   3. Security review first, then quality review, with no open finding of medium severity or higher.
   4. Docs and Library knowledge updated; PRD folder in the right lifecycle place with its `qa/` evidence.
   5. Owner approval.
3. **Add project items from the strategy and UX package.** For example, a phone-first product adds "works at the smallest supported phone width". Ask: "what would embarrass us if it shipped broken?" Turn each answer into a yes/no check.
4. **Keep it short.** A DoD that nobody can meet gets ignored. Put checks that only matter for one PRD into that PRD's checklist instead. Agile Alliance
5. **Make every line pass/fail.** "Code is clean" is not checkable. "Lint passes with zero errors" is.
6. **Fill the project-specific test commands** (build, type check, lint) from the repository if you can see them. If not, leave the placeholder and list it as an open question.
7. **Write the PRD-level checklist block.** It links the project DoD revision and leaves lines for PRD-specific extras. Library pastes it into each PRD.

## DoD is not acceptance criteria

Acceptance criteria say what one PRD must do (its ID table with Given/When/Then). The DoD says how finished every PRD must be. A PRD can pass all its acceptance criteria and still not be done. See `packs/business-and-product-tools/skills/agile-scrum-stinger/guides/04-definition-of-done.md` for the team-level version of this distinction; that Stinger owns sprint and team DoDs, this one owns the project floor tied to the Ship Gate.

Then follow [Guide 07](07-approve-and-revise.md) to get approval.
