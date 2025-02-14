import unittest
from unittest.mock import patch
import time
import random
from src.santa_workshop import SantaWorkshop

class TestRandomSleep(unittest.TestCase):
    def setUp(self):
        self.workshop = SantaWorkshop()

    @patch('time.sleep')
    @patch('random.randint')
    def test_random_sleep_basic(self, mock_randint, mock_sleep):
        # Test basic sleep functionality
        mock_randint.return_value = 100
        self.workshop.random_sleep(50, 150)
        mock_randint.assert_called_once_with(50, 150)
        mock_sleep.assert_called_once_with(0.1)  # 100ms = 0.1s

    @patch('time.sleep')
    @patch('random.randint')
    def test_random_sleep_with_scale(self, mock_randint, mock_sleep):
        # Test sleep with scaling factor
        mock_randint.return_value = 100
        self.workshop.random_sleep(50, 150, scale=2.0)
        mock_randint.assert_called_once_with(50, 150)
        mock_sleep.assert_called_once_with(0.05)  # (100ms / 2.0) = 0.05s

    @patch('time.sleep')
    @patch('random.randint')
    def test_random_sleep_min_equals_max(self, mock_randint, mock_sleep):
        # Test when min equals max
        mock_randint.return_value = 75
        self.workshop.random_sleep(75, 75)
        mock_randint.assert_called_once_with(75, 75)
        mock_sleep.assert_called_once_with(0.075)

    @patch('time.sleep')
    @patch('random.randint')
    def test_random_sleep_zero_scale(self, mock_randint, mock_sleep):
        # Test with zero scale factor
        mock_randint.return_value = 100
        self.workshop.random_sleep(50, 150, scale=0.0)
        mock_randint.assert_called_once_with(50, 150)
        # With zero scale, it defaults to scale=1.0
        mock_sleep.assert_called_once_with(0.1)  # 100ms = 0.1s

    @patch('time.sleep')
    @patch('random.randint')
    def test_random_sleep_small_scale(self, mock_randint, mock_sleep):
        # Test with very small scale factor
        mock_randint.return_value = 100
        self.workshop.random_sleep(50, 150, scale=0.5)
        mock_randint.assert_called_once_with(50, 150)
        mock_sleep.assert_called_once_with(0.2)  # (100ms / 0.5) = 200ms = 0.2s

if __name__ == '__main__':
    unittest.main()