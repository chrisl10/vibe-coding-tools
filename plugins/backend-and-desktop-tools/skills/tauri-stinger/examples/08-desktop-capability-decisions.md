# Desktop capability decision exercises

All records are SYNTHETIC supplied-case reviews; outcomes below are expected review decisions, not executed native verdicts. Source basis: [digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/tauri-stinger/references/research/desktop-capabilities-20261007/distilled-desktop-capabilities.md).

| Outcome | Supplied synthetic record | Review decision | Required evidence or action |
|---|---|---|---|
| O103 | Frontend allows a named sidecar with args:true; model output supplies arguments. | HOLD | Name alone does not constrain arguments. Rust-owned typed request or precise scoped argument contract plus deny tests required. |
| O103 | Rust invokes an exact sidecar, but any remote window can call its custom command. | HOLD | Permission/custom-command origin and business authorization remain unproven; Rust location does not imply capability restriction. |
| O103 | Post-event line length capped, sidecar never sends a newline. | HOLD | Full-line reader can allocate first; use bounded raw framing or enforced producer bound and process cleanup proof. |
| O103 | Encrypted vault is used, frontend has retrieval permission and receives provider key. | FAIL intended credential boundary | Encryption at rest does not preserve a Rust-only use contract; remove retrieval exposure and qualify broker/unlock lifecycle. |
| O103 | Child kill returns success; reader task and descendants not observed. | OPEN cleanup | One handle result does not prove tree termination, task join or bounded shutdown. |
| O096 | Migration fails inside explicit transaction; synthetic SQLite restores original schema and row. | PASS synthetic mechanics only | Tauri/plugin, OS durability, actual historical fixtures and app recovery remain OPEN. |
| O096 | Updater installs schema2; prior binary supports only schema1; reinstall recommended. | HOLD recovery | Prove backup restore/compatible forward repair; authenticated old code can still lose data or fail. |
| O096 | Live SQLite .db copied without backup API or WAL policy. | HOLD backup | Require application-consistent copy/backup with related-file and restore verification. |
| O096 | Missing legacy status filled with successful as guessed backfill. | FAIL data policy | Keep unknown values unknown; owner must define the historical meaning. |
| O100 | Artifact signature valid; feed returns an old signed release with comparison overridden. | HOLD rollback authorization | Signature integrity does not prove freshness or allowed downgrade/data compatibility. |
| O100 | New app trusts K2; K1-only installed clients receive K2-signed bridge. | FAIL trust transition | They cannot authenticate the bridge under K1. Prove an accepted transition or explicit recovery route. |
| O100 | OS code signature passes; updater .sig missing. | HOLD updater | Distinct signatures; OS identity cannot replace required updater signature verification. |
| O100 | Static signature field is a URL to a .sig file. | FAIL metadata contract | Use actual signature content bound to exact payload and target; no live update performed here. |
| O102 | Linux tray icon visible; double-click is sole restore path. | HOLD essential behavior | Documented tray mouse events unsupported; test menu/in-app fallback on target session. |
| O102 | Windows development notification shows PowerShell, no installed run. | OPEN installed identity | Development result does not establish installed app identity or delivery. |
| O102 | Global shortcut callback invokes privileged action on Pressed and Released. | HOLD callback semantics | Define one intended edge, repeat suppression, conflict behavior and cleanup. |
| O102 | Notification permission granted, OS quiet mode state not captured. | OPEN delivery | Grant does not prove display; record real policy/session and fallback without changing settings. |
| O104 | Browser mocks pass and capability schema is valid; native IPC declared accepted. | FAIL evidence classification | Mocks and shape checks do not execute runtime authority or native libraries. |
| O104 | macOS native tests configured with direct tauri-driver alone. | HOLD route | Official direct driver is Windows/Linux; qualify an embedded service or other real app route. |
| O104 | Actual app E2E passes but tested command is mocked by driver. | OPEN native command | Turn off that mock and execute authorized IPC allow/deny against actual app. |
| O104 | Embedded test automation bridge enabled in production bundle. | HOLD production boundary | Prove test-only exclusion/disable policy and independently review privileged backend access. |

The [SQLite exercise](09-sqlite-recovery-exercise.py) executes separate temporary-database mechanics. It does not execute these Tauri cases or grant publication/installation authority.
