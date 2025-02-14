class MinesweeperSolver:
    def __init__(self, board):
        self.board = [row[:] for row in board]  # Create a copy of the board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0
        self.visited = set()

    def click(self, row, col):
        """Handle click at given position and return updated board"""
        # Validate click position
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("Click position out of bounds")
            
        # Validate clicked cell type
        if self.board[row][col] not in ['M', 'E']:
            raise ValueError("Invalid click: cell must be 'M' or 'E'")
            
        # Rest of the click logic remains the same
        if self.rows == 0:
            return []
            
        if not self._is_valid(row, col):
            raise IndexError("Click position out of bounds")

        if self.board[row][col] == 'M':
            self.board[row][col] = 'X'
            return self.board

        if self.board[row][col] == 'E':
            self._reveal(row, col)

        return self.board

    def _reveal(self, row, col):
        """Recursively reveal cells"""
        if not self._is_valid(row, col) or self.board[row][col] not in ['E']:
            return

        # Count adjacent mines
        mines = self.count_adjacent_mines(row, col)
        
        # Mark current cell
        self.board[row][col] = 'B' if mines == 0 else str(mines)
        
        # If empty cell, reveal all adjacent cells
        if mines == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    next_row, next_col = row + dr, col + dc
                    if self._is_valid(next_row, next_col) and self.board[next_row][next_col] == 'E':
                        self._reveal(next_row, next_col)

    def count_adjacent_mines(self, row, col):
        """Count number of adjacent mines"""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self._is_valid(r, c) and self.board[r][c] in ['M', 'X']:
                    count += 1
        return count

    def _is_valid(self, row, col):
        """Check if position is within board boundaries"""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def visualize(self, board, title="Minesweeper Board"):
        """Visualize the current state of the board"""
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, PathPatch
        from matplotlib.path import Path
        
        plt.clf()
        if not plt.get_fignums():
            plt.figure(figsize=(8, 8))
        
        ax = plt.gca()
        
        # Define symbols using ASCII characters
        emojis = {
            'M': '⊗',    # Unrevealed Mine (circled X)
            'E': '',     # Unrevealed Empty
            'B': '',     # Revealed Blank
            'X': '✸',    # Revealed Mine (burst)
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8'
        }
        
        # Text colors for numbers and symbols
        number_colors = {
            'M': 'black',
            'X': 'red',
            '1': 'blue',
            '2': 'green',
            '3': 'red',
            '4': 'purple',
            '5': 'maroon',
            '6': 'turquoise',
            '7': 'black',
            '8': 'gray'
        }
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                cell = board[i][j]
                
                # Create beveled square effect
                if cell in ['E', 'M']:
                    # Unrevealed cell - raised effect
                    rect = Rectangle((j, len(board)-i-1), 1, 1, 
                                  facecolor='#C0C0C0', 
                                  edgecolor='#808080')
                    ax.add_patch(rect)
                    # Add highlight and shadow
                    plt.plot([j, j+1], [len(board)-i-1, len(board)-i-1], 'w-', lw=2)
                    plt.plot([j, j], [len(board)-i-1, len(board)-i], 'w-', lw=2)
                    plt.plot([j+1, j+1], [len(board)-i-1, len(board)-i], 'gray', lw=1)
                    plt.plot([j, j+1], [len(board)-i, len(board)-i], 'gray', lw=1)
                else:
                    # Revealed cell - flat effect
                    rect = Rectangle((j, len(board)-i-1), 1, 1, 
                                  facecolor='#E0E0E0', 
                                  edgecolor='#808080')
                    ax.add_patch(rect)
                
                # Add text/symbols
                if cell in number_colors:
                    plt.text(j+0.5, len(board)-i-0.5, cell, 
                            color=number_colors[cell],
                            ha='center', va='center', 
                            fontweight='bold', fontsize=14)
                elif cell in ['M', 'X']:
                    plt.text(j+0.5, len(board)-i-0.5, emojis[cell], 
                            ha='center', va='center', fontsize=12)
        
        plt.grid(True)
        plt.axis('equal')  # Changed from ax.set_aspect('equal')
        ax.set_xlim(-0.1, len(board[0])+0.1)
        ax.set_ylim(-0.1, len(board)+0.1)
        ax.axis('off')
        plt.title(title)
        plt.draw()
        plt.pause(0.1)

    def solve(self, row, col):
        """Recursively reveal cells starting from given position"""
        if not self._is_valid(row, col) or (row, col) in self.visited:
            return
        
        self.visited.add((row, col))
        
        # If current cell is a mine, game over
        if self.board[row][col] == 'X':
            return False
        
        # If current cell is empty (0), reveal adjacent cells
        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.solve(row + dr, col + dc)
        
        return True