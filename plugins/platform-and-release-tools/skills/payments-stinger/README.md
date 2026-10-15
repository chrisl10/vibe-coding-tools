# Payments Stinger

Use [SKILL.md](SKILL.md) for the integration routing and required conventions. The existing specialist implements Stripe Elements for SvelteKit 5 on Vercel.

For billing access, read the October 2026 update in this order:

1. [Server entitlements](guides/11-enforce-server-entitlements.md): tenant/version mapping, durable processing, semantic idempotency, pagination and reconciliation.
2. [Trial, payment and access state](guides/12-separate-trial-payment-and-access.md): effective boundaries, recovery, cancellation and dual server/UI evidence.
3. [Billing support preparation](guides/13-prepare-billing-support-actions.md): exact refund/dispute/cancellation packet and separate money, access and notification approvals.

The source digest traces facts to ten archived official documents and distinguishes product policy from provider behavior. Complete the [access contract](templates/billing-access-contract.md), [lifecycle worksheet](templates/billing-lifecycle-worksheet.md) and [support packet](templates/billing-support-action-packet.md). [Sixteen rendered cases](references/examples/billing-access-cases.md) are synthetic source reasoning, not runtime proof.

The historical webhook TypeScript file and SQL tables are incomplete scaffolds. They do not prove atomic processing or safe external effects. No actual Stripe operation, native receipt validation, other framework integration or trial-abuse defense is qualified by this update.
