#!/usr/bin/env python3
"""Behavioral and adversarial checks for the read-only handoff validator."""

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Running checks against a distributable must not add compiled cache files.
sys.dont_write_bytecode = True
from validate_handoff import validate


SCRIPT = Path(__file__).with_name("validate_handoff.py")
EXAMPLE = SCRIPT.parent.parent / "templates" / "wave-plan.example.json"


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def reject(self, fragment):
        result = validate(self.plan)
        self.assertEqual(result["verdict"], "FAIL", result)
        self.assertTrue(any(fragment in error["message"] for error in result["errors"]), result)

    def ready_plan(self):
        self.plan["example"] = False
        self.plan["capacity"]["verified"] = True
        for contract in self.plan["contracts"]:
            contract.update(status="Accepted", approved_by="Fictional owner", approval_evidence="local decision record, revision 1")
        for wave in self.plan["waves"]:
            wave["ready"] = True

    def test_generic_example_passes_without_implying_ready_implementation(self):
        result = validate(self.plan)
        self.assertEqual(result["verdict"], "PASS", result)
        self.assertTrue(result["warnings"])
        self.assertTrue(all(not wave["ready"] for wave in self.plan["waves"] if wave["implementation"]))
        self.assertTrue(any("human evidence is not verified" in text for text in result["limitations"]))

    def test_validator_does_not_mutate_input(self):
        before = copy.deepcopy(self.plan)
        validate(self.plan)
        self.assertEqual(self.plan, before)

    def test_declared_accepted_ready_plan_passes(self):
        self.ready_plan()
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_draft_cannot_activate_implementation(self):
        self.ready_plan()
        self.plan["contracts"][0]["status"] = "Draft"
        self.reject("Ready implementation requires")

    def test_missing_human_attribution_cannot_activate_implementation(self):
        self.ready_plan()
        self.plan["contracts"][0]["approved_by"] = None
        self.reject("Ready implementation requires")

    def test_missing_approval_evidence_cannot_activate_implementation(self):
        self.ready_plan()
        self.plan["contracts"][0]["approval_evidence"] = None
        self.reject("Ready implementation requires")

    def test_empty_approval_evidence_refused(self):
        self.plan["contracts"][0]["approval_evidence"] = "  "
        self.reject("Expected null or a nonempty string")

    def test_unknown_contract_status_refused(self):
        self.plan["contracts"][0]["status"] = "Approved"
        self.reject("Expected Draft or Accepted")

    def test_pin_must_match_exact_revision_even_for_blocked_wave(self):
        self.plan["waves"][1]["contract_pins"][0]["revision"] = 2
        self.reject("exact declared contract revision")

    def test_unknown_contract_refused(self):
        self.plan["waves"][1]["contract_pins"][0]["id"] = "CTR-does-not-exist"
        self.reject("Unknown contract")

    def test_unpinned_implementation_refused(self):
        self.plan["waves"][1]["contract_pins"] = []
        self.reject("must pin their contracts")

    def test_duplicate_pin_refused(self):
        self.plan["waves"][1]["contract_pins"] *= 2
        self.reject("Duplicate contract pin")

    def test_boolean_contract_revision_refused(self):
        self.plan["contracts"][0]["revision"] = True
        self.reject("booleans are not revisions")

    def test_boolean_pin_revision_cannot_equal_integer_revision(self):
        self.plan["waves"][1]["contract_pins"][0]["revision"] = True
        self.reject("booleans are not revisions")

    def test_boolean_capacity_refused(self):
        self.plan["capacity"]["limit"] = True
        self.reject("booleans are not integers")

    def test_fractional_capacity_refused(self):
        self.plan["capacity"]["limit"] = 12.0
        self.reject("positive integer")

    def test_coordinator_reservation_cannot_be_removed(self):
        self.plan["capacity"]["coordinator_slots"] = 0
        self.reject("exactly 1 logical")

    def test_review_limit_must_be_positive(self):
        self.plan["capacity"]["reviewer_slots"] = 0
        self.reject("positive simultaneous reviewer")

    def test_active_overhead_included_in_capacity(self):
        self.plan["capacity"]["limit"] = 2
        self.reject("exceed limit 2")

    def test_omitting_coordinator_does_not_evade_capacity(self):
        self.plan["capacity"]["limit"] = 2
        self.plan["waves"][1]["active_shards"] = ["S1", "S2"]
        self.reject("including coordinator overhead")

    def test_duplicate_ids_refused(self):
        for collection in ("contracts", "shards", "waves"):
            with self.subTest(collection=collection):
                changed = copy.deepcopy(self.plan)
                changed[collection].append(copy.deepcopy(changed[collection][0]))
                self.assertEqual(validate(changed)["verdict"], "FAIL")

    def test_unknown_wave_refused(self):
        self.plan["waves"][1]["depends_on"] = ["W404"]
        self.reject("Unknown reference: W404")

    def test_unknown_shard_refused(self):
        self.plan["waves"][1]["active_shards"].append("S404")
        self.reject("Unknown reference: S404")

    def test_cycle_stops_validation_without_hanging(self):
        self.plan["waves"][0]["depends_on"] = ["W3"]
        self.reject("Dependency cycle")

    def test_self_dependency_refused(self):
        self.plan["waves"][0]["depends_on"] = ["W0"]
        self.reject("Dependency cycle")

    def test_ready_dependency_cannot_be_blocked(self):
        self.ready_plan()
        self.plan["waves"][1]["ready"] = False
        self.reject("not ready: W1")

    def test_unverified_capacity_blocks_ready_implementation(self):
        self.ready_plan()
        self.plan["capacity"]["verified"] = False
        self.reject("verified capacity")

    def test_example_cannot_claim_implementation_ready(self):
        self.ready_plan()
        self.plan["example"] = True
        self.reject("Illustrative examples cannot")

    def test_ownership_prefix_conflict_refused(self):
        self.plan["shards"][2]["owned_paths"] = ["app"]
        self.reject("Concurrent ownership overlaps")

    def test_sibling_prefixes_do_not_collide(self):
        self.plan["shards"][2]["owned_paths"] = ["app/database"]
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_unsafe_paths_refused(self):
        for path in ("/tmp/product", "../secret", "src/../secret", "src//db", "./src", "src/", "src/*", "src/[abc]", "C:/src", "src\\db", "src\x00db", " src/db"):
            with self.subTest(path=path):
                changed = copy.deepcopy(self.plan)
                changed["shards"][2]["owned_paths"] = [path]
                self.assertEqual(validate(changed)["verdict"], "FAIL")

    def test_reviewer_cannot_own_product_source(self):
        for index in (0, 3, 4):
            with self.subTest(index=index):
                changed = copy.deepcopy(self.plan)
                changed["shards"][index]["owned_paths"] = ["src"]
                self.assertEqual(validate(changed)["verdict"], "FAIL")

    def test_exclusion_claim_cannot_hide_prefix_overlap(self):
        self.plan["shards"][2]["exclude_paths"] = ["src/lib/server/auth"]
        self.reject("Exclusion leases are unsupported")

    def test_parallel_wave_ownership_checked_across_waves(self):
        self.plan["waves"][1]["active_shards"] = ["S1"]
        self.plan["waves"][2]["depends_on"] = ["W0"]
        self.plan["waves"][2]["active_shards"] = ["S2"]
        self.plan["shards"][2]["owned_paths"] = ["app"]
        self.plan["waves"][3]["depends_on"] = ["W1", "W2"]
        self.reject("Concurrent ownership overlaps")

    def test_three_parallel_waves_cannot_evade_capacity_with_pairwise_checks(self):
        self.plan["shards"].append({"id": "S5", "role": "implementation", "owned_paths": ["app/export"]})
        self.plan["waves"][1]["active_shards"] = ["S1"]
        self.plan["waves"][2]["depends_on"] = ["W0"]
        self.plan["waves"][2]["active_shards"] = ["S2"]
        self.plan["waves"].append({"id": "P", "depends_on": ["W0"], "active_shards": ["S5"], "contract_pins": [{"id": "CTR-001-intake", "revision": 1}], "implementation": True, "ready": False})
        self.plan["waves"][3]["depends_on"] = ["W1", "W2", "P"]
        self.reject("Concurrent waves need 4")

    def test_serial_wave_ownership_transfer_allowed(self):
        self.plan["waves"][1]["active_shards"] = ["S1"]
        self.plan["waves"][2]["active_shards"] = ["S2"]
        self.plan["shards"][2]["owned_paths"] = ["app/data"]
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_worker_cannot_be_scheduled_twice_in_independent_waves(self):
        self.plan["waves"][2]["depends_on"] = ["W0"]
        self.plan["waves"][3]["depends_on"] = ["W1", "W2"]
        self.reject("active in multiple concurrent waves")

    def test_oversized_dag_fails_before_graph_expansion(self):
        self.plan["waves"] = [{"id": "W" + str(index)} for index in range(65)]
        self.reject("At most 64 waves")

    def test_short_or_symbolic_git_ref_refused(self):
        for value in ("main", "0123456", "g" * 40, True):
            with self.subTest(value=value):
                changed = copy.deepcopy(self.plan)
                changed["base_sha"] = value
                self.assertEqual(validate(changed)["verdict"], "FAIL")

    def test_sha256_repository_object_id_supported(self):
        self.plan["base_sha"] = "ab" * 32
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_malformed_types_report_errors_without_crashing(self):
        variants = [None, [], {}, {"project": "x", "shards": [None], "waves": [None], "contracts": [None]}]
        for collection, index, field, value in (("shards", 1, "role", []), ("shards", 1, "owned_paths", {}), ("waves", 1, "active_shards", {}), ("waves", 1, "contract_pins", [None]), ("contracts", 0, "revision", {})):
            changed = copy.deepcopy(self.plan)
            changed[collection][index][field] = value
            variants.append(changed)
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertEqual(validate(variant)["verdict"], "FAIL")

    def test_cli_passes_and_does_not_write_input_or_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(self.plan), encoding="utf-8")
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["verdict"], "PASS")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)
            self.assertEqual([file.name for file in Path(directory).iterdir()], ["plan.json"])

    def test_cli_rejects_malformed_json_and_duplicate_keys(self):
        for raw in ("{", '{"project":"a","project":"b"}'):
            with self.subTest(raw=raw):
                result = subprocess.run([sys.executable, str(SCRIPT), "-"], input=raw, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(json.loads(result.stdout)["verdict"], "FAIL")

    def test_cli_missing_file_reports_json_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(SCRIPT), str(Path(directory) / "missing.json")], capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["verdict"], "FAIL")

    def test_one_reviewer_slot_supports_ordered_reviews(self):
        self.plan["capacity"]["reviewer_slots"] = 1
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_legacy_two_reviewer_fields_without_mode_remain_valid(self):
        self.plan["capacity"].pop("mode")
        self.plan["capacity"]["reviewer_slots"] = 2
        self.plan["capacity"]["limit"] = 12
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_idle_review_limit_is_not_active_capacity(self):
        self.plan["capacity"]["reviewer_slots"] = 2
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def serial_preparation(self):
        self.plan["capacity"].update(mode="serial-preparation", limit=1)
        self.plan["waves"] = [self.plan["waves"][i] for i in (0, 3, 4)]
        self.plan["waves"][1]["depends_on"] = ["W0"]

    def test_serial_preparation_fits_one_inline_slot(self):
        self.serial_preparation()
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_serial_mode_refuses_any_implementation_readiness(self):
        self.ready_plan()
        self.plan["capacity"].update(mode="serial-preparation", limit=1)
        self.plan["waves"][1]["active_shards"] = ["S1"]
        self.reject("Serial preparation cannot declare implementation ready")

    def test_serial_mode_requires_explicit_single_capacity(self):
        self.plan["capacity"]["mode"] = "serial-preparation"
        self.reject("Serial preparation requires a limit of exactly 1")

    def test_parallel_coordinator_overhead_blocks_one_slot_worker(self):
        self.plan["capacity"]["limit"] = 1
        self.plan["waves"][1]["active_shards"] = ["S1"]
        self.reject("including coordinator overhead")

    def test_unknown_mode_cannot_hide_overhead(self):
        self.plan["capacity"]["mode"] = "unlimited"
        self.reject("Expected parallel or serial-preparation")

    def test_unknown_capacity_cannot_hide_extra_workers(self):
        self.plan["capacity"]["extra_slots"] = -9
        self.reject("Unknown capacity field")

    def test_nested_workers_must_be_explicit_active_shards(self):
        self.plan["shards"][1]["nested_workers"] = ["hidden helper"]
        self.reject("Flatten nested workers")

    def test_same_wave_security_quality_refused(self):
        self.plan["waves"][3]["active_shards"].append("S4")
        self.reject("Security must precede Quality")

    def test_parallel_review_waves_refused(self):
        self.plan["waves"][4]["depends_on"] = ["W2"]
        self.reject("Security must precede Quality")

    def test_quality_before_security_refused(self):
        self.plan["waves"][3]["active_shards"] = ["S4"]
        self.plan["waves"][4]["active_shards"] = ["S3"]
        self.reject("Quality needs preceding Security")

    def test_review_cannot_overlap_candidate_changes(self):
        self.plan["waves"][3]["depends_on"] = ["W1"]
        self.reject("candidate review cannot overlap implementation")

    def test_implementation_between_reviews_invalidates_security_coverage(self):
        self.plan["waves"].append({"id": "late", "depends_on": ["W3"], "active_shards": ["S1"], "contract_pins": [{"id": "CTR-001-intake", "revision": 1}], "implementation": True, "ready": False})
        self.plan["waves"][4]["depends_on"] = ["late"]
        self.reject("Quality needs preceding Security on the same candidate")

    def test_review_shard_cannot_occupy_two_parallel_waves(self):
        self.plan["waves"].append({"id": "second-security", "depends_on": ["W2"], "active_shards": ["S3"], "contract_pins": [], "implementation": False, "ready": False})
        self.plan["waves"][4]["depends_on"] = ["W3", "second-security"]
        self.reject("active worker or reviewer cannot occupy multiple concurrent waves")

    def test_unscheduled_review_role_is_not_a_review_gate(self):
        self.plan["waves"][4]["active_shards"] = ["S0"]
        self.reject("Schedule both Security and Quality")

    def test_implementation_after_final_quality_cannot_escape_review(self):
        self.plan["waves"].append({"id": "late", "depends_on": ["W4"], "active_shards": ["S1"], "contract_pins": [{"id": "CTR-001-intake", "revision": 1}], "implementation": True, "ready": False})
        self.reject("changes after final Quality are refused")

    def test_two_slot_parallel_plan_can_run_one_worker_and_ordered_reviews(self):
        self.plan["capacity"]["limit"] = 2
        self.plan["waves"][1]["active_shards"] = ["S1"]
        self.assertEqual(validate(self.plan)["verdict"], "PASS")

    def test_boolean_review_capacity_refused(self):
        self.plan["capacity"]["reviewer_slots"] = True
        self.reject("positive simultaneous reviewer")

    def test_runner_does_not_add_bytecode_to_a_distribution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "scripts"
            templates = root / "templates"
            scripts.mkdir()
            templates.mkdir()
            runner = scripts / Path(__file__).name
            runner.write_bytes(Path(__file__).read_bytes())
            (scripts / SCRIPT.name).write_bytes(SCRIPT.read_bytes())
            (templates / EXAMPLE.name).write_bytes(EXAMPLE.read_bytes())
            before = {str(path.relative_to(root)) for path in root.rglob("*")}
            result = subprocess.run(
                [sys.executable, "-E", str(runner),
                 "HandoffTests.test_generic_example_passes_without_implying_ready_implementation"],
                capture_output=True, text=True, timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                {str(path.relative_to(root)) for path in root.rglob("*")}, before,
            )


if __name__ == "__main__":
    unittest.main()
