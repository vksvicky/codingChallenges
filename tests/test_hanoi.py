import unittest
from src.hanoi import TowerOfHanoi

class TestTowerOfHanoi(unittest.TestCase):
    def setUp(self):
        self.hanoi = TowerOfHanoi()

    def test_initial_state(self):
        self.hanoi.setup(3)
        self.assertEqual(self.hanoi.pegs[0], [3, 2, 1])
        self.assertEqual(self.hanoi.pegs[1], [])
        self.assertEqual(self.hanoi.pegs[2], [])

    def test_invalid_disk_count(self):
        with self.assertRaises(ValueError):
            self.hanoi.setup(0)
        with self.assertRaises(ValueError):
            self.hanoi.setup(-1)

    def test_move_disk(self):
        self.hanoi.setup(3)
        self.hanoi.move_disk(0, 2)
        self.assertEqual(self.hanoi.pegs[0], [3, 2])
        self.assertEqual(self.hanoi.pegs[2], [1])

    def test_solve(self):
        self.hanoi.setup(3)
        moves = self.hanoi.solve()
        self.assertEqual(self.hanoi.pegs[0], [])
        self.assertEqual(self.hanoi.pegs[1], [])
        self.assertEqual(self.hanoi.pegs[2], [3, 2, 1])
        self.assertEqual(len(moves), 7)  # 2^n - 1 moves for n disks

if __name__ == '__main__':
    unittest.main()