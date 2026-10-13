# Artifact paths, owners and statuses

Load this when you need to know where a file goes, who may write it, or what a status means.

## Inputs (read only)

| Input | Path | Made by | If missing |
|---|---|---|---|
| Product Strategy | `library/knowledge/private/product/product-strategy.md` | `product-strategy-stinger` (sibling in this pack) | Stop. Ask the owner to run the strategy stage first. |
| UX package | `library/knowledge/private/product/design/` | `product-design-stinger` (sibling in this pack) | Stop, or plan with the owner's written OK and mark every journey gap. |
| Existing PRDs | `library/requirements/{backlog,in-work,completed}/prd-*/` | `library-stinger` | Fine for a new product. |
| Existing contracts | `library/knowledge/private/contracts/CTR-*.md` | `contract-writing-stinger` | Fine; every boundary is then `missing`. |
| Existing DoD | `library/knowledge/private/standards/definition-of-done.md` | this Stinger | Write a new one. |

## Outputs (this Stinger writes only these)

| Artifact | Path | Template |
|---|---|---|
| PRD Map | `library/requirements/plans/prd-map.md` | [templates/prd-map.md](templates/prd-map.md) |
| Wave Plan | `library/requirements/plans/wave-plan.md` | [templates/wave-plan.md](templates/wave-plan.md) |
| Definition of Done | `library/knowledge/private/standards/definition-of-done.md` | [templates/definition-of-done.md](templates/definition-of-done.md) |
| Handoff Packet | `library/requirements/plans/handoff-packet.md` | [templates/handoff-packet.md](templates/handoff-packet.md) |

Library's path table and the Get Started scaffold list `requirements/plans/` and `knowledge/private/standards/`. In an older repository that predates them, create the folders only when the owner approves the first artifact, and tell Library the new homes in the Handoff Packet.

## Never write

| Path | Owner |
|---|---|
| PRD folders and files | `library-stinger` |
| `CTR-*` contract records | `contract-writing-stinger` |
| `EXECUTION_LEDGER.md` and build code | `/smoke-it` and the build Drones |
| `library/notes/` | humans only; do not read it either |
| Product Strategy and UX package | their sibling Stingers; send changes back to them |

## Status words

| Status | Meaning | Who may act on it |
|---|---|---|
| Draft | Written, not approved | Nobody downstream |
| Approved | The owner said yes to this exact revision, with name and date | Library, contract-writing, `/smoke-it`, TARS |
| Superseded | A newer revision is Approved | Nobody; kept for history |

Approval belongs to one revision. Any change after approval makes a new Draft revision.

## Dependency words

| Word | Meaning |
|---|---|
| Depends on | End-to-start: the other PRD must be VERIFIED before this one may start its wave. |
| Shared boundary | An API, event, data shape, permission rule or state change that two or more PRDs rely on. Needs a CTR. |
| Wave | A group of PRDs that can be built at the same time because none depends on another in the group. |
| Entry criteria | Pass/fail checks that must be true before a wave starts. |
| Exit criteria | Pass/fail checks that must be true before a wave counts as finished. |
