# Report synthesis

Write the reviewed facts and explanations before rendering. Use the report skeletons under `templates/reports/` as authoring checklists; the builders do not load or substitute Markdown templates. Convert authored content to the strict [input contract](10-case-input-contract.md).

Each of the four report entry points needs `--case-facts FILE --out-dir DIR [--format docx|markdown]`. The selected kind must exist. The filename is `<matter.id>-<kind>.docx` or `.md`. Default Word output uses the existing `docx` dependency. Missing input, invalid input and missing selected kinds refuse without creating output.

The attorney kind is an evidence memo for counsel review. It has no assumed privilege, legal conclusions, default law or predicted outcome. Plain-language text should target grade eight and use one consistent analogy only when it helps explain a fact.

PDF conversion is a separate step using an available converter. These builders do not convert PDFs. Check every resulting page for clipped text, crowded tables, blank areas and missing sources. Report Word/PDF application checks only when actually run. Generating a valid ZIP-based DOCX does not prove display quality in every application.

Keep versions in separate private output folders. Compare every amount, date and evidence label across selected documents. The evidence register is included in each output; add precise page, row or hash coordinates in the supplied source URI or title. The optional ZIP helper takes `--src DIR --project-name NAME --out-dir DIR`; inspect its contents before any separately authorized sharing.
