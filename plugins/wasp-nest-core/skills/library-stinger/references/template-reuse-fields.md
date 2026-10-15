# Template reuse field contract

Use these fields inside an existing PRD or IRD, or adapt them to the repository's existing knowledge template. They are a reference fragment, not another document lifecycle. Basis: distillation.

| Field | Required content | Failure condition |
|---|---|---|
| Reader and outcome | Who needs what decision or action | Headings copied without a concrete reader |
| Source workflow | Real trigger, input, observed steps, output, failure and permission boundary | Fictional example presented as observed work |
| Source identity | Repository/path plus full commit; dirty bytes add SHA256; external URL plus retrieval date and version if known | Mutable branch link used as exact revision proof |
| Template identity | Existing template path and revision or SHA256 | Copied format has no traceable origin |
| Adaptations | Which values or rules vary by project, with assumptions identified | Product-specific service, credential, SLA, region or role silently retained |
| Evidence status | SOURCE_OBSERVED, EXECUTION_OBSERVED, PROPOSED, UNKNOWN, or NOT_RUN, with locator | A copied checkbox or specimen result treated as proof |
| Check record | Criterion, evidence/result, subject revision, date and verification owner | Passing check attributed to a different subject |
| Authority | Requested output and approval required for dependent effects | Documentation drafting implies permission to deploy, send, buy or change settings |
| Review trigger | Owner and changes that invalidate facts | Date refreshed without checking changed behavior |

A source hash establishes byte identity, not source truth, completeness, reviewer approval or runtime behavior. A planned requirement may deliberately differ from current code; explain that difference and keep it PROPOSED.
