import matplotlib.pyplot as plt
import numpy as np

class PerfectSquare:
    def is_perfect_square(self, num):
        if num < 0:
            return False
        if num == 0:
            return True
            
        left, right = 1, num
        
        while left <= right:
            mid = (left + right) // 2
            square = mid * mid
            
            if square == num:
                return True
            elif square < num:
                left = mid + 1
            else:
                right = mid - 1
                
        return False

    def visualize(self, num):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create visualization data
        is_square = self.is_perfect_square(num)
        root = int(np.sqrt(num)) if num >= 0 else 0
        
        if num >= 0:
            x = np.linspace(0, root + 2, 100)
            y = x * x
            ax.plot(x, y, 'b-', label='y = x²')
            
            # Mark the point
            if is_square:
                ax.plot(root, num, 'go', markersize=10, label=f'({root}, {num})')
            else:
                ax.plot(root, num, 'ro', markersize=10, label=f'({root}, {num})')
                
            ax.grid(True)
            ax.legend()
            ax.set_title(f"Number {num} {'IS' if is_square else 'is NOT'} a Perfect Square")
            
            # Add complexity information
            complexity_text = (
                "Perfect Square Check:\n"
                "Time Complexity: O(log n)\n"
                "Space Complexity: O(1)\n\n"
                f"Input: {num}\n"
                f"Method: Binary Search\n"
                f"Result: {'Perfect Square' if is_square else 'Not Perfect Square'}"
            )
            plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                       bbox=dict(facecolor='lightyellow', alpha=0.8),
                       verticalalignment='center')
            
        plt.show()