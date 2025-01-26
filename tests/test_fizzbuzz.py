import unittest
from src.fizzbuzz import FizzBuzz

class TestFizzBuzz(unittest.TestCase):
    def setUp(self):
        self.fizzbuzz = FizzBuzz()

    def test_fizz(self):
        result = self.fizzbuzz.generate(3)
        self.assertEqual(result[2], "Fizz")

    def test_buzz(self):
        result = self.fizzbuzz.generate(5)
        self.assertEqual(result[4], "Buzz")

    def test_fizzbuzz(self):
        result = self.fizzbuzz.generate(15)
        self.assertEqual(result[14], "FizzBuzz")

    def test_number(self):
        result = self.fizzbuzz.generate(2)
        self.assertEqual(result[1], "2")

    def test_sequence(self):
        result = self.fizzbuzz.generate(15)
        expected = ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", 
                   "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
        self.assertEqual(result, expected)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.fizzbuzz.generate(0)
        with self.assertRaises(ValueError):
            self.fizzbuzz.generate(-1)