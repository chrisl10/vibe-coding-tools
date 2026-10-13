# Guide 06: Write the Handoff Packet

Goal: one file at `library/requirements/plans/handoff-packet.md` that tells `contract-writing-stinger` which boundaries to draft and `library-stinger` exactly which PRDs to write. The packet is instructions for other owners. You do not write PRDs or CTRs yourself.

Template: [../references/templates/handoff-packet.md](../references/templates/handoff-packet.md).

## Before you start

The PRD Map, Wave Plan and Definition of Done must all be Approved (exact revisions). If any is Draft, stop and finish [Guide 07](07-approve-and-revise.md) first.

## Steps

1. **Fill the approved inputs table** with each artifact's path, revision and approval date.
2. **Step 1 for contract-writing.** Copy every boundary with status `missing` or `draft` from the PRD Map. Add "needed by wave": the earliest wave that has a PRD using it. Contracts come first because PRDs that use a missing or draft boundary cannot be finalized.
3. **Step 2 for Library.** One row per PRD in wave order: key, title, one-line scope, size, depends on, contract pins needed, wave. Copy these exactly from the approved map and plan. Do not add new scope here.
4. **Keep the five Library instructions** from the template. The important one: write acceptance criteria as the ID table with Given/When/Then from the PRD template (`src/skills/library-stinger/templates/prd-template.md`), not the checkbox list shown in Library guide 03. The two Library files disagree today; the PRD template wins.
5. **Ask Library to report the key to `PRD-###` mapping.** When it arrives, update the PRD column in the map and plan as a new revision (no scope change, so the owner can approve it quickly).
6. **List open decisions** that still block any PRD.
7. Get the packet approved ([Guide 07](07-approve-and-revise.md)), then tell the orchestrator it is ready. The orchestrator dispatches contract-writing first, then Library.

## What happens next (not your job)

- `contract-writing-stinger` drafts CTRs and the owner accepts them.
- `library-stinger` writes PRDs and pins accepted CTR revisions.
- `/smoke-it` or TARS reads the approved Wave Plan and builds.

Source: the order (contracts before parallel PRDs, Library owns PRDs and pins) follows `src/skills/contract-writing-stinger/guides/03-handoff-to-library.md` and `src/skills/library-stinger/guides/03-feature-prd.md`. These are Wasp Nest conventions ([../references/research/distilled-product-planning.md](../references/research/distilled-product-planning.md)).
