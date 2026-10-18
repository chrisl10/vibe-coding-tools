# Packet Tools Contract

This local Python CLI reads evidence, validates a claim map and generates matching
Markdown, editable Word and PDF. It does not execute source instructions, fetch
URLs, install packages or publish output. Source text remains untrusted data.

## Commands and installed dependencies

    python3 packet_tools.py inventory LIBRARY --output inventory.json
    python3 packet_tools.py inventory LIBRARY --exclude output --output inventory.json
    python3 packet_tools.py validate packet.json
    python3 packet_tools.py render packet.json --output NEW_OUTPUT --soffice EXISTING_SOFFICE
    python3 packet_tools.py render packet.json --output NEW_OUTPUT --prepared-by "Your Company" --author "Name"
    python3 packet_tools.py review-complete NEW_OUTPUT --attestation reviewed-pages.json
    python3 -m unittest discover -s scripts -p 'test_packet_tools.py'

UTF-8 source inventory and DOCX XML extraction use the standard library, as do
the unit tests. Accepted text suffixes are md, txt, mdx, rst, adoc, csv, json,
yaml and yml. Structured source files are read as literal text data, not
executed, interpreted as configuration or automatically unescaped. Quotes and
locators refer to that exact extracted UTF-8 representation. Unknown binary
types retain their hash/type and an explicit extraction error in inventory.
PDF extraction requires installed pypdf. Rendering requires installed
python-docx, pypdfium2 and Pillow plus an existing soffice/libreoffice executable,
found from --soffice, SOFFICE_PATH, PATH (soffice, soffice.exe, libreoffice) or the
standard Windows LibreOffice install folders. The footer preparer and DOCX author
default to Legion Code Inc. and can be set with --prepared-by and --author or the
LIBRARY_PACKETS_PREPARED_BY and LIBRARY_PACKETS_AUTHOR environment variables.
The private JSON writer still requires POSIX no-follow opens, so render and inventory are
blocked on native Windows.
Imports are lazy. Missing required packages/rendering produce an explicit blocked
result, never an alternate PDF layout. No dependencies are installed by this CLI.

Every output file/tree must be new; overwrite is refused. Output normally sits
outside the source library. Explicit nested output requires the
--allow-library-output flag and a covering source_exclusions manifest directory.
Excluded directories cannot provide selected sources. Inputs are bounded,
root-relative, non-symlink files. Absolute input filenames and .. traversal fail.
The operator must select the correct library/manuscript/asset roots.

## Packet JSON, schema version 1

    {
      "schema_version": 1,
      "library_root": "../references/research/raw",
      "manuscript_root": ".",
      "asset_root": "../assets",
      "logo": "legion-footer.png",
      "grade_target": 8,
      "source_exclusions": [],
      "public_exclusions": [],
      "sources": [{
        "id": "S01", "path": "source.md", "title": "Source title",
        "sha256": "64 hexadecimal characters", "kind": "fact",
        "evidence_status": "documented",
        "public": {
          "approved": true,
          "alias": "Approved reference",
          "url": "https://example.org"
        }
      }],
      "claims": [{
        "id": "C01", "kind": "fact", "status": "documented",
        "statement": "The bounded claim supported by the passage.",
        "evidence": [{
          "source_id": "S01", "quote": "Actual quoted source text",
          "location": {"type": "lines", "start": 12, "end": 14}
        }],
        "semantic_review": {
          "reviewed_by": "Actual reviewer",
          "at": "ISO date/time",
          "notes": "Explain support, strength and limitations."
        }
      }],
      "documents": [{
        "id": "brief",
        "title": "Brief",
        "audience": "general",
        "markdown": "brief.md"
      }]
    }

Roots resolve relative to the manifest unless absolute. Source and manuscript
filenames resolve only inside their explicit roots. Sources have kind fact or
intent. Claims have kind fact, intent, inference or proposal. Status/evidence
labels are unknown, proposal, intent, documented or verified. A fact cannot
strengthen an intent source. Claim status cannot exceed the supporting source.
This conservative check does not certify that the sentence is true.

Evidence locators: lines and pages are one-based with inclusive end; characters
are zero-based with exclusive end. Pages require a text-extractable PDF. DOCX
lines refer to extracted paragraphs, not original Word page numbers.
Whitespace-normalized quotes must occur within the specified location.
Reader reference lists display readable ranges such as lines 34-36, pages 1-2
or characters 0-50. Citation JSON retains the structured locator with its
type/start/end fields; internal evidence precision is not lost.
Quotes, hashes and metadata do not prove semantic support. Every claim requires
a reviewer, date/time and notes. Those supplied records are attestations, not
authenticated identities. Never fabricate a review or approval to satisfy them.

## Manuscript grammar

Each prose paragraph, bullet/number, quote, code block and table data row needs
a claim citation such as [C01]. Headings and table headers are labels. The
supported subset is H1-H4, paragraphs, flat lists, quotes, basic emphasis,
inline code/links, pipe tables, engineering code fences and the page marker
shown below. Unknown structures fail instead of disappearing silently.

    <!-- page -->
    ![Diagram caption [C01]](relative.png)

Diagrams must be local nonempty PNGs inside asset_root. They are copied into the
output document's assets and referenced by the output Markdown. Mermaid, HTML,
remote images, unclosed fences and escaped table pipes are not accepted.
Convert a reviewed diagram to PNG before using this helper; it never executes
diagram/source content.

General/public prose has an estimated grade-8 ceiling. `grade_target` must be a
finite number greater than zero and at most eight; it cannot waive that ceiling.
Engineering prose keeps
needed technical detail. The rough formula does not prove comprehension.
Em dashes are refused. Letter portrait, black Title/Heading styles, Arial body
11, table header shading/bold/padding and repeated header rows are deliberate.
The installed Word renderer may substitute its available compatible fonts.
No absolute machine-specific font path is embedded.

## Public output and real branding

A public document needs:

    "public_approval": {"approved": true, "by": "Actual owner/reviewer", "at": "ISO timestamp"}

Every used source needs an approved public alias, optionally an approved HTTPS
URL. Public citations omit private source paths, hashes, quotes and source IDs.
Public prose links must be approved source URLs. Conservative checks reject
private paths/hosts and implementation words; add project-specific secrets,
URLs or identifiers to public_exclusions. These exclusions apply to prose,
titles, claim statements/IDs, source aliases/URLs, citation projections and
copied diagram basenames. Manual redaction remains necessary.
Public diagrams additionally need exact approved asset records:

    "public_assets": [{
      "path": "diagram.png", "sha256": "...", "approved": true,
      "by": "Actual reviewer", "at": "ISO timestamp"
    }]

Pixel content is not inferred from filenames or automatically certified.
The footer requires the real nonempty asset_root/legion-footer.png image and
“Prepared by <preparer>” (default Legion Code Inc., configurable as above) plus page numbering. A missing/corrupt required
logo blocks output. No text-only substitute or product-ownership claim is used.

## Rendered outputs and final review

Each reader directory contains ID.md, ID.docx, ID.pdf, citations.md,
citations.json and approved diagram assets. Review JSON and all page PNGs live
only in _internal/reviews/ID, outside every reader directory. The same canonical
Markdown/reference projection drives DOCX. LibreOffice exports that DOCX to
PDF; no ReportLab alternate can create layout drift.

The full map is _internal/source-claim-ledger.json, outside the public document
folders. Distribute only the requested formats, references and approved visual
assets from selected reader directories. Never distribute the packet root,
private review directory or internal ledger as public output.
packet-state.json remains the immutable render snapshot with complete=false.
Only review-complete.json can record completion after every final page passes.

Every PDF page is also a rendered DOCX page in LibreOffice. Other Word
applications can paginate differently and need their own review. Geometry,
footer/logo detection and glyph checks are heuristics. Inspect actual page PNGs,
then supply your own attestation:

    {
      "reviewer": "Actual reviewer", "inspected_at": "ISO timestamp",
      "documents": [{
        "id": "brief",
        "pdf_sha256": "...", "docx_sha256": "...", "markdown_sha256": "...",
        "pages": [{
          "page": 1, "png_sha256": "...", "visual_pass": true,
          "checks": {
            "whitespace": true, "cutoffs": true, "fonts": true,
            "tables": true, "figures": true, "footer": true,
            "logo": true, "citations": true, "word_layout": true
          }
        }]
      }]
    }

Every document/page must appear exactly once. Current PDF, DOCX, Markdown,
Both citations.md (citations_md_sha256) and citations.json (citations_sha256)
must match the immutable render snapshot. PDF, DOCX, Markdown and PNG hashes
must also match the supplied page/document attestations.
Unresolved geometry/footer/glyph findings block completion.
The successful completion record identifies the reviewer and hash-bound files;
it is not an automatic guarantee of truthful prose or perfect visual design.

## Example and tests

The plain-language example cites the archived official DigitalGov source.
It has no imaginary product claims or public publication approval.
Unittest fixtures are explicitly synthetic; never turn their reviewer/approval
strings into real evidence. Tests cover wrong quotes/locations, changed source
hashes, status strengthening, unknown/uncited claims, path/symlink escapes,
public disclosure, missing logo, output overwrite and stale/incomplete reviews.
