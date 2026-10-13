# Go desktop application workflow

Use go-desktop-stinger/go-desktop-wasp-drone in backend-and-desktop-tools for an explicitly chosen Wails v2 desktop application with a Go backend. Core is required; web-development-tools is needed only when frontend design/framework work enters scope. This is a new shell-specific owner, because existing Go covers module/language mechanics and Tauri/Electron own different runtime boundaries.

1. [Inspect and scope](guides/01-inspect-and-scope.md).
2. [Bind a validated facade](guides/02-bind-and-validate.md).
3. [Own lifecycle/storage](guides/03-own-lifecycle-and-storage.md).
4. [Build and qualify](guides/04-build-and-qualify.md).

Read [the source digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/go-desktop-stinger/references/research/digest.md) and [boundary reference](references/REFERENCE.md), complete [evidence](templates/desktop-app-evidence.md), and review [the fictional plan](examples/01-fictional-go-desktop-plan.md) and [negative cases](examples/02-negative-decisions.md). Cases are NOT_RUN. Source snapshots and generated DTOs do not prove native safety, shutdown, persistence, distribution or installed availability.

The 2026-10-08 refresh captures Wails v2 versioned documentation at a recorded official commit after direct doc retrieval returned 403. This does not choose a consumer package version; inspect its actual graph and refresh advisories before work. Public-method binding, runtime readiness, frontend destruction on shutdown and asset-handler exposure are specific application boundaries. Wails v3/Fyne/mobile remain outside this pair. Parent owns catalog/roster/command registration, generated carriers, independent gates and activation; no installed availability is claimed by these source files.
