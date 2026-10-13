"""Owned synthetic exercise. No user imports, files, network or discovery."""
import io
import json
import platform
import unittest

def remaining(booked):
    if type(booked) is not int or not 0 <= booked <= 10:
        raise ValueError("booked must be an integer from 0 through 10")
    return 10 - booked

def extra_seat(booked):
    return remaining(booked) + 1

def clamp(booked):
    if type(booked) is not int:
        raise ValueError("wrong type")
    return 10 - max(0, min(10, booked))

def accept_bool(booked):
    if not isinstance(booked, int) or not 0 <= booked <= 10:
        raise ValueError("wrong domain")
    return 10 - booked

def suite(candidate):
    class Contract(unittest.TestCase):
        def test_exact_examples(self):
            for value, expected in [(0, 10), (1, 9), (9, 1), (10, 0)]:
                with self.subTest(value=value):
                    self.assertEqual(candidate(value), expected)
        def test_invalid_domain(self):
            for value in [-1, 11, True, 1.5, "1", None]:
                with self.subTest(value=value):
                    with self.assertRaises(ValueError):
                        candidate(value)
        def test_changed_booking(self):
            for value in range(10):
                with self.subTest(value=value):
                    self.assertEqual(candidate(value + 1), candidate(value) - 1)
    return unittest.defaultTestLoader.loadTestsFromTestCase(Contract)

def main():
    receipts = []
    for name, candidate, expected, expected_failures in [("correct", remaining, True, 0), ("extra-seat", extra_seat, False, 4), ("clamp", clamp, False, 2), ("accept-bool", accept_bool, False, 1)]:
        output = io.StringIO()
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite(candidate))
        receipts.append({"candidate": name, "expected_pass": expected, "actual_pass": result.wasSuccessful(), "test_methods": result.testsRun, "assertion_cases": 20, "expected_failure_count": expected_failures, "failures": len(result.failures), "errors": len(result.errors), "output": output.getvalue()})
        if result.wasSuccessful() != expected or len(result.failures) != expected_failures or result.errors:
            print(json.dumps({"status": "UNEXPECTED_RESULT", "receipts": receipts}, indent=2))
            return 1
    print(json.dumps({"status": "PASS", "python": platform.python_version(), "platform": platform.platform(), "scope": "owned synthetic contract only", "learner_understanding": "PENDING", "receipts": receipts}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
