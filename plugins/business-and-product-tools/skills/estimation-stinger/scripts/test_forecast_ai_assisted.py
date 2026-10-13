"""Boundary and accounting tests for the supplied-input forecasting calculator."""
import copy
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("forecast", HERE / "forecast-ai-assisted.py")
forecast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(forecast)


def fixture():
    return json.loads((HERE.parent / "references/ai-assisted-forecast/example-input.json").read_text())


class ForecastTests(unittest.TestCase):
    def first(self, data):
        return forecast.calculate(data)["scenarios"][0]

    def test_example_and_review_accounting(self):
        row = self.first(fixture())
        self.assertEqual(row["effective_project_hours"], "42")
        self.assertEqual(row["scheduled_owner_hours"], "52.5")
        self.assertEqual(row["working_days"], 18)
        self.assertEqual(row["build_completion_date"], "2026-11-04")
        self.assertEqual(row["direct_cash"], "76.25")
        self.assertEqual(row["owner_time_value"], "1312.50")

    def test_daily_hours_change_calendar_not_owner_effort(self):
        data = fixture()
        slower = self.first(data)
        data["hours_per_day"] = "6"
        faster = self.first(data)
        self.assertLess(faster["working_days"], slower["working_days"])
        self.assertEqual(faster["scheduled_owner_hours"], slower["scheduled_owner_hours"])
        self.assertEqual(faster["build_completion_date"], "2026-10-22")
        self.assertEqual(faster["release_ready_date"], "2026-10-26")

    def test_independent_dependencies_overlap(self):
        data = fixture()
        scenario = data["scenarios"][0]
        scenario["dependencies"] = [{"name": "one", "ready_after_calendar_days": 40}, {"name": "two", "ready_after_calendar_days": 35}]
        row = self.first(data)
        self.assertEqual(row["elapsed_calendar_days"], 40)
        self.assertEqual(row["release_ready_date"], "2026-11-21")
        self.assertEqual(row["recurring_30_day_blocks"], 2)

    def test_weekend_start_and_fraction(self):
        data = fixture()
        data["start_date"] = "2026-10-10"
        data["usable_fraction"] = "1"
        scenario = data["scenarios"][0]
        for field in forecast.EFFORT:
            scenario[field] = "0"
        scenario["engineering_hours"] = "3"
        scenario["dependencies"] = []
        row = self.first(data)
        self.assertEqual(row["working_days"], 1)
        self.assertEqual(row["build_completion_date"], "2026-10-12")
        self.assertEqual(row["elapsed_calendar_days"], 2)

    def test_zero_work_and_wait_only(self):
        data = fixture()
        scenario = data["scenarios"][0]
        for field in forecast.EFFORT:
            scenario[field] = "0"
        scenario["dependencies"] = []
        row = self.first(data)
        self.assertEqual(row["working_days"], 0)
        self.assertEqual(row["recurring_30_day_blocks"], 0)
        self.assertEqual(row["direct_cash"], "20.00")
        scenario["dependencies"] = [{"name": "ready", "ready_after_calendar_days": 30}]
        self.assertEqual(self.first(data)["recurring_30_day_blocks"], 2)

    def test_negative_nonfinite_boolean_and_excess_precision(self):
        for value in ["-1", "NaN", "Infinity", True, 0.5, "1e9999", "1e-100", "0e999999", "invalid"]:
            with self.subTest(value=value):
                data = fixture()
                data["scenarios"][0]["rework_hours"] = value
                with self.assertRaises(ValueError):
                    forecast.calculate(data)

    def test_fraction_daily_and_schema_bounds(self):
        for field, value in [("usable_fraction", "0"), ("usable_fraction", "1.01"), ("hours_per_day", "0"), ("hours_per_day", "25"), ("weekdays", [0, 0]), ("weekdays", [True]), ("weekdays", []), ("start_date", "2026-02-30"), ("start_date", "20261012"), ("scenarios", [])]:
            with self.subTest(field=field, value=value):
                data = fixture()
                data[field] = value
                with self.assertRaises(ValueError):
                    forecast.calculate(data)
        data = fixture()
        data["extra"] = 1
        with self.assertRaises(ValueError):
            forecast.calculate(data)

    def test_missing_duplicate_and_unknown_inputs(self):
        data = fixture()
        del data["scenarios"][0]["verification_hours"]
        with self.assertRaises(ValueError):
            forecast.calculate(data)
        data = fixture()
        data["scenarios"].append(copy.deepcopy(data["scenarios"][0]))
        with self.assertRaises(ValueError):
            forecast.calculate(data)
        for ready in [None, -1, True, 1.5, 36601]:
            data = fixture()
            data["scenarios"][0]["dependencies"][0]["ready_after_calendar_days"] = ready
            with self.assertRaises(ValueError):
                forecast.calculate(data)

    def test_horizon_and_date_overflow(self):
        data = fixture()
        data["hours_per_day"] = "0.000001"
        with self.assertRaises(ValueError):
            forecast.calculate(data)
        data = fixture()
        data["start_date"] = "9999-12-31"
        with self.assertRaises(ValueError):
            forecast.calculate(data)

    def test_decimal_rounding_and_json_numeric_input(self):
        data = fixture()
        scenario = data["scenarios"][0]
        scenario["one_time_cash"] = Decimal("20.005")
        self.assertEqual(self.first(data)["direct_cash"], "76.26")

    def test_cli_rejects_duplicate_keys_and_nonfinite_constants(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            for content in ['{"x":1,"x":2}', '{"x":NaN}', ' ' * 100001]:
                path.write_text(content)
                result = subprocess.run([sys.executable, str(HERE / "forecast-ai-assisted.py"), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn("forecast error:", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_cli_bounds_raw_json_numeric_exponents(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "numeric.json"
            for exponent in ["1e999999999999999999999999999999999999999", "1e-999999999999999999999999999999999999999", "0e999999999999999999999999999999999999999", "1e-13", "1e13"]:
                with self.subTest(exponent=exponent):
                    content = json.dumps(fixture()).replace('"rework_hours": "4"', f'"rework_hours": {exponent}')
                    path.write_text(content)
                    result = subprocess.run([sys.executable, str(HERE / "forecast-ai-assisted.py"), str(path)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("forecast error:", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(result.stdout, "")
            content = json.dumps(fixture()).replace('"one_time_cash": "20"', '"one_time_cash": 20.005')
            path.write_text(content)
            result = subprocess.run([sys.executable, str(HERE / "forecast-ai-assisted.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["scenarios"][0]["direct_cash"], "76.26")


if __name__ == "__main__":
    unittest.main()
