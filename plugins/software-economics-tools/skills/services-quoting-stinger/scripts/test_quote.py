import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("quote", HERE / "quote.py")
quote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quote)


def fixture():
    return {"scenarios": [{"name": "website", "basis": "Hypothetical supplied USD costs, 2026-10-07", "currency": "USD", "period": "project", "pricing_mode": "markup", "owner_hours": "40", "owner_cost_per_hour": "50", "subcontractor_cost": "0", "fixed_cost": "200", "contingency_fraction": ".1", "pricing_fraction": ".25", "pass_through_cost": "0"}]}


class QuoteTests(unittest.TestCase):
    def row(self, data):
        return quote.calculate(data)["scenarios"][0]

    def test_website_markup(self):
        row = self.row(fixture())
        self.assertEqual(row["service_cost_basis"], "2420.00")
        self.assertEqual(row["service_price"], "3025.00")
        self.assertEqual(row["planned_surplus"], "605.00")
        self.assertEqual(row["effective_service_margin"], "0.2")

    def test_app_margin_and_pass_through(self):
        data = fixture();s = data["scenarios"][0]
        s.update(owner_hours="120", owner_cost_per_hour="60", subcontractor_cost="1000", contingency_fraction=".15", pricing_mode="margin", pass_through_cost="100")
        row = self.row(data)
        self.assertEqual(row["service_price"], "12880.00")
        self.assertEqual(row["proposed_total"], "12980.00")
        self.assertEqual(row["baseline_cash"], "1300.00")

    def test_maintenance_and_scope_delta(self):
        data = fixture();s = data["scenarios"][0]
        s.update(owner_hours="4", fixed_cost="40", period="month")
        self.assertEqual(self.row(data)["proposed_total"], "330.00")
        s.update(owner_hours="6")
        self.assertEqual(self.row(data)["proposed_total"], "467.50")
        s.update(owner_hours="8", fixed_cost="0", period="project")
        self.assertEqual(self.row(data)["proposed_total"], "550.00")

    def test_zero_margin_is_undefined(self):
        data = fixture();s = data["scenarios"][0]
        s.update(owner_hours="0", fixed_cost="0")
        self.assertIsNone(self.row(data)["effective_service_margin"])

    def test_bounds_and_ambiguous_inputs(self):
        for field, value in [("owner_hours", None), ("owner_hours", True), ("owner_hours", "-1"), ("owner_hours", "NaN"), ("owner_hours", "0e99999999"), ("contingency_fraction", "1.01"), ("pricing_fraction", "11"), ("period", "year")]:
            data = fixture();data["scenarios"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):quote.calculate(data)
        data = fixture();s = data["scenarios"][0];s.update(pricing_mode="margin", pricing_fraction="1")
        with self.assertRaises(ValueError):quote.calculate(data)
        data = fixture();del data["scenarios"][0]["basis"]
        with self.assertRaises(ValueError):quote.calculate(data)
        data = fixture();data["scenarios"].append(dict(data["scenarios"][0]))
        with self.assertRaises(ValueError):quote.calculate(data)
        data = fixture();data["scenarios"][0]["owner_opportunity_cost"] = "2000"
        with self.assertRaises(ValueError):quote.calculate(data)
        with self.assertRaises(ValueError):quote.calculate({"scenarios": []})

    def test_cli_extreme_exponents_duplicate_and_normal_decimal(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "quote.json"
            for raw in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":1e99999999999999999999999999999999999}', '{"x":1e-99999999999999999999999999999999999}', ' '*100001]:
                path.write_text(raw)
                result = subprocess.run([sys.executable, str(HERE / "quote.py"), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn("quote error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
            path.write_text(json.dumps(fixture()).replace('"fixed_cost": "200"', '"fixed_cost": 200.005'))
            result = subprocess.run([sys.executable, str(HERE / "quote.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "PROPOSED_NOT_ACCEPTED")


if __name__ == "__main__":unittest.main()
