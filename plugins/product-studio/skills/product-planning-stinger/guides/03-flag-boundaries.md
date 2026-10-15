# Guide 03: Flag shared boundaries that need contracts

Goal: list every place where two or more PRDs must agree on the same thing, so `contract-writing-stinger` can write a contract (CTR) before the PRDs are finished. You flag boundaries. You do not write or accept contracts.

## What counts as a shared boundary

Something one PRD provides and another PRD relies on:

- an API call or endpoint,
- an event or message,
- a shared data shape or record,
- a permission rule (who may do what),
- a state change (for example, a booking moving from "held" to "confirmed").

If only one PRD uses it, it is not shared. If the swap point between a quick first version and a later real version is an interface, that interface is shared. Skeleton on crutches

## Steps

1. For each dependency edge in the PRD Map, ask "what exactly does the waiting PRD need from the other one?" Each answer is a candidate boundary.
2. Also look for two PRDs that read or write the same record even without a dependency edge.
3. Give each boundary an id (`B01`, `B02`, ...), a short "what is shared", one provider key and the consumer keys.
4. Check `library/knowledge/private/contracts/` for an existing `CTR-*` that already covers it. If one does, write its id and revision. Otherwise write `None`.
5. Mark status: `accepted` (an accepted CTR revision exists), `draft` (a CTR exists but is not accepted), or `missing`.
6. Copy the boundary ids into the "Shared boundaries" column of each PRD row that uses them.

## What you must not do

- Do not decide the fields, rules or error behavior of a boundary. That is contract work.
- Do not mark a boundary accepted yourself.
- Do not drop a PRD's dependency just because a contract will exist. The contract lets PRDs be written in parallel; the build order still follows the dependency.

## Done when

Every dependency edge either names a boundary or is clearly not about a shared interface, and every boundary has a provider, consumers and a status.

Source: this mirrors the boundary inventory in `contract-writing-stinger` (`src/skills/contract-writing-stinger/guides/01-identify-boundaries.md`), which owns the next step. It is a Wasp Nest convention, not an external standard ([../references/research/distilled-product-planning.md](../references/research/distilled-product-planning.md)).
