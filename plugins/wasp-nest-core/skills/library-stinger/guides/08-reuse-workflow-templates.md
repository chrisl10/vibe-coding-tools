# Guide 08 - Reuse templates from observed workflows

Trigger: "turn this workflow into a reusable template", "reuse our real process", or "make templates from these completed documents". Library owns template structure and PRD/IRD authoring; deep narrative docs route to Knowledge, QA findings to Quality, and CTR terms to Contract Writing. Existing repository restrictions and human approval always apply.

Grounding: distillation, [field contract](../references/template-reuse-fields.md). Purpose selection follows Diátaxis; source pinning follows GitHub. The procedure below is local Wasp Nest adaptation policy.

## Observe before generalizing

1. Read the supplied workflow, existing template and relevant code or documents within scope. Do not read human notes, secrets or unrelated private material. Record the operator's trigger, inputs, actual steps, output, errors and authority boundaries. If only a written procedure exists, label it SOURCE_OBSERVED and execution NOT_RUN. If no real source exists, stop the extraction and request one; a clearly labelled example may be drafted only if requested.
2. Capture source identity: full commit and path for committed sources; SHA256 of dirty working-copy bytes; external URL, retrieval date and stated version. Keep sensitive raw material in an approved private source location. Do not package customer records, credentials or private quotations in reusable templates.
3. Choose the reader outcome. Reuse Library's existing [PRD](../templates/prd-template.md) or [IRD](../templates/ird-template.md) for requirements. For knowledge documents, choose tutorial, how-to, reference or explanation based on reader needs and use the existing repository format. Do not build empty folder taxonomies or a second template library.
4. Separate stable structure from project values. Parameterize service names, paths, regions, identities, amounts, limits and rollback assumptions. Preserve ordering, failure behavior, and permission boundaries. Do not normalize away the reason a real workflow stopped or required approval.
5. Add the evidence fields from the field contract to the existing template. Document template identity and adaptations. Preserve schema-v2 numbering, lifecycle location and accepted CTR revision pins. Do not edit accepted terms or create QA content.
6. Fill a candidate using another supplied workflow or a constructed example labelled SYNTHETIC / NOT_RUN. Check that a reader can identify which behavior is observed, which is proposed and which remains unknown. A specimen passing this review is source guidance proof only.
7. Resolve actual links from the document's destination, check placeholders and affected path references, and request the appropriate independent reviewer. Record checks against the current subject revision. Do not mark shipped or move a document merely because its template looks complete; lifecycle actions also require applicable user authorization.
8. Assign a maintenance owner and review triggers: source change, contract revision, service policy change or a failed workflow. Keep older source identity in the document history and explicitly recheck affected facts. A newer document date alone does not establish freshness.

## Outputs and limits

Output an adapted existing template, source/evidence table, adaptation notes and unresolved requirements. A source-only extraction does not establish execution success, customer readiness, human acceptance or installed host behavior. No new accounts, installs, remote writes or production effects follow from creating a template.

For runtime knowledge prose, hand the evidence packet to Knowledge. For a missing contract agreement, request its owner and retain Draft dependencies. For independent acceptance results, request Quality after Security. Library records links to reviewer evidence and does not author the findings.
