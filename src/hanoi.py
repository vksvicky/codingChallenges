import matplotlib.pyplot as plt
import numpy as np
import time

class TowerOfHanoi:
    def __init__(self):
        self.pegs = [[], [], []]
        self.num_disks = 0
        self.moves = []
        
    def setup(self, num_disks):
        if num_disks <= 0:
            raise ValueError("Number of disks must be positive")
        self.num_disks = num_disks
        self.pegs = [list(range(num_disks, 0, -1)), [], []]
        self.moves = []
        
    def move_disk(self, from_peg, to_peg):
        if self.pegs[from_peg]:
            disk = self.pegs[from_peg].pop()
            self.pegs[to_peg].append(disk)
            self.moves.append((from_peg, to_peg))
            
    def solve(self):
        self.moves = []
        self._solve_recursive(self.num_disks, 0, 2, 1)
        return self.moves
        
    def _solve_recursive(self, n, source, target, auxiliary):
        if n > 0:
            self._solve_recursive(n-1, source, auxiliary, target)
            self.move_disk(source, target)
            self._solve_recursive(n-1, auxiliary, target, source)
            
    def visualize(self, delay=0.5):
        fig, ax = plt.subplots(figsize=(10, 5))
        plt.ion()
        
        # Setup initial state
        self.setup(self.num_disks)
        
        # Define colors for each peg
        peg_colors = ['#FF9999', '#99FF99', '#9999FF']
        
        # Add complexity information
        complexity_text = (
            "Tower of Hanoi Complexity:\n"
            f"Time: O(2^n)\n"
            f"Space: O(n)\n\n"
            f"n (disks): {self.num_disks}\n"
            f"Total moves: {2**self.num_disks - 1}\n\n"
            "Current Move:\n"
            "Time: O(1)\n"
            "Space: O(1)"
        )
        complexity_box = plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                                   bbox=dict(facecolor='lightyellow', alpha=0.8),
                                   verticalalignment='center')
        
        def draw_state():
            ax.clear()
            disk_height = 0.15  # Thinner disks
            base_height = 0.1
            max_height = self.num_disks + 1  # Total height for pegs
            
            # Calculate positions from bottom up
            positions = {i: [] for i in range(3)}  # Store y-positions for each peg
            
            # Draw base line
            ax.plot([-1, 3], [base_height, base_height], 'k-', linewidth=3)
            
            # Draw pegs first
            for i in range(3):
                ax.plot([i, i], [base_height, max_height], 'k-', linewidth=2)
            
            # Draw disks from bottom to top
            for i, peg in enumerate(self.pegs):
                current_height = base_height
                for disk in peg:
                    width = disk * 0.35  # Smaller disk width
                    ax.fill([i-width/2, i+width/2, i+width/2, i-width/2],
                           [current_height, current_height, 
                            current_height+disk_height, current_height+disk_height],
                           peg_colors[i], alpha=0.8,
                           edgecolor='black', linewidth=1)
                    current_height += disk_height * 1.2  # Add small gap between disks
            
            # Update display settings
            ax.set_xlim(-1, 3)
            ax.set_ylim(0, max_height)
            ax.set_title(f"Tower of Hanoi - Move {len(self.moves)}")
            
            # Update complexity info
            current_move = len(self.moves)
            move_info = (
                "Tower of Hanoi Complexity:\n"
                f"Time: O(2^n)\n"
                f"Space: O(n)\n\n"
                f"n (disks): {self.num_disks}\n"
                f"Total moves: {2**self.num_disks - 1}\n\n"
                f"Current Move: {current_move}\n"
                f"Progress: {current_move/(2**self.num_disks - 1)*100:.1f}%\n"
                "Move Complexity: O(1)"
            )
            complexity_box.set_text(move_info)
            plt.pause(delay)
            
        # Solve and animate
        moves = self.solve()
        self.setup(self.num_disks)
        
        draw_state()
        for from_peg, to_peg in moves:
            self.move_disk(from_peg, to_peg)
            draw_state()
            
        plt.ioff()
        plt.show()