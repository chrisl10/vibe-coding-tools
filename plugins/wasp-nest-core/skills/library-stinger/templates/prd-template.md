# PRD Template - Schema v2

> Canonical blank template for a PRD index file.
> Copy to: `library/requirements/backlog/prd-<###>-<slug>/prd-<###>-<slug>-index.md`
> Replace every `<placeholder>` before saving.
> See `library-schema-v2.md` for naming rules and lifecycle conventions.

---

<!-- ============================================================
     COPY EVERYTHING BELOW THIS LINE INTO YOUR PRD FILE
     ============================================================ -->

# PRD-<###>: <Module Title>

> **Status:** Backlog
> **Priority:** P0 | P1 | P2 | P3
> **Effort:** XS (< 1h) | S (1-3h) | M (3-8h) | L (1-3d) | XL (> 3d)
> **Schema changes:** None | Additive | Breaking
> **ClickUp:** [<id>](https://app.clickup.com/t/<id>) *(delete line if not using ClickUp)*

---

## Overview

<!-- One paragraph: what this module does and why it exists. -->

---

## Goals

<!-- Specific, measurable outcomes this module achieves. -->

- 
- 

## Non-Goals

<!-- What this module explicitly does NOT do. Be precise. -->

- 
- 

---

## Sub-features

<!-- If the module has multiple discrete sub-features, list them here with links to their sub-PRD files.
     Sub-PRD naming: prd-<###>a-<slug>-<feature>.md, prd-<###>b-..., etc.
     Delete this section if the module is small enough to need no sub-PRDs. -->

| Sub-PRD | Scope | Status |
|---|---|---|
| [`prd-<###>a-<slug>-<feature>`](./prd-<###>a-<slug>-<feature>.md) | <scope description> | Draft |

---

## Source workflow and evidence

<!-- Record the real workflow trigger, inputs, observed steps, output, failures and
     authority boundary. A procedure read from source is SOURCE_OBSERVED; do not
     claim it was executed. Record current behavior separately from proposed work. -->

**Reader and outcome:** <who needs which action or decision>
**Template origin:** <template path and revision or SHA256>
**Source identity:** <repository/path and full commit; dirty bytes add SHA256; external URL and retrieval date>
**Adaptations and assumptions:** <project-specific values changed or remaining unknown>
**Maintenance owner and review triggers:** <owner; source, contract or behavior changes>

| Claim or criterion | Status | Source or result locator | Subject revision | Observed date | Verification owner |
|---|---|---|---|---|---|
| <claim> | SOURCE_OBSERVED / EXECUTION_OBSERVED / PROPOSED / UNKNOWN / NOT_RUN | <exact location or missing evidence> | <revision or hash> | <date or NOT_RUN> | <owner> |

<!-- A template, checkbox or example result is not execution proof. Never copy
     credentials, customer records, permissions, production identifiers or approval
     claims into a reusable template. Unknowns remain explicit. -->

---

## Acceptance criteria

<!-- Testable, binary criteria for the module as a whole.
     Sub-PRD-level criteria live in their respective files. -->

| ID | Criterion |
|---|---|
| AC-1 | Given <context>, when <action>, then <outcome>. |
| AC-2 | |

---

## Definition of Done checklist

<!-- When library/knowledge/private/standards/definition-of-done.md exists,
     pin its Approved revision and copy its PRD-level checklist here. A PRD may
     add stricter items but never skips a project item. If the project has no
     Definition of Done yet, write: - None; no project Definition of Done. -->

- Inherits Definition of Done revision <n>: link it as `../../../knowledge/private/standards/definition-of-done.md` from any file in the PRD folder.
- <Any PRD-specific done items>

---

## Data model changes

<!-- Describe any new tables, columns, or index changes.
     Delete this section if no schema changes. -->

---

## API changes

<!-- New endpoints or changes to existing endpoints.
     Delete this section if no API changes. -->

---

## Contract dependencies

<!-- Inventory shared boundaries before parallel PRD work. Pin every accepted
     contract as CTR-<###> revision <n> with a relative link. If none apply,
     write: - None; no shared boundary identified. A Draft dependency blocks
     finalization of the affected PRD until accepted. -->

- None; no shared boundary identified.

---

## Open questions

<!-- Unresolved questions that must be answered before implementation. -->

- [ ] 

---

## Related

<!-- Link to relevant knowledge docs, ADRs, IRDs, or completed PRDs. Use relative paths. -->

- 
