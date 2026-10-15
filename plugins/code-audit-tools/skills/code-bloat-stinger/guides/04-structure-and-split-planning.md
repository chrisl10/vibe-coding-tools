# 04. Structure and split planning

Goal: show the shape of the code (where it piles up, how big single functions get, which files are one giant closure) and give a split plan for the largest files that a team could follow.

Loads: [../references/tool-commands.md](../references/tool-commands.md) (Function size), [../references/output-templates.md](../references/output-templates.md), `../scripts/function_profile.py`, `raw/size-profile.json` from guide 03, `raw/jscpd-*/recount.json` from guide 01.

## 1. Measure functions

1. Run lizard 1.24.0 from the scratch venv on the copy, with `--csv`, the languages in scope (`-l typescript -l tsx -l javascript`, or `-l python`, `-l go`, `-l rust`), and excludes for generated and vendor folders. Run it single-threaded: a `-t 4` run hung on macOS in testing while the plain run finished in seconds; if you try `-t` and nothing prints within a minute, kill it and rerun without. Save to `raw/lizard.csv` [../references/research/raw/lizard--readme-and-csv-test.md (source-repository research, not shipped)].
2. Run `scripts/function_profile.py --lizard-csv raw/lizard.csv --strip-prefix <copy> --closure-min 1000 --json-out raw/functions.json`. For JS and TS always add `--cross-check <copy>`: on a real tree lizard overstated four of the five largest JavaScript function spans (for example 233 lines for a 16-line function next to regex literals), while the brace-matching heuristic matched the real span [../references/research/raw/lizard--readme-and-csv-test.md (source-repository research, not shipped)]. Every WARNING it prints means: read the file to the closing brace and use the real end line.
3. Without lizard (no Python venv possible), run `function_profile.py --heuristic <copy>` for JS and TS only. Label every number from it "heuristic". It is approximate too: a type annotation with braces before the body, or unusual syntax, can shift a span.

Why lizard, despite that: it covers about 27 languages, reports nested and arrow functions as their own rows, and its `start`-`end` span for an outer function includes the inner ones. So the span measures a closure's size and the rows inside it are its inner functions [../references/research/raw/lizard--readme-and-csv-test.md (source-repository research, not shipped)].

The script reports:

- largest functions by span (record the top one as `largest_function_lines`, with the name in the label)
- closure factories: outermost functions over 1,000 lines that contain other functions, with the count of inner functions and the largest inner ones

## 2. Describe the shape of each large file

For the five to eight largest files (from `size-profile.json`), read the file's outline yourself. Do not split from numbers alone.

1. List the top-level structure: module helpers, then a factory, a router, a schema block, a class.
2. If a factory closure holds most of the file, write: "helpers, then a N-line closure with M inner functions", and name the two or three largest inner functions with their sizes. This is the WHIPT shape: four services were single closures of 5K to 19K lines, one with 179 inner functions and a 5,527-line function inside [../references/research/raw/gold--whipt-bloat-audit-method.md (source-repository research, not shipped)].
3. Note pure data files (schemas, OpenAPI specs, route tables). They are easy to split and low risk.
4. Note files that already use separate top-level functions. They split by moving code only.
5. Pull each file's duplication at 50 and 100 tokens from the recount. A high figure that drops at 100 tokens points at a helper that would absorb short repeated snippets (for example a shared "load the record and check access" helper in a route file).

## 3. Write the split plan

One row per large file:

| Column | How to fill it |
| --- | --- |
| File, lines | from the size profile |
| Shape | one sentence from step 2 |
| Modules | estimated number of modules after the split: count the concerns you listed. Give a range (for example 22 to 26) |
| Risk | Very low (pure data), Low (already separate functions, or a route file where each handler is independent), Medium (one closure with moderate shared state), Med-high (a large closure with heavy shared state and very large inner functions) |

Then per file, the module list by concern (for example: OAuth start and refresh; connection lifecycle; gallery catalog and preflight; grants and tokens).

Then the total: "about X to Y modules, averaging A to B lines each". If the average is still over 1,000, say so: splitting alone does not finish the job.

## 4. The context-object step for closures

A factory closure cannot be split by moving functions, because every inner function reads and writes state captured from the closure. State this step explicitly in the plan, as WHIPT does:

1. First, mechanically pass the captured state as one explicit context object (for example `ctx` with the database handle, config, caches, and mutable counters) to each inner function, still in the same file. This is the step that carries the risk; it touches every function and needs tests or careful review.
2. Then move functions into modules grouped by concern, importing what they need and taking `ctx`. This part is moving code.
3. Split the largest inner function into phase functions last (for example prepare, resolve, invoke, finalize, follow-ups), each taking `ctx`.

Without step 1, any estimate of how easily the file splits is wrong.

## 5. Record

- Measures: `largest_function_lines`. The share in big files comes from guide 03.
- Findings (all `medium`, effort `L`, unless smaller): `BLOAT-SIZE-NNN` for each function over 1,000 lines and each file far past the rest; `BLOAT-STRUCT-NNN` for closure factories over 5,000 lines and for files that mix unrelated concerns. Put lizard's row or the script's output in `evidence`; put "read the closure start and confirmed inner functions use captured state" in `verified_by`.
- `notes.md` section 3: the split table, per-file module lists, the context-object note, and any question you could not check (for example "not checked: whether these schemas repeat the shared validators").

## Sources

The notes listed below are source-repository research, not shipped.

- ../references/research/raw/lizard--readme-and-csv-test.md (source-repository research, not shipped)
- ../references/research/raw/gold--whipt-bloat-audit-method.md (source-repository research, not shipped)
- ../references/research/raw/research--arxiv-2603-27130-ai-vs-human-duplication.md (source-repository research, not shipped)
