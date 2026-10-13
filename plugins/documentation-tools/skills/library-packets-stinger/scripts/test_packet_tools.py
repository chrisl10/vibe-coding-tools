"""Synthetic safety/contract fixtures only. These are not product evidence."""
import base64
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import packet_tools as pt

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lZsAAAAASUVORK5CYII=")


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.lib = self.root / "library"
        self.lib.mkdir()
        self.assets = self.root / "assets"
        self.assets.mkdir()
        (self.assets / "legion-footer.png").write_bytes(PNG)
        self.source = self.lib / "synthetic.txt"
        self.source.write_text("Synthetic fixture only.\nThe test team plans a page.\n")
        self.doc = self.root / "brief.md"
        self.doc.write_text("# Test brief\n\nThe test team plans a page. [C01]\n")
        self.manifest = self.root / "packet.json"
        self.packet = {
            "schema_version": 1, "library_root": "library", "asset_root": "assets",
            "sources": [{"id": "S01", "path": "synthetic.txt", "title": "Synthetic source",
                         "sha256": pt.digest(self.source), "kind": "intent",
                         "evidence_status": "intent",
                         "public": {"approved": True, "alias": "Synthetic reference",
                                    "url": "https://example.org/reference"}}],
            "claims": [{"id": "C01", "kind": "intent", "status": "intent",
                        "statement": "The test team plans a page.",
                        "evidence": [{"source_id": "S01",
                                      "quote": "The test team plans a page.",
                                      "location": {"type": "lines", "start": 2, "end": 2}}],
                        "semantic_review": {"reviewed_by": "Synthetic test reviewer",
                                            "at": "2026-10-06", "notes": "Test fixture only."}}],
            "documents": [{"id": "brief", "title": "Test brief", "audience": "general",
                           "markdown": "brief.md"}]}

    def tearDown(self):
        self.tmp.cleanup()

    def result(self):
        self.manifest.write_text(json.dumps(self.packet))
        return pt.validate(self.manifest)

    def rejected(self, contains):
        r = self.result()
        self.assertFalse(r["valid"], r)
        self.assertIn(contains, "\n".join(r["errors"]))

    def test_valid_intent_and_md_without_optional_imports(self):
        with patch.object(pt, "optional", side_effect=AssertionError("optional import")):
            self.assertTrue(self.result()["valid"])
            self.assertEqual(pt.inventory(self.lib)["errors"], 0)

    def test_grade_target_cannot_waive_reader_contract(self):
        for target in (float("nan"), float("inf"), float("-inf"), True, False,
                       "8", None, [], {}, 0, -1, 9, 1000000):
            with self.subTest(target=target):
                self.packet["grade_target"] = target
                with self.assertRaisesRegex(pt.PacketError, "grade_target"):
                    self.result()
        self.packet["grade_target"] = 8
        self.assertTrue(self.result()["valid"])

    def test_difficult_prose_rejected_for_general_and_public(self):
        prose = "Internationalization institutionalization interoperability " * 12
        self.doc.write_text("# Test\n\n" + prose + ". [C01]\n")
        self.assertGreater(pt.grade(prose), 8)
        self.rejected("estimated grade")
        self.public_packet()
        self.rejected("estimated grade")

    def test_engineering_prose_exempt_from_grade_ceiling(self):
        prose = "Internationalization institutionalization interoperability " * 12
        self.doc.write_text("# Test\n\n" + prose + ". [C01]\n")
        self.packet["documents"][0]["audience"] = "engineering"
        self.assertTrue(self.result()["valid"])

    def test_insufficient_sources(self):
        self.packet["sources"] = []
        self.rejected("Insufficient")

    def test_hash_changes(self):
        self.source.write_text("Changed source.\n")
        self.rejected("SHA-256 mismatch")

    def test_unknown_source(self):
        self.packet["claims"][0]["evidence"][0]["source_id"] = "S99"
        self.rejected("unknown/unusable source")

    def test_wrong_quote(self):
        self.packet["claims"][0]["evidence"][0]["quote"] = "The team shipped it."
        self.rejected("quote not found")

    def test_quote_wrong_location(self):
        self.packet["claims"][0]["evidence"][0]["location"] = {"type": "lines", "start": 1, "end": 1}
        self.rejected("quote not found")

    def test_intent_not_strengthened_to_fact(self):
        self.packet["claims"][0]["kind"] = "fact"
        self.rejected("strengthened into a fact")

    def test_status_not_strengthened(self):
        self.packet["claims"][0]["status"] = "verified"
        self.rejected("strengthens source status")

    def test_prose_strengthening(self):
        self.doc.write_text("# Test\n\nIt is available now. [C01]\n")
        self.rejected("apparent status strengthening")

    def test_unknown_citation(self):
        self.doc.write_text("# Test\n\nThe test team plans a page. [C99]\n")
        self.rejected("unknown citation IDs")

    def test_uncited_paragraph(self):
        self.doc.write_text("# Test\n\nThe test team plans a page.\n")
        self.rejected("uncited paragraph")

    def test_em_dash(self):
        self.doc.write_text("# Test\n\nIt plans a page \u2014 a test. [C01]\n")
        self.rejected("em dash")

    def test_source_traversal(self):
        self.packet["sources"][0]["path"] = "../brief.md"
        self.rejected("Unsafe relative path")

    def test_source_symlink_escape(self):
        (self.lib / "escape.txt").symlink_to(self.doc)
        self.packet["sources"][0]["path"] = "escape.txt"
        self.rejected("Symlink input")

    def test_inventory_keeps_extraction_errors(self):
        (self.lib / "broken.pdf").write_bytes(b"not a PDF")
        with patch.object(pt, "optional", side_effect=pt.Blocked("Missing PDF reader")):
            inv = pt.inventory(self.lib)
        row = next(x for x in inv["sources"] if x["path"] == "broken.pdf")
        self.assertIsNotNone(row["sha256"])
        self.assertIn("Missing PDF reader", row["extraction_error"])

    def test_common_utf8_formats_are_read_only_data(self):
        for ext in ("mdx", "rst", "adoc", "csv", "json", "yaml", "yml"):
            with self.subTest(extension=ext):
                path = self.lib / ("data." + ext)
                path.write_text("Raw UTF-8 data only.\n")
                self.assertEqual(pt.extract(path), {
                    "text": "Raw UTF-8 data only.\n", "pages": None})

    def test_structured_json_inventory_and_source_validation_no_execution(self):
        sentinel = self.root / "MUST_NOT_EXIST"
        data = self.lib / "native-capture.json"
        data.write_text(json.dumps({
            "markdown": "The test team plans a page.",
            "untrusted_code": f'__import__("pathlib").Path({str(sentinel)!r}).write_text("BAD")'}))
        self.packet["sources"][0].update(path=data.name, sha256=pt.digest(data))
        self.packet["claims"][0]["evidence"][0]["location"] = {
            "type": "lines", "start": 1, "end": 1}
        with patch.object(pt, "optional", side_effect=AssertionError("optional import")):
            r = self.result()
            self.assertTrue(r["valid"], r["errors"])
            row = next(x for x in pt.inventory(self.lib)["sources"]
                       if x["path"] == data.name)
        self.assertEqual(row["type"], "json")
        self.assertEqual(row["sha256"], pt.digest(data))
        self.assertIsNone(row["extraction_error"])
        self.assertFalse(sentinel.exists())

    def test_readable_locator_ranges(self):
        self.assertEqual(pt.format_locator({"type": "lines", "start": 34, "end": 36}),
                         "lines 34-36")
        self.assertEqual(pt.format_locator({"type": "pages", "start": 1, "end": 2}),
                         "pages 1-2")
        self.assertEqual(pt.format_locator({"type": "characters", "start": 0, "end": 50}),
                         "characters 0-50")

    def test_markdown_reference_readable_and_json_locator_retained(self):
        result = self.result()
        md, projection = pt.citation_projection(result, result["documents"][0])
        self.assertIn("lines 2", md)
        self.assertNotIn('{"type"', md)
        self.assertEqual(projection["claims"][0]["references"][0]["location"],
                         {"type": "lines", "start": 2, "end": 2})

    def test_explicit_public_approval(self):
        self.packet["documents"][0]["audience"] = "public"
        self.rejected("explicit public approval")

    def public_packet(self):
        self.packet["documents"][0].update(audience="public", public_approval={
            "approved": True, "by": "Synthetic fixture", "at": "2026-10-06"})

    def test_public_private_path(self):
        self.public_packet()
        self.doc.write_text("# Test\n\nUse /Users/test/private. [C01]\n")
        self.rejected("private/code")

    def test_public_relative_link(self):
        self.public_packet()
        self.doc.write_text("# Test\n\nSee [private](../secret.md). [C01]\n")
        self.rejected("not an approved source URL")

    def test_public_source_filename_leak(self):
        self.public_packet()
        self.doc.write_text("# Test\n\nRead synthetic.txt for this plan. [C01]\n")
        self.rejected("private source filename")

    def test_public_credential_url(self):
        self.public_packet()
        self.packet["sources"][0]["public"]["url"] = "https://example.org?token=secret"
        self.rejected("public reference leaks")

    def test_public_diagram_requires_pixel_review(self):
        self.public_packet()
        (self.assets / "chart.png").write_bytes(PNG)
        self.doc.write_text("# Test\n\n![Chart [C01]](chart.png)\n")
        self.rejected("hash-bound visual/content approval")

    def test_public_diagram_basename_exclusion(self):
        self.public_packet()
        self.packet["public_exclusions"] = ["Project Cedar"]
        path = self.assets / "Project-Cedar.png"
        path.write_bytes(PNG)
        self.packet["public_assets"] = [{"path": path.name, "sha256": pt.digest(path),
                                        "approved": True, "by": "Synthetic reviewer",
                                        "at": "2026-10-06"}]
        self.doc.write_text("# Test\n\n![Chart [C01]](Project-Cedar.png)\n")
        self.rejected("private/code")

    def test_hidden_html_in_joined_paragraph(self):
        self.doc.write_text("# Test\n\nA plan. [C01]\nHere is <script>bad</script>.\n")
        self.rejected("Unsupported Markdown")

    def test_source_exclusions_enforced(self):
        self.packet["source_exclusions"] = ["synthetic.txt"]
        self.rejected("excluded directory")

    def test_renderer_unavailable_is_blocked(self):
        self.result()
        with patch.object(pt, "optional", side_effect=pt.Blocked("missing installed renderer package")):
            with self.assertRaisesRegex(pt.Blocked, "missing installed renderer"):
                pt.render(self.manifest, self.root / "new-output")

    def test_public_alias_approval(self):
        self.public_packet()
        self.packet["sources"][0]["public"]["approved"] = False
        self.rejected("approved public source alias")

    def test_public_projection_never_contains_internal_ledger(self):
        self.public_packet()
        result = self.result()
        self.assertTrue(result["valid"], result["errors"])
        md, projection = pt.citation_projection(result, result["documents"][0])
        out = md + json.dumps(projection)
        for secret in ("synthetic.txt", pt.digest(self.source), "The test team plans", "S01"):
            self.assertNotIn(secret, out)

    def test_public_excluded_name_in_alias_only(self):
        self.public_packet()
        self.packet["public_exclusions"] = ["Project Cedar"]
        self.packet["sources"][0]["public"]["alias"] = "Project Cedar notes"
        self.rejected("public reference leaks")

    def test_public_excluded_name_in_url_only(self):
        self.public_packet()
        self.packet["public_exclusions"] = ["Project Cedar"]
        self.packet["sources"][0]["public"]["url"] = "https://example.org/Project-Cedar"
        self.rejected("public reference leaks")

    def test_public_excluded_name_in_claim_only(self):
        self.public_packet()
        self.packet["public_exclusions"] = ["Project Cedar"]
        self.packet["claims"][0]["statement"] = "Project Cedar plans a page."
        self.rejected("leaks private detail")

    def test_projection_defense_before_any_format(self):
        self.public_packet()
        r = self.result()
        self.assertTrue(r["valid"])
        r["packet"]["public_exclusions"] = ["Project Cedar"]
        r["packet"]["sources"][0]["public"]["alias"] = "Project Cedar notes"
        with self.assertRaisesRegex(pt.PacketError, "citation projection"):
            pt.citation_projection(r, r["documents"][0])

    def test_no_semantic_truth_without_review_record(self):
        del self.packet["claims"][0]["semantic_review"]
        self.rejected("semantic review record")

    def test_unsupported_markdown_not_silently_ignored(self):
        self.doc.write_text("# Test\n\n<!-- execute file -->\n")
        self.rejected("Unsupported")

    def test_asset_escape(self):
        self.doc.write_text("# Test\n\n![Chart [C01]](../outside.png)\n")
        self.rejected("Unsafe relative path")

    def test_logo_missing(self):
        (self.assets / "legion-footer.png").unlink()
        with self.assertRaises(pt.PacketError):
            self.result()

    def test_no_overwrite(self):
        f = self.root / "already.json"
        f.write_text("keep")
        with self.assertRaises(FileExistsError):
            pt.json_write(f, {})
        self.assertEqual(f.read_text(), "keep")

    def test_json_output_is_private_with_permissive_umask(self):
        f = self.root / "new-output" / "ledger.json"
        previous = pt.os.umask(0)
        try:
            pt.json_write(f, {"source_quote": "synthetic private evidence"})
        finally:
            pt.os.umask(previous)
        self.assertEqual(f.stat().st_mode & 0o777, 0o600)
        self.assertEqual(f.parent.stat().st_mode & 0o777, 0o700)

    def test_private_json_blocks_unsupported_runtime(self):
        with patch.object(pt.os, "O_NOFOLLOW", create=True) as flag:
            del pt.os.O_NOFOLLOW
            with self.assertRaises(pt.Blocked):
                pt.json_write(self.root / "unsupported.json", {})
        self.assertFalse((self.root / "unsupported.json").exists())

    def test_json_output_symlinks_preserve_external_sentinel(self):
        sentinel = self.root / "sentinel.json"
        sentinel.write_text("keep")
        alias = self.root / "alias.json"
        alias.symlink_to(sentinel)
        with self.assertRaises(FileExistsError):
            pt.json_write(alias, {})
        self.assertEqual(sentinel.read_text(), "keep")
        directory_alias = self.root / "alias-folder"
        directory_alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(pt.PacketError):
            pt.json_write(directory_alias / "never.json", {})
        self.assertFalse((self.root / "never.json").exists())

    def synthetic_render_state(self):
        out = self.root / "rendered"
        folder = out / "brief"
        folder.mkdir(parents=True)
        for ext in ("md", "docx", "pdf"):
            (folder / f"brief.{ext}").write_bytes(b"synthetic fixture")
        review_folder = out / "_internal/reviews/brief"
        review_folder.mkdir(parents=True)
        self.review_png = review_folder / "page-001.png"
        self.review_png.write_bytes(PNG)
        (folder / "citations.json").write_text("{}")
        (folder / "citations.md").write_text("# Synthetic References\n")
        page = {"page": 1, "png": "page-001.png", "png_sha256": pt.digest(self.review_png),
                "out_of_page_glyphs": 0, "out_of_page_images": 0, "missing_glyphs": False,
                "footer_text_present": True, "footer_logo_detected": True, "footer_region_extra_text": ""}
        doc = {"id": "brief", "page_count": 1, "pages": [page]}
        for ext in ("md", "docx", "pdf"):
            doc[{"md": "markdown", "docx": "docx", "pdf": "pdf"}[ext] + "_sha256"] = pt.digest(folder / f"brief.{ext}")
        doc["citations_sha256"] = pt.digest(folder / "citations.json")
        doc["citations_md_sha256"] = pt.digest(folder / "citations.md")
        pt.json_write(out / "packet-state.json", {"complete": False, "documents": [doc]})
        a = copy.deepcopy(doc)
        a["pages"] = [{"page": 1, "png_sha256": page["png_sha256"], "visual_pass": True,
                       "checks": {k: True for k in pt.PAGE_CHECKS}}]
        att = self.root / "attestation.json"
        pt.json_write(att, {"reviewer": "Synthetic test reviewer", "inspected_at": "2026-10-06",
                            "documents": [a]})
        return out, att, folder

    def test_every_page_attestation_required(self):
        out, att, _ = self.synthetic_render_state()
        a = pt.json_read(att)
        a["documents"][0]["pages"] = []
        att.write_text(json.dumps(a))
        with self.assertRaisesRegex(pt.PacketError, "every page"):
            pt.review_complete(out, att)

    def test_stale_docx_review(self):
        out, att, folder = self.synthetic_render_state()
        (folder / "brief.docx").write_bytes(b"changed")
        with self.assertRaisesRegex(pt.PacketError, "stale docx"):
            pt.review_complete(out, att)

    def test_stale_pdf_review(self):
        out, att, folder = self.synthetic_render_state()
        (folder / "brief.pdf").write_bytes(b"changed")
        with self.assertRaisesRegex(pt.PacketError, "stale pdf"):
            pt.review_complete(out, att)

    def test_stale_page_image(self):
        out, att, folder = self.synthetic_render_state()
        self.review_png.write_bytes(b"changed")
        with self.assertRaisesRegex(pt.PacketError, "stale page"):
            pt.review_complete(out, att)

    def test_stale_markdown_citation_list(self):
        out, att, folder = self.synthetic_render_state()
        (folder / "citations.md").write_text("Changed references.")
        with self.assertRaisesRegex(pt.PacketError, "Markdown citation list changed"):
            pt.review_complete(out, att)

    def test_stale_json_citation_projection(self):
        out, att, folder = self.synthetic_render_state()
        (folder / "citations.json").write_text('{"changed":true}')
        with self.assertRaisesRegex(pt.PacketError, "citation projection changed"):
            pt.review_complete(out, att)

    def test_word_layout_attestation_required(self):
        out, att, _ = self.synthetic_render_state()
        a = pt.json_read(att)
        a["documents"][0]["pages"][0]["checks"]["word_layout"] = False
        att.write_text(json.dumps(a))
        with self.assertRaisesRegex(pt.PacketError, "visual checks"):
            pt.review_complete(out, att)

    def test_completion_only_after_all_hash_bound_checks(self):
        out, att, _ = self.synthetic_render_state()
        self.assertFalse(pt.json_read(out / "packet-state.json")["complete"])
        self.assertTrue(pt.review_complete(out, att)["complete"])


if __name__ == "__main__":
    unittest.main()
