
# Algorithm Visualizer

  

  

An interactive Python application that visualizes various algorithms and mathematical concepts with matplotlib animations.

  

  

## Features

  

  

-  **Pascal's Triangle**: Generate and visualize Pascal's triangle of any size

  

-  **Dijkstra's Algorithm**: Visualize shortest path finding in random graphs

  

-  **Tower of Hanoi**: Animated solution for the Tower of Hanoi puzzle

  

-  **Palindrome Checker**: Visual representation of palindrome verification

  

-  **Roman Numerals**: Convert between numbers, Roman numerals, and words

  

-  **N-Queens Puzzle**: Visualize solutions to the N-Queens problem

  

-  **String Reversal**: Animate in-place string reversal process

  

-  **Perfect Square**: Visual verification of perfect square numbers

  

-  **FizzBuzz**: Visualize number sequence with divisibility rules for 3 and 5

  

## Requirements

  

  

- Python 3.7+

  

- matplotlib

  

- numpy

  

  

## Installation

  

  
  

# Clone the repository

  

```

git clone https://github.com/yourusername/algorithm-visualizer.git

```

  

# Install dependencies

  

```

pip install matplotlib numpy

```

  

## Usage

  

1. Run the main program:

  

```

python main.py

```

  

2. Select an algorithm from the menu (1-9):

  

```Algorithm Visualizer

  

1. Pascal's Triangle

  

2. Dijkstra's Algorithm

  

3. Tower of Hanoi

  

4. Palindrome Checker

  

5. Roman Numerals

  

6. N-Queens Puzzle

  

7. String Reversal

  

8. Perfect Square

  

9. FizzBuzz

  

10. Exit

  

```

  
  

3. Follow the prompts to input parameters:

  

  

- Pascal's Triangle: Enter size (rows)

  

- Dijkstra's Algorithm: Enter number of nodes

  

- Tower of Hanoi: Enter number of disks and animation delay

  

- Palindrome Checker: Enter text to check

  

- Roman Numerals: Choose conversion type and enter number/numeral

  

- N-Queens: Enter board size

  

- String Reversal: Enter text to reverse

  

- Perfect Square: Enter number to check

  

- FizzBuzz: Enter number to check

  

## Testing

  

Run all tests using:

```

python run_tests.py

```

  

## Algorithm Details

  

### Pascal's Triangle

  

- Description : Generates a triangular array where each number is the sum of the two numbers above it

  

- Applications : Binomial expansions, probability calculations

  

- Complexity : Time O(n²), Space O(n²)

  

- Visualization : Color-coded triangle showing number relationships

  

### Dijkstra's Algorithm

  

- Description : Finds shortest paths between nodes in a weighted graph

  

- Applications : GPS navigation, network routing

  

- Complexity : Time O(V² + E), Space O(V)

  

- Visualization : Dynamic graph with highlighted paths and distances

  

### Tower of Hanoi

  

- Description : Recursive solution to move disks between three rods

  

- Applications : Recursive problem solving, backup rotation schemes

  

- Complexity : Time O(2ⁿ), Space O(n)

  

- Visualization : Animated disk movements with step counter

  

### Palindrome Checker

  

- Description : Verifies if text reads the same forwards and backwards

  

- Applications : String processing, data validation

  

- Complexity : Time O(n), Space O(1)

  

- Visualization : Character-by-character comparison animation

  

### Roman Numerals

  

- Description : Converts between decimal numbers and Roman numerals

  

- Applications : Historical dating, traditional numbering

  

- Complexity : Time O(1), Space O(1)

  

- Visualization : Step-by-step conversion process

  

### N-Queens Puzzle

  

- Description : Places N queens on an NxN chessboard without conflicts

  

- Applications : Constraint satisfaction, backtracking algorithms

  

- Complexity : Time O(n!), Space O(n)

  

- Visualization : All valid solutions with queen placements

  

### String Reversal

  

- Description : In-place reversal of character array

  

- Applications : String manipulation, palindrome creation

  

- Complexity : Time O(n), Space O(1)

  

- Visualization : Two-pointer swap animation

  

### Perfect Square Checker

  

- Description : Determines if a number is a perfect square

  

- Applications : Mathematical verification, geometry

  

- Complexity : Time O(log n), Space O(1)

  

- Visualization : Square root plotting with result indication

  

### FizzBuzz

- Description : Converts numbers to Fizz (divisible by 3), Buzz (divisible by 5), or FizzBuzz (divisible by both)

- Applications : Programming interviews, number theory, divisibility rules

- Complexity : Time O(n), Space O(n)

- Visualization : Color-coded sequence with divisibility indicators

- Numbers: Regular integers (lightblue)

- Fizz: Numbers divisible by 3 (lightcoral)

- Buzz: Numbers divisible by 5 (lightyellow)

- FizzBuzz: Numbers divisible by both 3 and 5 (lightgreen)

  

## Contributing

  

1. Fork the repository

  

2. Create your feature branch:

  

```

  

git checkout -b feature/new-algorithm

  

```

  

3. Implement your changes:

  

- Add new algorithm class in src/

  

- Create test file in tests/

  

- Update main.py with new menu option

  

- Add visualization using matplotlib

  

- Document complexity and usage

  

4. Commit your changes:

  

```

  

git commit -m 'Add new algorithm: Algorithm Name'

  

```

  

5. Push to your fork:

  

```

  

git push origin feature/new-algorithm

  

```

  

6. Submit a Pull Request

  

  

### Contribution Guidelines

  

- Follow PEP 8 style guide

  

- Include unit tests

  

- Add visualisation for algorithm steps

  

- Document time and space complexity

  

- Update README.md with algorithm details

  
  
  

# Algorithm Visualizer

  

An interactive Python application that visualizes various algorithms and mathematical concepts with matplotlib animations.

  
  
  

## Features

-  **Pascal's Triangle**: Generate and visualize Pascal's triangle of any size

-  **Dijkstra's Algorithm**: Visualise shortest path finding in random graphs

-  **Tower of Hanoi**: Animated solution for the Tower of Hanoi puzzle

-  **Palindrome Checker**: Visual representation of palindrome verification

-  **Roman Numerals**: Convert between numbers, Roman numerals, and words
 
-  **N-Queens Puzzle**: Visualise solutions to the N-Queens problem
 
-  **String Reversal**: Animate in-place string reversal process

-  **Perfect Square**: Visual verification of perfect square numbers
  
-  **FizzBuzz**: Visualise number sequence with divisibility rules for 3 and 5
  

## Requirements

- Python 3.7+

- matplotlib

- numpy
  

# Installation

  
## Clone the repository

```

git clone https://github.com/yourusername/algorithm-visualizer.git

```

  

## Install dependencies

  

```

pip install matplotlib numpy

```

  

## Usage

  

1. Run the main program:

  

```

python main.py

```

  

2. Select an algorithm from the menu (1-9):

  

```

Algorithm Visualizer

1. Pascal's Triangle

  

2. Dijkstra's Algorithm

  

3. Tower of Hanoi

  

4. Palindrome Checker

  

5. Roman Numerals

  

6. N-Queens Puzzle

  

7. String Reversal

  

8. Perfect Square

  

9. Exit

```

  

3. Follow the prompts to input parameters:

```

- Pascal's Triangle: Enter size (rows)
- Dijkstra's Algorithm: Enter number of nodes
- Tower of Hanoi: Enter number of disks and animation delay
- Palindrome Checker: Enter text to check
- Roman Numerals: Choose conversion type and enter number/numeral
- N-Queens: Enter board size
- String Reversal: Enter text to reverse
- Perfect Square: Enter number to check
- FizzBuzz: Enter number to check
```

  

## Algorithm Details

  

### Pascal's Triangle

  

- Description : Generates a triangular array where each number is the sum of the two numbers above it

  

- Applications : Binomial expansions, probability calculations

  

- Complexity : Time O(n²), Space O(n²)

  

- Visualization : Color-coded triangle showing number relationships

  

### Dijkstra's Algorithm

  

- Description : Finds shortest paths between nodes in a weighted graph

  

- Applications : GPS navigation, network routing

  

- Complexity : Time O(V² + E), Space O(V)

  

- Visualization : Dynamic graph with highlighted paths and distances

  

### Tower of Hanoi

  

- Description : Recursive solution to move disks between three rods

  

- Applications : Recursive problem solving, backup rotation schemes

  

- Complexity : Time O(2ⁿ), Space O(n)

  

- Visualization : Animated disk movements with step counter

  

### Palindrome Checker

  

- Description : Verifies if text reads the same forwards and backwards

  

- Applications : String processing, data validation

  

- Complexity : Time O(n), Space O(1)

  

- Visualization : Character-by-character comparison animation

  

### Roman Numerals

  

- Description : Converts between decimal numbers and Roman numerals

  

- Applications : Historical dating, traditional numbering

  

- Complexity : Time O(1), Space O(1)

  

- Visualization : Step-by-step conversion process

  

### N-Queens Puzzle

  

- Description : Places N queens on an NxN chessboard without conflicts

  

- Applications : Constraint satisfaction, backtracking algorithms

  

- Complexity : Time O(n!), Space O(n)

  

- Visualization : All valid solutions with queen placements

  

### String Reversal

  

- Description : In-place reversal of character array

  

- Applications : String manipulation, palindrome creation

  

- Complexity : Time O(n), Space O(1)

  

- Visualization : Two-pointer swap animation

  

### Perfect Square Checker

  

- Description : Determines if a number is a perfect square

  

- Applications : Mathematical verification, geometry

  

- Complexity : Time O(log n), Space O(1)

  

- Visualization : Square root plotting with result indication]


### FizzBuzz
- Description: Classic programming problem that outputs numbers from 1 to n, replacing:
  - Numbers divisible by 3 with "Fizz"
  - Numbers divisible by 5 with "Buzz"
  - Numbers divisible by both 3 and 5 with "FizzBuzz"
  - Other numbers remain unchanged
- Applications:
  - Divisibility rule demonstration
  - Pattern recognition exercises
- Complexity:
  - Time: O(n) - Linear traversal through numbers
  - Space: O(n) - Storing the result sequence
- Visualization:
  - Color-coded sequence representation:
    - Regular numbers: Lightblue boxes
    - Fizz (÷3): Lightcoral boxes
    - Buzz (÷5): Lightyellow boxes
    - FizzBuzz (÷3&5): Lightgreen boxes
  - Divisibility indicators above each number
  - Grid layout with number sequence

  

## Contributing

  

1. Fork the repository

  

2. Create your feature branch:

  

```

git checkout -b feature/new-algorithm

```

  

3. Implement your changes:

  

- Add new algorithm class in src/

  

- Create test file in tests/

  

- Update main.py with new menu option

  

- Add visualization using matplotlib

  

- Document complexity and usage

  

4. Commit your changes:

  

```

git commit -m 'Add new algorithm: Algorithm Name'

```

  

5. Push to your fork:

  

```

git push origin feature/new-algorithm

```

  

6. Submit a Pull Request

  

### Contribution Guidelines

  

- Follow PEP 8 style guide

  

- Include unit tests

  

- Add visualization for algorithm steps

  

- Document time and space complexity

  

- Update README.md with algorithm details

  

## License

  
  

The MIT License (MIT)

  

Copyright (c) 2015 Chris Kibble

  

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.