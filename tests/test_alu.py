import unittest

from alu import sqrt

MAX_CONST = (1 << 30) - 1
MAX_CONST_ROOT = 32767


class TestSqrt(unittest.TestCase):

    def check_pairs(self, pairs):
        for value, root in pairs:
            with self.subTest(value=value):
                self.assertEqual(sqrt(value), root)

    def test_perfect_squares(self):
        self.check_pairs([(0, 0), (1, 1), (4, 2), (49, 7), (144, 12)])

    def test_rounds_down(self):
        self.check_pairs([(2, 1), (10, 3), (99, 9), (101, 10)])

    def test_largest_constant(self):
        self.check_pairs([(MAX_CONST, MAX_CONST_ROOT)])


if __name__ == "__main__":
    unittest.main()