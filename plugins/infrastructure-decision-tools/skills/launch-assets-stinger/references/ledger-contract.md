# Readiness ledger contract

Use the editable CSV template or the equivalent Markdown table. Keep the reader summary to immediate blockers and deferred assets; preserve the detailed rows for preparation owners.

Required fields: `asset_id`, `category`, `purpose`, `product_scope`, `environment`, `accountable_owner`, `access_boundary`, `provider`, `selected_reason`, `requirement_source`, `source_date`, `observed_at`, `evidence_ref`, `evidence_kind`, `reviewed_by`, `status`, `blocking`, `prerequisite_ids`, `lead_time_days`, `lead_time_basis`, `cost_amount`, `cost_currency`, `cost_unit`, `cost_source`, `cost_date`, `next_owner_action`.

| Field | Meaning |
|---|---|
| product_scope | The exact product, platform and release route served |
| environment | development, staging, production, distribution, or not-applicable |
| accountable_owner | Person or role accountable for resolving the row, not a borrowed identity |
| access_boundary | Who may inspect/use it and for what scope; no credential values |
| requirement_source | Applicable provider/accepted-design reference, or unknown |
| source_date/observed_at | Known source date or unknown; separate current observation date |
| evidence_ref/kind | Reference to owner report, authorized observation, official documentation, or none |
| status | unknown, reported, blocked, observed-ready, deferred, not-applicable |
| blocking | yes/no relative to the intended milestone, not all future product versions |
| prerequisite_ids | Semicolon-separated existing row IDs; no hidden dependency cycles |
| lead_time_days/basis | Applicable sourced duration or unknown; owner estimates labeled estimate |
| cost | Numeric amount with currency/unit/source/date, or unknown amount; never treat blank/unknown as zero |
| next_owner_action | One concrete action or decision needed; does not itself grant authority |

`reported` means the owner supplied a claim. `observed-ready` means an authorized inspection and named reviewer matched the milestone/environment and recorded evidence. The checker validates that these fields exist; it cannot establish that an account exists, verify approval or promote statuses. Official documentation is requirement evidence, not account-state evidence. A store membership is not a store submission approval.

For secrets, store only a reference name/location supplied within scope. Never copy API keys, bearer tokens, passwords, connection strings, payment details or identity documents into the ledger. A fixture's fictional evidence IDs are illustrations and cannot prove actual readiness.

Unknown price/duration stays unknown. A price observation includes its per-month, per-year, per-request or one-time unit. Provider/project plan, region, currency/tax and usage assumptions are separate when material. Add a recurring renewal responsibility even when enrollment is already complete.
