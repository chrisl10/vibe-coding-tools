---
title: "Product Strategy: {product name}"
status: draft
owner: "{owner name}"
last-reviewed: "{YYYY-MM-DD}"
next-review: "{YYYY-MM-DD, about six months out}"
source: product-strategy-stinger
---

<!--
Template for library/knowledge/private/product/product-strategy.md.
Fill every section from the owner's answers. If the owner has not answered, write
"OPEN: {question}" instead of guessing. Keep page one to sections 1 through 8.
Plain words, short sentences, 8th-grade reading level. No em dashes or en dashes.
Each [D-###] tag points to a decision note in decisions/.
-->

# Product Strategy: {product name}

**In one sentence:** {For [who], who struggle with [problem], [product] helps them [job] better than [main alternative] because [key difference].}

## 1. The problem

{One short, specific story about one real person and why the way they do it today does not work. Who, what they tried, what went wrong, what it cost them.}

- **How we know:** {evidence, such as interviews, support tickets, the owner's own experience. Say "owner belief, not yet tested" if that is all there is.}

## 2. Who it is for

- **Best-fit customer:** {one segment, described by situation and need, not by age or job title alone}
- **Who decides and who pays:** {user, buyer, approver; same or different people?}
- **Not for (yet):** {segments we are choosing to ignore}
- **Deeper ICP work:** {link to an icp-research dossier, or "not needed yet" with the reason}

## 3. The job to be done

When {situation}, they want to {motivation}, so they can {outcome}.

- **Pains today:** {top 2 or 3}
- **Gains they want:** {top 2 or 3}

## 4. Positioning and how we are different

| Part | Our answer |
|---|---|
| What they use today instead (competitive alternatives, including "do nothing") | {list} |
| What we have that those do not (unique attributes) | {list} |
| Why that matters to them (value) | {list} |
| Who cares the most about that value (best-fit customers) | {segment} |
| The market we say we are in (category) | {existing category, or a niche of one} |

- **Competitive research:** {link to a competitive-research report, or "not done yet"}
- **Positioning check-in:** {date, about six months out} [D-###]

## 5. Our big bets (2 to 4)

| # | Bet | Why we believe it | What would prove us wrong | Moves which input |
|---|---|---|---|---|
| B1 | {bet} | {evidence or belief} | {signal} | {I1, I2 or I3} |
| B2 | {bet} | {evidence or belief} | {signal} | {input} |

## 6. How we will know it is working

- **The game we are playing:** {attention, transaction, or productivity, with one line on why}
- **North-star metric:** **{name}**: {exact definition: who counts, what action, what time window}
- **Why this one:** {how it shows customer value and leads revenue}

| Input | Definition | Bet that moves it |
|---|---|---|
| I1 {name} | {definition} | {B#} |
| I2 {name} | {definition} | {B#} |
| I3 {name} | {definition} | {B#} |

- **Not our north star:** {revenue, sign-ups, or other lagging or vanity numbers we will watch but not steer by}

## 7. Version 1

- **Appetite:** {how much time or money v1 is worth, as a limit}
- **In v1:** {the smallest set of things that lets the best-fit customer finish the job once}
- **NOT in v1:** {explicit list. Each item says why it waits.}
- **Rabbit holes to avoid:** {known traps and how we will sidestep them}

## 8. Risks and the riskiest assumption

| # | Assumption (must be true) | Type | Importance | Evidence today | Risk |
|---|---|---|---|---|---|
| A1 | {specific statement} | desirability / viability / feasibility / usability / ethical | high/med/low | strong/some/none | {high if important and weak evidence} |

**Riskiest assumption:** {A#}: {statement}

**Test it first:**

- **Smallest test:** {what we will do, without building the product}
- **Pass looks like:** {threshold set before the test}
- **Fail looks like:** {threshold}
- **If it fails:** {what we change}
- **Owner and date:** {who, by when}
- **Detailed test plan:** {link to discovery-research work, or "not started"}

---

## Pricing hypothesis

{One or two lines: who pays, roughly how (per seat, per use, flat), and the rough number we will test. Mark it "hypothesis".} Owner for real pricing work: SaaS pricing (software-economics-tools). [D-###]

## Rough size of the opportunity (optional)

{Bottom-up only: number of best-fit customers we can reach x rough price x share we can win in year one. Show the math and label every guess.}

## Open questions

- OPEN: {question still waiting on the owner}

## Decision log

| ID | Date | Decision | Note |
|---|---|---|---|
| D-001 | {date} | {short decision} | [decisions/D-001-{slug}.md](decisions/D-001-{slug}.md) |

## Hand-off

- **Next:** product-design-stinger reads sections 2, 3, 4 and 7. product-planning-stinger reads sections 5, 6, 7 and 8.
- **Not covered here:** PRDs (library-stinger), OKRs (okr-goal-setting-stinger).
