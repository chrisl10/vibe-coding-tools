# Manifest to stack id map

Loaded by [guides/00-scoping-and-ecosystem-detection.md](../../guides/00-scoping-and-ecosystem-detection.md). This table is what `scripts/detect_ecosystems.py` implements. Use it to check the script's output by hand, or to classify a folder when the script cannot run.

## Stack ids

| Stack id | Detected from | Version reported | Framework details recorded |
| --- | --- | --- | --- |
| `nextjs` | `package.json` with `next` in any dependency section | resolved `next` version from the nearest lockfile, else the cleaned spec | `next`, `react` |
| `react` | `package.json` with `react`, without `next` and without `@sveltejs/kit` | resolved `react` | react-native, expo, vite, remix, react-router, tanstack-start, gatsby |
| `sveltekit` | `package.json` with `@sveltejs/kit` | resolved `@sveltejs/kit` | `svelte` |
| `svelte` | `package.json` with `svelte`, without `@sveltejs/kit` | resolved `svelte` | |
| `node-server` | `package.json` with a server framework (express, fastify, @nestjs/core, hono, koa, @hapi/hapi, and others), or a non-frontend package with runtime dependencies or an entry point; `deno.json` / `deno.jsonc` without `package.json` | Node version from `engines.node`, `volta.node`, `.nvmrc`, or `.node-version` | server frameworks with resolved versions; `runtime` node, bun, or deno |
| `python` | `pyproject.toml` with `[project]`, `[tool.poetry]`, or `[build-system]`; `requirements*.txt` / `.in`; `setup.py`; `setup.cfg`; `Pipfile`; `manage.py`; `environment.yml` | `requires-python`, poetry `python`, `.python-version`, or `runtime.txt` | django, djangorestframework, django-ninja, fastapi, flask, starlette, litestar, celery, sqlalchemy, jinja2, others; versions from uv.lock, poetry.lock, pdm.lock, Pipfile.lock |
| `go` | `go.mod` | `toolchain` or `go` directive | gin, echo, fiber, chi, gorilla/mux, grpc, gorm, sqlx; `net/http` when no framework and a `.go` file imports it |
| `rust` | `Cargo.toml` with `[package]` (pure `[workspace]` roots are skipped; members are found on their own) | `rust-version`, else `rust-toolchain(.toml)` channel | axum, actix-web, rocket, warp, poem, tonic, sqlx, diesel, sea-orm, tokio, tower-http; versions from Cargo.lock |
| `ruby` | `Gemfile` (or a `.gemspec`) | `ruby` line in Gemfile, else `.ruby-version` | rails, sinatra, hanami, grape, roda, devise, pundit, cancancan; versions from Gemfile.lock |
| `php` | `composer.json`; or `.php` files outside any composer project (reported per top-level folder as `plain-php`) | `require.php` | laravel, lumen, symfony, slim, cakephp, yii2, codeigniter, laminas, drupal, wordpress, twig; versions from composer.lock |
| `java-kotlin` | `pom.xml`, `build.gradle`, `build.gradle.kts` | `java.version`, `maven.compiler.release`, Gradle toolchain, `sourceCompatibility`, `jvmToolchain` | spring-boot (version from parent or plugin), spring-security, quarkus, micronaut, ktor, vertx, dropwizard, javalin; `languages` Java or Kotlin |
| `dotnet` | `*.csproj`, `*.fsproj`, `*.vbproj` | first `TargetFramework(s)` (for example `net10.0` reported as `10.0`) | aspnetcore (Web, Razor, Blazor SDKs), efcore, newtonsoft-json, dapper, microsoft-identity-web; versions from PackageReference or Directory.Packages.props |
| `other` | `mix.exs`, `pubspec.yaml`, `Package.swift`, `CMakeLists.txt`, `meson.build`, `build.zig`, `stack.yaml`, `dune-project`, `Project.toml`, `DESCRIPTION`, `cpanfile`, `build.sbt`, `deps.edn`, `project.clj`; or source files with no manifest at all | none | `language` |

A folder can hold several ids: a Next.js app with a custom Express server is both `nextjs` and `node-server`.

## Skipped while walking

`node_modules`, `vendor`, `.git`, `dist`, `build`, `target` (required), plus `.venv`, `venv`, `__pycache__`, `.tox`, `.nox`, tool caches, `.next`, `.nuxt`, `.svelte-kit`, `.turbo`, `coverage`, `.terraform`, `.gradle`, `obj`, `out`, `.output`, `.vercel`, `.serverless`, IDE folders, `Pods`, `bower_components`. Symlinked folders are never followed. Agent worktree folders (`.claude/worktrees`, `.cursor/worktrees` and similar) and any child folder whose `.git` file points into another repository's `worktrees/` are skipped and listed in `coverage.skipped_worktrees`. Submodules are scanned. Add more with `--exclude NAME`.

## Output contract

- `stacks`: exactly `[{"id", "version", "paths"}]`, matching `intake.json.stacks`. Paths are repo-relative POSIX; `.` is the root. Nested paths of the same id collapse to the outermost. `version` is the most common version across that id's paths.
- `details.<id>[]`: per folder `path`, `version`, `version_source`, `frameworks[{name, version, spec, source}]`, `manifests`, plus `runtime`, `languages`, `module`, `target_framework`, or `note` when relevant. `source: manifest` means the version came from a spec, not a lockfile.
- `routing`: a hint that applies contract section 2 (nextjs to the Next.js and React Drones, react to the React Drone, svelte and sveltekit to the SvelteKit Drone, everything else to this Drone). The orchestrator decides.
- `infra`: Dockerfiles, compose files, GitHub workflows, GitLab CI, Terraform folders, Helm charts, Kubernetes-looking manifests, committed `.env` files.
- `languages`, `language_file_counts`, `coverage`, `warnings`.

Sources: [raw/deps--osv-scanner-supported-lockfiles.md] (which lockfiles carry exact versions), [raw/tools--version-pins-2026-09-30.md].
