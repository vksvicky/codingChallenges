import unittest
from unittest.mock import Mock, patch
import numpy as np
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.cube_solver import CubeSolver

class TestCubeSolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])
            cls.owns_app = True
        else:
            cls.owns_app = False

    def setUp(self):
        # Create mock cube
        self.mock_cube = Mock()
        self.mock_cube.size = 4
        self.mock_cube.state = np.zeros((6, 4, 4), dtype=int)
        self.mock_cube.window = Mock()
        self.mock_cube.app = Mock()
        
        # Create solver instance
        self.solver = CubeSolver(self.mock_cube)

    def test_initialization(self):
        """Test solver initialization"""
        self.assertEqual(self.solver.cube, self.mock_cube)
        self.assertEqual(len(self.solver.move_stack), 0)
        self.assertIsInstance(self.solver.inverse_moves, dict)

    def test_add_move(self):
        """Test adding moves to stack"""
        moves = ['R', 'U', "F'", '2L']
        for move in moves:
            self.solver.add_move(move)
        self.assertEqual(self.solver.move_stack, moves)

    def test_reset(self):
        """Test solver reset"""
        # Add some moves
        self.solver.move_stack = ['R', 'U', 'F']
        self.mock_cube.solution_moves = ['F', 'U', 'R']
        
        # Reset solver
        self.solver.reset()
        
        self.assertEqual(len(self.solver.move_stack), 0)
        self.assertEqual(len(self.mock_cube.solution_moves), 0)

    def test_solve_empty_stack(self):
        """Test solving with empty move stack"""
        with patch('builtins.print') as mock_print:
            self.solver.solve()
            mock_print.assert_called_once_with("Stack is empty, nothing to solve", flush=True)

    def test_solve_basic_moves(self):
        """Test solving basic moves"""
        # Add some moves
        moves = ['R', 'U', 'F']
        for move in moves:
            self.solver.add_move(move)
        
        # Solve
        self.solver.solve()
        
        # Check solution moves
        expected_solution = ["F'", "U'", "R'"]
        self.assertEqual(self.mock_cube.solution_moves, expected_solution)

    def test_solve_layer_moves(self):
        """Test solving layer moves"""
        # Add layer moves
        moves = ['2R', '3U', '2F']
        for move in moves:
            self.solver.add_move(move)
        
        # Solve
        self.solver.solve()
        
        # Check solution moves
        expected_solution = ["2F'", "3U'", "2R'"]
        self.assertEqual(self.mock_cube.solution_moves, expected_solution)

    @patch('PyQt6.QtCore.QTimer.singleShot')
    def test_solve_animation(self, mock_timer):
        """Test solve animation"""
        self.solver.add_move('R')
        self.solver.solve()
        
        # Check window and app updates
        self.mock_cube.window.update.assert_called()
        self.mock_cube.app.processEvents.assert_called()
        mock_timer.assert_called_with(100, unittest.mock.ANY)

    # def test_solve_centers(self):
    #     """Test center solving for 4x4 cube"""
    #     # Create a mock state with unsolved centers
    #     mock_state = np.zeros((6, 4, 4), dtype=int)
    #     for face in range(6):
    #         mock_state[face] = np.full((4, 4), face)
    #         # Make center pieces wrong
    #         mock_state[face, 1:3, 1:3] = (face + 1) % 6
        
    #     # Setup mock cube with necessary attributes and methods
    #     self.mock_cube.state = mock_state
    #     self.mock_cube.size = 4
    #     self.mock_cube.moves = {
    #         'F': Mock(return_value=True),
    #         'B': Mock(return_value=True),
    #         'R': Mock(return_value=True),
    #         'L': Mock(return_value=True),
    #         'U': Mock(return_value=True),
    #         'D': Mock(return_value=True)
    #     }
        
    #     # Setup move tracking
    #     self.mock_cube.solution_moves = []
    #     def track_move(move):
    #         self.mock_cube.solution_moves.append(move)
    #         # Simulate state change
    #         if len(self.mock_cube.solution_moves) > 4:  # After some moves
    #             mock_state[0, 1:3, 1:3] = 0  # Fix centers on first face
    #         return True
            
    #     self.mock_cube.make_move = Mock(side_effect=track_move)
        
    #     # Add necessary methods for center solving
    #     def get_center_color(face):
    #         return face  # Return the expected color for each face
    #     self.mock_cube.get_center_color = Mock(side_effect=get_center_color)
        
    #     # Mock state checking
    #     def is_centers_solved():
    #         return len(self.mock_cube.solution_moves) > 8  # Solve after enough moves
    #     self.mock_cube.is_centers_solved = Mock(side_effect=is_centers_solved)
        
    #     # Call solve_centers
    #     self.solver.solve_centers()
        
    #     # Verify moves were made
    #     self.assertGreater(len(self.mock_cube.solution_moves), 0)
    #     self.assertTrue(any('F' in move for move in self.mock_cube.solution_moves))
    #     self.assertTrue(any('R' in move for move in self.mock_cube.solution_moves))

    def test_solve_edges(self):
        """Test edge pairing for 4x4 cube"""
        self.solver.solve_edges()
        # Verify moves were added to stack
        self.assertGreater(len(self.solver.move_stack), 0)

    def test_solve_3x3_centers(self):
        """Test center solving for 3x3 cube"""
        self.mock_cube.size = 3
        self.solver.solve_centers()
        # Verify no moves were added for 3x3
        self.assertEqual(len(self.solver.move_stack), 0)

    def test_solve_error_handling(self):
        """Test error handling during solve"""
        # Setup mock to raise exception
        self.mock_cube.make_move.side_effect = Exception("Test error")
        
        # Add a move and try to solve
        self.solver.add_move('R')
        self.solver.solve()
        
        # Verify error handling
        self.assertEqual(len(self.solver.move_stack), 0)
        self.assertEqual(len(self.mock_cube.solution_moves), 0)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'owns_app') and cls.owns_app:
            cls.app.quit()

if __name__ == '__main__':
    unittest.main()