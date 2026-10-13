# Product Strategy Stinger

Turns a raw product idea, or the product inside an existing repo, into a one-page-plus Product Strategy. It interviews the owner in short batches, offers a "(Recommended)" answer with a reason, and writes down only what the owner decides. It never invents strategy.

**Output:** `library/knowledge/private/product/product-strategy.md`, plus one decision note per real choice in `library/knowledge/private/product/decisions/`.

**What the strategy covers:** the problem, who it is for, the job to be done, positioning and differentiation, 2 to 4 big bets, a north-star metric with 3 input metrics, v1 scope with an explicit NOT-in-v1 list, risks and the riskiest assumption test, and a pricing hypothesis pointer.

## Read by task

| Task | Guide |
|---|---|
| Running the interview | [Interview the owner](guides/interview-the-owner.md) |
| The product already exists in code | [Start from an existing repo](guides/start-from-existing-repo.md) |
| Problem, customer, job (sections 1 to 3) | [Define problem and customer](guides/define-problem-and-customer.md) |
| Positioning (section 4) | [Position the product](guides/position-the-product.md) |
| Big bets (section 5) | [Choose big bets](guides/choose-big-bets.md) |
| North star and inputs (section 6) | [Set the north star](guides/set-north-star.md) |
| V1 and the NOT list (section 7) | [Scope v1](guides/scope-v1.md) |
| Riskiest assumption (section 8) | [Find the riskiest assumption](guides/find-riskiest-assumption.md) |
| Decision notes | [Record decisions](guides/record-decisions.md) |
| Assemble, check, save, update, hand off | [Write and hand off](guides/write-and-hand-off.md) |

## References

| File | Use it for |
|---|---|
| [templates/product-strategy.md](references/templates/product-strategy.md) | The strategy document shape |
| [templates/interview-question-bank.md](references/templates/interview-question-bank.md) | Batched questions with (Recommended) answers |
| [templates/decision-note.md](references/templates/decision-note.md) | One decision per note |
| [handoffs.md](references/handoffs.md) | Which owner to call for ICP, competitors, discovery, pricing; who reads this next |
| [examples/worked-example.md](references/examples/worked-example.md) | A made-up, filled strategy that passes the checker |
| [research/distilled-product-strategy.md](references/research/distilled-product-strategy.md) | Cited research behind every rule here |
| [research/source-ledger.json](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-strategy-stinger/references/research/source-ledger.json) | URL, fetch date, hash and date window for each raw source |
| [scripts/check-strategy.py](scripts/check-strategy.py) | Structural check of a finished strategy |

## Related owners and host support

This skill calls into other owners instead of copying them: `icp-research-stinger` and `competitive-research-stinger` and `go-to-market-stinger` (growth-and-customer-tools), `discovery-research-stinger` and `okr-goal-setting-stinger` (business-and-product-tools), `saas-pricing-stinger` (software-economics-tools), and Core's `library-stinger` and `get-started-stinger`. Its output feeds the sibling pairs `product-design-stinger` and `product-planning-stinger` in this pack. Resolve every owner through the installed plugin catalog. A missing optional owner does not block the strategy; mark that section OPEN.

Claude Code and Cowork use the plugin's skill and agent surfaces. Cursor uses the projected agent in `cursor-agents/`. Codex uses the generated role and this skill directly. If a host cannot delegate to the paired Drone, use this skill directly and say so.

Runtime writes planning documents only, never app code. It still writes into repositories, so the Ship Gate in [SKILL.md](SKILL.md) applies before any commit.

## Provenance

Research fetched 2026-10-13 (UTC): 21 raw sources. 8 fall inside the requested 6-month window; 8 are foundational sources older than 12 months, kept for definitions and flagged for owner consent. See section 0 of the distillation.
