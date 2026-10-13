# 13. Prepare refund, dispute and cancellation actions

Use for O278. The deliverable is a reviewable [support packet](../templates/billing-support-action-packet.md). No refund, recharge, credit, reversal, cancellation, price change, dispute acceptance/submission or notification is automatically authorized by reading a support ticket or receiving a webhook.

## Resolve the exact financial context

Identify account/environment, tenant, authorized actor, mapped customer and the actual payment/refund/dispute/invoice/subscription relationships from authorized evidence. Record API/event versions and object IDs in an access-controlled packet; examples use synthetic identifiers and no PII. For API versions starting at Basil, the invoice-payment relationship differs from older Charge-to-Invoice fields and can yield multiple invoices. An absent relationship is unresolved, not permission to guess the subscription. Paginate and verify each relation. [Version-specific mapping source](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/platform-and-release-tools/skills/payments-stinger/references/research/billing-access-update/raw/subscription-events.md)

Record currency and integer minor-unit amounts, refundable remainder, previous refunds and their current statuses, charge settlement, disputed amount/status/reason and evidence deadline when available. Separate a provider amount from an estimated conversion or fee. Do not promise receipt of funds from a refund-request response alone; pending and failed refund states need observation and reconciliation. [Refund source](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/platform-and-release-tools/skills/payments-stinger/references/research/billing-access-update/raw/refunds.md)

Cancellation preparation must show immediate versus scheduled effective time, pending invoices, usage, credits/prorations, feature end and permitted data access. A cancellation is not a refund; prorations are not necessarily immediate invoice collection or cash return. Capture the preview/read evidence without performing the operation. [Cancellation source](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/platform-and-release-tools/skills/payments-stinger/references/research/billing-access-update/raw/cancel-subscriptions.md), [Proration source](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/platform-and-release-tools/skills/payments-stinger/references/research/billing-access-update/raw/prorations.md)

## Require specific approval before execution

The packet names one action, exact object scope, environment, amount/currency if relevant, timing, expected billing/access consequences, known reversibility limits and approver. If several actions are wanted, obtain approval for each explicit action: cancellation, refund, credit/recharge, dispute response, local restriction/restoration and outbound message. Approval to investigate or draft a packet grants none of them. A policy authorized in advance must explicitly cover that action and conditions; record its source and bounds.

For a dispute, prepare the relevant evidence for authorized review with provenance and minimal personal data. Record the current deadline; do not invent a universal number of days. Accepting a dispute or submitting evidence is an external action. Do not issue a compensating refund/recharge because a dispute arrived or assume a won dispute restores access. [Dispute response source](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/platform-and-release-tools/skills/payments-stinger/references/research/billing-access-update/raw/disputes.md)

## Execution handoff, only after authorization

1. Recheck current object status and ownership at execution time. A packet based on yesterday's refundable balance may be stale.
2. Use a durable operation identity with exact parameters for supported retryable writes. Record unknown outcomes as unknown. After timeout, retrieve/inspect before another distinct action; do not invent a new key to bypass an ambiguous earlier result. Provider keys have finite retention. [Idempotency source](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/platform-and-release-tools/skills/payments-stinger/references/research/billing-access-update/raw/idempotency.md)
3. Record submitted, observed provider result and applied local access projection separately. Reconcile through the serialized entitlement writer. No support form grants access by changing a browser flag.
4. Draft any customer notification as a separate artifact with its recipients/channel/content and authorization status. No email, SMS or portal notification is sent by this preparation guide.
5. Verify sandbox cases and actual authorized execution output before claiming completion. Refunds can be pending/failed, cancellations can be scheduled, and disputes can remain under review. Do not report an intended outcome as observed.

Scope remains SvelteKit Stripe Billing/Elements. Connect, transfers and marketplace financial actions need another qualified owner. Actual provider accounts, test clocks, CLI traffic, keys, settings and live operations require their applicable authorization; this source update performs none.
