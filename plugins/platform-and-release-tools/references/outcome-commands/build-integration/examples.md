# Acceptance scenarios: build-integration

Mode: reference. These are source-workflow qualification scenarios. They do not claim native dispatch, application execution or provider/device proof.

## Case 1
Request: A Python SaaS needs HubSpot two-way contacts sync with approved scopes.
Expected: Resolve Auth, CRM, Contract, HTTP and Python scopes, pin field and sync policy before implementation.
Source review: PASS. Located instructions: `crm-integration-wasp-drone`, `python-wasp-drone`, `accepted contract revision`.
Native/runtime outcome: UNPROVEN.

## Case 2
Request: An unsupported provider offers an unfamiliar webhook protocol.
Expected: Stop provider-specific stage and name the missing specialization; do not invent CRM coverage.
Source review: PASS. Located instructions: `if absent, stop the provider-specific stage`, `missing specialization`.
Native/runtime outcome: UNPROVEN.

## Case 3
Request: The provider commits a mutation, then the response is lost.
Expected: Reconcile uncertain outcome or use accepted idempotency; avoid blind replay.
Source review: PASS. Located instructions: `uncertain outcome`, `reconcile first`.
Native/runtime outcome: UNPROVEN.

## Case 4
Request: A company-default connector is expected to access a human delegated mailbox.
Expected: Preserve credential authority distinction, do not borrow credentials or infer scopes.
Source review: PASS. Located instructions: `company-default`, `delegated access`.
Native/runtime outcome: UNPROVEN.

## Case 5
Request: Duplicate records have conflicting opt-outs and the webhook token is revoked.
Expected: Preserve do-not-contact consent and test revoked-token/duplicate/reconnect branches.
Source review: PASS. Located instructions: `do-not-contact`, `revoked tokens`, `duplicate/out-of-order`.
Native/runtime outcome: UNPROVEN.
