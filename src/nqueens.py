import matplotlib.pyplot as plt
import numpy as np
import time

class NQueens:
    def __init__(self):
        self.count = 0
        self.solutions = []

    def _create_board(self, queens, n):
        board = []
        for row in range(n):
            if row < len(queens):
                # Create a row with a queen at the specified column
                board_row = '.' * queens[row] + 'Q' + '.' * (n - queens[row] - 1)
            else:
                # Fill remaining rows with empty spaces
                board_row = '.' * n
            board.append(board_row)
        return board
        
    def solve(self, n):
        if n <= 0:
            raise ValueError("Board size must be positive")
        
        self.count = 0
        self.solutions = []
        
        # Initialize helper sets for faster checking
        cols = set()
        pos_diag = set()  # r + c
        neg_diag = set()  # r - c
        current_queens = []
        
        def backtrack(row):
            if row == n:
                self.count += 1
                self.solutions.append(self._create_board(current_queens, n))
                return
            
            for col in range(n):
                if col in cols or \
                   (row + col) in pos_diag or \
                   (row - col) in neg_diag:
                    continue
                    
                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)
                current_queens.append(col)
                
                backtrack(row + 1)
                
                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)
                current_queens.pop()
        
        backtrack(0)
        return self.solutions
    
    def get_solution_count(self, n):
        self.solve(n)
        return self.count

    def visualize(self, n, delay=0.5):
        solutions = self.solve(n)
        num_solutions = self.count
        
        # Calculate grid dimensions for subplots
        grid_size = int(np.ceil(np.sqrt(num_solutions)))
        fig = plt.figure(figsize=(15, 15))
        
        print(f"\nFound {num_solutions} distinct solutions for {n}-Queens puzzle")
        
        # Add complexity information
        complexity_text = (
            "N-Queens Problem:\n"
            f"Board Size: {n}x{n}\n"
            f"Total Solutions: {num_solutions}\n\n"
            "Time Complexity: O(n!)\n"
            "Space Complexity: O(n)"
        )
        plt.figtext(0.02, 0.02, complexity_text, fontsize=10,
                   bbox=dict(facecolor='lightyellow', alpha=0.8))
        
        # Create and display all solutions
        for idx, board in enumerate(solutions):
            ax = fig.add_subplot(grid_size, grid_size, idx + 1)
            
            # Create chess board pattern
            board_img = np.zeros((n, n))
            board_img[1::2, 0::2] = 1
            board_img[0::2, 1::2] = 1
            
            # Display board
            ax.imshow(board_img, cmap='gray')
            
            # Place queens
            for i, row in enumerate(board):
                j = row.index('Q')
                ax.plot(j, i, 'ro', markersize=20 - n)  # Adjust queen size based on board size
            
            # Add grid
            ax.grid(True)
            ax.set_xticks(np.arange(-0.5, n, 1))
            ax.set_yticks(np.arange(-0.5, n, 1))
            
            # Remove axis labels
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            
            ax.set_title(f"Solution {idx + 1}")
        
        plt.tight_layout()
        plt.show()