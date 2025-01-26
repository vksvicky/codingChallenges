import unittest
from src.nqueens import NQueens

class TestNQueens(unittest.TestCase):
    def setUp(self):
        self.solver = NQueens()

    def test_4_queens(self):
        solutions = self.solver.solve(4)
        self.assertEqual(len(solutions), 2)  # 4x4 board has 2 solutions
        
    def test_8_queens(self):
        solutions = self.solver.solve(8)
        self.assertEqual(len(solutions), 92)  # 8x8 board has 92 solutions
        
    def test_invalid_board_size(self):
        with self.assertRaises(ValueError):
            self.solver.solve(0)
        with self.assertRaises(ValueError):
            self.solver.solve(-1)
            
    def test_solution_validity(self):
        solutions = self.solver.solve(4)
        for board in solutions:
            self.assertTrue(self.solver.is_valid_solution(board))
            
    def test_board_format(self):
        solutions = self.solver.solve(4)
        for board in solutions:
            self.assertEqual(len(board), 4)
            for row in board:
                self.assertEqual(len(row), 4)
                self.assertEqual(row.count('Q'), 1)