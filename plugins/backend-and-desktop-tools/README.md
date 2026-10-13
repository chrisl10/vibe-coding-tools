# Backend and Desktop Tools

Implement TypeScript, Python, Go, Rust, native apps, APIs and terminal workflows.

Implementation languages and native delivery share code ownership and build boundaries; mobile store publication stays beside app delivery.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 10 skills, 10 agents and 4 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [app-store-submission-stinger](skills/app-store-submission-stinger/SKILL.md) | Prepare iOS and Android app submissions. Use for store review, ASO, privacy forms, or rejection remediation. |
| [electron-app-stinger](skills/electron-app-stinger/SKILL.md) | Electron application engineering for process boundaries, preload APIs, IPC, sandboxing, packaging, updates, and desktop verification. Use for Electron app implementation or review. |
| [go-desktop-stinger](skills/go-desktop-stinger/SKILL.md) | Build Wails v2 desktop apps around Go backends: typed bindings, lifecycle, storage, native builds and package evidence. Use after Wails is explicitly selected. |
| [go-stinger](skills/go-stinger/SKILL.md) | Go specialist for modules, toolchains, vendoring and fork-in-tree freezes, cgo .so plugin ABI, project layout, and builds. Use for go.mod, replace directives, vendoring upstream repos, plugin crashes. |
| [http-rest-fundamentals-stinger](skills/http-rest-fundamentals-stinger/SKILL.md) | Audit HTTP and REST behavior. Use for methods, status codes, headers, caching, CORS, conditional requests, or API semantics. |
| [python-stinger](skills/python-stinger/SKILL.md) | Python code specialist for Django, FastAPI, Celery, Channels, pytest, uv, and Ruff. Use when reviewing, refactoring, or authoring Python code, or migrating DRF to Ninja. |
| [rust-stinger](skills/rust-stinger/SKILL.md) | Rust development specialist for Cargo, async services, persistence, CLI/TUI, tests, upgrades, and current toolchains. Use for Rust implementation, review, migration, or release guidance. |
| [tauri-stinger](skills/tauri-stinger/SKILL.md) | Tauri 2 engineering for desktop and mobile: updates, migration, IPC, capabilities, sidecars, AI runtimes, persistence, signing, updater, testing, and distribution. Use for Tauri-specific work. |
| [terminal-bash-stinger](skills/terminal-bash-stinger/SKILL.md) | Improve terminal workflows. Use for Bash, Zsh, Fish, modern CLI tools, dotfiles, tmux, or just/make automation. |
| [typescript-node-stinger](skills/typescript-node-stinger/SKILL.md) | Review TypeScript and Node code. Use for SvelteKit types, tsconfig, ESM, Zod boundaries, testing, or npm package builds. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install backend-and-desktop-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use python-stinger to review [Python service] and its tests. Explain the observed behavior and the smallest needed change.
```

Expected result: Language or desktop implementation/review evidence. Select the skill that matches the actual runtime.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/backend-and-desktop-tools:build-desktop-app` ([procedure](commands/build-desktop-app.md)) | Scope and build an authorized desktop-app slice with an explicit native boundary and native verification. |
| `/backend-and-desktop-tools:build-mobile-backend` ([procedure](commands/build-mobile-backend.md)) | Build the server side of a mobile product with accepted identity, API compatibility and unreliable-network contracts. |
| `/backend-and-desktop-tools:choose-backend` ([procedure](commands/choose-backend.md)) | Recommend one backend language/runtime from workload, integration, operations and actual implementation coverage. |
| `/backend-and-desktop-tools:choose-desktop-stack` ([procedure](commands/choose-desktop-stack.md)) | Choose one desktop architecture with native boundary, operating-system support, persistence, update and release evidence. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [app-store-submission-wasp-drone](agents/app-store-submission-wasp-drone.md) | App store publication specialist for iOS (App Store Connect + TestFlight) and Android (Google Play Console). | [app-store-submission-stinger](skills/app-store-submission-stinger/SKILL.md) |
| [electron-app-wasp-drone](agents/electron-app-wasp-drone.md) | Electron desktop application specialist for main, preload, renderer, IPC, sandbox, permissions, packaging, and native verification. | [electron-app-stinger](skills/electron-app-stinger/SKILL.md) |
| [go-desktop-wasp-drone](agents/go-desktop-wasp-drone.md) | Wails v2 desktop application specialist for Go backends, generated web bindings, validated facades, lifecycle, app-local storage and native/package evidence. | [go-desktop-stinger](skills/go-desktop-stinger/SKILL.md) |
| [go-wasp-drone](agents/go-wasp-drone.md) | Go implementation drone for modules, toolchains, vendoring/fork freezes, cgo .so plugin builds, and project layout. | [go-stinger](skills/go-stinger/SKILL.md) |
| [http-rest-fundamentals-wasp-drone](agents/http-rest-fundamentals-wasp-drone.md) | HTTP and REST protocol authority. | [http-rest-fundamentals-stinger](skills/http-rest-fundamentals-stinger/SKILL.md) |
| [python-wasp-drone](agents/python-wasp-drone.md) | Python architecture specialist for Django + Django Ninja + FastAPI + Celery + Channels + pytest + uv codebases: enforces the canonical stack (Pydantic v2 at boundaries, Ruff + pyright, httpx for outbound HTTP), reviews Django app architecture, audits the ORM (N+1 prevention via select_related/prefetch_related, raw SQL only when justified), polices migrations (expand-backfill-contract; never edit applied migrations), migrates DRF to Django Ninja, sets up Celery jobs (retries, idempotency, acks_late), enables Channels (consumers + Daphne), configures pytest (pytest-django + factory_boy + pytest-asyncio), drives type adoption (pyright basic minimum, strict on new), Ruff config, uv migration, async refactors, settings split, and the Django + React decoupled-architecture surface (CORS, auth handoff, API contract). | [python-stinger](skills/python-stinger/SKILL.md) |
| [rust-wasp-drone](agents/rust-wasp-drone.md) | Rust implementation and code-review specialist for production `*.rs`, `Cargo.toml`, Cargo workspaces, Tokio/Axum/Tower services, SQLx/SQLite state, Clap/Ratatui clients, Rust tests, and local packaging evidence. | [rust-stinger](skills/rust-stinger/SKILL.md) |
| [tauri-wasp-drone](agents/tauri-wasp-drone.md) | Tauri 2 desktop and mobile application engineering specialist. | [tauri-stinger](skills/tauri-stinger/SKILL.md) |
| [terminal-bash-wasp-drone](agents/terminal-bash-wasp-drone.md) | Terminal productivity specialist for Bash/Zsh/Fish configuration, modern CLI tools (ripgrep, fd, fzf, bat, eza, zoxide), shell scripting best practices, dotfile architecture, tmux/Zellij setup, and just/make task automation. | [terminal-bash-stinger](skills/terminal-bash-stinger/SKILL.md) |
| [typescript-node-wasp-drone](agents/typescript-node-wasp-drone.md) | Modern TypeScript/Node specialist for this Wasp Nest's stack - SvelteKit (Svelte 5) on Vercel as the primary case (tsconfig bundler resolution and verbatimModuleSyntax, typed load functions/form actions/+server.ts, Drizzle type-inference patterns, zod vs valibot at boundaries, Vitest plus Playwright, Biome vs ESLint, pnpm and monorepo choice, Node-on-Vercel version policy), with full continued support for the legacy npm library/CLI publishing case this Drone was originally forged for (Hivemind: strict ESM on Node16 resolution, esbuild multi-harness bundling, zod v3/v4 MCP split, jscpd, husky lint-staged as the whole gate). | [typescript-node-stinger](skills/typescript-node-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `web frontend in a desktop app` also needs `web-development-tools`.
- `build-desktop-app-ui` also needs `web-development-tools`.
- `build-mobile-backend-data` also needs `data-and-ai-tools`.
- `build-mobile-backend-identity` also needs `platform-and-release-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
