# Desktop capability evidence record

Derived worksheet. Store completed records in the consumer repository report path. Never include credential values, private keys, personal data or raw private process output.

- Outcome, requirement and acceptance owner:
- Authority for effects and explicit exclusions:
- Source revision, dependency lock graph, Tauri/plugin/driver versions:
- OS/version/architecture/session/package route:
- Window/webview/origin/capability union/custom command:
- App, sidecar, database fixture and package hashes:

| Boundary | Expected allow or deny / recovery behavior | Actual observation, command and sanitized evidence | Level | State OPEN/PASS/FAIL/N/A with reason |
|---|---|---|---|---|
| Exact sidecar and fixed/validated arguments | | | | OPEN |
| Child/readers/descendants shutdown | | | | OPEN |
| Credential ownership, vault unlock/revocation, redaction | | | | OPEN |
| Prior schema -> new schema / repeated startup | | | | OPEN |
| Transaction failure / backup restore / old reader | | | | OPEN |
| Updater payload signature / OS signature / feed policy | | | | OPEN |
| Old-key -> bridge -> new-key / stale version | | | | OPEN |
| Update interrupted / data-compatible recovery | | | | OPEN |
| Tray/menu/focus/close/quit | | | | OPEN |
| Global shortcut collision/reload/Pressed/Released | | | | OPEN |
| Notification denied/revoked/installed identity | | | | OPEN |
| Real app IPC allow/deny with mocks disabled | | | | OPEN |
| Packaged resources, install, restart and target rows | | | | OPEN |
| Automation bridge excluded from production | | | | OPEN |

## Recovery and handoff

Data schema transition; backup protection and restore proof; old-reader support; no-replay policy; key trust transition; unsupported OS/driver rows; Security then Quality reports; publication/installation owner approvals separately. A document-shape or synthetic exercise PASS cannot fill a native acceptance row.
