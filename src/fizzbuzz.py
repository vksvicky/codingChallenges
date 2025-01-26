import matplotlib.pyplot as plt
import numpy as np

class FizzBuzz:
    def generate(self, n):
        if n <= 0:
            raise ValueError("Number must be positive")
            
        result = []
        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 == 0:
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))
        return result

    def visualize(self, n):
        result = self.generate(n)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create visualization
        for i, value in enumerate(result, 1):
            color = 'lightblue'
            title = f"Number: {i}"
            
            if value == "FizzBuzz":
                color = 'lightgreen'
                title = f"{i} is divisible by both 3 and 5"
            elif value == "Fizz":
                color = 'lightcoral'
                title = f"{i} is divisible by 3"
            elif value == "Buzz":
                color = 'lightyellow'
                title = f"{i} is divisible by 5"
                
            ax.add_patch(plt.Rectangle((i-0.5, -0.5), 1, 1, fill=True, color=color))
            ax.text(i, 0, value, ha='center', va='center', fontsize=10)
            
            # Add title above each number
            ax.text(i, 0.5, title, ha='center', va='bottom', fontsize=8, rotation=45)
        
        # Add grid and labels
        ax.grid(True)
        ax.set_xlim(0, n+1)
        ax.set_ylim(-1, 1)
        ax.set_title(f"FizzBuzz Sequence (n={n})")
        
        # Add complexity information
        complexity_text = (
            "FizzBuzz:\n"
            "Time Complexity: O(n)\n"
            "Space Complexity: O(n)\n\n"
            "Color Legend:\n"
            "■ Numbers (lightblue)\n"
            "■ Fizz ÷3 (lightcoral)\n"
            "■ Buzz ÷5 (lightyellow)\n"
            "■ FizzBuzz ÷3&5 (lightgreen)"
        )
        plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                   bbox=dict(facecolor='white', alpha=0.8),
                   verticalalignment='center')
        
        plt.show()