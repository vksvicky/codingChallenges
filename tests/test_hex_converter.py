import unittest
from src.hex_converter import HexConverter

class TestHexConverter(unittest.TestCase):
    def setUp(self):
        self.converter = HexConverter()

    def test_positive_numbers(self):
        self.assertEqual(self.converter.to_hex(26), "1a")
        self.assertEqual(self.converter.to_hex(0), "0")
        self.assertEqual(self.converter.to_hex(16), "10")
        self.assertEqual(self.converter.to_hex(255), "ff")

    def test_negative_numbers(self):
        self.assertEqual(self.converter.to_hex(-1), "ffffffff")
        self.assertEqual(self.converter.to_hex(-16), "fffffff0")
        self.assertEqual(self.converter.to_hex(-26), "ffffffe6")

    def test_large_numbers(self):
        self.assertEqual(self.converter.to_hex(2147483647), "7fffffff")
        self.assertEqual(self.converter.to_hex(-2147483648), "80000000")