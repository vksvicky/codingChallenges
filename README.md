# Algorithm Visualizer

An interactive Python application that visualizes various algorithms, mathematical concepts, and puzzles with PyQt6 and matplotlib animations.

## Features

- **Pascal's Triangle**: Generate and visualize Pascal's triangle of any size
- **Dijkstra's Algorithm**: Visualize shortest path finding in random graphs
- **Tower of Hanoi**: Animated solution for the Tower of Hanoi puzzle
- **Palindrome Checker**: Visual representation of palindrome verification
- **Roman Numerals**: Convert between numbers, Roman numerals, and words
- **N-Queens Puzzle**: Visualize solutions to the N-Queens problem
- **String Reversal**: Animate in-place string reversal process
- **Perfect Square**: Visual verification of perfect square numbers
- **FizzBuzz**: Visualize number sequence with divisibility rules for 3 and 5
- **Sudoku Solver**: Interactive Sudoku puzzle solver with visualization
- **Rubik's Cube**: Interactive 2x2 to 6x6 Rubik's Cube simulator and solver
- **Santa's Workshop**: Multi-threaded simulation of Santa's workshop operations
- **Minesweeper Solver**: Visualize recursive mine revealing algorithm with safety checks

## Requirements

- Python 3.7+
- PyQt6
- matplotlib
- numpy
- coverage

## Installation

# Clone the repository

    git clone https://github.com/vksvicky/codingChallenges.git

# Setup environment
```

python3 -m venv .venv

source .venv/bin/activate
```

# Install dependencies

    pip install PyQt6 matplotlib numpy

## Usage

1. Run the main program:

   ```
   python main.py
   ```

2. Select an algorithm from the menu (1-14):

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
9. FizzBuzz
10. Sudoku Solver
11. Rubik's Cube
12. Santa's Workshop
13. Minesweeper Solver
14. Exit
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
- Sudoku Solver: Enter initial puzzle grid (use 0 for empty cells)
- Rubik's Cube: Select cube size (2x2 to 6x6) and operation
- Santa's Workshop: Set number of elves and reindeer
- Minesweeper Solver: Enter board configuration and click position

## Testing

Run all tests using:
   ```    
   python run_tests.py
   or
   python -m unittest discover tests
   ```

To run individual test files:
   ```
   python tests/test_pascal_triangle.py
   python tests/test_dijkstra.py
   ...
   ```
   
To view test coverate
   ```
   coverage run -m unittest discover tests
   coverage report
   ```

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

# Visualisation

## Menu Options

![Pascal Triangle](images/02.%20Pascal%20Triangle.png)

### Example 01

![Sudoku](images/03.%20Sudoku.gif)

### Example 02

![Rubik's Cube](images/04.%20Rubik's%20Cube.gif)

### Contribution Guidelines

- Follow PEP 8 style guide
- Include unit tests
- Add visualisation for algorithm steps
- Document time and space complexity
- Update README.md with algorithm details

## License

The MIT License (MIT)
Copyright (c) 2015 Chris Kibble

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For detailed information about each algorithm, please see the [Wiki](wiki.md).
