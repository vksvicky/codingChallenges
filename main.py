import sys
from src.pascal_triangle import PascalTriangle
from src.dijkstra import Graph
from src.hanoi import TowerOfHanoi
from src.palindrome import PalindromeChecker
from src.roman import RomanConverter
from src.nqueens import NQueens
from src.string_reversal import StringReversal
from src.perfect_square import PerfectSquare

def run_palindrome():
    checker = PalindromeChecker()
    text = input("Enter text to check for palindrome: ").strip()
    result = checker.is_palindrome(text)
    print(f"\nResult: '{text}' {' IS ' if result else ' IS NOT '} a palindrome")
    checker.visualize(text)

def run_roman():
    converter = RomanConverter()
    while True:
        print("\nRoman Numeral Converter")
        print("1. Number to Roman")
        print("2. Roman to Number")
        print("3. Number to Words")
        print("4. Roman to Words")
        print("5. Back to main menu")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '5':
            break
        elif choice == '1':
            try:
                num = int(input("Enter a number (1-3999): "))
                roman = converter.to_roman(num)
                print(f"Roman numeral: {roman}")
                converter.visualize(number=num)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            try:
                roman = input("Enter a Roman numeral: ").strip()
                num = converter.from_roman(roman)
                print(f"Number: {num}")
                converter.visualize(roman=roman)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '3':
            try:
                num = int(input("Enter a number (1-3999): "))
                words = converter.number_to_words(num)
                print(f"In words: {words}")
                converter.visualize(number=num)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '4':
            try:
                roman = input("Enter a Roman numeral: ").strip()
                words = converter.roman_to_words(roman)
                print(f"In words: {words}")
                converter.visualize(roman=roman)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Invalid option")

def run_nqueens():
    solver = NQueens()
    while True:
        try:
            n = int(input("Enter board size (4-10, default=8): ") or "8")
            if n < 4:
                print("Board size must be at least 4")
                continue
            if n > 10:
                print("Maximum board size is 10")
                continue
                
            delay = float(input("Enter animation delay in seconds (default=1.0): ") or "1.0")
            
            print(f"\nSolving {n}-Queens puzzle...")
            solver.visualize(n, delay)
            break
            
        except ValueError as e:
            print(f"Error: {e}")

def run_pascal_triangle(size):
    pascal = PascalTriangle()
    triangle = pascal.generate(size)
    print(f"Pascal's Triangle (size: {pascal.size}):")
    for row in triangle:
        print(row)
    pascal.plot(size)

def run_hanoi(disks, delay):
        hanoi = TowerOfHanoi()
        print(f"\nSolving Tower of Hanoi with {disks} disks...")
        hanoi.setup(disks)
        hanoi.visualize(delay)

def run_dijkstra():
    try:
        num_nodes = int(input("Enter number of nodes (1-10): ") or "5")
        if num_nodes < 1 or num_nodes > 10:
            print("Number of nodes must be between 1 and 10")
            return
            
        graph = Graph()
        start, end = graph.generate_random_graph(num_nodes)
        
        distance, path = graph.shortest_path(start, end)
        
        print(f"\nGraph with {num_nodes} nodes")
        print(f"Shortest path from {start} to {end}:")
        print(f"Distance: {distance}")
        print(f"Path: {' -> '.join(path)}")
        
        graph.visualize(start, end, path)
        
    except ValueError as e:
        print(f"Error: {e}")

def run_string_reversal():
    reverser = StringReversal()
    text = input("Enter text to reverse: ").strip()
    if text:
        print("\nReversing the string...")
        reverser.visualize(text)
    else:
        print("Please enter a non-empty string")

def run_perfect_square():
    checker = PerfectSquare()
    while True:
        try:
            num = int(input("Enter a number to check if it's a perfect square: "))
            result = checker.is_perfect_square(num)
            print(f"\nResult: {num} {'IS' if result else 'is NOT'} a perfect square")
            checker.visualize(num)
            break
        except ValueError:
            print("Please enter a valid number")

def run_hex_converter():
    converter = HexConverter()
    while True:
        try:
            num = int(input("Enter a 32-bit integer: "))
            if num > 2**31 - 1 or num < -2**31:
                print("Number must be a 32-bit integer")
                continue
            result = converter.to_hex(num)
            print(f"\nHexadecimal: {result}")
            converter.visualize(num)
            break
        except ValueError:
            print("Please enter a valid integer")

def main():
    while True:
        print("\nAlgorithm Visualizer")
        print("1. Pascal's Triangle")
        print("2. Dijkstra's Algorithm")
        print("3. Tower of Hanoi")
        print("4. Palindrome Checker")
        print("5. Roman Numerals")
        print("6. N-Queens Puzzle")
        print("7. String Reversal")
        print("8. Perfect Square")
        print("9. Exit")
        
        choice = input("\nSelect an option (1-9): ").strip()
        
        if choice == '9':
            print("Goodbye!")
            break
            
        if choice == '1':
            while True:
                try:
                    size = int(input("Enter the size of Pascal's Triangle (default=5): ") or "5")
                    if size <= 0:
                        print("Please provide a positive number")
                        continue
                    run_pascal_triangle(size)
                    break
                except ValueError:
                    print("Please enter a valid number")
                    
        elif choice == '2':
            while True:
                try:
                    num_nodes = int(input("Enter number of nodes (1-10, default=5): ") or "5")
                    if num_nodes < 1:
                        print("Please provide a positive number of nodes")
                        continue
                    if num_nodes > 10:
                        print("Maximum 10 nodes supported in this example")
                        num_nodes = 10
                    run_dijkstra()
                    break
                except ValueError:
                    print("Please enter a valid number")
                    
        elif choice == '3':
            while True:
                try:
                    disks = int(input("Enter number of disks (default=3): ") or "3")
                    delay = float(input("Enter animation delay in seconds (default=0.5): ") or "0.5")
                    if disks <= 0:
                        print("Please provide a positive number of disks")
                        continue
                    run_hanoi(disks, delay)
                    break
                except ValueError:
                    print("Please enter valid numbers")
                    
        elif choice == '4':
            run_palindrome()
                    
        elif choice == '5':
            run_roman()

        elif choice == '6':
            run_nqueens()
        
        elif choice == '7':
            run_string_reversal() 
            
        elif choice == '8':
            run_perfect_square()

        elif choice == '8':
            run_perfect_square()
                    
        else:
            print("Invalid option. Please select 1-10")

if __name__ == "__main__":
    main()