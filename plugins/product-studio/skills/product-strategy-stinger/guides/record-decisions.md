# Record strategy decisions

Each real choice gets a short note in `library/knowledge/private/product/decisions/`, using the [decision note template](../references/templates/decision-note.md).

Why: a strategy should be traceable, so that months later you can walk from any choice back to the evidence it rested on, and see what falls if that evidence breaks [raw/mtp-three-products-three-failures.html].

## What counts as a decision

- Picking the best-fit segment over others
- The market category
- The bets, and what we are not betting on
- The north star and its inputs, and every later change to them
- The v1 appetite and the NOT-in-v1 cut
- The riskiest assumption and its pass line
- The pricing hypothesis
- The positioning check-in date

Small wording edits are not decisions.

## Steps

1. **List the folder first.** Use the next free number (`D-001`, `D-002`, ...). Never reuse, renumber, or overwrite an existing note, even one that looks unrelated. Another session may own it.
2. **Name the file** `D-###-{short-slug}.md`, lowercase, hyphens.
3. **Fill every field.** Include the options not picked and the signal that would reopen it.
4. **Mark beliefs honestly.** If the owner chose without evidence, write "owner belief, not yet tested" and link the matching assumption in section 8.
5. **Supersede, do not edit history.** When a decision changes, write a new note with `supersedes: D-###`, and set the old note's `status: superseded`. Leave the rest of the old note as it was.
6. **Link both ways.** Add the `[D-###]` tag in the strategy section and a row in the strategy's Decision log.
