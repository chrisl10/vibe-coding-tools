# Content and voice

<!-- Grounding: research/raw/ux--nngroup-ten-heuristics.md (real-world language, consistency), ux--nngroup-error-messages.md, ux--nngroup-empty-states.md. Vocabulary lives in information-architecture.md section 3; this file says how to speak. -->

## Voice in three traits

| Trait | Means | Sounds like | Never sounds like |
|---|---|---|---|
| {Plain} | {everyday words} | {"Send invoice"} | {"Leverage invoicing workflows"} |
| {Calm} | | | |
| {Direct} | | | |

## Mechanics

- Sentence case for titles and buttons.
- Buttons are verb plus object: "Create invoice", not "Submit" or "OK".
- Numbers, dates and currency: {format and locale rules}.
- No em dashes or en dashes in product copy; use commas, colons or periods.
- No humor in errors. No exclamation marks in system messages.

## Message patterns

| Situation | Pattern | Example |
|---|---|---|
| Empty, first use | What this is + how to fill it + action | "No invoices yet. Invoices you send appear here. Create invoice" |
| Empty, no results | What was searched + how to widen | "No invoices match 'acme'. Check spelling or clear filters." |
| Loading, long | What is happening + expected wait | "Importing 1,240 contacts. This takes about a minute." |
| Validation error | What is needed, next to the field | "Enter a due date after today." |
| System error | What happened + what is safe + what to do | "We could not save. Your changes are still here. Try again." |
| Permission | Who can + how to ask | "Only admins can change billing. Ask an admin." |
| Success | What happened + next step | "Invoice sent to Acme. View invoice" |
| Destructive confirm | Name the object + consequence + undo or not | "Delete 'Q3 report'? This cannot be undone." |

## Words to avoid

{Product-specific banned terms and generic AI marketing phrases such as "unlock", "seamless", "supercharge", "revolutionize".}
