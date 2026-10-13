# Code Forensics

Review a software or agency engagement using the user's own contracts, invoices, communications and delivery records. Build cited evidence drafts for human and counsel review.

The public examples are newly invented training data. No supplied fixture is a retained matter or evidence about a real party.

Start with [principles](guides/00-principles.md), then [intake](guides/01-intake.md). The [renderer contract](guides/10-case-input-contract.md) explains exact inputs and outputs. The [fictional fixture](examples/example-case-a/case-facts.json) exercises all five document kinds.

Five Node entry points render one selected document each as Word or Markdown. The pre-litigation entry point renders one combined review document. These tools do not investigate, calculate damages, provide legal advice, establish privilege, convert PDFs or send letters. Workbook size depends on the supplied records.

Use existing dependencies only. Word output needs the `docx` dependency from `scripts/package.json`; Markdown uses Node's standard library. Optional Python extractors have their own requirements and limitations documented in the guides. Their shared output guard needs POSIX directory-descriptor support; choose a fresh private workspace and never reuse output filenames.
