import unittest
from src.string_reversal import StringReversal

class TestStringReversal(unittest.TestCase):
    def setUp(self):
        self.reverser = StringReversal()

    def test_basic_reversal(self):
        s = ["h", "e", "l", "l", "o"]
        self.reverser.reverse(s)
        self.assertEqual(s, ["o", "l", "l", "e", "h"])

    def test_palindrome(self):
        s = ["r", "a", "c", "e", "c", "a", "r"]
        self.reverser.reverse(s)
        self.assertEqual(s, ["r", "a", "c", "e", "c", "a", "r"])

    def test_single_char(self):
        s = ["a"]
        self.reverser.reverse(s)
        self.assertEqual(s, ["a"])

    def test_empty_string(self):
        s = []
        self.reverser.reverse(s)
        self.assertEqual(s, [])