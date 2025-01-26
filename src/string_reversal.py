import matplotlib.pyplot as plt
import numpy as np
import time

class StringReversal:
    def reverse(self, s):
        left, right = 0, len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
        return s

    def visualize(self, text):
        s = list(text)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Original string
        self._draw_string(ax1, s, "Original String")
        
        # Reverse the string
        self.reverse(s)
        
        # Reversed string
        self._draw_string(ax2, s, "Reversed String")
        
        # Add complexity information
        complexity_text = (
            "String Reversal:\n"
            "Time Complexity: O(n)\n"
            "Space Complexity: O(1)\n\n"
            f"String Length: {len(s)}\n"
            "Method: Two-pointer swap"
        )
        plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                   bbox=dict(facecolor='lightyellow', alpha=0.8),
                   verticalalignment='center')
        
        plt.tight_layout()
        plt.show()
    
    def _draw_string(self, ax, s, title):
        n = len(s)
        for i, char in enumerate(s):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, color='lightblue'))
            ax.text(i + 0.5, 0.5, char, ha='center', va='center', fontsize=12)
        
        ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(-0.5, 1.5)
        ax.set_title(title)
        ax.grid(True)
        ax.set_xticks(range(n))
        ax.set_yticks([])