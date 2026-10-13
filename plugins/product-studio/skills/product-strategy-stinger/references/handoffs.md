# Hand-offs and routing

This skill writes the strategy. It calls into other owners for deep work instead of copying their methods. Resolve each owner through the installed plugin catalog (Core's selected-plugin resolver, or `plugin-catalog.json` in a source checkout). Do not assume a sibling pack is installed because its folder exists. If an owner is missing, say so, mark the section "OPEN: needs {owner}", and keep going.

## Calls out (this skill asks another owner for help)

| Need | Owner skill (pack) | When to call | What comes back into the strategy |
|---|---|---|---|
| Deeper ICP than an owner summary | `icp-research-stinger` (growth-and-customer-tools) | Owner is not the customer, B2B with an unclear buyer, or Q2.5 says yes | Link in section 2; best-fit segment and buying roles summarized in 3 to 5 lines |
| Competitor landscape | `competitive-research-stinger` (growth-and-customer-tools) | Q3.5 says yes, or the owner names more than 3 alternatives they cannot rank | Link in section 4; alternatives list and the gap we exploit |
| Interviews, assumption maps, experiments | `discovery-research-stinger` (business-and-product-tools) | The riskiest assumption needs a real test plan, or demand is untested | Link in section 8; test design and pass/fail thresholds |
| Real pricing work | `saas-pricing-stinger` (software-economics-tools) | Owner wants more than a one-line hypothesis | Link under Pricing hypothesis |
| First acquisition channel | `go-to-market-stinger` (growth-and-customer-tools) | Owner asks "how do we reach them" | Not part of this doc; note the link in Open questions |

## Feeds (who reads this strategy next)

| Reader | Sections it needs | Contract |
|---|---|---|
| `product-design-stinger` (product-studio) | 2 Who, 3 Job, 4 Positioning, 7 Version 1 | These sections must be filled or marked OPEN. Design must not add scope that section 7 lists as NOT in v1 without a new decision note |
| `product-planning-stinger` (product-studio) | 5 Bets, 6 Metrics, 7 Version 1, 8 Riskiest assumption | Planning sequences work so the riskiest assumption test comes first. Each planned item should name the bet or input it serves |

## Do not route here

| Request | Correct owner |
|---|---|
| A new feature idea while the product is mid-build | KIPP in the TARS desk |
| Writing a PRD or IRD | `library-stinger` (Core) |
| Writing or grading OKRs | `okr-goal-setting-stinger` (business-and-product-tools) |
| Full competitor workbook or battlecards | `competitive-research-stinger` |
| Running customer interviews | `discovery-research-stinger` |

If a strategy session turns up a PRD-sized idea, record it under Open questions and hand it to `library-stinger` after the strategy is saved. Do not write the PRD here.

## Output paths

| Artifact | Path |
|---|---|
| Strategy | `library/knowledge/private/product/product-strategy.md` |
| Decision notes | `library/knowledge/private/product/decisions/D-###-{slug}.md` |

If `library/` does not exist, ask the owner before creating it, and suggest `get-started-stinger` (Core) for a full Library setup. Never overwrite another agent's in-progress file in these folders.
