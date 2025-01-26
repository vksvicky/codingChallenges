import unittest
from src.perfect_square import PerfectSquare

class TestPerfectSquare(unittest.TestCase):
    def setUp(self):
        self.checker = PerfectSquare()

    def test_perfect_squares(self):
        self.assertTrue(self.checker.is_perfect_square(16))
        self.assertTrue(self.checker.is_perfect_square(25))
        self.assertTrue(self.checker.is_perfect_square(100))
        self.assertTrue(self.checker.is_perfect_square(0))

    def test_non_perfect_squares(self):
        self.assertFalse(self.checker.is_perfect_square(14))
        self.assertFalse(self.checker.is_perfect_square(26))
        self.assertFalse(self.checker.is_perfect_square(99))

    def test_large_numbers(self):
        self.assertTrue(self.checker.is_perfect_square(10000))
        self.assertFalse(self.checker.is_perfect_square(10001))

    def test_negative_numbers(self):
        self.assertFalse(self.checker.is_perfect_square(-16))
        self.assertFalse(self.checker.is_perfect_square(-4))