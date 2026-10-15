# Product Planning Stinger

Turns an approved Product Strategy and UX package into a build plan the rest of the Wasp Nest can follow: which PRDs to write, in what order to build them, what "done" means for every one of them, and a handoff that tells the Library and the contract writer exactly what to do next.

It plans. It does not write PRDs, write contracts, or build anything.

## What it makes

| Artifact | Saved at | Read by |
|---|---|---|
| PRD Map | `library/requirements/plans/prd-map.md` | Library, contract-writing, the owner |
| Wave Plan (with Mermaid graph) | `library/requirements/plans/wave-plan.md` | `/smoke-it`, TARS |
| Definition of Done | `library/knowledge/private/standards/definition-of-done.md` | every PRD, Security, Quality, `/smoke-it` |
| Handoff Packet | `library/requirements/plans/handoff-packet.md` | contract-writing, then Library |

The owner approves each one, by exact revision, before anyone uses it.

## Guide map

| Step | Guide |
|---|---|
| Read the strategy and UX package | [guides/01-read-inputs.md](guides/01-read-inputs.md) |
| Break the product into PRDs | [guides/02-map-features.md](guides/02-map-features.md) |
| Flag shared boundaries for contracts | [guides/03-flag-boundaries.md](guides/03-flag-boundaries.md) |
| Order the PRDs into waves | [guides/04-plan-waves.md](guides/04-plan-waves.md) |
| Write the Definition of Done | [guides/05-set-definition-of-done.md](guides/05-set-definition-of-done.md) |
| Write the Handoff Packet | [guides/06-write-handoff.md](guides/06-write-handoff.md) |
| Get approval and handle changes | [guides/07-approve-and-revise.md](guides/07-approve-and-revise.md) |

## References

- [Artifact paths, owners and status words](references/artifact-paths.md)
- Templates: [PRD Map](references/templates/prd-map.md), [Wave Plan](references/templates/wave-plan.md), [Definition of Done](references/templates/definition-of-done.md), [Handoff Packet](references/templates/handoff-packet.md)
- Worked example: [PRD Map](references/examples/example-prd-map.md) and [Wave Plan](references/examples/example-wave-plan.md)
- [Research distillation](references/research/distilled-product-planning.md) and its raw sources
- [Wave Plan checker](scripts/check_wave_plan.py): `python3 scripts/check_wave_plan.py wave-plan.md --prd-map prd-map.md`

## Where it sits in Product Studio

1. `product-strategy-stinger` writes the Product Strategy.
2. `product-design-stinger` writes the UX package.
3. **This Stinger** writes the plan, DoD and handoff.
4. `contract-writing-stinger` drafts contracts; `library-stinger` writes PRDs.
5. `/smoke-it` or TARS builds, wave by wave.

The two sibling Stingers in steps 1 and 2 live in this same pack. Core owners (Library, Contract Writing, `/smoke-it`, TARS) resolve through the selected Core plugin.

## Provenance

Research swept 2026-10-12 over the six months before it. 14 raw sources archived; settled methods older than the window are marked with their real age, and secondary sources are marked as thin. See the distillation for limits.

Part of The Wasp Nest, curated by [Mario Aldayuz a.k.a @thenotoriousllama](https://github.com/thenotoriousllama).
