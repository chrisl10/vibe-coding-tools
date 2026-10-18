# Rendered billing access cases

Synthetic source reasoning, 7 October 2026. No Stripe SDK, account, network event, database, UI or actual authorization engine executed. Names below are fictitious subjects, not provider object IDs. Target SDK and event version remain UNRESOLVED; production qualification requires the target's actual contract and runtime evidence.

For these examples only, a hypothetical owner-approved policy P1 allows report access during a verified trial or settled paid period. Past due has a fixed two-day grace, bounded by its explicit timestamp. Unpaid/canceled has no report access. Account support remains available. P1 is an illustrative policy, not permission for any real product. Billing subject A belongs only to tenant A; B belongs only to tenant B.

| Case | Input and failure boundary | Reasoned local state/result | Server + UI expectation |
|---|---|---|---|
| C01 | Browser returns `paid=true`; no verified event or current provider state | No grant; payment pending | Direct report request denied; UI says awaiting confirmation. |
| C02 | Valid signed event for customer B arrives while tenant A mapping is selected by request metadata | Mapping disagreement quarantined; neither tenant changed | Tenant A remains denied; no B billing data shown. |
| C03 | Same event ID delivered concurrently to two workers | One transaction owns processing; other retries/observes committed completion; one feature-set transition | UI and direct request reflect one committed projection, no duplicated fulfillment. |
| C04 | Two event IDs cover the same invoice-period renewal | Two receipt records can exist; one semantic period-extension action | Paid-through set to the verified boundary once, never old expiry plus two durations. |
| C05 | Subscription canceled currently; older active snapshot arrives later with equal creation second to another event | Serialized current refresh confirms canceled; snapshot cannot restore | Report request denied even if old UI still displays active. |
| C06 | Verified trial ends at T without verified paid transition | Trial feature expires at T under P1; no paid state invented | Request at T denied; before T allowed if membership valid; UI explains expiry. |
| C07 | Past-due grace expires at G; no later event arrives | Fixed grace is not renewed by retries; server time expires access at G | Request at/after G denied; UI prompts billing recovery. |
| C08 | New paid invoice arrives, current subscription active and applicable invoice verified; late prior failure follows | Current-state recompute preserves paid access; old failure does not extend/restart grace | Report allowed after verified recovery; UI shows observed current state. |
| C09 | Cancellation scheduled before verified paid-through P | Record cancellation intent; retain justified rights until effective boundary; current state checked at P | Request before P allowed; after actual terminal transition denied; UI shows scheduled end. |
| C10 | Entitlement summary includes ten entries and `has_more=true`; page two fails | Complete set unresolved; never delete absent features from a truncated page; approved freshness policy governs old projection | Server/UI use the declared stale policy, not an invented empty set. |
| C11 | Database fails after attempted projection update, before completion commit | Entire local claim/projection/outbox transaction rolls back | No success/provisioned claim; retry can safely process. |
| C12 | Outbox destination succeeds, worker crashes before recording acknowledgment | Unknown external result; inspect using operation identity/downstream idempotency before retry | Local feature commit unaffected; no claim of exactly-once external delivery. |
| C13 | Partial refund requested in ticket; no exact action approval | Draft packet only; no refund/cancel/recharge/access edit/send | Support UI may show draft; server financial mutation not invoked. |
| C14 | Dispute closes won but subscription currently canceled | Record outcome; no automatic recharge or restoration | Report denied until separately authorized restoration conditions verified. |
| C15 | Correct event type with invalid signature or changed raw bytes | Reject before any mapping/projection work | No grant and no raw payload/exception logging. |
| C16 | `proration_behavior=none` proposed for a price switch next month | No inference of future scheduling; require distinct effective-time evidence and approved action | UI must not promise next-month start from this parameter alone. |

Provider facts underlying C03-C05/C15: webhooks. C06-C09/C14: subscription events and cancellation. C10: entitlements. C12: API idempotency. C13-C14: refunds and disputes. C16: prorations. Tenant authorization, P1, transactions and approval boundaries are explicit engineering/example policy assumptions requiring actual application proof.

Use the contract and lifecycle worksheets to replace every hypothetical input with target evidence. These sixteen cases do not qualify trial-abuse controls, live payment behavior, native receipts, Connect or another framework.
