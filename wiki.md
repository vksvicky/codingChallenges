# Algorithm Details

### Pascal's Triangle
- Problem Statement: Given a non-negative integer n, generate the first n rows of Pascal's triangle where each number is the sum of the two numbers directly above it.
  - Input: Number of rows n
  - Output: Complete triangle with n rows
  - Requirements: Handle n=0 and large values of n efficiently
- Description : Generates a triangular array where each number is the sum of the two numbers above it
- Applications : Binomial expansions, probability calculations
- Complexity : Time O(n²), Space O(n²)
- Visualization : Color-coded triangle showing number relationships

### Dijkstra's Algorithm
- Problem Statement: Find the shortest path between two vertices in a weighted graph where all edges have non-negative weights.
  - Input: Graph G(V,E), source vertex s, destination vertex d
  - Output: Shortest path and its total cost
  - Requirements: Handle disconnected graphs and invalid inputs
- Description : Finds shortest paths between nodes in a weighted graph
- Applications : GPS navigation, network routing
- Complexity : Time O(V² + E), Space O(V)
- Visualization : Dynamic graph with highlighted paths and distances

### Tower of Hanoi
- Problem Statement: Move n disks from source rod to destination rod using an auxiliary rod, following these rules:
  - Only one disk can be moved at a time
  - A larger disk cannot be placed on top of a smaller disk
  - Input: Number of disks n
  - Output: Sequence of moves to solve the puzzle
  - Requirements: Minimize number of moves
- Description : Recursive solution to move disks between three rods
- Applications : Recursive problem solving, backup rotation schemes
- Complexity : Time O(2ⁿ), Space O(n)
- Visualization : Animated disk movements with step counter

### Palindrome Checker
- Problem Statement: Determine if a given string is a palindrome, considering the following rules:
  - Ignore case sensitivity
  - Skip non-alphanumeric characters
  - Empty strings are considered palindromes
  - Input: String of any length
  - Output: Boolean result and visualization of comparison
  - Requirements: Handle Unicode characters and special symbols
- Description : Verifies if text reads the same forwards and backwards
- Applications : String processing, data validation
- Complexity : Time O(n), Space O(1)
- Visualization : Character-by-character comparison animation

### Roman Numerals
- Problem Statement: Convert between Roman numerals and decimal numbers following standard Roman numeral rules:
  - Numbers range from 1 to 3999
  - Use subtractive notation (IV instead of IIII)
  - Valid symbols: I, V, X, L, C, D, M
  - Input: Roman numeral or decimal number
  - Output: Corresponding decimal or Roman numeral
  - Requirements: Validate input format and handle edge cases
- Description : Converts between decimal numbers and Roman numerals
- Applications : Historical dating, traditional numbering
- Complexity : Time O(1), Space O(1)
- Visualization : Step-by-step conversion process

### N-Queens Puzzle
- Problem Statement: Place N queens on an NxN chessboard so that no two queens threaten each other:
  - Queens can move horizontally, vertically, and diagonally
  - Find all possible solutions
  - Input: Board size N
  - Output: All valid queen placements
  - Requirements: Handle boards of size 1 to 12 efficiently
- Description : Places N queens on an NxN chessboard without conflicts
- Applications : Constraint satisfaction, backtracking algorithms
- Complexity : Time O(n!), Space O(n)
- Visualization : All valid solutions with queen placements

### String Reversal
- Problem Statement: Reverse a given string in-place:
  - Maintain proper handling of Unicode characters
  - Preserve whitespace positions
  - Input: String of any length
  - Output: Reversed string
  - Requirements: Minimize additional space usage
- Description : In-place reversal of character array
- Applications : String manipulation, palindrome creation
- Complexity : Time O(n), Space O(1)
- Visualization : Two-pointer swap animation

### Perfect Square Checker
- Problem Statement: Determine if a given number is a perfect square:
  - Handle both positive and negative numbers
  - Support large numbers efficiently
  - Input: Integer number
  - Output: Boolean result and visual proof
  - Requirements: Handle edge cases (0, 1, negative numbers)
- Description : Determines if a number is a perfect square
- Applications : Mathematical verification, geometry
- Complexity : Time O(log n), Space O(1)
- Visualization : Square root plotting with result indication

### FizzBuzz
- Problem Statement: Generate a sequence where numbers are replaced by Fizz, Buzz, or FizzBuzz based on:
  - "Fizz" for numbers divisible by 3
  - "Buzz" for numbers divisible by 5
  - "FizzBuzz" for numbers divisible by both
  - Input: Range end number
  - Output: Sequence with replacements
  - Requirements: Support custom divisors and replacements
- Description : Converts numbers to Fizz (divisible by 3), Buzz (divisible by 5), or FizzBuzz (divisible by both)
- Applications : Programming interviews, number theory, divisibility rules
- Complexity : Time O(n), Space O(n)
- Visualization : Color-coded sequence with divisibility indicators
- Numbers: Regular integers (lightblue)
- Fizz: Numbers divisible by 3 (lightcoral)
- Buzz: Numbers divisible by 5 (lightyellow)
- FizzBuzz: Numbers divisible by both 3 and 5 (lightgreen)

### Sudoku Solver
- Problem Statement: Solve a 9x9 Sudoku puzzle following standard rules:
  - Each row must contain digits 1-9 without repetition
  - Each column must contain digits 1-9 without repetition
  - Each 3x3 box must contain digits 1-9 without repetition
  - Input: Partially filled 9x9 grid
  - Output: Complete solution or "no solution"
  - Requirements: Validate input puzzle and handle multiple solutions
- Description: Interactive Sudoku puzzle solver with real-time visualization
- Applications:
    - Constraint satisfaction problems
    - Backtracking algorithm demonstration
    - Game solving
- Features:
    - Interactive GUI with input validation
    - Real-time solving visualization
    - Solution statistics and complexity analysis
    - Solution verification
- Complexity:
    - Time: O(9^m) where m is the number of empty cells
    - Space: O(1) for the board representation
- Visualization:
    - Color-coded cell filling:
    - Given numbers: Black
    - Solved numbers: Red
    - Real-time solving progress
    - Backtracking visualization
    - Final solution display with statistics

### Rubik's Cube
- Problem Statement: Simulate and solve Rubik's Cubes of various sizes (2x2x2 to 6x6x6):
  - Core Requirements:
    - Support standard cube sizes: 2x2, 3x3, 4x4, 5x5, and 6x6
    - Implement all standard moves (F, B, R, L, U, D) and their variations (F', F2, etc.)
    - Support middle layer rotations (M, E, S) for 3x3+
    - Track and validate cube state after each move
    - Detect solved state and impossible configurations 
  - Size-Specific Requirements:
    - 2x2: Handle simplified corner-only solving
    - 3x3: Support advanced methods (CFOP, Roux, ZZ)
    - 4x4: Handle parity cases and center orientation
    - 5x5: Manage edge pairing and center piece patterns
    - 6x6: Support complex parity resolution and center manipulation
  - Input:
    - Cube size selection (2-6)
    - Initial cube state or scramble sequence
    - Solving method preference
    - Animation speed control
  - Output:
    - Current cube state visualization
    - Solution steps with move notation
    - Move count and efficiency metrics
    - Parity detection warnings
  - Additional Requirements:
    - Support custom color schemes
    - Save/load cube states
    - Record and replay move sequences
    - Generate random scrambles
    - Provide solution hints
    - Handle multiple solution methods
- Description: Simulation and solver for the 3x3x3 Rubik's Cube puzzle
- Applications:
    - Group theory demonstration
    - Pattern recognition algorithms
    - 3D visualization techniques
- Features:
    - 3D cube representation
    - Standard move notation (F, B, R, L, U, D)
    - Solution path finding
    - Pattern detection
- Complexity:
    - Time: O(1) for moves, O(n) for solution finding
    - Space: O(1) for cube state
- Visualization:
    - 3D interactive cube display
    - Move animation sequences
    - Layer rotation visualization
    - Solution step highlighting

### Santa's Workshop
- Problem Statement: Implement a thread-safe simulation of Santa's workshop with the following rules:
  - Santa sleeps until woken by either:
    - All 9 reindeer returning from vacation (time to deliver toys)
    - 3 elves having problems (need help)
  - Reindeer return from vacation periodically
  - Elves can get help in groups of exactly 3
  - Santa must prioritize reindeer over elves when both conditions are met
  - Input: None (continuous simulation)
  - Output: Real-time status of Santa, reindeer, and elves
  - Requirements: Prevent deadlocks and ensure thread safety
- Description: Multi-threaded simulation of Santa's workshop with elves and reindeer
- Applications:
    - Thread synchronization demonstration
    - Resource management
    - Producer-consumer problem
- Features:
    - Real-time activity monitoring
    - Thread-safe operations
    - GUI status display
    - Event logging system
- Complexity:
    - Time: O(1) for thread operations
    - Space: O(n) where n is number of active threads
- Visualization:
    - Real-time status updates
    - Activity timeline
    - Thread state indicators
    - Resource usage monitoring
    
### Minesweeper
- Problem Statement: Implement a Minesweeper game solver that reveals cells based on clicks:
  - Input: Board configuration and click position
  - Output: Updated board state after each click
  - Requirements:
    - Handle valid board configurations
    - Process clicks on mines and empty cells
    - Implement recursive revealing for empty cells
    - Support visualization of game state
- Description: Simulates the classic Minesweeper game mechanics
- Board Elements:
    - 'M': Unrevealed Mine
    - 'E': Unrevealed Empty Square
    - 'B': Revealed Blank Square
    - '1'-'8': Number of adjacent mines
    - 'X': Revealed Mine
- Applications:
    - Recursive algorithms
    - Graph traversal
    - Game state management
- Features:
    - Board state visualization
    - Recursive cell revealing
    - Adjacent mine counting
    - Game over detection
- Complexity:
    - Time: O(mn) for board reveal, O(1) for single click
    - Space: O(mn) where m×n is the board size
- Visualization:
    - Color-coded cells
    - Beveled squares for unrevealed cells
    - Flat squares for revealed cells
    - Numbered cells with distinct colors
    - Mine and explosion indicators
- Constraints:
    - Board dimensions: 1 ≤ rows, cols ≤ 50
    - Cell contents: Only 'M' (mine) or 'E' (empty) initially
    - Click position: Must be within board boundaries
    - Valid clicks: Only on unrevealed cells ('M' or 'E')
    - Board state: Must be rectangular (all rows same length)
    - Mine placement: No restrictions on number or pattern
    - Empty board: Not allowed (must have at least one cell)
