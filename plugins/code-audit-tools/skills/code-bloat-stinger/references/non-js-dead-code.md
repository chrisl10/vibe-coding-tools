# Dead code and unused dependencies outside JavaScript and TypeScript

jscpd covers 224 languages, so duplication works everywhere [research/raw/jscpd--homepage.md]. cloc, scc and lizard work everywhere too. Only the dead-code step changes per ecosystem.

| Ecosystem | Detect by | Tool and command | What it finds | Honest limits | Source |
| --- | --- | --- | --- | --- | --- |
| Python | `pyproject.toml`, `setup.py`, `requirements*.txt` | vulture 2.16 in a scratch venv: `vulture COPY --min-confidence 80 --sort-by-size` | unused imports (90%), functions, classes, variables (60%), unreachable code (100%) | code called implicitly (framework hooks, decorators) is reported as unused; the README's example fix is `--ignore-decorators "@app.route"` for Flask; sample heavily | [research/raw/vulture--readme.md] |
| Python, JS, TS | any | jscpd 5 `--dead-code` | unused files, exports, symbols, imports | new feature, accuracy not verified in this sweep; use as a second opinion only | [research/raw/jscpd--v5-readme-and-cli-help.md] |
| Go program (has `package main`) | `go.mod` | `go run golang.org/x/tools/cmd/deadcode@latest ./...` | functions unreachable from any `main`, exported included | no roots in a library-only module; `-whylive=<func>` explains why a function is live | [research/raw/go--deadcode-blog-and-test.md] |
| Go any | `go.mod` | `go run honnef.co/go/tools/cmd/staticcheck@2026.2.1 -checks U1000 ./...` | unused unexported identifiers | exported identifiers are not reported | [research/raw/go--staticcheck-u1000-test.md] |
| Rust dependencies | `Cargo.toml` | cargo-machete 0.9.2 | unused dependencies, fast | build.rs-generated use and renamed crates give false positives; `--with-metadata` may rewrite `Cargo.lock`, so only in the copy | [research/raw/rust--cargo-machete-readme.md] |
| Rust dependencies | `Cargo.toml` | `cargo +nightly udeps` | unused dependencies via a real build | needs nightly and a working build; misses some | [research/raw/rust--cargo-udeps-readme.md] |
| Rust code | `Cargo.toml` | `cargo check --message-format=json` in the copy, count `dead_code` warnings (jscpd 5 `--rust-diagnostics` reads the same file) | unused functions, structs, fields | needs a working build in the copy | [research/raw/rust--cargo-udeps-readme.md] [research/raw/jscpd--v5-readme-and-cli-help.md] |
| Java, Kotlin, C#, Ruby, PHP, Swift, others | build files | no tool verified in this research window | | Say so in `notes.md` and `coverage.skipped`: "dead-code step not run: no verified tool for <language>". Report duplication and size only. Set the dead-code measure band to `not-run`. Do not guess a percentage | none (thin spot) |

## Turning output into a "truly dead" estimate

1. Count flagged lines: for each flagged function or file, take its line span (vulture prints line numbers; deadcode prints `file:line`; read the function to its end).
2. Spot-check at least 12 items across categories (guide 05).
3. Apply the per-bucket dead ratio from the spot-check to that bucket's flagged lines.
4. Divide by core code lines from cloc or scc.

For Python, sample at least 20 items (a design choice of this skill): Vulture's own README warns that implicitly called code is reported as unused and that confidence values below 100% are very rough [research/raw/vulture--readme.md].
