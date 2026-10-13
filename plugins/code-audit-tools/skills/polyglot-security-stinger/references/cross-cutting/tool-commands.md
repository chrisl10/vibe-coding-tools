# Tool commands, pins, and the fallback ladder

Every guide loads this file. It defines the shared `$RG` search helper, the throwaway copy, the exact tool commands with pinned versions, and what to record when a tool cannot run.

## 1. Ground rules

1. Never run a tool against the audited repository itself. Run it in `<workspace>/.scratch/repo-copy/` as the contract requires (section 3 of the audit contract).
2. Never run a tool that executes or evaluates project code (installs with scripts, builds, `mvn`, `gradlew`, `cargo build`, `dotnet restore`, `dotnet package list` (it restores and evaluates MSBuild files), `govulncheck` (it loads the module and can honor its `toolchain` line), `pip-audit -r` without `--no-deps`, `composer` with plugins, `--call-analysis=rust`) unless `intake.json.execution.allowed` is true, the guide step says so, and the copy is the target, in the consented mode. When `allowed` is false, use osv-scanner on lockfiles and lockfile reading instead, and record the cap `<tool> not run: user declined code execution`. Run Go tools with `GOTOOLCHAIN=local`. Tool-driven resolution is recorded in the notes file.
3. Strip credentials before running anything: run tools with a minimal environment (`env -i PATH="$PATH" HOME="$SCRATCH_HOME"`), no cloud profiles, no `GITHUB_TOKEN`. Security tools were themselves supply-chain targets in 2026 (Trivy v0.69.4 and trivy-action tags, March 2026) [raw/ci--trivy-teampcp-compromise-2026.md].
4. Pin the version you run. The pins below are the latest releases on 2026-09-30 [raw/tools--version-pins-2026-09-30.md]. Do not use Trivy v0.69.4.
5. No tool may send the user's code or secrets to a third party without consent: Semgrep `--config auto` sends the project URL to the registry, so always name rulesets and pass `--metrics=off` [raw/sast--semgrep-cli.md]; trufflehog verification calls provider APIs with the found secret, so default to `--no-verification` [raw/secrets--trufflehog.md].
6. Save every raw output to `<workspace>/02-security/raw/polyglot/` and list it under `## Evidence` in the notes file (the orchestrator builds `evidence-index.md`). This Drone's own deliverables are `02-security/findings-polyglot-security-wasp-drone.jsonl`, `02-security/metrics-polyglot-security-wasp-drone.json`, and `02-security/notes-polyglot-security-wasp-drone.md` (per the arming line), so parallel security Drones never overwrite each other.
7. When a tool cannot run (no network, not installed, sandbox denies it), use the manual fallback named in the ladder and add one line to `metrics.json.coverage.caps`, for example: `"osv-scanner not run (no network); dependency audit used lockfile reading plus npm audit for apps/api only"`.

## 2. Setup

```bash
WS="<workspace>"                          # from intake.json.workspace
COPY="$WS/.scratch/repo-copy"
RAW="$WS/02-security/raw/polyglot"
mkdir -p "$RAW" "$WS/.scratch/home"
SCRATCH_HOME="$WS/.scratch/home"
# Copy creation is owned by the orchestrator (contract section 3: git archive, never git worktree add,
# which writes metadata into the audited repository's .git). If it is missing:
#   mkdir -p "$COPY" && git -C "<repo>" archive HEAD | tar -x -C "$COPY"
# The archive copy has no history. For history scans make a separate bare clone; cloning only reads the source:
HIST="$WS/.scratch/history.git"
#   git clone --bare --no-local --quiet "<repo>" "$HIST"
# Shared search helper used by every reference file:
rgs() { rg -n --no-heading -S --hidden \
  -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/.git/**' -g '!**/dist/**' \
  -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/venv/**' \
  -g '!**/*.min.js' -g '!**/*.map' "$@" < /dev/null; }
RG=rgs
# The < /dev/null matters: when stdin is a pipe (as in many agent shells), rg without a path
# argument searches stdin instead of the current folder and appears to hang.
```

Exit codes: 0 hits, 1 no hits, 2 an error or "No files were searched" (ripgrep 15 prints that when no file of the requested type exists in the path; it is not a failure, record "no <type> files" and move on). Run `$RG` from inside the stack path (`cd "$COPY/<path>"`) so hits are scoped and paths are repo-relative after you prefix the stack path. If `rg` is missing, use `grep -rnE` with `--exclude-dir` for the same folders and record the cap "ripgrep missing; grep -E used, PCRE patterns skipped".

Library names in the sink tables are search hints. A hit becomes a finding only after the call site is read and the value is traced to a source.

## 3. The ladder, by job

Try rows top to bottom. Stop at the first that runs.

### Ecosystem detection

| Step | Command | Notes |
| --- | --- | --- |
| 1 | read `intake.json.stacks` | The orchestrator already ran detection |
| 2 | `python3 "$SKILL_DIR/scripts/detect_ecosystems.py" "$COPY" > "$RAW/detect.json"` | Standard library only; never fails for lack of network |

### Secrets

| Step | Command | Network |
| --- | --- | --- |
| 1 | `go run github.com/zricethezav/gitleaks/v8@v8.30.1 git --redact --report-format json --report-path "$RAW/gitleaks-history.json" "$COPY"` | module download only |
| 1b | `go run github.com/zricethezav/gitleaks/v8@v8.30.1 dir --redact --report-format json --report-path "$RAW/gitleaks-tree.json" "$COPY"` | |
| 2 | `trufflehog git "file://$COPY" --no-verification --json > "$RAW/trufflehog.json"` (binary or `go run github.com/trufflesecurity/trufflehog/v3@v3.97.9`) | verification off |
| 3 | `python3 "$SKILL_DIR/scripts/secrets_fallback.py" "$COPY" --json "$RAW/secrets-tree.json"` and `python3 "$SKILL_DIR/scripts/secrets_fallback.py" "$HIST" --history --no-tree --json "$RAW/secrets-history.json"` | none |
| 4 | the manual `rg` sweep in [secrets-patterns.md](secrets-patterns.md) | none |

gitleaks exit code 1 means leaks found, not a crash; 126 is a bad flag [raw/secrets--gitleaks.md]. History mode needs git history and the `git archive` copy has none, so point `gitleaks git`, `trufflehog git`, and `secrets_fallback.py --history` at the bare clone `$HIST` (gitleaks: `gitleaks git --redact ... "$HIST"`; trufflehog: `trufflehog git "file://$HIST" --no-verification --json`). Never run them with the audited repository's own `.git` as the target. If the clone cannot be made, record the cap "git history not scanned".

### Dependency vulnerabilities

| Step | Command | Notes |
| --- | --- | --- |
| 1 | `go run github.com/google/osv-scanner/v2/cmd/osv-scanner@v2.6.0 scan -r --format json "$COPY" > "$RAW/osv.json"` | Exit 1 means vulnerabilities found. Go call analysis on by default [raw/deps--osv-scanner-usage.md] |
| 1b | add `--call-analysis=rust` only when cargo is installed and `execution.allowed` is true (it compiles the code) | experimental |
| 1c | offline: `osv-scanner scan --offline-vulnerabilities --download-offline-databases -r "$COPY"` once with network, then offline | pom.xml transitive resolution is off offline [raw/deps--osv-scanner-supported-lockfiles.md] |
| 2 node | `npm audit --omit=dev --json > "$RAW/npm-audit-<path>.json"` in each folder with package-lock.json | never `audit fix` [raw/deps--npm-audit.md] |
| 2 python | `pipx run --spec pip-audit==2.10.1 pip-audit --no-deps -r requirements.txt -f json` or `--locked .` | `-r` without `--no-deps` resolves like pip install [raw/deps--pip-audit.md] |
| 2 go | only when `execution.allowed`: `GOTOOLCHAIN=local go run golang.org/x/vuln/cmd/govulncheck@v1.8.0 -json ./...` | reachability built in; loads the module [raw/deps--govulncheck.md] |
| 2 rust | `cargo audit --file <path>/Cargo.lock --json` run from outside the project | avoids build scripts [raw/deps--cargo-audit.md] |
| 2 ruby | `bundle-audit check --update --format json --output "$RAW/bundle-audit.json"` | [raw/deps--bundler-audit.md] |
| 2 php | `composer audit --locked --format=json` | [raw/deps--composer-audit.md] |
| 2 dotnet | only when `execution.allowed`: `dotnet package list --vulnerable --include-transitive --format json` (SDK 10) or `dotnet list package ...` (SDK 9 or earlier) | restores packages [raw/deps--dotnet-package-list.md] |
| 3 | read lockfiles and list exact versions of framework packages; compare against advisories you can cite from the raw archive only | no invented CVEs |

### Static analysis

| Step | Command | Notes |
| --- | --- | --- |
| 1 | `pipx run --spec semgrep==1.178.0 semgrep scan --metrics=off --config p/security-audit --config p/secrets --config <ecosystem packs> --json --json-output="$RAW/semgrep.json" <paths>` | packs per [static-analysis-rulesets.md](static-analysis-rulesets.md) |
| 2 | `opengrep scan -f <local-rules-dir> --sarif-output="$RAW/opengrep.sarif" <paths>` (Opengrep v1.30.0) | runs Semgrep rules unchanged [raw/sast--opengrep.md] |
| 2 go | `go run github.com/securego/gosec/v2/cmd/gosec@v2.29.0 -fmt json -out "$RAW/gosec.json" ./...` | Go only [raw/go--gosec.md] |
| 3 | the `rg` patterns in each ecosystem reference | always run, even when 1 or 2 ran |

### CI/CD and infrastructure

| Step | Command | Notes |
| --- | --- | --- |
| 1 | `uvx zizmor@1.30.1 --offline --format json "$COPY/.github/workflows" > "$RAW/zizmor.json"` (or `pipx run --spec zizmor==1.30.1 zizmor ...`) | [raw/ci--zizmor-audits.md] |
| 2 | `trivy config --format json "$COPY" > "$RAW/trivy-config.json"` with Trivy v0.74.0 | downloads a checks bundle; never v0.69.4 [raw/infra--trivy-misconfiguration.md] |
| 3 | the `rg` patterns in [ci-cd-infra.md](ci-cd-infra.md) | always run |

## 4. Recording what ran

For each tool, add a `measures` entry or a `notes.md` line with: tool, exact version, command, exit code, output file, and duration. Example measure:

```json
{"key": "dep_vulns_osv", "label": "Known vulnerable packages (osv-scanner)", "value": 7, "unit": "packages", "band": "at-risk", "threshold": "0 healthy, any high or critical reachable at-risk", "source": "osv-scanner 2.6.0"}
```

Sources: [raw/tools--version-pins-2026-09-30.md], [raw/sast--semgrep-cli.md], [raw/sast--opengrep.md], [raw/secrets--gitleaks.md], [raw/secrets--trufflehog.md], [raw/deps--osv-scanner-usage.md], [raw/deps--osv-scanner-supported-lockfiles.md], [raw/ci--zizmor-audits.md], [raw/infra--trivy-misconfiguration.md], [raw/ci--trivy-teampcp-compromise-2026.md]
