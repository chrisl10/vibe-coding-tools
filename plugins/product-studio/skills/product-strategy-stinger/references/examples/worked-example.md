---
title: "Product Strategy: Tallyline (made-up example)"
status: draft
owner: "Example Owner"
last-reviewed: "2026-10-12"
next-review: "2027-04-12"
source: product-strategy-stinger
---

<!--
MADE-UP EXAMPLE. Tallyline, its customers, and every number here are invented to show
the shape of a finished strategy. Nothing here is research or a recommendation.
Run: python3 scripts/check-strategy.py references/examples/worked-example.md
-->

# Product Strategy: Tallyline

**In one sentence:** For solo bookkeepers who chase clients for receipts every month, Tallyline collects and matches receipts by text message, so month-end closes in hours instead of days, which email and shared folders cannot do because clients ignore them.

## 1. The problem

Dana keeps the books for 22 small shops. Every month she emails each client for missing receipts. Half do not answer. She spends the last four days of each month chasing, and twice this year she filed late and paid the penalty for a client.

- **How we know:** the owner did this job for six years, and 5 bookkeepers in an online group described the same chase. Demand from people who are not the owner is still owner belief, not yet tested (A1).

## 2. Who it is for

- **Best-fit customer:** solo bookkeepers with 10 to 40 small-business clients who mostly pay with cards.
- **Who decides and who pays:** the bookkeeper uses it and pays. Their clients only reply to texts.
- **Not for (yet):** accounting firms with staff, and businesses doing their own books.
- **Deeper ICP work:** not needed yet. The owner was this customer. Revisit after 20 paying users.

## 3. The job to be done

When the month is ending, they want every client receipt matched to its bank line, so they can close on time without chasing anyone.

- **Pains today:** clients ignore email; matching by hand is slow; late filing penalties.
- **Gains they want:** close in one day; look professional to clients.

## 4. Positioning and how we are different

| Part | Our answer |
|---|---|
| What they use today instead (competitive alternatives, including "do nothing") | Email reminders, shared folders, the receipt feature in their accounting software, or doing nothing and estimating |
| What we have that those do not (unique attributes) | Clients reply by text photo with no app or login; auto-match to the bank line |
| Why that matters to them (value) | Clients actually answer; month-end shrinks from days to hours |
| Who cares the most about that value (best-fit customers) | Solo bookkeepers with many small clients |
| The market we say we are in (category) | Receipt collection for bookkeepers (a niche of receipt capture) |

- **Competitive research:** not done yet.
- **Positioning check-in:** 2027-04-12 [D-002]

## 5. Our big bets (2 to 4)

| # | Bet | Why we believe it | What would prove us wrong | Moves which input |
|---|---|---|---|---|
| B1 | Text messages beat email for getting clients to respond | Owner saw clients answer texts same day | Fewer than half of requested receipts come back within 3 days | I1 |
| B2 | Win solo bookkeepers before firms | Owner knows this group; fast buying decision | Solo users churn within 2 months | I3 |
| B3 | Auto-match is good enough without manual review | Most card receipts carry amount and date | More than 1 in 5 matches need fixing | I2 |

Not betting on: a mobile app for clients, or full bookkeeping features.

## 6. How we will know it is working

- **The game we are playing:** productivity. Bookkeepers want month-end work done faster.
- **North-star metric:** **Months closed on time**: count of client-months where every receipt was matched by the 3rd of the next month.
- **Why this one:** it is the value the bookkeeper pays for, and on-time closes should lead renewals.

| Input | Definition | Bet that moves it |
|---|---|---|
| I1 Reply rate | Share of receipt requests answered within 3 days | B1 |
| I2 Auto-match rate | Share of receipts matched with no manual fix | B3 |
| I3 Clients connected | Average clients per bookkeeper set up in their first 2 weeks | B2 |

- **Not our north star:** revenue, sign-ups, and texts sent. We watch them but do not steer by them.

## 7. Version 1

- **Appetite:** 6 weeks of one builder.
- **In v1:** add clients by phone number; send a receipt request text; receive photos; match to an uploaded bank CSV; month-end checklist.
- **NOT in v1:** bank feed connections (CSV upload is enough to test the bets); accounting software sync (wait for 20 paying users to ask); client app (texts only, by design); team accounts (solo bookkeepers first).
- **Rabbit holes to avoid:** reading handwritten receipts. v1 only matches on amount and date.

## 8. Risks and the riskiest assumption

| # | Assumption (must be true) | Type | Importance | Evidence today | Risk |
|---|---|---|---|---|---|
| A1 | Solo bookkeepers other than the owner lose 2 or more days a month chasing receipts | desirability | high | some | med |
| A2 | Clients will reply to a text from their bookkeeper with a photo within 3 days | desirability | high | none | high |
| A3 | Bookkeepers will pay 30 dollars a month for this | viability | high | none | high |
| A4 | Amount and date are enough to match most card receipts | feasibility | med | some | med |

**Riskiest assumption:** A2: clients will reply to a text with a photo within 3 days.

**Test it first:**

- **Smallest test:** the owner texts 30 real clients of 3 friendly bookkeepers by hand, from a normal phone, for one month-end. No product built.
- **Pass looks like:** 60 percent or more reply with a usable photo within 3 days.
- **Fail looks like:** under 40 percent.
- **If it fails:** test email with a one-tap upload link instead before building anything.
- **Owner and date:** Example Owner, by 2026-11-05.
- **Detailed test plan:** not started.

---

## Pricing hypothesis

Bookkeeper pays a flat 30 dollars a month (hypothesis, tests A3). Owner for real pricing work: SaaS pricing (software-economics-tools). [D-003]

## Open questions

- OPEN: Do bookkeepers need client consent rules for texting? Check before the A2 test.

## Decision log

| ID | Date | Decision | Note |
|---|---|---|---|
| D-001 | 2026-10-12 | Solo bookkeepers first | decisions/D-001-solo-bookkeepers-first.md |
| D-002 | 2026-10-12 | Positioning check-in every 6 months | decisions/D-002-positioning-check-in.md |
| D-003 | 2026-10-12 | Flat monthly price hypothesis | decisions/D-003-flat-price-hypothesis.md |

## Hand-off

- **Next:** product-design-stinger reads sections 2, 3, 4 and 7. product-planning-stinger reads sections 5, 6, 7 and 8, and schedules the A2 test first.
- **Not covered here:** PRDs (library-stinger), OKRs (okr-goal-setting-stinger).
