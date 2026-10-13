# Write, check, save, and hand off

Turns the interview answers into `library/knowledge/private/product/product-strategy.md` and passes it on.

## Write

1. Copy the [strategy template](../references/templates/product-strategy.md). Keep sections 1 to 8 on the first page; supporting parts go below the line.
2. Fill each section only from the owner's answers, repo evidence the owner confirmed, or linked research. Mark anything else "OPEN: {question}".
3. Use the owner's words where you can. Plain language, short sentences, 8th-grade reading level. No em dashes or en dashes.
4. Add the pricing hypothesis in one or two lines, labeled "hypothesis", with a pointer to the SaaS pricing owner. Do not design pricing here.
5. Add a rough bottom-up opportunity size only if the owner wants one. Show the math and label every guess. Top-down market numbers are framing, not forecasts [raw/productnotebook-market-sizing.html].

## Check

Run the checker before saving and fix every error it reports. The script lives in this skill's `scripts/` folder; pass the draft's path:

```
python3 <this-skill-folder>/scripts/check-strategy.py library/knowledge/private/product/product-strategy.md
```

It checks that all eight sections exist, there are 2 to 4 bets, exactly 3 inputs, a NOT-in-v1 list, a named riskiest assumption, a pricing hypothesis line, no leftover `{placeholders}`, and no em or en dashes. If the host has no shell, walk the same list by hand and say so. See the [made-up worked example](../references/examples/worked-example.md) for a passing file. It does not judge whether the strategy is good. That is the owner's call.

Then read it back to the owner: "Anything here that does not sound like you?" Save only after they say it is right.

## Save

- Create `library/knowledge/private/product/` and `decisions/` only if the owner agrees. If `library/` itself is missing, suggest `get-started-stinger` first.
- If a strategy already exists, this is an update (see below). Never overwrite a file another session is editing.
- Do not commit or push. The Ship Gate in SKILL.md applies before any commit.

## Update mode

1. Read the current strategy and every decision note.
2. Ask what changed: new evidence, a failed test, a new segment, a positioning check-in.
3. Change only the affected sections. Write a superseding decision note for each changed choice.
4. Update `last-reviewed` and `next-review`. Positioning should get a structured look about every six months [raw/mtp-dunford-position-for-future.html], and the north star should change when the strategy does [raw/amplitude-good-bad-north-star.html].

## Hand off

Tell the owner, in plain words, what comes next:

- `product-design-stinger` uses sections 2, 3, 4 and 7.
- `product-planning-stinger` uses sections 5, 6, 7 and 8, and should plan the riskiest assumption test first.
- PRDs go to `library-stinger`. OKRs go to `okr-goal-setting-stinger`.

List every OPEN item so the next owner knows what is still a guess. See [handoffs](../references/handoffs.md) for the full contract.
