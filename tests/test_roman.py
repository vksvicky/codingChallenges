import unittest
from src.roman import RomanConverter

class TestRomanConverter(unittest.TestCase):
    def setUp(self):
        self.converter = RomanConverter()

    def test_basic_numerals(self):
        self.assertEqual(self.converter.to_roman(1), "I")
        self.assertEqual(self.converter.to_roman(5), "V")
        self.assertEqual(self.converter.to_roman(10), "X")
        self.assertEqual(self.converter.to_roman(50), "L")
        self.assertEqual(self.converter.to_roman(100), "C")
        self.assertEqual(self.converter.to_roman(500), "D")
        self.assertEqual(self.converter.to_roman(1000), "M")

    def test_complex_numbers(self):
        self.assertEqual(self.converter.to_roman(4), "IV")
        self.assertEqual(self.converter.to_roman(9), "IX")
        self.assertEqual(self.converter.to_roman(49), "XLIX")
        self.assertEqual(self.converter.to_roman(99), "XCIX")
        self.assertEqual(self.converter.to_roman(999), "CMXCIX")

    def test_from_roman(self):
        self.assertEqual(self.converter.from_roman("IV"), 4)
        self.assertEqual(self.converter.from_roman("IX"), 9)
        self.assertEqual(self.converter.from_roman("XLIX"), 49)
        self.assertEqual(self.converter.from_roman("XCIX"), 99)
        self.assertEqual(self.converter.from_roman("CMXCIX"), 999)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.converter.to_roman(0)
        with self.assertRaises(ValueError):
            self.converter.to_roman(4000)
        with self.assertRaises(ValueError):
            self.converter.from_roman("ABC")

    def test_number_to_words(self):
        self.assertEqual(self.converter.number_to_words(1), "one")
        self.assertEqual(self.converter.number_to_words(21), "twenty-one")
        self.assertEqual(self.converter.number_to_words(999), "nine hundred ninety-nine")
        self.assertEqual(self.converter.number_to_words(3999), "three thousand nine hundred ninety-nine")

    def test_roman_to_words(self):
        self.assertEqual(self.converter.roman_to_words("I"), "one")
        self.assertEqual(self.converter.roman_to_words("XXI"), "twenty-one")
        self.assertEqual(self.converter.roman_to_words("CMXCIX"), "nine hundred ninety-nine")
        self.assertEqual(self.converter.roman_to_words("MMMCMXCIX"), "three thousand nine hundred ninety-nine")