# 03: Write key task flows

Goal: for each key task, the ideal path plus the failure branches, in Mermaid, so screen specs inherit their error and empty states from real decisions.

Grounding: journeys vs flows, Mermaid flowchart, Mermaid accessibility, WCAG 2.2 new criteria.

## Procedure

1. Choose the tasks: every opportunity in a journey that leads to a task inside the product, plus sign-in and first-run if the product has them. Assign `F-nn`.
2. Copy [task-flow.md](../references/templates/task-flow.md) to `design/flows/F-nn.md`.
3. Write the ideal path first: user step, then system response, each landing on a screen ID.
4. Add the failure branches this skill requires (a house convention beyond NN/g's ideal-path definition, see distilled section 2):
   - validation failure (stays on the screen, input kept)
   - request or network failure (retry, nothing lost)
   - permission or plan limit (who can, how to ask)
   - empty result (what is shown, how to fill it)
5. Mermaid rules: `flowchart TD` or `LR`; decisions as `{Question?}` diamonds; labelled edges `-->|Yes|`; `accTitle` and `accDescr` right after the declaration; never a node labelled lowercase `end` (use `Done` or `End`); `%%` comments on their own line.
6. Fill the steps table, then the edge cases table. Check the three flow-level WCAG 2.2 items: no re-asking for data already given (3.3.7), a single-pointer alternative for any drag (2.5.7), and no cognitive puzzle at sign-in (3.3.8).

## Checks

- Each branch ends at a screen and a named state that the screen spec will define.
- `python3 scripts/check-design-package.py package <design-dir>` reports no flow findings.
