# IRD Template - Schema v2

> Canonical blank template for an IRD index file.
> Copy to: `library/issues/backlog/ird-<###>-<slug>/ird-<###>-<slug>-index.md`
> `<###>` MUST equal the GitHub issue number. Never invent a number.
> Replace every `<placeholder>` before saving.
> See `library-schema-v2.md` for naming rules and lifecycle conventions.

---

<!-- ============================================================
     COPY EVERYTHING BELOW THIS LINE INTO YOUR IRD FILE
     ============================================================ -->

# IRD-<###>: <Issue Title>

> **GitHub Issue:** [#<###>]({issue-url}) - Bug | Enhancement | Regression | Security
>
> **Status:** Backlog
> **Priority:** P0 | P1 | P2 | P3
> **Effort:** XS (< 1h) | S (1-3h) | M (3-8h) | L (1-3d)
> **Reporter:** <name> (@<handle>)

---

## Problem

<!-- Precise description of what is wrong.
     What is observed vs what is expected.
     Include reproduction steps if applicable. -->

**Observed:** 

**Expected:** 

**Reproduction steps:**

1. 
2. 
3. 

---

## Root cause

<!-- Fill in once the cause is identified. Leave blank initially. -->

---

## Fix plan

<!-- Step-by-step approach. Cite specific files and line numbers where known.
     Keep scope to this one issue - no scope creep. -->

1. 
2. 
3. 

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

| ID | Criterion |
|---|---|
| AC-1 | Given <context>, when <action>, then <outcome>. |
| AC-2 | |

---

## Files touched

<!-- List every file this fix will modify. -->

- 

---

## Out of scope

<!-- Explicitly list things this IRD does NOT fix to prevent scope creep. -->

- 

---

## Related

<!-- Link to related IRDs, PRDs, or knowledge docs. Use relative paths. -->

-
