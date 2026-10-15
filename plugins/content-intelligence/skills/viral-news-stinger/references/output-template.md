# Output template (viral-news-stinger)

The run's final deliverable is ONE message in exactly this shape. Every post option must already be finished, voice-checked against the user's configured voice skill (or written in the neutral voice when none is configured), and copy-paste ready. No placeholders, no "you could say something like".

````markdown
## Today's post: {topic in seven words or fewer}

**Voice:** {name of the voice skill used, or "none configured: neutral voice"}

**Why now:** {one sentence: what broke, when (with timestamp), and why it will travel}

### Micro (9 words or less)
```
{post}
```

### Medium (10-60 words)
```
{post}
```

### Long form (200+ words)
```
{post}
```

**Link:** {the single most relevant URL: the primary story, the receipt, or the source document}

**Hashtags (2-4, currently moving on this topic):**
`#One` `#Two` `#Three`

### Receipts
1. {Source name}, {headline}, {published timestamp}: {URL}
2. {Source name}, {headline}, {published timestamp}: {URL}
3. {optional third source}
````

## Rules bound to this template

- The three posts are three independent options on the SAME topic, not a thread. Each must stand alone.
- Micro: 9 words or less, per the voice skill's micro register (or the default band in `references/editorial-preferences.md`). Count the words.
- Medium: the voice skill's short-form band, 10-60 words.
- Long form: the voice skill's long-form band, 200+ words.
- Every factual claim inside any post must be traceable to a numbered receipt below it.
- Receipts show published timestamps so the 24-hour gate is auditable at a glance.
- Hashtags come from what is actually trending on the topic right now (trend mirror or live X search), not from imagination. Two minimum, four maximum.
- Punctuation follows the voice skill's hard rules when one is configured. In the neutral voice, avoid em dashes and use a comma, colon, or spaced hyphen instead.

## No-post output

If the run found nothing that clears every gate, the entire output is a short plain statement: what was swept, why the candidates failed (stale, repeat, off-limits, or unverifiable), and nothing else. No forced post, no filler research.
