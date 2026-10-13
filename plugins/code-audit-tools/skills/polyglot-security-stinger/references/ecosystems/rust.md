# Rust reference (Axum, Actix)

Loaded by [guides/04-rust.md](../../guides/04-rust.md). Stack id `rust`. `$RG` is defined in [../cross-cutting/tool-commands.md](../cross-cutting/tool-commands.md). Library names in sink tables are search hints; a hit becomes a finding only after the call site is read.

Rust removes memory-safety bugs in safe code, not logic bugs. Most real findings in Rust web services are the same as elsewhere: SQL text building, missing authorization, path joins, SSRF, and secrets.

Thin spot: Axum and Actix extractor, CSRF, and body-limit defaults are not in the archive. Confirm in the code which layers and middleware are registered; never assert a framework default as a fact [research/distilled-polyglot-security.md].

## Checklist

| # | Check | Refs |
| --- | --- | --- |
| R1 | No SQL text built with `format!`, `concat!`, or `+` and passed to `sqlx::query`, `query_as`, `diesel::sql_query`, or `Statement::from_string`; use `query!` macros or `.bind()` | CWE-89 |
| R2 | `QueryBuilder` uses `push_bind` for values; plain `push` only for allowlisted identifiers | CWE-89 |
| R3 | `std::process::Command` is not `sh -c` with user data; program name not user controlled | CWE-78 |
| R4 | `Path::join` / `PathBuf::push` with user input are confined after canonicalizing; absolute user paths replace the base when joined | CWE-22 |
| R5 | `reqwest::get(user_url)` and clients with user URLs are allowlisted; redirect policy considered | CWE-918 |
| R6 | Every protected route sits behind an auth layer or an extractor that rejects anonymous users; handlers check ownership | CWE-862, CWE-639 |
| R7 | `serde` request structs for updates do not include role, owner, or tenant fields that the handler writes straight to the database | CWE-915 |
| R8 | `unsafe` blocks in request handling are justified and reviewed | CWE-119 |
| R9 | `.unwrap()` / `.expect()` / indexing on request-derived data do not let a client crash the worker | CWE-248, OWASP A10:2025 |
| R10 | `danger_accept_invalid_certs(true)` absent outside tests | CWE-295 |
| R11 | Cookie sessions on state-changing routes use CSRF protection or SameSite plus origin checks | CWE-352 |
| R12 | No secrets as string literals; config read from env or a secret store | CWE-798 |
| R13 | `rand::thread_rng` and OS RNG for secrets, not a seeded or non-crypto RNG | CWE-338 |

Sources: [raw/rust--sqlx-query-macro.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md].

## Sources of untrusted input

Axum extractors `Path<T>`, `Query<T>`, `Json<T>`, `Form<T>`, `HeaderMap`, `Multipart`, `TypedHeader`; Actix `web::Path`, `web::Query`, `web::Json`, `web::Form`, `HttpRequest::headers`, `Multipart`; WebSocket frames; queue messages.

## ripgrep patterns

```bash
# SQL text building
$RG -t rust -e '(sqlx::)?query(_as|_scalar)?\(\s*&?format!' -e 'sql_query\(\s*format!' -e 'Statement::from_string\([^)]*format!' -e 'QueryBuilder' -e '\.push\(\s*&?format!'
# Command execution
$RG -t rust -e 'Command::new\(' -e '"(sh|bash)"\)\s*\.arg\("-c"\)' -e '\.arg\("-c"\)'
# Paths
$RG -t rust -e '\.join\([^)]*(path|name|file|query|params)' -e 'File::open\(' -e 'fs::(read|read_to_string|write|remove_file)\(' -e 'ServeDir::new'
# SSRF and TLS
$RG -t rust -e 'reqwest::(get|Client)' -e '\.get\(\s*&?(url|target)' -e 'danger_accept_invalid_certs\(\s*true'
# Panics on request data
$RG -t rust -e '\.(unwrap|expect)\(' -e 'unsafe\s*\{'
# Auth layers present
$RG -t rust -e '(route_layer|from_fn|middleware::from_fn|wrap\(|RequireAuthorizationLayer|ValidateRequestHeaderLayer)'
# Update structs with privileged fields
$RG -t rust -e '#\[derive\([^)]*Deserialize' -A6 | rg -e '\b(role|is_admin|admin|owner_id|tenant_id|user_id)\s*:'
# Secrets
$RG -t rust -e '(?i)(secret|password|api_key|token)\s*[:=]\s*"[^"]{12,}"'
```

## Vulnerable vs fixed pairs

**SQL (sqlx)**

```rust
// vulnerable
let sql = format!("SELECT * FROM users WHERE email = '{}'", q.email);
let rows = sqlx::query(&sql).fetch_all(&pool).await?;
// fixed (checked at compile time)
let rows = sqlx::query!("SELECT id, email FROM users WHERE email = $1", q.email).fetch_all(&pool).await?;
```

**Dynamic ORDER BY**

```rust
// vulnerable
qb.push(format!(" ORDER BY {}", params.sort));
// fixed: allowlist identifiers, bind values
let col = match params.sort.as_str() { "name" => "name", "created" => "created_at", _ => "id" };
qb.push(" ORDER BY ").push(col);
qb.push(" LIMIT ").push_bind(params.limit.min(100));
```

**Path traversal**

```rust
// vulnerable: "../../etc/passwd" or an absolute path escapes BASE
let p = Path::new(BASE).join(&name);
// fixed
let p = Path::new(BASE).join(&name).canonicalize()?;
if !p.starts_with(Path::new(BASE).canonicalize()?) { return Err(StatusCode::NOT_FOUND.into()); }
```

**Command**

```rust
// vulnerable
Command::new("sh").arg("-c").arg(format!("convert {} out.png", file)).status()?;
// fixed
Command::new("convert").arg("--").arg(&safe_file).arg("out.png").status()?;
```

**Panic on input**

```rust
// vulnerable: a missing header crashes the task with a 500 and noisy logs
let id: i64 = headers.get("x-id").unwrap().to_str().unwrap().parse().unwrap();
// fixed
let id: i64 = headers.get("x-id").and_then(|v| v.to_str().ok()).and_then(|s| s.parse().ok())
    .ok_or(StatusCode::BAD_REQUEST)?;
```

## Dependency audit for this ecosystem

1. `osv-scanner scan -r .` reads Cargo.lock; Rust call analysis (`--call-analysis=rust`) compiles the code and is experimental, so use it only in the throwaway copy and only when cargo is present [raw/deps--osv-scanner-usage.md].
2. Fallback: `cargo audit --file path/to/Cargo.lock --json`, run from outside the project directory so no build scripts run [raw/deps--cargo-audit.md].
3. RustSec "unmaintained" and "yanked" warnings are `low` unless a vulnerability advisory is attached.

## Sources

[raw/rust--sqlx-query-macro.md], [raw/deps--cargo-audit.md], [raw/deps--osv-scanner-usage.md], [raw/owasp--os-command-injection-cheat-sheet.md], [raw/owasp--ssrf-cheat-sheet.md], [raw/owasp--mass-assignment-cheat-sheet.md]
