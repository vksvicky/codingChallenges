import unittest
from PyQt6.QtWidgets import QApplication
import sys

class TestRubiksCube(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance before tests
        cls.app = QApplication(sys.argv)

    def setUp(self):
        from src.rubiks_cube import RubiksCube
        self.cube = RubiksCube(size=3)

    def tearDown(self):
        # Clean up resources
        self.cube.window.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up QApplication
        cls.app.quit()