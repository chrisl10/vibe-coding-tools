"""Offline invoice-semantics and boundary tests, stdlib only."""

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

ROOT = Path(__file__).resolve().parents[1]


class CostTests(unittest.TestCase):
    def setUp(self):
        self.input = json.loads((ROOT / "references/templates/input.json").read_text())

    def test_allowance_floor_credit_and_labor(self):
        rows = model(self.input)["scenarios"]
        self.assertEqual([r["provider_cash"] for r in rows], ["10", "30", "90"])
        self.assertEqual([r["monthly_cash_estimate"] for r in rows], ["50", "70", "130"])
        self.assertEqual([r["monthly_cost_with_time_valuation"] for r in rows], ["150", "170", "230"])
        self.assertEqual(rows[0]["credit_pools"][0]["unused"], "10")
        self.assertEqual(rows[1]["providers"][0]["meters"][0]["billable_quantity"], "20")

    def test_additive_fee_is_different_from_usage_floor(self):
        self.input["scenarios"][1]["providers"][0]["fee_mode"] = "additive"
        row = model(self.input)["scenarios"][1]
        self.assertEqual(row["provider_cash"], "40")

    def test_usage_credit_does_not_erase_floor(self):
        scenario = self.input["scenarios"][1]
        scenario["providers"][0]["meters"][0]["quantity"] = "15"
        row = model(self.input)["scenarios"][1]
        self.assertEqual(row["providers"][0]["gross_usage"], "10")
        self.assertEqual(row["provider_cash"], "10")
        scenario["credit_pools"][0]["scope"] = "total"
        row = model(self.input)["scenarios"][1]
        self.assertEqual(row["provider_cash"], "0")

    def test_shared_credit_is_allocated_once(self):
        scenario = self.input["scenarios"][1]
        second = copy.deepcopy(scenario["providers"][0])
        second["name"] = "fictional-other"
        scenario["providers"].append(second)
        scenario["credit_pools"][0]["eligible_providers"].append(second["name"])
        with self.assertRaisesRegex(InputError, "shared pool budget exceeded"):
            model(self.input)
        second["credit_allocations"][0]["amount"] = "0"
        row = model(self.input)["scenarios"][1]
        self.assertEqual(row["provider_cash"], "70")
        self.assertEqual(row["credit_pools"][0]["allocated"], "10")

    def test_credit_eligibility_scope_and_overallocation(self):
        cases = ["unknown pool", "unknown eligible", "usage exceed", "total exceed", "duplicate pool"]
        for case in cases:
            self.setUp()
            scenario = self.input["scenarios"][1]
            provider = scenario["providers"][0]
            if case == "unknown pool":
                provider["credit_allocations"][0]["pool"] = "missing"
            elif case == "unknown eligible":
                scenario["credit_pools"][0]["eligible_providers"] = ["missing"]
            elif case == "usage exceed":
                provider["meters"][0]["quantity"] = "10"
            elif case == "total exceed":
                scenario["credit_pools"][0]["scope"] = "total"
                provider["fee_amount"] = "0"
                provider["meters"][0]["quantity"] = "10"
            else:
                provider["credit_allocations"].append(copy.deepcopy(provider["credit_allocations"][0]))
            with self.subTest(case=case), self.assertRaises(InputError):
                model(self.input)

    def test_independent_scenario_credit_budgets(self):
        rows = model(self.input)["scenarios"]
        self.assertEqual(rows[1]["credit_pools"][0]["allocated"], "10")
        self.assertEqual(rows[2]["credit_pools"][0]["allocated"], "10")

    def test_zero_rate_and_empty_labor(self):
        scenario = self.input["scenarios"][1]
        scenario["labor"] = []
        provider = scenario["providers"][0]
        provider["credit_allocations"] = []
        provider["fee_amount"] = "0"
        provider["meters"][0]["rate"] = "0"
        row = model(self.input)["scenarios"][1]
        self.assertEqual(row["monthly_cash_estimate"], "0")
        self.assertEqual(row["unpaid_time_valuation"], "0")

    def test_nonfinite_negative_boolean_precision_and_bounds(self):
        for value in (True, "NaN", Decimal("NaN"), Decimal("Infinity"), "-0", -1,
                      "0.0000001", "1000000000001", 1.5, None, []):
            self.setUp()
            self.input["scenarios"][1]["providers"][0]["fee_amount"] = value
            with self.subTest(value=value), self.assertRaises(InputError):
                model(self.input)

    def test_required_identity_units_dates_schema_and_names(self):
        for case in ("currency", "period", "date", "missing rate", "duplicate meter", "empty unit", "bad mode", "bad labor", "extra root", "missing scenario"):
            self.setUp()
            provider = self.input["scenarios"][1]["providers"][0]
            if case == "currency":self.input["currency"] = "usd"
            elif case == "period":self.input["period"] = "year"
            elif case == "date":provider["observed_at"] = "2026-02-30"
            elif case == "missing rate":del provider["meters"][0]["rate"]
            elif case == "duplicate meter":provider["meters"].append(copy.deepcopy(provider["meters"][0]))
            elif case == "empty unit":provider["meters"][0]["unit"] = ""
            elif case == "bad mode":provider["fee_mode"] = "guess"
            elif case == "bad labor":self.input["scenarios"][1]["labor"][0]["kind"] = "maybe"
            elif case == "extra root":self.input["unexpected"] = "yes"
            else:self.input["scenarios"].pop()
            with self.subTest(case=case), self.assertRaises(InputError):
                model(self.input)

    def test_json_limits_duplicate_keys_and_extreme_exponents(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            for value in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1e9999999999999999999999}',
                          '{"x":1e-7}', ' ' * 262145):
                path.write_text(value)
                with self.subTest(value=value[:30]), self.assertRaises(InputError):
                    load_input(path)

    def test_cli_success_safe_error_and_exact_json_decimal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(self.input).replace('"2"', '2.1'))
            out = model(load_input(path))
            self.assertEqual(out["scenarios"][1]["providers"][0]["gross_usage"], "42")
            args = [sys.executable, "-B", "-m", "scripts.calculate", "--input"]
            good = subprocess.run(args + [str(path)], cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(good.returncode, 0)
            self.assertEqual(json.loads(good.stdout)["period"], "month")
            self.assertEqual(good.stderr, "")
            path.write_text('{"x":1e9999999999999999999999}')
            bad = subprocess.run(args + [str(path)], cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(bad.returncode, 2)
            self.assertEqual(bad.stdout, "")
            self.assertNotIn("Traceback", bad.stderr)


if __name__ == "__main__":
    unittest.main()
