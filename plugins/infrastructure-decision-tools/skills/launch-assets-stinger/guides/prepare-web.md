# Prepare a web product

1. Confirm static website versus authenticated app, stored data, payment flow, expected users and accepted hosting decision. Resolve Builder Readiness for missing product decisions through the selected owner; do not choose a full stack silently.
2. Inventory domain/brand/content ownership, host/project reference, environments, HTTPS owner and support contact. Ask whether hosting manages TLS; add manual issuance only when actually needed.
3. Add a selected database/storage owner if customer data exists. Separate project existence from production access/security/backups. Add identity assets only for login; Google OAuth preparation requires its applicable production project/callback/brand/scopes evidence.
4. Add payment assets only for money flow, then error/uptime/alert/recovery responsibility for the intended paid-user milestone. Choose the minimum fitting vendors. Record budget/rate uncertainty instead of guessing operating cost.
5. Build the ledger, identify prerequisite blockers and defer unused services with a trigger. Give one preparation summary, editable rows and selected-owner handoffs. No DNS/provider/account/credential actions occur in this workflow.

Grounding: TLS, Supabase readiness, Google OAuth, Stripe go-live. Selection/status rules are the [ledger contract](../references/ledger-contract.md).
