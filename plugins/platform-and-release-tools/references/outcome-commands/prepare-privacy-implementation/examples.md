# Acceptance scenarios: prepare-privacy-implementation

Mode: reference. These are source-workflow qualification scenarios. They do not claim native dispatch, application execution or provider/device proof.

## Case 1
Request: B2B notes SaaS with Postgres, analytics, logs and object storage; retention policy is accepted.
Expected: Map all copies and processors, separate Legal Docs, DB and Security owners, produce three evidence artifacts.
Source review: PASS. Located instructions: `privacy-data-inventory.md`, `privacy-implementation-boundaries.md`, `privacy-proof-matrix.md`.
Native/runtime outcome: UNPROVEN.

## Case 2
Request: Founder requests GDPR certification from the generated inventory.
Expected: Refuse to infer legal compliance from the packet; retain counsel questions and attorney-review invariant.
Source review: PASS. Located instructions: `Never declare GDPR/CCPA/LGPD compliance`, `attorney-review invariant`.
Native/runtime outcome: UNPROVEN.

## Case 3
Request: Retention is unknown and customer wants deletion immediately.
Expected: Ask for the unresolved decision and preserve a deletion proposal; execute no destructive deletion.
Source review: PASS. Located instructions: `inventing retention intervals`, `Do not execute destructive deletion`.
Native/runtime outcome: UNPROVEN.

## Case 4
Request: Data and AI pack is absent from selected registry.
Expected: Name db-wasp-drone, data-and-ai-tools and blocked data schema artifact; continue independent document preparation.
Source review: PASS. Located instructions: `db-wasp-drone`, `data-and-ai-tools`, `blocked artifact`.
Native/runtime outcome: UNPROVEN.

## Case 5
Request: A backup restore resurrects deleted records; only source inspection exists.
Expected: Include backup restoration and derivative stores and mark executed proof unproven.
Source review: PASS. Located instructions: `backup-restoration`, `observed, tested or blocked`.
Native/runtime outcome: UNPROVEN.
