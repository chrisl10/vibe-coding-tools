# Library Packets

Turn an accessible library into a source-grounded document set for founders, investors, sales, service, account managers and engineers. The evidence determines the breadth. Every selected document has Markdown, editable Word, PDF and citations.

## Start

Invoke `/library-packets` with the standalone Claude command installed, or use the installed plugin namespace, such as `/documentation-tools:library-packets`. In Codex desktop, select the installed `library-packets-stinger` or generated `source-command-library-packets` skill. Plain ChatGPT uses the [portable starter](references/chatgpt-starter.md) with uploaded skill/library files and available document tools. The [portability guide](guides/07-desktop-portability.md) describes the actual carriers and limits.

## Guide map

| Step | Guide | Result |
|---|---|---|
| 1 | [Intake](guides/01-intake-and-scope.md) | Reader, decision, source/status, privacy, research, brand and output answers |
| 2 | [Evidence](guides/02-read-and-map-evidence.md) | Inventory, source hashes, feature census and coverage/claim map |
| 3 | [Research and decisions](guides/03-research-and-decide.md) | Dated primary evidence, usable edges and concrete product gaps |
| 4 | [Writing](guides/04-write-for-the-reader.md) | Clear, cited audience manuscripts with public boundaries |
| 5 | [Build](guides/05-build-the-packet.md) | Markdown, Word, PDF and citations from one reviewed model |
| 6 | [Review](guides/06-review-and-deliver.md) | Every-page inspection tied to current artifact identities |
| 7 | [Desktop portability](guides/07-desktop-portability.md) | Tool detection and honest fallback when a capability is missing |

## References

- [Ten invocation questions](references/intake.md)
- [Evidence-driven document catalogue](references/document-catalogue.md)
- [Evidence and public publication rules](references/evidence-and-publication.md)
- [Brief template](references/brief-template.md) and [coverage CSV](references/coverage-template.csv)
- [Helper contract](scripts/README.md)
- [Domain research](references/research/distilled-library-packets.md) with original primary-source captures
- [Real footer asset provenance](assets/PROVENANCE.md)

## Branding and platform support

The footer reads "Prepared by Legion Code Inc." and the DOCX author is "Legion Code Inc." by default. To rebrand the text, pass `--prepared-by "Your Company"` (and optionally `--author "Name"`) to `render`, or set `LIBRARY_PACKETS_PREPARED_BY` and `LIBRARY_PACKETS_AUTHOR`. An argument wins over the environment, and the author defaults to the prepared-by text. The footer image comes from the packet's `logo` file in `asset_root`, so supply your own PNG there; the bundled Legion image is only the default.

The renderer is found from `--soffice`, then `SOFFICE_PATH`, then `soffice`, `soffice.exe` or `libreoffice` on `PATH`, then `Program Files\LibreOffice\program\soffice.exe` (also `Program Files (x86)`). Windows status: renderer discovery accepts `soffice.exe` and those install paths, but the helper's private output writer still requires POSIX directory handles and no-follow opens, so `render` and `inventory` (which also write JSON) report blocked on native Windows. `validate` does not use that writer, but nothing here has been run on a Windows machine. macOS and Linux are the qualified platforms. See the [portability guide](guides/07-desktop-portability.md).

## Output contract

Each document's folder contains its audience-safe `.md`, `.docx`, `.pdf`, `citations.md` and `citations.json`. The packet's `_internal` folder holds full provenance, quotes, source/status decisions and review records. Public delivery contains only the explicitly approved document folders and assets. The full internal output tree is not a public archive.

No document/page minimum. No invented metrics, customers, behavior or citations. No automatic publication, messages, paid account creation, installation or source modification. Missing source coverage or a required rendering capability remains a specific deferred/blocked item.

This capability derives from the library-to-brief workflow, generalized beyond any one product. Runtime document production is research-only; committing or publishing changes follows the host's existing authority and review rules.


## Source-preserving novice explanation

For a novice PRD packet, read guides/08-explain-prd-with-constraints.md and templates/prd-preservation-ledger.md before the unchanged citation/render/every-page review workflow.
