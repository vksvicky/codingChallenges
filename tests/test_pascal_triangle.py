import unittest
from src.pascal_triangle import PascalTriangle

class TestPascalTriangle(unittest.TestCase):
    def setUp(self):
        self.pascal = PascalTriangle()

    def test_first_row(self):
        self.assertEqual(self.pascal.generate(1), [[1]])

    def test_second_row(self):
        self.assertEqual(self.pascal.generate(2), [[1], [1, 1]])

    def test_third_row(self):
        self.assertEqual(self.pascal.generate(3), [[1], [1, 1], [1, 2, 1]])

    def test_fifth_row(self):
        expected = [
            [1],
            [1, 1],
            [1, 2, 1],
            [1, 3, 3, 1],
            [1, 4, 6, 4, 1]
        ]
        self.assertEqual(self.pascal.generate(5), expected)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.pascal.generate(0)
        with self.assertRaises(ValueError):
            self.pascal.generate(-1)

if __name__ == '__main__':
    unittest.main()