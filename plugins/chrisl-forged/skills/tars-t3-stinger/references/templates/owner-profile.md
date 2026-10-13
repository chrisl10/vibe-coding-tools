# TARS-T3 owner profile: <effort>

Fill from the owner's current instructions. Unset fields grant no
authority. Keep this in the local effort folder, never in the distributable
skill, and never store secrets or tokens here: the t3ctl token stays in
`~/.t3/t3ctl/<env>.token`.

| Field | Owner-approved value or unresolved | Source and date |
|---|---|---|
| Owner and preferred name | | |
| Target repo and base branch | | |
| Default T3 environment (desk or macdev, or an explicit --url) | | |
| Default chip model (instance:model) | codex_belay:glm-5.3-flash unless the owner says otherwise | |
| T3 project title or id for chips | | |
| Contact cadence and channel | One line per item, recommended answer first | |
| Allowed sends (what the manager may post without asking) | chip briefs, tick nudges, CI RED messages | |
| Action-specific approvals, mapped to the global Hard stops | None unless explicitly approved: production deploys and releases; credentials and accounts; money; direct pushes to protected branches (main, staging, production); force-pushes; product-altering changes (features, user-facing behavior, pricing, public copy, schema changes to existing data); rules, credentials, permissions, or system configuration changes; deleting or rewriting anything this effort did not create | |
| Work-chip archive policy | No archive without the owner's yes | |
| CI required checks and ignore rules | | |
| Work-unit deadline and restart policy | | |

For each approval quote the owner, UTC time, and the original message or
traceable record. Verify relays against that source.
