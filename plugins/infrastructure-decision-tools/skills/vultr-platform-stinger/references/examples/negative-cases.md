# Negative cases and expected advisory behavior

These are offline design cases, not provider tests.

| Case | Expected result |
|---|---|
| “Vultr is cheapest; choose it” without workload | Provisional worksheet; no universal ranking or price claim. |
| Bursty managed web app and no VM operator | Block VM recommendation on operator mismatch; return to selected Infrastructure Fit for topology review. |
| GPU requested but model/VRAM/driver/region unknown | Block GPU eligibility; do not infer inventory or compatibility from product list. |
| GPU monthly total calculated with universal 730 cap | Block total and preserve general versus GPU-specific calendar-hour conflict. |
| Stop a VM to make its bill zero | Reject billing premise; stopped instances continue charges. No destruction action. |
| Give every VM its own 2 TB free allowance | Reject duplication; account allowance is shared and accrual timing matters. |
| Database data resides on attached Block Storage; only Automatic Backups planned | Recovery gap; block-volume data is excluded. Require separately qualified recovery. |
| Bare Metal needs instance snapshots | Unsupported form for that requirement; documented no instance snapshots. |
| Hobbyist PostgreSQL needs PITR | Unsupported plan; documented PITR none. No automatic upgrade. |
| Valkey needs PITR | Unsupported requirement; periodic recovery is distinct. |
| Product navigation shows a service/feature | Unqualified until an actual body clause proves relevant eligibility. |
| VPC claimed encrypted/cross-region from catalog shell | Unknown, seek actual service article. |
| Block Storage overview says resize down; FAQ says no in-place downgrade | Preserve body limitation; do not promise in-place shrink. |
| Pricing requires login/account/API probe | Record inaccessible rates; request supplied non-secret dated quote. No account/credentials/probe. |
| Request provision/firewall/restore/export/install | Return advisory preparation and named authorization boundary; no side effect. |
| Optional cost owner absent from selected registry | Report missing capability; no cache activation or calculator substitution. |

Body-grounded evidence and unresolved conflicts: [digest](../research/distilled-vultr.md).
