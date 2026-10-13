"""Behavior and boundary tests using the Python standard library only."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from scripts.calculate import InputError, load_input, model

SKILL_ROOT = Path(__file__).resolve().parents[1]


class EconomicsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.input = json.loads((SKILL_ROOT / "references/templates/input.json").read_text())

    def run_model(self, **changes):
        self.input["scenarios"][0].update(changes)
        return model(self.input)["scenarios"][0]

    def test_baseline_and_independent_margins(self):
        out = self.run_model()
        self.assertEqual(out["net_revenue"], "600")
        self.assertEqual(out["payment_fees"], "24")
        self.assertEqual(out["contribution_per_attempted_unit"], "23.8")
        self.assertEqual(out["contribution"], "476")
        self.assertEqual(out["gross_profit"], "400")
        self.assertEqual(out["modeled_operating_surplus"], "176")
        self.assertEqual(out["break_even_units"], 13)

    def test_retained_fee_on_refund_and_failed_service_cost(self):
        out = self.run_model(failed_payment_rate="0.1", refund_rate="0.5", refund_fee_fixed="1")
        self.assertEqual(out["successful_units"], "18")
        self.assertEqual(out["refunds"], "270")
        self.assertEqual(out["processing_fees_before_returns"], "21.6")
        self.assertEqual(out["processing_fee_returns"], "0")
        self.assertEqual(out["refund_fees"], "9")
        self.assertEqual(out["variable_cost"], "130.6")
        self.assertEqual(out["contribution"], "139.4")

    def test_explicit_fee_return_no_double_count(self):
        out = self.run_model(refund_rate="0.5", payment_fee_return_rate="1")
        self.assertEqual(out["processing_fee_returns"], "12")
        self.assertEqual(out["payment_fees"], "12")
        self.assertEqual(out["net_revenue"], "300")

    def test_full_refund_losses_and_null_margin(self):
        out = self.run_model(refund_rate="1")
        self.assertEqual(out["net_revenue"], "0")
        self.assertIsNone(out["gross_margin_ratio"])
        self.assertIsNone(out["contribution_margin_ratio"])
        self.assertEqual(out["modeled_operating_surplus"], "-424")
        self.assertEqual(out["break_even_status"], "impossible")
        self.assertIsNone(out["break_even_units"])

    def test_no_volume_has_fixed_loss_but_defined_unit_economics(self):
        out = self.run_model(units="0")
        self.assertEqual(out["modeled_operating_surplus"], "-300")
        self.assertIsNone(out["gross_margin_ratio"])
        self.assertEqual(out["break_even_units"], 13)

    def test_zero_contribution_break_even_cases(self):
        out = self.run_model(price_per_unit="5", payment_fee_rate="0", payment_fee_fixed="0")
        self.assertEqual(out["contribution"], "0")
        self.assertEqual(out["break_even_status"], "impossible")
        self.input["scenarios"][0]["costs"] = [self.input["scenarios"][0]["costs"][-1]]
        out = self.run_model()
        self.assertEqual(out["break_even_status"], "all_volumes")
        self.assertEqual(out["break_even_units"], 0)

    def test_negative_contribution_zero_fixed_cost(self):
        out = self.run_model(price_per_unit="0", costs=[])
        self.assertEqual(out["break_even_status"], "zero_volume_only")
        self.assertEqual(out["modeled_operating_surplus"], "-6")

    def test_classification_changes_only_gross_margin(self):
        baseline = self.run_model()
        changed = self.run_model(payment_fee_classification="cost_of_revenue")
        self.assertEqual(changed["gross_profit"], "376")
        self.assertEqual(changed["contribution"], baseline["contribution"])
        self.assertEqual(changed["modeled_operating_surplus"], baseline["modeled_operating_surplus"])

    def test_scenarios_are_independent_high_usage_can_lose(self):
        high = copy.deepcopy(self.input["scenarios"][0])
        high["name"] = "Fictional high usage"
        high["costs"][-1]["amount"] = "40"
        self.input["scenarios"].append(high)
        rows = model(self.input)["scenarios"]
        self.assertEqual(rows[0]["break_even_status"], "finite")
        self.assertEqual(rows[1]["break_even_status"], "impossible")
        self.assertEqual(rows[1]["modeled_operating_surplus"], "-524")

    def test_whole_unit_break_even_rounding(self):
        out = self.run_model(price_per_unit="30.01")
        self.assertEqual(out["break_even_units"], 13)
        at_floor = self.run_model(units="12")
        at_ceil = self.run_model(units="13")
        self.assertLess(Decimal(at_floor["modeled_operating_surplus"]), 0)
        self.assertGreaterEqual(Decimal(at_ceil["modeled_operating_surplus"]), 0)

    def test_invalid_numeric_inputs(self):
        for value in (True, -1, "-0", "NaN", "Infinity", Decimal("NaN"), Decimal("Infinity"),
                      Decimal("-0"), "1e3", "0.0000001", "1000000000001", 1.2, [], None):
            with self.subTest(value=value), self.assertRaises(InputError):
                self.run_model(units=value)

    def test_rate_bounds(self):
        for key in ("refund_rate", "failed_payment_rate", "payment_fee_rate", "payment_fee_return_rate"):
            with self.subTest(key=key), self.assertRaises(InputError):
                self.run_model(**{key: "1.000001"})

    def test_schema_and_duplicate_names(self):
        for change in ({"unexpected": "1"}, {"costs": {}}, {"currency": "usd"},
                       {"observed_at": "2026-02-30"}, {"name": "\n"},
                       {"payment_fee_classification": []}):
            self.setUp()
            with self.subTest(change=change), self.assertRaises(InputError):
                self.run_model(**change)
        self.setUp()
        self.input["scenarios"].append(copy.deepcopy(self.input["scenarios"][0]))
        with self.assertRaises(InputError):
            model(self.input)
        self.setUp()
        self.input["scenarios"][0]["costs"].append(copy.deepcopy(self.input["scenarios"][0]["costs"][0]))
        with self.assertRaises(InputError):
            model(self.input)

    def test_missing_and_excess_scenarios(self):
        for value in ({}, {"scenarios": []}, {"scenarios": [self.input["scenarios"][0]] * 21}):
            with self.subTest(value=value), self.assertRaises(InputError):
                model(value)
        del self.input["scenarios"][0]["units"]
        with self.assertRaises(InputError):
            model(self.input)

    def test_json_duplicate_keys_nonfinite_and_size(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "in.json"
            for value in ('{"scenarios": [], "scenarios": []}', '{"scenarios": NaN}', " " * 262145):
                path.write_text(value)
                with self.subTest(value=value[:50]), self.assertRaises(InputError):
                    load_input(path)

    def test_json_decimal_exactness(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "in.json"
            path.write_text(json.dumps(self.input).replace('"30"', '30.1'))
            out = model(load_input(path))["scenarios"][0]
            self.assertEqual(out["net_revenue"], "602")
            self.assertEqual(out["payment_fees"], "24.06")

    def test_extreme_json_exponents_are_safe_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "in.json"
            for value in ('1e999999999999999999999999', '1e-999999999999999999999999', '1e-7', '1e13'):
                path.write_text('{"scenarios": ' + value + '}')
                with self.subTest(value=value), self.assertRaises(InputError):
                    load_input(path)
                run = subprocess.run([sys.executable, "-B", "-m", "scripts.calculate", "--input", str(path)],
                                     cwd=SKILL_ROOT, capture_output=True, text=True, check=False)
                self.assertEqual(run.returncode, 2)
                self.assertEqual(run.stdout, "")
                self.assertNotIn("Traceback", run.stderr)

    def test_cli_success_and_errors_stdout_is_clean(self):
        args = [sys.executable, "-B", "-m", "scripts.calculate", "--input"]
        good = subprocess.run(args + ["references/templates/input.json"], cwd=SKILL_ROOT,
                              capture_output=True, text=True, check=False)
        self.assertEqual(good.returncode, 0)
        self.assertEqual(json.loads(good.stdout)["scenarios"][0]["break_even_units"], 13)
        self.assertEqual(good.stderr, "")
        bad = subprocess.run(args + ["does-not-exist.json"], cwd=SKILL_ROOT,
                             capture_output=True, text=True, check=False)
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(bad.stdout, "")
        self.assertEqual(bad.stderr, "Input error: input must be an explicit regular JSON file\n")


if __name__ == "__main__":
    unittest.main()
