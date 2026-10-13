# 03. Size and line counts with cloc or scc

Goal: a code-only line count for the core, the share of code living in files over 1,000 lines, and the largest files.

Loads: [../references/tool-commands.md](../references/tool-commands.md) (Line counts), [../references/bands.md](../references/bands.md), `../scripts/size_profile.py`.

## 1. Pick the counter

| Counter | Use when | How to run without a global install | Caps to record |
| --- | --- | --- | --- |
| cloc 2.10 | Perl is available; the reference audit used cloc for core code lines | upstream release script, or a system cloc. `npx cloc` works but runs the older 2.06 from the npm wrapper (`2.6.0-cloc`), and still needs Perl | identical files counted once unless `--skip-uniqueness`; files over 100 MB skipped (`--max-file-size`) |
| scc 4.1.0 | faster, single binary, no Perl | download the release tarball for the OS into `.scratch/tools/`, verify against `checksums.txt` | large-file caps only with `--no-large`; duplicate files kept unless `-d` |
| `size_profile.py --root` | neither tool can run | built in | no comment detection: "code" means non-blank lines; say so |

Sources: [../references/research/raw/cloc--readme-and-cli-help.md] [../references/research/raw/scc--readme-and-cli-help.md].

## 2. Count by file

1. Run the counter on the copy with `--by-file` and JSON output, excluding the same folders as the scope. The copy made with `git archive` has no `.git`, so do not use cloc's `--vcs=git`; the archive already left out gitignored files.
2. Pass `--skip-uniqueness` to cloc so a copied file counts every time. A repo with whole-file copies is otherwise undercounted, which hides exactly the bloat you are measuring. Record it in `coverage.caps`.
3. Save to `raw/cloc-by-file.json` or `raw/scc-by-file.json`, and the version to `raw/versions.txt`.

## 3. Profile

Run `scripts/size_profile.py` with `--cloc` or `--scc`, `--strip-prefix` if paths carry the copy's folder, the scope's `--exclude` globs, `--include-lang` with the languages in scope (or rely on the default `--exclude-lang`, which drops Markdown, JSON, text, YAML and other prose and data formats that cloc and scc also count), `--threshold 1000`, your areas, and `--json-out raw/size-profile.json`.

It reports:

- total files, code lines, physical lines
- files over the threshold and the share of code in them, by code lines and by physical lines (the threshold is applied to physical lines, the length a reader sees)
- the largest files
- per area: code lines and the share in big files

The headline measure is `big_file_share`: share of core code lines in files over 1,000 lines. Write the core code-line total in `notes.md`; it is a count, not a banded measure.

## 4. Reconcile with jscpd

jscpd counts raw lines including comments and blanks; cloc counts code only. They compare only roughly (WHIPT: 1.08M raw lines in the duplication scope, 977K core code lines) [../references/research/raw/gold--whipt-bloat-audit-method.md]. Put that footnote in `notes.md`. Use cloc or scc code lines as the denominator for the dead-code percentage (guide 05) and for `big_file_share`; use jscpd's own lines for the duplication percentages.

If the file sets differ by more than a few percent, the scopes drifted. Fix the excludes, do not explain it away.

## 5. Band and record

Band `big_file_share` with [../references/bands.md](../references/bands.md): under 15% healthy, over 30% bloated (heuristic), mapped to the contract scale. Raise `BLOAT-SIZE-NNN` findings for single files that are far beyond the rest (guide 04 decides how to split them; this guide only measures).

## Sources

- [../references/research/raw/cloc--readme-and-cli-help.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/cloc--readme-and-cli-help.md)
- [../references/research/raw/scc--readme-and-cli-help.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/scc--readme-and-cli-help.md)
- [../references/research/raw/gold--whipt-bloat-audit-method.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/gold--whipt-bloat-audit-method.md)
