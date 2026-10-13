# PRD Map: Tidy Bookings (worked example)

> **Status:** Approved
> **Revision:** 1
> **Approved by:** Example Owner on 2026-10-12
> **Strategy source:** `library/knowledge/private/product/product-strategy.md` (read 2026-10-12)
> **UX source:** `library/knowledge/private/product/design/` (read 2026-10-12)

This is a made-up example. Tidy Bookings lets customers book a dog-grooming slot online. The strategy says the first goal is "a customer can book without phoning". The UX package has two journeys: J1 customer books, J2 groomer runs the day.

## PRDs to write

| Key | PRD | Title | One-line scope | Size | Depends on | Shared boundaries | Journey steps covered | Risk | Nice-to-have |
|---|---|---|---|---|---|---|---|---|---|
| F01 | TBD | Service list | The groomer adds services with a name, length and price; customers can see them. | S | None | B01 | J1.1 | Low | No |
| F02 | TBD | Book a slot | A customer picks a service and a free slot and gets a booking; double booking is refused. | M | F01, F03 | B01, B02, B03 | J1.2, J1.3 | High | No |
| F03 | TBD | Open hours | The groomer sets weekly open hours and days off; the system turns them into free slots. | M | None | B02 | J2.1 | High | No |
| F04 | TBD | Booking email | The customer and groomer get an email when a booking is made or cancelled. | S | F02 | B03 | J1.4 | Medium | No |
| F05 | TBD | Day schedule | The groomer sees today's bookings in time order on a phone. | S | F02 | B03 | J2.2 | Low | No |
| F06 | TBD | Text reminders | The customer gets a text the day before. | S | F04 | B03 | J1.5 | Medium | Yes |

## Shared boundaries that need CTR contracts

| Boundary | What is shared | Provider PRD | Consumer PRDs | Existing CTR | Status for contract-writing |
|---|---|---|---|---|---|
| B01 | Service record (id, name, minutes, price) | F01 | F02 | None | missing |
| B02 | Free slot shape and the rule for what counts as free | F03 | F02 | None | missing |
| B03 | Booking record and the booking created or cancelled event | F02 | F04, F05, F06 | None | missing |

## Journey coverage check

| Journey step | Covered by |
|---|---|
| J1.1 See services | F01 |
| J1.2 Pick a slot | F02 |
| J1.3 Confirm booking | F02 |
| J1.4 Get confirmation | F04 |
| J1.5 Get reminder | F06 |
| J2.1 Set open hours | F03 |
| J2.2 See the day | F05 |

## Out of scope

- Online payment. The strategy says pay in person for the first release.

## Gaps and open questions

- Cancellation window: the strategy does not say how late a customer may cancel. Owner to decide before F02 is written.
