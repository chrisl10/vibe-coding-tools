# 10 Dependency vulnerabilities across ecosystems

Loads [../references/cross-cutting/dependency-triage.md](../references/cross-cutting/dependency-triage.md), [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md), and the "Dependency audit" section of each ecosystem reference in scope.

## Steps

1. **List the lockfiles** in scope (from `detect.json.details.*.manifests` and a `--files` search for lockfile names). Note every deployable package with no lockfile; that is both a cap and, for deployable services, a `low` supply-chain finding.
2. **Run osv-scanner first** (multi-ecosystem default): `go run github.com/google/osv-scanner/v2/cmd/osv-scanner@v2.6.0 scan -r --format json "$COPY/<path>" > "$RAW/osv-<slug>.json"`, one run per stack path or one recursive run at the root filtered later. Exit code 1 means vulnerabilities were found [raw/deps--osv-scanner-usage.md].
   - Go call analysis is on by default. Add `--call-analysis=rust` only if cargo is available and compiling in the copy is acceptable.
   - Without network: use offline databases if they were downloaded earlier, otherwise drop to rung 2 and record the cap. Maven transitive resolution is off offline [raw/deps--osv-scanner-supported-lockfiles.md].
3. **Fill the gaps with ecosystem tools** for anything osv-scanner cannot read (see the coverage map in dependency-triage.md section 1): `npm audit`, `pip-audit`, `govulncheck`, `cargo audit`, `bundle-audit`, `composer audit`, `dotnet package list --vulnerable`. Use the exact commands in tool-commands.md; `govulncheck` and `dotnet package list` load or evaluate project code, so run them only when `intake.json.execution.allowed` is true (tool-commands.md rule 2) [raw/deps--pip-audit.md] [raw/deps--cargo-audit.md].
4. **Triage every advisory** with dependency-triage.md section 2: scope, production or dev, reachability, fix version, grouping, severity mapping, and no invented ids.
5. **Reachability is the noise filter.** Go: trust govulncheck's called or not called. Others: search for the vulnerable function or feature named in the advisory; read the call site. Unknown reachability caps the finding at `medium` with `possible` [raw/deps--govulncheck.md].
6. **Supply-chain hygiene** checks from dependency-triage.md section 4, including suspicious or non-existent package names (see guide 13) [raw/ai--csa-slopsquatting-2026.md].
7. **Write findings**: one per package and fixed version, all advisory ids in `refs`, the tool output line in `evidence` (cite the raw file), and the upgrade command or manifest edit in `remediation`.
8. **Record measures**: `dep_vulns_total` (all advisories after scoping), `dep_vulns_reachable` (production and reachable or unknown), `dep_lockfiles_missing`, with tool versions as `source`. Record every ecosystem that no tool could audit in `coverage.caps`.

## Done when

Every lockfile in scope was scanned by at least one tool or has a cap, every advisory was triaged, and the measures and caps are written.

## Sources

[raw/deps--osv-scanner-usage.md], [raw/deps--osv-scanner-supported-lockfiles.md], [raw/deps--npm-audit.md], [raw/deps--pip-audit.md], [raw/deps--govulncheck.md], [raw/deps--cargo-audit.md], [raw/deps--bundler-audit.md], [raw/deps--composer-audit.md], [raw/deps--dotnet-package-list.md], [raw/ai--csa-slopsquatting-2026.md]
