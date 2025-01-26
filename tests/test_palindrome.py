import unittest
from src.palindrome import PalindromeChecker

class TestPalindromeChecker(unittest.TestCase):
    def setUp(self):
        self.checker = PalindromeChecker()

    def test_simple_palindrome(self):
        self.assertTrue(self.checker.is_palindrome("radar"))
        self.assertTrue(self.checker.is_palindrome("level"))
        
    def test_non_palindrome(self):
        self.assertFalse(self.checker.is_palindrome("hello"))
        self.assertFalse(self.checker.is_palindrome("python"))
        
    def test_case_sensitivity(self):
        self.assertTrue(self.checker.is_palindrome("Racecar"))
        self.assertTrue(self.checker.is_palindrome("Madam"))
        
    def test_spaces_and_punctuation(self):
        self.assertTrue(self.checker.is_palindrome("A man a plan a canal Panama"))
        self.assertTrue(self.checker.is_palindrome("Was it a car or a cat I saw?"))
        
    def test_empty_and_single(self):
        self.assertTrue(self.checker.is_palindrome(""))
        self.assertTrue(self.checker.is_palindrome("a"))

if __name__ == '__main__':
    unittest.main()