import unittest
from unittest.mock import Mock, patch
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QColor
import sys
from src.rubiks_cube import RubiksCube
from src.cube_solver import CubeSolver

class TestRubiksCube(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication for all tests
        cls.qapp = QApplication.instance()
        if cls.qapp is None:
            cls.qapp = QApplication([])
            cls.owns_qapp = True
        else:
            cls.owns_qapp = False

    def setUp(self):
        # Create mocks
        self.app_patcher = patch('src.rubiks_cube.QApplication')
        self.window_patcher = patch('src.rubiks_cube.QMainWindow')
        self.solver_patcher = patch('src.rubiks_cube.CubeSolver')
        
        # Start patches
        self.mock_app = self.app_patcher.start()
        self.mock_window = self.window_patcher.start()
        self.mock_solver = self.solver_patcher.start()
        
        # Configure QApplication mock
        self.mock_app.instance.return_value = self.qapp
        self.mock_app.return_value = self.qapp
        
        # Create cube instance
        self.cube = RubiksCube()

    def tearDown(self):
        # Stop all patches
        self.app_patcher.stop()
        self.window_patcher.stop()
        self.solver_patcher.stop()
        self.cube = None

    @classmethod
    def tearDownClass(cls):
        # Clean up QApplication if we created it
        if cls.owns_qapp:
            cls.qapp.quit()

    def test_initialization(self):
        """Test basic initialization"""
        self.assertEqual(self.cube.size, 3)
        self.assertEqual(self.cube.state.shape, (6, 3, 3))
        self.assertEqual(len(self.cube.moves_to_solve), 0)
        self.mock_solver.assert_called_once_with(self.cube)
        self.mock_app.assert_called_once_with(sys.argv)
        self.mock_window.assert_called_once()

    def test_custom_size(self):
        """Test custom size initialization"""
        sizes = [2, 4, 5, 6]
        for size in sizes:
            with self.subTest(size=size):
                cube = RubiksCube(size=size)
                self.assertEqual(cube.size, size)
                self.assertEqual(cube.state.shape, (6, size, size))

    def test_invalid_sizes(self):
        """Test invalid size handling"""
        invalid_sizes = [-1, 0, 1, 7]  # Added 7 as it's beyond valid range
        for size in invalid_sizes:
            with self.subTest(size=size):
                with self.assertRaisesRegex(ValueError, r"Cube size must be between 2 and 6"):
                    RubiksCube(size=size)

    def test_initial_state(self):
        """Test initial cube state"""
        for face in range(6):
            with self.subTest(face=face):
                expected = np.full((3, 3), face)
                np.testing.assert_array_equal(self.cube.state[face], expected)

    def test_colors(self):
        """Test color initialization"""
        expected_colors = {
            0: 'white',
            1: 'yellow',
            2: 'red',
            3: 'orange',
            4: 'blue',
            5: 'green'
        }
        for face, color in expected_colors.items():
            with self.subTest(face=face, color=color):
                self.assertEqual(self.cube.colors[face].name(), QColor(color).name())

    def test_moves(self):
        """Test moves initialization"""
        expected_moves = ['U', 'D', 'L', 'R', 'F', 'B']
        self.assertEqual(sorted(self.cube.moves.keys()), sorted(expected_moves))
        for move in self.cube.moves.values():
            self.assertTrue(callable(move))

if __name__ == '__main__':
    unittest.main()