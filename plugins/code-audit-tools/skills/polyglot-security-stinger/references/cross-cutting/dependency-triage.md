# Dependency vulnerability triage

Loaded by [guides/10-dependency-vulnerabilities.md](../../guides/10-dependency-vulnerabilities.md). The goal is a short list a founder can act on, not a dump of every advisory.

## 1. Coverage map: what each tool can see

| Ecosystem | osv-scanner reads | Fallback | Blind spot to record as a cap |
| --- | --- | --- | --- |
| node-server | package-lock.json, pnpm-lock.yaml, yarn.lock, bun.lock | `npm audit --omit=dev --json` | no lockfile at all |
| python | uv.lock, poetry.lock, pdm.lock, Pipfile.lock, pylock.toml, requirements.txt (best effort) | `pip-audit --no-deps -r ...` or `--locked .` | unpinned requirements lines have no version |
| go | go.mod (with call analysis) | `govulncheck ./...` | none when go is installed |
| rust | Cargo.lock | `cargo audit --file Cargo.lock` | library crates without a committed Cargo.lock |
| ruby | Gemfile.lock, gems.locked | `bundle-audit check --update` | none with a lockfile |
| php | composer.lock | `composer audit --locked` | plain PHP without composer |
| java-kotlin | pom.xml (transitive through deps.dev, off offline), gradle.lockfile, verification-metadata.xml | none without running the build | Gradle without dependency locking; offline Maven transitive deps |
| dotnet | packages.lock.json, packages.config, deps.json | `dotnet package list --vulnerable --include-transitive` | PackageReference-only projects when the SDK is absent |

[raw/deps--osv-scanner-supported-lockfiles.md] [raw/deps--npm-audit.md] [raw/deps--pip-audit.md] [raw/deps--govulncheck.md] [raw/deps--cargo-audit.md] [raw/deps--bundler-audit.md] [raw/deps--composer-audit.md] [raw/deps--dotnet-package-list.md]

## 2. Triage steps (apply to every advisory)

1. **Scope.** Drop advisories in packages that live only under paths outside this Drone's stack paths (another Drone owns them) and say so in notes.
2. **Production or dev.** Mark dev-only (`devDependencies`, `require-dev`, `[dev-dependencies]`, test scopes). Dev-only advisories cap at `low` unless the package runs in CI with secrets (then treat as supply chain and keep the original severity).
3. **Reachability.**
   - Go: osv-scanner and govulncheck mark called vs not called. Called: keep severity, `confidence: confirmed` for reachability. Not called: `low`, note it [raw/deps--govulncheck.md].
   - Rust: experimental call analysis only when cargo ran it.
   - Others: search the code for the vulnerable function or feature named in the advisory (`$RG` for the import and the function). Found and fed by request data: keep severity, `likely`. Imported but the vulnerable function is not used: drop to `low`, `likely`. Could not tell: keep the advisory severity but cap at `medium` with `possible`.
4. **Fix available.** Record the first fixed version from the tool output. No fix: say so and suggest the mitigation the advisory gives, or replacing the package.
5. **Group.** One finding per package and fixed version, listing all advisory ids in `refs`. Do not write one finding per CVE when a single upgrade closes them all.
6. **Map severity.** Start from the advisory's own severity (CVSS or GHSA level), then apply steps 2 and 3. Never raise above the advisory unless you confirmed exploitation in this code.
7. **Never invent ids.** Every CVE, GHSA, RUSTSEC, PYSEC, or GO id in `refs` must appear in the tool output file you cite in `evidence`.

## 3. Noise controls

- Group duplicates across lockfiles of one monorepo into one finding with several `locations`.
- Ignore advisories already suppressed in a committed ignore file only after reading the reason (`.osv-scanner.toml`, `audit.toml`, `.bundler-audit.yml`); an unexplained suppression is itself an `info` or `low` note.
- Outdated but not vulnerable is not a security finding (bloat or quality may care).
- Malicious or typosquatted packages (osv `MAL-` ids, composer malware flag) are always `critical` if present in production dependencies [raw/deps--composer-audit.md].

## 4. Supply-chain hygiene checks (no tool needed)

| Check | Severity when failing |
| --- | --- |
| Lockfile committed for every deployable package | `low` (`medium` if CI installs without a lock) |
| CI and Dockerfiles use `npm ci` / `pnpm install --frozen-lockfile` / `pip install --require-hashes` / `bundle install --frozen` style installs | `low` |
| Unknown or very new packages that the code imports but no one seems to use elsewhere (possible hallucinated or slopsquatted name): check registry existence, publish date, publisher | `high` if the package exists and is not the intended project, `medium` if unverified [raw/ai--csa-slopsquatting-2026.md] |
| Gem sources over `http://` or `git://` | `medium` [raw/deps--bundler-audit.md] |
| `npm config` or `.npmrc` disabling `ignore-scripts` is not a finding; enabling install scripts is the default. Recommend `--ignore-scripts` only as hardening (`low`) [raw/node--nodejs-security-best-practices.md] |

## 5. Finding text example

```json
{"id": "SEC-POLY-014", "dimension": "security", "source": "polyglot-security-wasp-drone",
 "title": "The API server uses a version of a web library with a known flaw that lets attackers crash it",
 "severity": "high", "confidence": "likely",
 "locations": [{"path": "services/api/package-lock.json", "line_start": 1, "line_end": 1}],
 "evidence": "osv-scanner 2.6.0 (raw/polyglot/osv.json): <package>@<version> <advisory id> severity HIGH, fixed in <version>. rg shows services/api/src/server.js:14 imports it and calls the affected parser on req.body.",
 "why_it_matters": "Anyone on the internet can send one request that stops the API, taking the product offline.",
 "remediation": "Upgrade <package> to <fixed version> in services/api/package.json, regenerate package-lock.json with npm install, and redeploy.",
 "effort": "S", "refs": ["<advisory id from osv.json>", "OWASP A03:2025", "polyglot-security-stinger/guides/10-dependency-vulnerabilities.md"],
 "verified_by": "Matched the advisory's affected function to the call site in server.js and confirmed request data reaches it."}
```

Angle-bracket placeholders above are for illustration only; a real finding uses the exact package, version, and id from the tool output.

Sources: listed inline.
