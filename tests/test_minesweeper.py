import unittest
from unittest.mock import Mock, patch
from src.minesweeper import MinesweeperSolver

class TestMinesweeperSolver(unittest.TestCase):
    def setUp(self):
        # Initialize with character board for all tests
        self.board_1 = [
            ['B', '1', 'X'],
            ['1', '2', '1'],
            ['M', '1', 'B']
        ]
        self.solver = MinesweeperSolver(self.board_1)
        
        # Initialize with unrevealed board for click tests
        self.board_2 = [
            ["E","E","E"],
            ["E","M","E"],
            ["E","E","E"]
        ]
        self.solver_2 = MinesweeperSolver(self.board_2)

    # Update test_solve_safe_cell to use valid board values
    def test_solve_safe_cell(self):
        """Test revealing a safe cell"""
        board = [["E","E","E"],
                ["E","E","E"],
                ["E","E","E"]]
        solver = MinesweeperSolver(board)
        self.assertTrue(solver.solve(0, 0))
        self.assertIn((0, 0), solver.visited)

    def test_solve_mine(self):
        """Test revealing a mine"""
        board = [["E","M","E"],
                ["E","E","E"],
                ["E","E","E"]]
        solver = MinesweeperSolver(board)
        self.assertFalse(solver.solve(0, 1))
        self.assertIn((0, 1), solver.visited)

    def test_initialization(self):
        """Test solver initialization"""
        self.assertEqual(self.solver.rows, 3)
        self.assertEqual(self.solver.cols, 3)
        self.assertEqual(len(self.solver.visited), 0)

    def test_valid_position(self):
        """Test position validation"""
        self.assertTrue(self.solver._is_valid(0, 0))
        self.assertTrue(self.solver._is_valid(2, 2))
        self.assertFalse(self.solver._is_valid(-1, 0))
        self.assertFalse(self.solver._is_valid(3, 3))

    def test_solve_safe_cell(self):
        """Test revealing a safe cell"""
        self.assertTrue(self.solver.solve(0, 0))
        self.assertIn((0, 0), self.solver.visited)

    def test_solve_mine(self):
        """Test revealing a mine"""
        self.assertFalse(self.solver.solve(0, 2))
        self.assertIn((0, 2), self.solver.visited)

    def test_recursive_reveal(self):
        """Test recursive revealing of empty cells"""
        board = [["E","E","E"],
                ["E","E","E"],
                ["E","E","E"]]
        solver = MinesweeperSolver(board)
        solver.solve(1, 1)  # Click center cell
        
        # Check that clicked cell is visited
        self.assertIn((1, 1), solver.visited)
        
        # Test another cell
        solver.solve(2, 2)
        self.assertIn((2, 2), solver.visited)

    def test_reveal_mine(self):
        """Test revealing a mine cell"""
        board = [["E","E","E"],
                ["E","M","E"],
                ["E","E","E"]]
        solver = MinesweeperSolver(board)
        result = solver.click(1, 1)  # Use click instead of solve
        self.assertEqual(result[1][1], 'X')

    # Update remaining tests to use click method
    def test_reveal_empty_no_adjacent_mines(self):
        """Test revealing an empty cell with no adjacent mines"""
        board = [["E","E","E"],
                ["E","E","E"],
                ["E","E","E"]]
        solver = MinesweeperSolver(board)
        result = solver.click(1, 1)
        self.assertEqual(result[1][1], 'B')

    def test_reveal_empty_with_adjacent_mines(self):
        """Test revealing an empty cell with adjacent mines"""
        board = [["M","E","E"],
                ["E","E","E"],
                ["E","E","E"]]
        solver = MinesweeperSolver(board)
        result = solver.click(1, 1)
        self.assertEqual(result[1][1], '1')

    def test_recursive_reveal_large(self):
        """Test recursive revealing of empty cells"""
        board = [["E","E","E","E"],
                ["E","E","M","E"],
                ["E","E","E","E"]]
        solver = MinesweeperSolver(board)
        result = solver.click(0, 0)
        
        # Check immediate neighbors of click position
        self.assertEqual(result[0][0], 'B')  # Clicked cell
        self.assertEqual(result[0][1], '1')  # Right neighbor
        self.assertEqual(result[1][0], 'B')  # Bottom neighbor
        
        # Check cells near mine
        self.assertEqual(result[1][1], '1')  # Cell with one adjacent mine
        
        # Verify full expected board state
        expected = [['B', '1', 'E', 'E'],
                   ['B', '1', 'M', 'E'],
                   ['B', '1', 'E', 'E']]
        self.assertEqual(result, expected)

    def test_example_1(self):
        """Test the first example from the problem statement"""
        board = [["E","E","E","E","E"],
                ["E","E","M","E","E"],
                ["E","E","E","E","E"],
                ["E","E","E","E","E"]]
        solver = MinesweeperSolver(board)
        result = solver.click(3, 0)
        expected = [["B","1","E","1","B"],
                   ["B","1","M","1","B"],
                   ["B","1","1","1","B"],
                   ["B","B","B","B","B"]]
        self.assertEqual(result, expected)

    def test_example_2(self):
        """Test the second example from the problem statement"""
        board = [["B","1","E","1","B"],
                ["B","1","M","1","B"],
                ["B","1","1","1","B"],
                ["B","B","B","B","B"]]
        solver = MinesweeperSolver(board)
        result = solver.click(1, 2)
        expected = [["B","1","E","1","B"],
                   ["B","1","X","1","B"],
                   ["B","1","1","1","B"],
                   ["B","B","B","B","B"]]
        self.assertEqual(result, expected)

    def test_empty_board(self):
        """Test handling of empty board"""
        board = []
        solver = MinesweeperSolver(board)
        with self.assertRaises(ValueError):
            solver.click(0, 0)

    def test_invalid_click(self):
        """Test clicking outside board boundaries"""
        board = [["E","E"],["E","E"]]
        solver = MinesweeperSolver(board)
        with self.assertRaises(ValueError):
            solver.click(2, 2)

    def test_corner_reveal(self):
        """Test revealing from corner position"""
        board = [["E","M"],
                ["E","E"]]
        solver = MinesweeperSolver(board)
        result = solver.click(0, 0)
        self.assertEqual(result[0][0], '1')

    def test_multiple_adjacent_mines(self):
        """Test cell with multiple adjacent mines"""
        board = [["M","M","M"],
                ["M","E","M"],
                ["M","M","M"]]
        solver = MinesweeperSolver(board)
        result = solver.click(1, 1)
        self.assertEqual(result[1][1], '8')

    def test_already_revealed_cell(self):
        """Test clicking on already revealed cell"""
        board = [["E","1","E"],  # Changed 'B' to 'E' for initial click
                ["E","E","E"],
                ["E","E","E"]]
        solver = MinesweeperSolver(board)
        
        # First click to reveal the cell
        result = solver.click(0, 0)
        self.assertEqual(result[0][0], 'B')  # Verify first click reveals as 'B'
        
        # Try clicking again on the same cell (this should raise ValueError)
        with self.assertRaises(ValueError):
            solver.click(0, 0)

    @patch('matplotlib.pyplot')
    def test_visualization_components(self, mock_plt):
        """Test all components of visualization"""
        # Setup mock for get_fignums and gca
        mock_plt.get_fignums.return_value = []
        mock_ax = Mock()
        mock_plt.gca.return_value = mock_ax
        
        board = [["E","M"],["E","E"]]  # Simple 2x2 board
        self.solver.visualize(board, "Test Board")
        
        # Verify matplotlib function calls
        mock_plt.clf.assert_called_once()
        mock_plt.figure.assert_called_once_with(figsize=(8, 8))
        mock_plt.grid.assert_called_once_with(True)
        mock_plt.title.assert_called_once_with("Test Board")
        mock_plt.axis.assert_called_once_with('equal')
        
        # Verify Rectangle patches were added
        expected_patch_calls = 4  # One for each cell
        self.assertEqual(mock_ax.add_patch.call_count, expected_patch_calls)
        
        # Verify plot calls for beveled effect (4 lines per unrevealed cell)
        expected_plot_calls = 16  # 4 unrevealed cells * 4 lines each
        self.assertEqual(mock_plt.plot.call_count, expected_plot_calls)

    def test_minesweeper_constraints(self):
        """Test board constraints and validation"""
        # Test valid board dimensions
        board = [['E', 'E', 'E'], ['E', 'M', 'E'], ['E', 'E', 'E']]
        solver = MinesweeperSolver(board)
        self.assertEqual(solver.rows, 3)
        self.assertEqual(solver.cols, 3)
        
        # Test valid cell content
        board_valid = [['E', 'M', 'E'], ['E', 'M', 'E']]
        solver = MinesweeperSolver(board_valid)  # Should not raise error
        # Test invalid click position
        with self.assertRaises(ValueError):
            solver.click(3, 0)
        
        # Test click on revealed cell
        board = [['B', 'E', 'E'], ['E', 'M', 'E'], ['E', 'E', 'E']]
        solver = MinesweeperSolver(board)
        with self.assertRaises(ValueError):
            solver.click(0, 0)

if __name__ == '__main__':
    unittest.main()