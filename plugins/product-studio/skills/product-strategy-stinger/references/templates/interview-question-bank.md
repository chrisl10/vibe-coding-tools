# Interview question bank

Ask the owner in small batches: 3 to 5 questions per batch, one batch per strategy area. Every question offers answer choices, and one is marked **(Recommended)** with a one-line reason. The owner can pick, edit, or write their own. You never fill a section with your own idea and call it the owner's.

How to pick the (Recommended) answer:

- Base it on what the owner already said, what the repo shows, or a rule in [the distillation](../research/distilled-product-strategy.md). Name which one.
- If you have nothing to base it on, say "(Recommended: no basis yet, pick what is true for you)" and do not lean.
- A recommendation is a suggestion, not a decision. Record only what the owner picks.

Format each question like this:

```
Q2.1 Who feels this problem the most?
  a) Solo freelancers who bill by the hour (Recommended: matches the story you told in Q1.1)
  b) Small agencies with 5 to 20 people
  c) In-house teams at larger companies
  d) Something else: ____
```

## Batch 0: Starting point (always first)

| ID | Question | Typical choices |
|---|---|---|
| Q0.1 | Is this a brand-new idea or a product that already exists in this repo? | New idea / Existing repo (Recommended if a repo with app code is open) |
| Q0.2 | How much time should this strategy session take? | Quick pass, about 20 minutes (Recommended for a first draft) / Full pass / Just one section |
| Q0.3 | Is there an older strategy, pitch deck, or notes I should read first? | Yes, here: ____ / No |

## Batch 1: The problem (section 1)

| ID | Question | Notes |
|---|---|---|
| Q1.1 | Tell me about one real person who has this problem. What happened last time? | Open answer. Push for one specific story, not a summary |
| Q1.2 | What do they do about it today? | Choices: spreadsheet or manual work / another product / pay someone / nothing |
| Q1.3 | How do you know this problem is real? | I have it myself / I talked to people (how many?) / I saw it in data / It is a guess (Recommended answer if no evidence: say so, it becomes an assumption) |
| Q1.4 | What does the problem cost them? | Time / money / risk / stress. Ask for a rough number |

## Batch 2: Who it is for and the job (sections 2 and 3)

| ID | Question | Notes |
|---|---|---|
| Q2.1 | Who feels this problem the most? | Offer 2 to 4 segments drawn from Batch 1 answers |
| Q2.2 | Is the person who uses it the same person who pays? | Same / Different. If different, who approves the purchase? |
| Q2.3 | Who is this NOT for, at least for now? | Ask for at least one |
| Q2.4 | Finish this: "When ___, they want to ___, so they can ___." | Offer a draft built from their words, marked (Recommended) |
| Q2.5 | Do we need deeper ICP research before going on? | No, we know them well enough (Recommended if the owner is the customer) / Yes, run icp-research |

## Batch 3: Positioning (section 4)

| ID | Question | Notes |
|---|---|---|
| Q3.1 | If your product did not exist, what would they use? | Must include "do nothing" as a choice |
| Q3.2 | What can you do that those cannot? | List; then ask "so what?" for each |
| Q3.3 | Which of those differences matter most to the best-fit customer? | Pick 1 or 2 |
| Q3.4 | What would you call the kind of product this is? | Existing category (Recommended: cheaper to explain) / A niche of an existing category / A brand-new category |
| Q3.5 | Should we run competitive research now? | Not yet, positioning is a first guess (Recommended for a raw idea) / Yes |

## Batch 4: Big bets (section 5)

| ID | Question | Notes |
|---|---|---|
| Q4.1 | What are the 2 to 4 big things you are betting on? | Offer candidates drawn from Batches 1 to 3. Each bet must be a choice, not a feature list |
| Q4.2 | For each bet, what would prove you wrong? | One signal per bet |
| Q4.3 | What are we choosing NOT to bet on? | At least one |

## Batch 5: Metrics (section 6)

| ID | Question | Notes |
|---|---|---|
| Q5.1 | Which game is this product playing? | Attention (time spent) / Transaction (things bought or completed) / Productivity (work done faster or better). Recommend one and say why |
| Q5.2 | Which of these north-star options best shows customers getting value? | Offer 2 or 3 drafts with exact definitions. Never offer revenue, sign-ups, or daily active users as the recommended pick |
| Q5.3 | Pick 3 inputs that your work can move directly. | Offer 4 or 5 candidates; owner picks 3 |
| Q5.4 | Can we measure these today? | Yes / Not yet, that is fine for now / Never. "Never" means pick another metric |

## Batch 6: Version 1 (section 7)

| ID | Question | Notes |
|---|---|---|
| Q6.1 | How much time or money is v1 worth to you? | 2 weeks / 6 weeks (Recommended for a first product) / 3 months / other. This is a limit, not an estimate |
| Q6.2 | What is the smallest thing that lets one best-fit customer finish the job once? | Offer a draft list |
| Q6.3 | Which of these ideas can wait until after v1? | Show every extra idea raised so far; default each to "wait" (Recommended) unless the owner says it is needed for Q6.2 |
| Q6.4 | What could swallow the whole timeline? | Rabbit holes |

## Batch 7: Risks and the riskiest assumption (section 8)

| ID | Question | Notes |
|---|---|---|
| Q7.1 | What has to be true for this to work? | Draft assumptions from earlier answers, sorted by the five types; owner confirms or edits |
| Q7.2 | For each, how much proof do you have today? | Strong / Some / None |
| Q7.3 | Which one, if wrong, kills the idea? | Recommend the one that is high importance with the least proof |
| Q7.4 | What is the smallest test of that one, without building the product? | Offer 2 options. Hand off to discovery-research for detail |
| Q7.5 | What result counts as a pass? | Set the number before the test |

## Batch 8: Pricing pointer and wrap-up

| ID | Question | Notes |
|---|---|---|
| Q8.1 | Who pays, and roughly how? | Per person / per use / flat monthly / one-time / free plus paid. This is only a hypothesis |
| Q8.2 | What rough price will we test first? | A number, labeled hypothesis. Point to SaaS pricing for real work |
| Q8.3 | When should we look at this strategy again? | In about 6 months (Recommended, matches the positioning check-in cadence) / after the riskiest assumption test |
| Q8.4 | Anything I wrote that does not sound like you? | Always ask before saving |

## Existing-repo variant

When Q0.1 is "existing repo", read the repo first (see [the repo guide](../../guides/start-from-existing-repo.md)), then turn each finding into a confirm question:

```
Q1.1 From the README and the routes, it looks like this is for clinic front-desk staff booking appointments. Is that right?
  a) Yes (Recommended: README line 3 and the /appointments routes say so)
  b) Partly: ____
  c) No: ____
```

The repo shows what was built. It does not show who it is for, why, or what wins. Those still come from the owner.
