# knip false-positive classes and how to test each one

Before calling a flagged item dead, test it against every class below. Each test is a read-only search in the throwaway copy (`COPY`). Replace `NAME` with the file's base name without extension, or the export or dependency name.

Sources: [research/raw/gold--whipt-bloat-audit-method.md] [research/raw/knip--cli-help-and-fixture-test.md] [research/raw/knip--entry-files.md] [research/raw/knip--handling-issues.md] [research/raw/knip--source-mapping.md].

| # | Class | Test | Verdict if the test hits |
| --- | --- | --- | --- |
| 1 | Package `exports`, `main` or `types` pointing at `dist/` that knip did not map to source | `rg -n '"(exports|main|module|types)"' COPY/<ws>/package.json -A12` then check `tsconfig.json` for `outDir`; look for a consumer importing the package subpath: `rg -n "from ['\"]<pkg-name>(/|['\"])" COPY` | False alarm. If one workspace has many flagged files, this is usually why |
| 2 | Service worker or worklet registered by string | `rg -n "serviceWorker\.register\|audioWorklet\.addModule\|paintWorklet\|importScripts\(" COPY` and look for `NAME` | False alarm |
| 3 | Entry of a separate build (second Vite, Rollup, esbuild, tsup or webpack config, preview build, Storybook) | `rg -n --glob '*{vite,rollup,tsup,webpack,esbuild}*.config.*' "NAME" COPY`; `rg -n "input:\|entry:\|entryPoints" COPY --glob '*.config.*'` | False alarm |
| 4 | `bin` entry or published CLI | `rg -n '"bin"' -A6 COPY/**/package.json` | False alarm |
| 5 | Script run from `package.json`, a Makefile, a CI workflow, a git hook | `rg -n "NAME" COPY --glob 'package.json' --glob 'Makefile' --glob '.github/workflows/*' --glob '.husky/*' --glob 'justfile'` | False alarm (live script) or Dead (one-off codemod never run again: check the commit message and age) |
| 6 | CLI spawned by name (a dependency used as a binary, often agent or tool CLIs) | `rg -n "spawn\|execa\|exec(File)?\(\|\\$\`" COPY` near the dependency name | False alarm for the dependency |
| 7 | File or dependency used only by tests | `rg -ln "NAME" COPY \| rg -i "test\|spec\|e2e\|fixture"` returns the only hits | Partial: production-dead, move to devDependencies or test helpers |
| 8 | Dependency belongs to another workspace | `rg -ln "from ['\"]DEP" COPY` shows imports only in a different workspace | Partial: listed in the wrong package.json |
| 9 | Disabled plugin artifacts | the flagged file is the config of a plugin you turned off, or the flagged package is that plugin's tool | False alarm, caused by the workaround |
| 10 | Dynamic import with a template string or computed path | `rg -n "import\(\`\|require\(\`\|import\([a-zA-Z_]" COPY` | Possibly live; mark Partial unless the computed path cannot reach the file |
| 11 | Framework convention (file-based routing, auto-imports, auto-mocks, migrations, generated route trees) | the file sits under `app/`, `pages/`, `routes/`, `migrations/`, `__mocks__/`, or a generated file is missing | False alarm when the convention loads it |
| 12 | Asset or stylesheet exported from a package and imported by examples or consumers | `rg -n "NAME\.(css\|scss)" COPY`; check `exports` for `./styles.css` | False alarm |
| 13 | Barrel re-export with no importers | `rg -n "from ['\"].*/(index\|NAME)['\"]" COPY` returns nothing | Dead: but the files it re-exports may still be live |
| 14 | Export used only inside its own file | `knip_summarize.py` counts these; confirm with `rg -c "\bNAME\b" <file>` greater than 1 | Partial: drop the `export` keyword, keep the code |
| 15 | Native addon or generated file in "unresolved imports" (`.node`, `.wasm`, codegen output) | the extension or a build step produces it | False alarm for the import |
| 16 | Standalone CLI run by hand, documented in a README, guide or runbook (`node scripts/x.mjs`, `python tools/y.py`) but not in any package script | `rg -n "NAME\.(mjs\|js\|ts\|py)" COPY --glob '*.md' --glob '*.mdx' --glob '*.txt'` | False alarm when the docs tell people to run it; Dead when no doc, script, or workflow mentions it |

A finding is **Dead** only when every applicable test misses and you searched for the name across the whole copy, including non-code files (`rg -n NAME COPY` with no type filter, then read each hit).

A finding is **Partial** when the code is live in some way but misplaced (tests-only, wrong workspace, exported but used only in its file).

Record the reason in plain words, as the WHIPT report does: "Barrel re-export with no importers (44 lines)", "Service worker registered by string", "Reached through package exports to dist/; knip missed the mapping".
