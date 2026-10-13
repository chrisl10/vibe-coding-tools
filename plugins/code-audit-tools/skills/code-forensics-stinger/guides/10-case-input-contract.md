# Explicit case document contract

The five Node builders use the same schema. `templates/case-facts-schema.json` mirrors the runtime validator in `scripts/case-input.js`; the runtime adds date validity, unique evidence IDs, known source references, table-width and total-block checks. No default case, party, amount or text is injected.

Required root keys: `schema_version: 1`, `matter`, explicit boolean `fictional`, `evidence`, and `documents`. Unknown keys are refused. Input is a regular UTF-8 JSON file no larger than 2 MiB. Symlinks and parent traversal are refused, apart from documented macOS system aliases. Source URIs are labels, never opened or fetched.

`matter` requires `id`, `title`, `client`, `prepared_by` and real ISO `report_date`. The ID is lowercase words/numbers separated by hyphens and forms the output filename. Evidence entries require unique `id`, `title`, `uri`.

`documents` contains one or more of `master`, `agency`, `attorney`, `plain_language`, `pre_litigation`. Each requires `title` and nonempty `sections`. Each section has `title` and nonempty `blocks`. Blocks use `paragraph`/`text`, `bullets`/`items`, or `table`/`headers`/`rows` plus `tier`, `source_ids` and optional boolean `estimate`. Source IDs must exist in the evidence register. PROVEN and DERIVED require at least one source; HYPOTHESIS may have none. Estimates cannot be PROVEN.

The renderer labels every block and appends the supplied evidence register. Fictional examples carry a training notice. Attorney and pre-litigation outputs carry a human/counsel-review notice and state that no legal conclusion or privilege is established. Supplied narrative still requires review; structural validation cannot certify truth or prevent an author from writing an unsupported assertion.

Run from any working directory:

```bash
node /path/to/skill/scripts/build_master_report.js --case-facts /path/to/case-facts.json --out-dir /path/to/private/revision-1
node /path/to/skill/scripts/build_master_report.js --case-facts /path/to/case-facts.json --out-dir /path/to/private/markdown-1 --format markdown
```

Success prints one JSON object with `kind`, `format`, `output`, `fictional`. Failure prints `Case document refused: ...` to stderr and exits 1. It refuses an existing destination, including a symlink. New directories use mode 0700 and files 0600. Existing output directories must be user-owned mode 0700; unsafe directories are refused without changing their permissions. Writes use a random exclusive temporary file and atomic no-overwrite publication. Run in a private workspace whose directories cannot be renamed by an untrusted local process; portable path checks are not a sandbox against a concurrent privileged filesystem actor.

Python investigation helpers retain their own intermediate formats. Review them, then author this input explicitly. No automatic conversion from old accumulators exists, and no missing field is silently filled with a retained matter's data.

## Python helper output policy

All six Python output helpers share `scripts/private_output.py`. They require POSIX directory-descriptor support. Select a fresh private output directory, or an existing directory owned by the current user with mode 0700. They never chmod existing user directories or overwrite output files. Each batch checks all known destinations first, then writes mode-0600 temporary files and publishes no-clobber links through checked directory handles. A pre-existing collision refuses before any batch file is written. Revisions require a new directory. The ZIP helper preserves its source/member symlink checks and publishes from an in-memory ZIP buffer.
