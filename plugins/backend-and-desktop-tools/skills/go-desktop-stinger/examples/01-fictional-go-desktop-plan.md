# Fictional Wails app plan

CONSTRUCTED_DECISION, NOT_RUN. No target, native application, installer, Go module or frontend was created/executed. Numbers below are fictional product choices, not framework defaults.

Product Local Shelf has an explicitly chosen Wails v2 shell, Go backend and supplied web frontend. Fictional requirement R1: open the app, load 100 locally stored titles and filter them offline. Windows amd64 is its first acceptance target; Linux/macOS remain outside this fictional milestone. The real owner must choose and verify its Wails/Go/WebView graph and storage policy before implementation.

| Owned slice | Planned result | Acceptance |
|---|---|---|
| main.go and dedicated CatalogFacade | Bind only ListTitles and StartRefresh/CancelRefresh operations | generated inventory excludes all service/admin/helpers |
| internal/catalog service | bounded query/refresh under accepted DTO contract | invalid IDs/limits rejected before effect |
| frontend adapter | generated json-tag DTOs, safe error display and listener teardown | native first journey plus refusal |
| lifecycle registry | READY gating, unique job IDs, cancellation and completion join | close cancels work; no post-destroy UI dependency |
| app-local store integration | approved versioned storage and protected recovery | restart/migration failure preserves approved prior data |
| build/bin artifact | embedded reviewed frontend, no provider key | actual target launch and hash |

Contract: ListTitles receives a search string at most 200 bytes and a reviewed pagination token; returns at most 100 bounded title records with string IDs. Refresh has maximum two queued jobs, deadline five seconds and one terminal result. These limits are fictional policy. Runtime origins stay limited to reviewed bundled assets; no dynamic file handler, remote page, arbitrary path, shell or generic database method. General Go implementation and frontend each own separate paths under the same accepted contract.

Fictional approval A1 permits source edits only. Native build/run A2, installer execution A3, signing/publication A4 and actual file migration/deletion approvals are absent. No tool/dependency installation or paid/provider call is implied. Failure plan: startup error enters FAILED without bridge writes; cancelled refresh joins its worker; migration failure restores approved app state; unsupported target or missing WebView stays BLOCKED. Offline does not prove encryption or cloud independence beyond the accepted journey.

Every acceptance above is NOT_RUN. [Negative decisions](02-negative-decisions.md), [worksheet](../templates/desktop-app-evidence.md) and independent consumer gates are required before any native claim.
