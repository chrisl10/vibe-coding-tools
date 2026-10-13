# Handoff Packet template

> Copy to: `library/requirements/plans/handoff-packet.md`
> Replace every `<placeholder>`. Delete these quote lines when done.
> Guide: [../../guides/06-write-handoff.md](../../guides/06-write-handoff.md)

---

# Handoff Packet: <product name>

> **Status:** Draft | Approved
> **Revision:** <n>
> **Approved by:** <owner name> on <YYYY-MM-DD> | Not yet approved
> **Built from:** PRD Map revision <n>, Wave Plan revision <n>, Definition of Done revision <n>

## Approved inputs

| Artifact | Path | Revision | Approved on |
|---|---|---|---|
| PRD Map | `library/requirements/plans/prd-map.md` | <n> | <YYYY-MM-DD> |
| Wave Plan | `library/requirements/plans/wave-plan.md` | <n> | <YYYY-MM-DD> |
| Definition of Done | `library/knowledge/private/standards/definition-of-done.md` | <n> | <YYYY-MM-DD> |

Do not act on this packet unless every row above says Approved.

## Step 1: to contract-writing-stinger (do this first)

Draft or reuse one CTR record per boundary below. The owner accepts each exact revision. Product planning does not write CTRs.

| Boundary | What is shared | Provider | Consumers | Existing CTR | Needed by wave |
|---|---|---|---|---|---|
| B01 | <description> | F01 | F02, F04 | <None or CTR-### revision n> | 1 |

PRDs that use a boundary still marked missing or draft cannot be finalized.

## Step 2: to library-stinger

Write one PRD per row, in wave order. Product planning does not write PRDs.

| Key | Title | One-line scope | Size | Depends on | Contract pins needed | Wave |
|---|---|---|---|---|---|---|
| F01 | <title> | <scope> | S | None | <B01> | 1 |

Instructions for Library:

1. Assign each key the next free `PRD-###` number and report the mapping back so the PRD Map and Wave Plan can be updated in a new revision.
2. Write acceptance criteria as the ID table with Given/When/Then from `templates/prd-template.md`. Do not use the checkbox list shown in guide 03.
3. Add the PRD-level Definition of Done checklist to each PRD and link the project Definition of Done revision.
4. Pin each accepted CTR revision under `## Contract dependencies`.
5. Do not change scope, dependencies or wave without sending the change back for a new plan revision.

## Step 3: to the build (later, not part of this packet's work)

When PRDs exist and contracts are accepted, `/smoke-it` (or TARS) reads the approved Wave Plan and runs the waves in order.

## Open decisions for the owner

- <decision, options, and which artifacts it affects>
