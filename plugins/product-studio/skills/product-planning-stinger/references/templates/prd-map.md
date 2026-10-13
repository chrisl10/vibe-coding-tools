# PRD Map template

> Copy to: `library/requirements/plans/prd-map.md`
> Replace every `<placeholder>`. Delete these quote lines when done.
> Guide: [../../guides/02-map-features.md](../../guides/02-map-features.md)

---

# PRD Map: <product name>

> **Status:** Draft | Approved
> **Revision:** <n>
> **Approved by:** <owner name> on <YYYY-MM-DD> | Not yet approved
> **Strategy source:** `library/knowledge/private/product/product-strategy.md` (read <YYYY-MM-DD>)
> **UX source:** `library/knowledge/private/product/design/` (read <YYYY-MM-DD>)

## What this is

A list of the PRDs that need to be written, one row each. This file does not contain the PRDs. `library-stinger` writes them from this list. `F##` keys are planning keys; Library assigns the real `PRD-###` numbers and writes them back into the PRD column.

## PRDs to write

| Key | PRD | Title | One-line scope | Size | Depends on | Shared boundaries | Journey steps covered | Risk | Nice-to-have |
|---|---|---|---|---|---|---|---|---|---|
| F01 | TBD | <short name of what it delivers> | <one sentence: who can do what, and the limit> | S / M / L | None | <B01, B02 or None> | <J1.1, J1.2> | High / Medium / Low | No |
| F02 | TBD | | | | F01 | | | | |

Column rules:

- **Size:** a budget, not an estimate. S fits in a few days, M in about a week, L in two weeks. Anything bigger gets split.
- **Depends on:** keys this PRD cannot finish without (end-to-start). Use `None` when there are none.
- **Shared boundaries:** ids from the table below. A boundary is shared when two or more PRDs rely on the same API, event, data shape, permission rule or state change.
- **Journey steps covered:** step ids from the UX package journeys.
- **Nice-to-have:** `Yes` means it can be cut without breaking the main journey.

## Shared boundaries that need CTR contracts

| Boundary | What is shared | Provider PRD | Consumer PRDs | Existing CTR | Status for contract-writing |
|---|---|---|---|---|---|
| B01 | <for example: the order record shape> | F01 | F02, F04 | <CTR-### revision n, or None> | missing / draft / accepted |

## Journey coverage check

| Journey step | Covered by |
|---|---|
| <J1.1 step name> | F01 |

Every step must name at least one key, or be listed under Gaps.

## Out of scope

- <strategy items deliberately left out, with the reason>

## Gaps and open questions

- <missing input, unclear scope, or a decision the owner must make>
