# knowledge-wasp-drone

**Plugin owner:** `wasp-nest-core`. **Required selection:** Core itself. Resolve the selected installed owner before dispatch; use the source link for the canonical procedure.


## Domain
This Drone authors the narrative, human-readable knowledge documentation under library/knowledge/private/<domain>/: system overviews with Mermaid diagrams, auth architecture docs with sequence diagrams, consolidated SQL schema references, Valkey key catalogs, security trust-boundary diagrams, coding standards, and every other deep technical doc that explains how a system works and why it was built that way. It works from ADRs and PRDs as source material but never copies spec language verbatim, and it never touches PRDs or IRDs itself.

## Paired Stinger
[knowledge-stinger](../../knowledge-stinger) - domain taxonomy for library/knowledge/, the strict document-format spec, the analysis workflow, a blank template, and target-quality examples (system overview, auth architecture).

## Trigger phrases
- "document the auth architecture"
- "write the system overview"
- "create knowledge docs for this repo"
- "build out the knowledge base"
- "same quality as the legion-secure wiki"
- "document how our container runtime works internally"

## Do NOT route when
- The ask is a PRD or an IRD; those are authored by library-wasp-drone, and this Drone never writes them.
- The ask is a QA report; that belongs to quality-wasp-drone.
- The ask is authoring a new ADR (the WHY-decision record itself, not the narrative doc built from it); that belongs to adr-writing-wasp-drone.
- The target file is under library/notes/; that folder is human-only, no agent writes there.

## Inputs the Drone needs
- Which domain (auth, data, security, frontend, etc.) or "full knowledge base" scope.
- The relevant ADRs to read first for the WHY behind the design.
- The relevant PRDs to extract DDL, API specs, and technical considerations from.
- Source code as ground truth for file paths and actual behavior.

## Outputs
- Knowledge docs with the standard header (Category, Version, Date, Status) and a Related section linking 3-8 sibling docs and ADRs.
- Mermaid diagrams (flowchart, sequenceDiagram, stateDiagram-v2) with no explicit colors and camelCase node IDs.
- Complete SQL DDL and trust-boundary diagrams where the domain calls for them.

## Commonly sequenced with
- library-wasp-drone: supplies the PRDs this Drone reads as source material for the WHAT and HOW.
- adr-writing-wasp-drone: supplies the ADRs this Drone reads as source material for the WHY.
- quality-wasp-drone: authors the QA reports that sit alongside, but outside, this Drone's docs.

## Supplied local meeting decisions and action drafts

Route an explicitly supplied local note or transcript handoff to [guide 05](../../knowledge-stinger/guides/05-turn-meeting-sources-into-decision-drafts.md). Preserve source revision, participant context, speaker evidence, uncertainty, decision authority, responsible-owner acceptance and next-action conditions. Outputs stay Draft; meeting statements and agent messages do not authorize current actions.

Live Littlebird retrieval belongs to Meeting Scribe only with its actually selected owner and capability gate. A separately authorized standing commitment ledger belongs to Commitment Tracker. ADR artifacts belong to ADR Writing; PRDs and IRDs belong to Library. No live fetch, external send, ticket creation or Accepted contract follows from this route.

## Source-grounded behavior diagrams

Route "diagram this flow", "show who can do what" and "is this diagram faithful to the code" to the existing Knowledge pair using [guide 06](../../knowledge-stinger/guides/06-preserve-behavior-in-diagrams.md). Inputs must identify the journey, actual code/contract and revision or hashes. Outputs preserve caller/gates/returns/errors, queue and transaction/external boundaries with exact locators, intended/current distinctions and missing evidence. Local render success adds no product runtime or authorization proof. ADR decisions, PRD/IRD specs and independent QA retain their owners.
