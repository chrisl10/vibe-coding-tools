# 05. CASE and decisions: the Jev lane

CASE is our Jev decision lane from the global agent rules, not a separate
session, thread, or skill. Jev is the fabric decision lane: a call is cheap,
deliberation is not. The manager defers to the global rules everywhere here
and never contradicts them.

## Classify first

1. **Routine manager decision**: chip briefs, nudges, tick rulings, watch
   list contents, ledger entries. The manager answers within the assigned
   scope and records a ruling with UTC time and evidence.
2. **CASE question (proportion)**: anything larger than one small PR, any
   split, any workaround instead of the obvious fix, any rewrite, anything
   the chip itself called "big". CASE runs BEFORE spawning.
3. **Owner-only gate (Hard stops)**: never decided by the manager or Jev.

## The CASE request

Build one DECISION REQUEST in the global shape, extended with numbered
questions, and include the manager's lean on every question:

```text
DECISION REQUEST (CASE)
Project: <name>
Task: <one line>
Questions:
  1) <question>
     A) <option> - <main tradeoff>
     B) <option> - <main tradeoff>
  2) <next question, same shape>
TARS-T3 lean:
  1) <letter> - <one sentence>
  2) <letter> - <one sentence>
Context: <one or two lines of product or technical facts>
Constraints: <deadline, stack, cost, anything binding>
Reply with exactly one line per question:
  <n> PROCEED|SIMPLIFY|OVERKILL|ASK OWNER - <one sentence>
```

## Send it to Jev

POST to `http://macdevs-macbook-pro.tail8264da.ts.net:4000/v1/chat/completions`
as a single user message with model `auto` and the fabric bearer key
(`FABRIC_API_KEY` in `~/.config/codex/secrets/fabric.env`, referenced by
path only, never inlined, committed, or logged). Parse the reply lines. If
the fabric is unreachable or the answer is not parseable in two tries,
decide yourself, say so in the ledger and the final report, and keep the
effort moving.

## Verdicts and limits

- `PROCEED` is advice, never the owner's approval. A PROCEED authorizes
  nothing that the owner alone may gate.
- `SIMPLIFY` names the smallest option that still meets the full ask.
- `OVERKILL` names what to drop and the smallest workable answer.
- `ASK OWNER` names the short question and the gate it touches.
- Owner gates always go to Chris, regardless of Jev's answer: production
  deploys and releases, credentials and accounts, money, direct pushes to
  protected branches (main, staging, production), force-pushes and pushes
  outside a PR flow, product-altering changes (features, user-facing
  behavior, pricing, public copy, schema changes affecting existing data),
  and changes to the rules, credentials, permissions, or system
  configuration. Deleting, overwriting, or rewriting anything this effort
  did not create is in the same class.

## Proportion disputes

The smaller option wins only when it still meets the full ask. Do not cut a
required outcome because it is hard, and do not use a simplification to fix
unrelated defects. When the smaller option drops a required outcome, the
owner decides.

## Records

Every CASE exchange goes in the ledger: the request sent, Jev's reply
verbatim, the action taken, UTC time. The final report lists each Jev
decision: question, pick, one line why. Pushing task or feature branches
and opening PRs through the repo's normal flow is normal chip work and
needs no CASE ruling; everything above stays gated.
