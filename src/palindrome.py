class PalindromeChecker:
    def is_palindrome(self, text):
        # Remove spaces and punctuation, convert to lowercase
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        return cleaned_text == cleaned_text[::-1]
    
    def visualize(self, text):
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Clean the text for checking
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        is_pal = cleaned_text == cleaned_text[::-1]
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Display original text
        ax.text(0.5, 0.8, f'Original: "{text}"', 
                ha='center', va='center', fontsize=12)
        
        # Display cleaned text
        ax.text(0.5, 0.6, f'Cleaned: "{cleaned_text}"', 
                ha='center', va='center', fontsize=12)
        
        # Display reversed text
        ax.text(0.5, 0.4, f'Reversed: "{cleaned_text[::-1]}"', 
                ha='center', va='center', fontsize=12)
        
        # Display result
        result = "IS" if is_pal else "IS NOT"
        color = 'green' if is_pal else 'red'
        ax.text(0.5, 0.2, f'This text {result} a palindrome', 
                ha='center', va='center', fontsize=14, color=color)
        
        # Add complexity information
        complexity_text = (
            "Palindrome Check Complexity:\n"
            "Time: O(n)\n"
            "Space: O(n)\n\n"
            f"Text length: {len(text)}\n"
            f"Cleaned length: {len(cleaned_text)}"
        )
        plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                    bbox=dict(facecolor='lightyellow', alpha=0.8),
                    verticalalignment='center')
        
        ax.axis('off')
        plt.show()