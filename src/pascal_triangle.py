import matplotlib.pyplot as plt
import numpy as np
import time

class PascalTriangle:
    def __init__(self):
        self._size = 0
        self._triangle = []

    def generate(self, num_rows):
        if num_rows <= 0:
            raise ValueError("Number of rows must be positive")
        
        self._triangle = [[1]]
        for i in range(1, num_rows):
            prev_row = self._triangle[-1]
            new_row = [1]
            
            for j in range(1, i):
                new_row.append(prev_row[j-1] + prev_row[j])
            
            new_row.append(1)
            self._triangle.append(new_row)
        
        self._size = num_rows
        return self._triangle

    @property
    def size(self):
        return self._size

    @property
    def triangle(self):
        return self._triangle
    
    def plot(self, num_rows):
        triangle = self.generate(num_rows)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_aspect('equal')
        
        # Add explanation text area
        explanation = plt.figtext(0.02, 0.02, '', fontsize=10, wrap=True,
                                bbox=dict(facecolor='white', alpha=0.8))
        
        # Add complexity annotation area on the right
        complexity_text = plt.figtext(0.85, 0.5, '', fontsize=10, 
                                    bbox=dict(facecolor='lightyellow', alpha=0.8),
                                    verticalalignment='center')
        
        for i, row in enumerate(triangle):
            y = num_rows - i - 1
            row_width = len(row)
            start_x = -(row_width - 1) / 2
            
            # Update explanation and complexity
            if i == 0:
                exp_text = "First row always starts with 1"
            else:
                exp_text = f"Row {i+1}: Each number is the sum of the two numbers above it"
            explanation.set_text(exp_text)
            
            # Show complexity for current row
            complexity = f"Row {i+1} Complexity:\nTime: O({i+1})\nSpace: O(1)"
            complexity_text.set_text(complexity)
            
            for j, val in enumerate(row):
                x = start_x + j
                circle = plt.Circle((x, y), 0.4, fill=False)
                ax.add_patch(circle)
                
                # If not first row, draw arrows from parent numbers
                if i > 0 and j > 0:
                    prev_y = y + 1
                    prev_x1 = -(len(triangle[i-1])-1)/2 + (j-1)
                    prev_x2 = prev_x1 + 1
                    plt.arrow(prev_x1, prev_y-0.3, x-prev_x1, y-prev_y+0.7, 
                            head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                    plt.arrow(prev_x2, prev_y-0.3, x-prev_x2, y-prev_y+0.7,
                            head_width=0.1, head_length=0.1, fc='gray', ec='gray', alpha=0.3)
                
                ax.text(x, y, str(val), ha='center', va='center')
                plt.pause(0.5)  # Add delay for animation
        
        ax.set_xlim(-(num_rows-1), num_rows-1)
        ax.set_ylim(-1, num_rows)
        ax.axis('off')
        plt.title("Pascal's Triangle Construction")
        plt.show()