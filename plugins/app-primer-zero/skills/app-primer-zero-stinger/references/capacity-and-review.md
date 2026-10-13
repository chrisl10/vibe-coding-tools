# Capacity and ordered review

The handoff describes a bounded plan. It does not discover a runtime, launch workers or prove that a person approved its fields.

## Capacity fields

| Field | Rule |
|---|---|
| `mode` | `parallel` by default; `serial-preparation` is explicit when preparation runs in one inline assistant |
| `limit` | Positive integer for the whole compatible set of waves; serial preparation requires exactly 1 |
| `coordinator_slots` | Exactly 1 logical integrator; this role cannot be removed to evade overhead |
| `reviewer_slots` | Positive ceiling on actually simultaneous reviewers; idle capacity is not charged as active work |
| `verified` | Boolean if present; only `true` can support a declared ready implementation wave in parallel mode |

Existing plans without `mode` use parallel mode. Existing `reviewer_slots: 2` remains valid, but scheduling Security and Quality concurrently is refused. Unsupported capacity fields are rejected rather than silently treated as additional capacity.

In parallel mode, count one coordinator plus each active implementation worker or reviewer, once. The coordinator is charged even when omitted from `active_shards`. Repeating its logical ID across independent waves does not create extra integrators. A three-slot plan can schedule two implementers, then one Security reviewer, then one Quality reviewer. A two-slot plan can schedule one implementer and its later reviews. Review ceilings alone do not reserve idle agents.

In serial preparation, the coordinator works inline in the one slot. Preparation and sequential review-shaped tasks can be described, but they do not prove independent review. Even with `verified: true`, this mode refuses every `ready: true` implementation wave. A later execution handoff must qualify the actual runtime and independent review surface; changing an assertion is not qualification.

Flatten all nested work into explicit shard IDs. Hidden `nested_workers`, `nested_slots` or `reserved_slots` declarations are refused. The validator cannot detect an author who omits real workers from the artifact; the coordinator must check actual runtime activity.

## Wave and review rules

Dependency edges serialize waves. Independent waves can overlap, so the helper checks every maximal compatible set for aggregate capacity, repeated worker IDs and lexical ownership conflicts. Setting `ready: false` does not exempt a future wave from structural counting.

Each implementation shard owns explicit canonical relative prefixes. No absolute paths, traversal, globs or exclusion leases are accepted. Coordinators and reviewers own no product source paths. The helper does not resolve symlinks or inspect files; real leases need runtime inspection.

Schedule Security and Quality in separate waves. A review cannot overlap implementation changes. Every Quality wave must follow a Security wave whose ancestors cover all implementation preceding that Quality wave. Implementation between the reviews requires another Security wave. Every implementation wave must lead to a later ordered review; changes after final Quality cannot escape the gate.

These dependency checks establish planned ordering only. Review success, independent authorship and exact candidate identity require actual reports. The integrator still clears Security before Quality and checks repository health under the applicable authority.

## Contract and readiness rules

Pin exact declared CTR revisions. Draft contracts can exist in a valid preparation plan, while their implementation remains blocked. Ready implementation requires Accepted status, nonempty approver and approval evidence, declared verified capacity, ready dependencies and a non-example plan. Those strings are author assertions, not proof of human acceptance.

The helper checks full Git object-ID syntax, not commit existence. Illustrative fixtures cannot declare implementation ready. A PASS means structural checks passed; it does not authorize implementation, installation, configuration, provider use, publication or deployment.

## Bounded analysis

The helper accepts at most 64 waves and enumerates at most 4,096 compatible sets. Larger or more complex plans need smaller handoffs. It reads JSON through the standard library, reports limitations with every result, and writes no plan or application files.

Run the installed [validator](../scripts/validate_handoff.py) and its [tests](../scripts/test_validate_handoff.py) against the proposed artifact. Read the [wave handoff template](../templates/wave-handoff.md) for the surrounding evidence and authority record.
