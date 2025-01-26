import matplotlib.pyplot as plt

class RomanConverter:
    def __init__(self):
        self.roman_values = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]
        
        self.number_words = {
            0: "", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
            11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
            16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
            20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
            60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"
        }

    def number_to_words(self, num):
        if not 0 < num < 4000:
            raise ValueError("Number must be between 1 and 3999")
            
        if num < 20:
            return self.number_words[num]
            
        if num < 100:
            tens = (num // 10) * 10
            ones = num % 10
            return self.number_words[tens] + ("-" + self.number_words[ones] if ones else "")
            
        if num < 1000:
            hundreds = num // 100
            rest = num % 100
            result = self.number_words[hundreds] + " hundred"
            if rest:
                result += " " + self.number_to_words(rest)
            return result
            
        thousands = num // 1000
        rest = num % 1000
        result = self.number_words[thousands] + " thousand"
        if rest:
            result += " " + self.number_to_words(rest)
        return result

    def to_roman(self, num):
        if not 0 < num < 4000:
            raise ValueError("Number must be between 1 and 3999")
            
        result = ""
        for value, symbol in self.roman_values:
            while num >= value:
                result += symbol
                num -= value
        return result

    def from_roman(self, roman):
        values = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
                 'C': 100, 'D': 500, 'M': 1000}
        
        result = 0
        prev_value = 0
        
        for char in reversed(roman.upper()):
            if char not in values:
                raise ValueError("Invalid Roman numeral")
            curr_value = values[char]
            if curr_value >= prev_value:
                result += curr_value
            else:
                result -= curr_value
            prev_value = curr_value
            
        if self.to_roman(result) != roman.upper():
            raise ValueError("Invalid Roman numeral")
            
        return result

    def roman_to_words(self, roman):
        return self.number_to_words(self.from_roman(roman))

    def visualize(self, number=None, roman=None):
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.ion()
        
        if number is not None:
            roman = self.to_roman(number)
            words = self.number_to_words(number)
        elif roman is not None:
            number = self.from_roman(roman)
            words = self.roman_to_words(roman)
        
        # Display conversion
        ax.text(0.5, 0.8, f"Number: {number}", ha='center', va='center', fontsize=14)
        ax.text(0.5, 0.6, f"Roman: {roman}", ha='center', va='center', fontsize=14)
        ax.text(0.5, 0.4, "↕", ha='center', va='center', fontsize=20)
        ax.text(0.5, 0.2, f"Words: {words}", ha='center', va='center', fontsize=14)
        
        # Add complexity information
        complexity_text = (
            "Roman Numeral Conversion:\n"
            "Time Complexity: O(1)\n"
            "Space Complexity: O(1)\n\n"
            "Valid Range: 1-3999\n"
            "Symbols: I, V, X, L, C, D, M\n\n"
            "Basic Values:\n"
            "I = 1    V = 5\n"
            "X = 10   L = 50\n"
            "C = 100  D = 500\n"
            "M = 1000"
        )
        plt.figtext(0.85, 0.5, complexity_text, fontsize=10,
                   bbox=dict(facecolor='lightyellow', alpha=0.8),
                   verticalalignment='center')
        
        ax.axis('off')
        plt.show()