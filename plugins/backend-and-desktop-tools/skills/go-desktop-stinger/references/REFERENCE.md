# Go desktop boundary reference

DERIVED contract, grounded in [the digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/go-desktop-stinger/references/research/digest.md).

| Boundary | Owner | Required artifact |
|---|---|---|
| Explicit Wails v2 shell choice, app options, generated bindings and lifecycle | go-desktop-wasp-drone | desktop brief and bridge inventory |
| General Go modules, language internals, cgo and business services | go-wasp-drone | bounded service implementation under accepted bridge |
| Frontend framework and visual design | selected frontend/Impeccable owner | accepted UI-to-Go DTO mapping |
| Generic schema, migrations and data retention policy | DB owner | persistence contract |
| Tauri or Electron shell with Go child | existing shell owner | approved process/protocol/lifecycle contract |
| Protocol, provider/runtime and AI orchestration | protocol/AI owners | accepted HTTP/MCP/provider contract |
| Formal security and dependency disposition | Core Security/dependency owners | independent reports |
| Signing identity, CI, installer distribution and release | release/DevOps owner | approved target artifact and external-effect evidence |

## Bridge operation record

For each bound public method: purpose, exact input/output DTO and json tags, validator location, length/count/type limits, caller/auth model, permitted resource, storage/network effects, deadline/cancellation, retry/idempotency, stable safe error code, redacted diagnostics and tests. Bind dedicated facade instances, not service objects containing exported admin/helpers. IDs crossing JavaScript numeric limits should use a reviewed string representation.

State model: app BOOTING -> READY or FAILED -> STOPPING -> CLOSED; jobs QUEUED -> RUNNING -> COMPLETED/CANCELLED/FAILED exactly once. These states, bounded queues and event correlation are application designs. Context cancellation signals require explicit worker completion coordination. Public events never approve a file write or provider action.
