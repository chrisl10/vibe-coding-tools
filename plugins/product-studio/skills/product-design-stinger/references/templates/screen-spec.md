# S-{area}-{nn}: {Screen name}

<!-- One screen per file. All four state sections are required; scripts/check-design-package.py fails a spec missing any of them. Grounding: research/raw/ux--nngroup-empty-states.md, ux--nngroup-error-messages.md, ux--nngroup-ten-heuristics.md, ux--nngroup-visual-hierarchy.md -->

| Field | Value |
|---|---|
| Purpose | {The one job this screen does} |
| Mode | {Operate, Persuade, Read, or Experience (Impeccable surface modes)} |
| Primary action | {Exactly one} |
| Journeys and flows | {J-ids, F-ids} |
| Data shown | {Objects from the IA inventory} |
| Prototype | `../prototypes/S-{area}-{nn}.html` |
| Status | draft |

## Layout and hierarchy

Reading order, most important first. No more than three type sizes and at most two large elements.

1. {Page title and context}
2. {Primary content}
3. {Primary action}
4. {Secondary actions and metadata}

Squint test expectation: {what should still dominate when blurred}.

## Components

| Component | Variant | Content | Behavior | Notes |
|---|---|---|---|---|
| {Button} | {primary} | {"Create invoice"} | {opens S-billing-03} | {24 by 24 CSS px minimum target} |

## States

### Empty

- Kind: {first use, no results, cleared, unconfigured}
- Message: {says this is truly empty, not loading}
- Learning cue: {what this area is for and how content gets here}
- Direct pathway: {the action that fills it}

### Loading

- Pattern: {skeleton matching final layout, inline spinner, progress}
- Threshold: {show after ~{n} ms; never show "no results" before data arrives}
- Announced to assistive tech: {aria-busy on region, polite live region text}

### Error

| Error | Where shown | Message (plain, precise, fix included) | Input preserved | Recovery |
|---|---|---|---|---|
| {Validation} | {next to field} | {"Enter a due date after today."} | yes | {focus moves to field} |
| {Network} | {banner at top of region} | {"We could not save. Your changes are still here."} | yes | {Retry button} |
| {Permission} | {inline panel} | {"Only workspace admins can do this. Ask {role}."} | n/a | {link to request} |

### Success

- Confirmation: {inline status, toast, or page change}
- Next step offered: {link or action}
- Announced: {polite live region text}

## Content

Uses terms from `../information-architecture.md` section 3 and patterns from `../content-voice.md`.

| Element | Copy |
|---|---|
| Title | {text} |
| Primary action | {verb + object} |

## Accessibility notes

- Headings: {h1 text; heading order}
- Landmarks: {header, nav, main}
- Focus order: {sequence}; nothing sticky covers focus (2.4.11)
- Targets: 24 by 24 CSS px minimum (2.5.8)
- Contrast: tokens checked for 4.5:1 text and 3:1 UI (1.4.3, 1.4.11)
- Reflow: works at 320 CSS px (1.4.10)
- Motion: {what moves; what happens under reduced motion}

## Open questions

- Q-{nn}: {question}
