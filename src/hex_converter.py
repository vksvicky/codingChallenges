import matplotlib.pyplot as plt
import numpy as np

class HexConverter:
    def to_hex(self, num):
        if num == 0:
            return "0"
            
        hex_chars = "0123456789abcdef"
        result = []
        
        # Handle negative numbers using two's complement (32 bits)
        if num < 0:
            num = (1 << 32) + num
        
        while num:
            result.append(hex_chars[num & 15])  # num & 15 is equivalent to num % 16
            num = num >> 4  # Right shift by 4 is equivalent to num // 16
            
        return "".join(reversed(result))

    def visualize(self, num):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Binary representation
        binary = format(num & ((1 << 32) - 1), '032b')  # 32-bit binary
        self._draw_bits(ax1, binary, "Binary (32-bit)")
        
        # Hex representation
        hex_val = self.to_hex(num)
        hex_padded = hex_val.zfill(8)  # Ensure 8 characters for visualization
        self._draw_hex(ax2, hex_padded, "Hexadecimal")
        
        # Add complexity information
        complexity_text = (
            "Hexadecimal Conversion:\n"
            "Time Complexity: O(log n)\n"
            "Space Complexity: O(1)\n\n"
            f"Input: {num}\n"
            f"Binary: {binary}\n"
            f"Hex: {hex_val}\n"
            "Method: Bitwise operations"
        )
        plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                   bbox=dict(facecolor='lightyellow', alpha=0.8),
                   verticalalignment='center')
        
        plt.tight_layout()
        plt.show()
    
    def _draw_bits(self, ax, binary, title):
        n = len(binary)
        for i, bit in enumerate(binary):
            color = 'lightblue' if bit == '0' else 'lightgreen'
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, color=color))
            ax.text(i + 0.5, 0.5, bit, ha='center', va='center', fontsize=10)
            if (i + 1) % 4 == 0:  # Add separator every 4 bits
                ax.axvline(x=i+1, color='gray', linestyle=':')
        
        ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(-0.5, 1.5)
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    
    def _draw_hex(self, ax, hex_str, title):
        n = len(hex_str)
        for i, char in enumerate(hex_str):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, color='lightyellow'))
            ax.text(i + 0.5, 0.5, char, ha='center', va='center', fontsize=12)
        
        ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(-0.5, 1.5)
        ax.set_title(title)
        ax.set_xticks(range(n))
        ax.set_yticks([])