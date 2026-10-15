# Tool commands

Copy-ready commands for every step. They are bash: on macOS and Linux run them as written; on Windows run them in Git Bash or WSL (PowerShell and cmd cannot run them). The copy and the Python helpers (`make_scratch_copy.py`, `size_profile.py`, `function_profile.py`, and the others in `scripts/`) are plain Python and run anywhere. Variables:

- `WS`: the run workspace, for example `<parent>/<repo>-code-audit/2026-09-30-vibe`
- `COPY`: `$WS/.scratch/repo-copy` (the throwaway copy, never the audited repo)
- `TOOLS`: `$WS/.scratch/tools` (where tools are installed, outside the copy)
- `RAW`: `$WS/01-bloat/raw`
- `SKILL_DIR`: this skill's folder

## Two rules for every command below

1. **Clean environment.** Run every tool with `"${SAFE_ENV[@]}"` in front, so nothing the tool or the repository runs can read the user's credentials (`GITHUB_TOKEN`, `AWS_*`, API keys, `NPM_TOKEN`):

   ```bash
   mkdir -p "$WS/.scratch/home" "$WS/.scratch/tmp"
   SAFE_ENV=(env -i PATH="$PATH" HOME="$WS/.scratch/home" TMPDIR="$WS/.scratch/tmp" LANG="${LANG:-C.UTF-8}" CI=1)
   # Git Bash on Windows: Node, Python and Go fail without these system variables, which hold no credentials.
   [ -n "${SYSTEMROOT:-}" ] && SAFE_ENV+=(SYSTEMROOT="$SYSTEMROOT" COMSPEC="${COMSPEC:-}" PATHEXT="${PATHEXT:-}" TEMP="$WS/.scratch/tmp" TMP="$WS/.scratch/tmp")
   ```

2. **Consent before repository code runs.** jscpd, cloc, scc, lizard, vulture, and cargo-machete only read files. knip loads the project's own config files (`vitest.config.ts`, `playwright.config.ts`, `next.config.js`, and others) by executing them, installing dependencies runs package code, and `cargo check` runs `build.rs`. Run those only when `intake.json.execution.allowed` is true, in the consented mode (`container`: if knip plugins need the copy's dependencies, install them first in a container with network and scripts off, as in the contract's two-phase container mode; then run `docker run --rm --network none -v "$COPY":/w -v "$TOOLS":/tools -w /w node:<exact version> node /tools/node_modules/knip/bin/knip.js ...`; `host`: the commands below with `SAFE_ENV`). Use an exact image tag that matches the repository's runtime (from `.nvmrc`, `engines`, or `.tool-versions`, for example `node:22.12.0`), never a floating major tag, and record it in `raw/versions.txt`. When it is false, skip them and record the cap "unused-code analysis not run: knip executes the project's config files and the user declined code execution", with dead-code measures set to `not-run`.

Pin exact versions and record them. Versions below were current on 2026-09-30 [research/raw/jscpd--npm-release-timeline.md] [research/raw/knip--cli-help-and-fixture-test.md].

## Setup (guide 00)

```bash
mkdir -p "$WS/.scratch" "$TOOLS" "$RAW"
# Throwaway copy (usually already made by the orchestrator): git archive, never writes to the audited repo's .git
[ -d "$COPY" ] || python3 "<audit-my-code-stinger>/scripts/make_scratch_copy.py" "<repo>" "$COPY"
git -C "<repo>" rev-parse HEAD > "$RAW/sha.txt"
# Tools live outside the copy so the copy's package.json is untouched
cd "$TOOLS" && npm init -y >/dev/null && "${SAFE_ENV[@]}" npm i --ignore-scripts --no-audit --no-fund jscpd@5.4.0 knip@6.39.0
(cd "$TOOLS" && "${SAFE_ENV[@]}" npx jscpd --version && "${SAFE_ENV[@]}" npx knip --version && node --version) > "$RAW/versions.txt"
```

If the copy needs dependencies for knip plugins, and only when `execution.allowed` is true, install inside the copy with lifecycle scripts off, and record it in `coverage.caps`:

```bash
cd "$COPY" && "${SAFE_ENV[@]}" pnpm install --frozen-lockfile --ignore-scripts   # or: npm ci --ignore-scripts / yarn install --immutable --mode=skip-build
```

## Duplication (guide 01)

Exclusions are passed with `--ignore`, comma-separated, whole-path globs [research/raw/jscpd--v5-readme-and-cli-help.md]. Build one list and reuse it for every tool.

```bash
IGN='**/node_modules/**,**/dist/**,**/build/**,**/vendor/**,**/*.d.ts,**/*.min.js,**/generated/**,**/__snapshots__/**,**/fixtures/**,**/*.test.*,**/*.spec.*,**/e2e/**'
FMT='typescript,tsx,javascript,jsx'
cd "$TOOLS"
# jscpd 5.x: lift the 1 MB per-file size cap
"${SAFE_ENV[@]}" npx jscpd "$COPY" --format "$FMT" --ignore "$IGN" --min-tokens 50  --max-size 100mb --reporters json --output "$RAW/jscpd-50"  --silent
"${SAFE_ENV[@]}" npx jscpd "$COPY" --format "$FMT" --ignore "$IGN" --min-tokens 100 --max-size 100mb --reporters json --output "$RAW/jscpd-100" --silent
# Coverage pass: at --min-tokens 1 every in-scope file is counted, so sources must equal the file list
"${SAFE_ENV[@]}" npx jscpd "$COPY" --format "$FMT" --ignore "$IGN" --min-tokens 1   --max-size 100mb --reporters json --output "$RAW/jscpd-coverage" --silent
# jscpd 4.x instead: lift both caps
# npx jscpd@4.3.0 "$COPY" ... --max-lines 1000000 --max-size 100mb ...
```

List the supported format names with `npx jscpd --list`. For a non-JS repo pick the formats you scan, for example `python`, `go`, `rust`.

Recount (both copies, per area, big versus small, top pairs):

```bash
python3 "$SKILL_DIR/scripts/jscpd_recount.py" --report "$RAW/jscpd-50/jscpd-report.json" \
  --coverage-report "$RAW/jscpd-coverage/jscpd-report.json" --root "$COPY" \
  --ext ts,tsx,js,jsx,mjs,cjs --exclude '**/node_modules/**' --exclude '**/dist/**' ... \
  --area-depth 2 --area 'packages/adapters/*' --big-lines 1000 --top 20 --json-out "$RAW/jscpd-50/recount.json"
```

Repeat for `jscpd-100`. Use one `--exclude` per glob in `IGN`.

## Unused code (guide 02)

```bash
mkdir -p "$WS/.scratch/knip"
# Only if a plugin config throws: disable that plugin from OUTSIDE the repo
cat > "$WS/.scratch/knip/knip.json" <<'JSON'
{"$schema": "https://unpkg.com/knip@6/schema.json",
 "workspaces": {".": {"playwright": false}}}
JSON
# Only when execution.allowed is true (knip runs the project's config files):
cd "$TOOLS"
"${SAFE_ENV[@]}" npx knip -D "$COPY" --reporter json --no-progress --no-exit-code > "$RAW/knip.json" 2> "$RAW/knip.stderr"; echo "exit $?" >> "$RAW/knip.stderr"
"${SAFE_ENV[@]}" npx knip -D "$COPY" -c "$WS/.scratch/knip/knip.json" --reporter json --no-progress --no-exit-code > "$RAW/knip.json" 2> "$RAW/knip.stderr"
"${SAFE_ENV[@]}" npx knip -D "$COPY" -c "$WS/.scratch/knip/knip.json" --production --reporter json --no-progress --no-exit-code > "$RAW/knip-production.json" 2>> "$RAW/knip.stderr"
"${SAFE_ENV[@]}" npx knip -D "$COPY" --debug > "$RAW/knip-debug.txt" 2>&1   # workspaces, enabled plugins, source mapping
```

Workspaces declared in `package.json` or `pnpm-workspace.yaml` are still analyzed when the external config names only `"."`; config entries add to them [research/raw/knip--configuration-reference.md] [research/raw/knip--cli-help-and-fixture-test.md]. To disable a plugin in one workspace only, key it by that workspace directory instead of `"."`. Exit code 2 means a config failed to load and the JSON is incomplete [research/raw/knip--known-issues.md]. Never pass `--fix` or `--allow-remove-files`.

```bash
python3 "$SKILL_DIR/scripts/knip_summarize.py" --report "$RAW/knip.json" --root "$COPY" \
  --exclude '**/vendor/**' --exclude '**/fixtures/**' --exclude '**/examples/**' --exclude '**/*.test.*' \
  --sample 16 --json-out "$RAW/knip-summary.json" --sample-out "$RAW/spot-check.md"
```

## Line counts (guide 03)

```bash
# cloc (preferred for code-only counts). Needs Perl. --skip-uniqueness so copied files count every time.
cloc --version > "$RAW/cloc-version.txt"
# The git-archive copy has no .git, so cloc walks the folder; the archive already left out gitignored files.
cd "$COPY" && cloc --by-file --json --quiet --skip-uniqueness --exclude-dir=vendor,dist,node_modules,build . > "$RAW/cloc-by-file.json"
# scc (faster, single binary; download into the scratch folder)
SCC_ASSET=scc_Linux_x86_64.tar.gz   # pick the asset for the OS
curl -fsSL -o "$TOOLS/$SCC_ASSET" "https://github.com/boyter/scc/releases/download/v4.1.0/$SCC_ASSET"
curl -fsSL -o "$TOOLS/checksums.txt" "https://github.com/boyter/scc/releases/download/v4.1.0/checksums.txt"
(cd "$TOOLS" && shasum -a 256 -c --ignore-missing checksums.txt) && tar -xzf "$TOOLS/$SCC_ASSET" -C "$TOOLS" scc   # extract only after the checksum passes
"${SAFE_ENV[@]}" "$TOOLS/scc" --by-file -f json --exclude-dir .git,node_modules,dist,vendor "$COPY" > "$RAW/scc-by-file.json"
python3 "$SKILL_DIR/scripts/size_profile.py" --cloc "$RAW/cloc-by-file.json" --threshold 1000 --area-depth 2 --top 20 --json-out "$RAW/size-profile.json"
# no tool available:
python3 "$SKILL_DIR/scripts/size_profile.py" --root "$COPY" --exclude '**/vendor/**' --json-out "$RAW/size-profile.json"
```

The commands above verify the scc archive against the release's `checksums.txt` before extracting it; never skip that step [research/raw/scc--readme-and-cli-help.md].

## Function size (guide 04)

```bash
python3 -m venv "$WS/.scratch/venv"
VENV_BIN="$WS/.scratch/venv/bin"; [ -d "$WS/.scratch/venv/Scripts" ] && VENV_BIN="$WS/.scratch/venv/Scripts"   # Windows venvs use Scripts/
"$VENV_BIN/pip" -q install lizard==1.24.0
"${SAFE_ENV[@]}" "$VENV_BIN/lizard" --csv -l typescript -l tsx -l javascript -x "*/node_modules/*" -x "*/dist/*" "$COPY" > "$RAW/lizard.csv"
python3 "$SKILL_DIR/scripts/function_profile.py" --lizard-csv "$RAW/lizard.csv" --strip-prefix "$COPY" --cross-check "$COPY" \
  --exclude '**/node_modules/**' --top 20 --closure-min 1000 --json-out "$RAW/functions.json"   # --cross-check for JS/TS
# fallback for JS/TS without lizard (label as heuristic):
python3 "$SKILL_DIR/scripts/function_profile.py" --heuristic "$COPY" --exclude '**/node_modules/**' --json-out "$RAW/functions.json"
```

## Non-JS dead code (guide 02, section 6)

```bash
"$VENV_BIN/pip" -q install vulture==2.16   # VENV_BIN as set in the function-size block
"${SAFE_ENV[@]}" "$VENV_BIN/vulture" "$COPY" --min-confidence 80 --sort-by-size --exclude "*/.venv/*,*/tests/*" > "$RAW/vulture.txt"
cd "$COPY" && "${SAFE_ENV[@]}" GOPATH="$WS/.scratch/gopath" GOCACHE="$WS/.scratch/gocache" go run golang.org/x/tools/cmd/deadcode@v0.50.0 ./... > "$RAW/deadcode.txt"
cd "$COPY" && "${SAFE_ENV[@]}" GOPATH="$WS/.scratch/gopath" GOCACHE="$WS/.scratch/gocache" go run honnef.co/go/tools/cmd/staticcheck@2026.2.1 -checks U1000 ./... > "$RAW/staticcheck-u1000.txt"
"${SAFE_ENV[@]}" CARGO_HOME="$WS/.scratch/cargo" cargo install --locked cargo-machete --version 0.9.2 && cd "$COPY" && "${SAFE_ENV[@]}" "$WS/.scratch/cargo/bin/cargo-machete" > "$RAW/cargo-machete.txt"
# Only when execution.allowed is true: cargo check compiles the crate and runs its build.rs.
cd "$COPY" && "${SAFE_ENV[@]}" CARGO_HOME="$WS/.scratch/cargo" cargo check --message-format=json > "$RAW/cargo-check.json"   # dead_code warnings
```

## Contract check (guide 06)

```bash
python3 "$SKILL_DIR/scripts/validate_outputs.py" --dir "$WS/01-bloat"
```

## Cleanup

```bash
rm -rf "$WS/.scratch"    # only after every raw artifact you cite is in $RAW
```
