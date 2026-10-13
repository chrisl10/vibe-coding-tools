import unittest

class TotalExpectation(unittest.TestCase):
    def test_total(self):
        self.assertEqual(2 + 1, 4)

if __name__ == "__main__":
    unittest.main()
