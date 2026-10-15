# 12. Separate trial, payment and access state

Use for O277 alongside [server entitlements](11-enforce-server-entitlements.md). Record the observed Stripe object state, the application's approved policy decision and the effective feature projection separately in [the lifecycle worksheet](../templates/billing-lifecycle-worksheet.md). A browser payment success message does not grant access. A zero-value paid invoice does not prove a positive charge.

The following are source distinctions; the exact access policy requires the product owner's decision. Subscription status source

| Observed state | Required policy decision and evidence |
|---|---|
| `trialing` | Verified trial membership, allowed features and exact trial end. Grant only the approved trial feature set while its validity window holds. Trial creation alone proves no payment. |
| `incomplete`, `incomplete_expired` | Initial payment pending/action required/expired. No paid grant from Checkout return. Explain the pending state using server data; test delayed events and abandoned authentication. |
| `active` | Verify the applicable invoice/payment and current subscription or complete provider entitlement set. Active status can coexist with outstanding invoices; record which collection/status-resolution policy the product actually uses. |
| `past_due` | Owner-approved bounded grace or restriction, with exact end and allowed operations. Do not infer that another retry is guaranteed. Expiry must be enforced by server time even with no new event. |
| `unpaid`, `canceled` | Revoke paid features according to the approved policy and preserve the permitted account/export/support surface. Do not erase customer data as a billing side effect. |
| `paused` | Subscription paused after a trial without a payment method has different behavior from pausing payment collection. Record whether any feature is allowed; never copy an `active` grant by default. |
| Cancellation scheduled | `cancel_at_period_end` marks an intent, not immediate termination. Retain only the justified trial/paid/grace rights through their recorded boundaries. The actual cancellation event or reconciliation changes the terminal state. |
| Refund/dispute observed | Record amount, status, object mapping and policy separately. A partial refund is not automatically a full subscription cancellation; dispute victory is not automatically a feature restoration. Use [support preparation](13-prepare-billing-support-actions.md). |

Stopping an uncompleted period-end cancellation is distinct from creating a new subscription after cancellation. Restore access only after the same current-state reconciliation/authorization path confirms the approved conditions. Multiple subscriptions and mixed product periods need a per-feature/per-item policy; do not pick one arbitrary period end. Cancellation source

## Procedure

1. Record policy identity/version and the actual SDK/API/event version contract. Declare trial end, paid-through, grace expiry, freshness limit, pending-plan effective time, refunds/disputes restriction and restoration conditions. Missing policy remains an unresolved product decision.
2. For `invoice.paid`, resolve invoice to the current subscription using the target API version's supported shape. Check tenant/customer/account/environment ownership and status before access extension. Dedup by invoice/period/action semantics, not by repeatedly adding a duration to the old expiry. Renewal source
3. Preview plan-change effects when authorized. `proration_behavior=none` suppresses proration; it does not by itself schedule the new plan for a future billing boundary. Negative prorations are not automatic cash refunds. Capture scheduling, invoice and entitlement effective times separately. Proration source
4. Exercise the boundary immediately before, at and after expiry using an injected clock in the target app's existing test facility. Do not extend grace from repeated failed event deliveries. Test an old UI session and a queued job admitted before revocation according to the declared job policy.
5. Test recovery: paid invoice after grace, late failed invoice after later recovery, canceled-subscription late active snapshot, trial with no payment method, and restoration after an approved support decision. Verify both server response and UI state without granting from the client.
6. Record actual implementation evidence and remaining gaps. Synthetic tables do not qualify trial-abuse prevention, rate limits, identity abuse defenses, store receipts or another framework's implementation.

If notification or money effects are proposed, they require the specific action authorization in [guide 13](13-prepare-billing-support-actions.md). A recorded event is evidence, not approval.
