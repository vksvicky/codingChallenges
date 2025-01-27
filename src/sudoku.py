from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                           QLineEdit, QPushButton, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np
import time
import sys

class Sudoku:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None
        self.cells = []
        self.delay = 0.05
        self.solving = False
        # Pre-compute sets for faster lookups
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]
        # Pre-compute box indices
        self.box_indices = []
        for box in range(9):
            indices = []
            start_row = (box // 3) * 3
            start_col = (box % 3) * 3
            for i in range(3):
                for j in range(3):
                    indices.append((start_row + i, start_col + j))
            self.box_indices.append(indices)

    def initialize_constraints(self, board):
        """Initialize constraint sets"""
        for i in range(9):
            for j in range(9):
                if board[i][j] != ".":
                    num = int(board[i][j])
                    self.rows[i].add(num)
                    self.cols[j].add(num)
                    self.boxes[(i // 3) * 3 + j // 3].add(num)
    
    # # def solve(self, board):
    #     if not self.is_valid_board(board):
    #         raise ValueError("Invalid Sudoku board")
        
    #     self.solving = True
    #     find = self.find_best_empty(board)
    #     if not find:
    #         return board
            
    #     row, col = find
    #     possible = self.get_possible_numbers(board, row, col)
        
    #     for i in possible:
    #         if not self.solving:
    #             return None
                
    #         board[row][col] = str(i)
            
    #         if hasattr(self, 'cells') and self.cells:
    #             self.cells[row][col].setText(str(i))
    #             self.cells[row][col].setStyleSheet("""
    #                 QLineEdit {
    #                     font-size: 20px;
    #                     background-color: white;
    #                     border: 1px solid gray;
    #                     color: red;
    #                 }
    #             """)
    #             QApplication.processEvents()
    #             time.sleep(self.delay)
            
    #         if self.solve(board):
    #             return board
                
    #         board[row][col] = "."
    #         if hasattr(self, 'cells') and self.cells:
    #             self.cells[row][col].setText("")
    #             self.cells[row][col].setStyleSheet("""
    #                 QLineEdit {
    #                     font-size: 20px;
    #                     background-color: white;
    #                     border: 1px solid gray;
    #                 }
    #             """)
    #             QApplication.processEvents()
        
    #     return False

    def solve(self, board):
        if not self.is_valid_board(board):
            raise ValueError("Invalid Sudoku board")
        
        self.solving = True
        self.start_time = time.time()
        self.initial_empty_cells = sum(row.count('.') for row in board)
        self.solve_attempts = 0  # Initialize solve attempts counter
        self.backtrack_count = 0  # Initialize backtrack counter
        
        # Initialize constraint sets
        self.initialize_constraints(board)
        return self._solve(board)

    def _solve(self, board):
        if not self.solving:
            return None
            
        # Update statistics in window title
        current_time = time.time() - self.start_time
        empty_cells = sum(row.count('.') for row in board)
        cells_filled = self.initial_empty_cells - empty_cells
        
        title_text = (
            f"Sudoku Solver | Time: {current_time:.2f}s | "
            f"Filled: {cells_filled}/{self.initial_empty_cells}"
        )
        self.window.setWindowTitle(title_text)
        QApplication.processEvents()
        
        cell = self.find_most_constrained_cell(board)
        if not cell:
            return board
            
        row, col = cell
        possible = self.get_possible_values(row, col)
        
        for num in possible:
            self.solve_attempts += 1  # Increment attempts counter
            if self.is_safe_to_place(board, row, col, num):
                # Place number and update constraints
                board[row][col] = str(num)
                self.update_constraints(row, col, num, add=True)
                
                # Update GUI
                if hasattr(self, 'cells') and self.cells:
                    self.cells[row][col].setText(str(num))
                    self.cells[row][col].setStyleSheet("""
                        QLineEdit {
                            font-size: 20px;
                            background-color: white;
                            border: 1px solid gray;
                            color: red;
                        }
                    """)
                    QApplication.processEvents()
                    time.sleep(self.delay)
                
                if self._solve(board):
                    return board
                    
                # Backtrack and remove constraints
                self.backtrack_count += 1  # Increment backtrack counter
                board[row][col] = "."
                self.update_constraints(row, col, num, add=False)
                
                # Update GUI for backtracking
                if hasattr(self, 'cells') and self.cells:
                    self.cells[row][col].setText("")
                    self.cells[row][col].setStyleSheet("""
                        QLineEdit {
                            font-size: 20px;
                            background-color: white;
                            border: 1px solid gray;
                        }
                    """)
                    QApplication.processEvents()
        
        return False

    def update_constraints(self, row, col, num, add=True):
        """Update constraint sets"""
        if add:
            self.rows[row].add(num)
            self.cols[col].add(num)
            self.boxes[(row // 3) * 3 + col // 3].add(num)
        else:
            self.rows[row].remove(num)
            self.cols[col].remove(num)
            self.boxes[(row // 3) * 3 + col // 3].remove(num)

    def get_possible_values(self, row, col):
        """Get possible values for a cell using constraint sets"""
        used = self.rows[row] | self.cols[col] | self.boxes[(row // 3) * 3 + col // 3]
        return set(range(1, 10)) - used

    def find_most_constrained_cell(self, board):
        """Find empty cell with fewest possible values"""
        min_possibilities = 10
        best_cell = None
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    possible = self.get_possible_values(i, j)
                    if len(possible) < min_possibilities:
                        min_possibilities = len(possible)
                        best_cell = (i, j)
                        if min_possibilities == 1:
                            return best_cell
        
        return best_cell

    def is_safe_to_place(self, board, row, col, num):
        """Quick check if number can be placed"""
        return (num not in self.rows[row] and 
                num not in self.cols[col] and 
                num not in self.boxes[(row // 3) * 3 + col // 3])

    def get_possible_numbers(self, board, row, col):
        box_id = (row // 3) * 3 + col // 3
        used = set()
        
        # Check row and column simultaneously
        for i in range(9):
            if board[row][i] != ".":
                used.add(int(board[row][i]))
            if board[i][col] != ".":
                used.add(int(board[i][col]))
        
        # Check box using pre-computed indices
        for i, j in self.box_indices[box_id]:
            if board[i][j] != ".":
                used.add(int(board[i][j]))
        
        return set(range(1, 10)) - used

    def find_best_empty(self, board):
        min_possibilities = 10
        best_cell = None
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    possible = self.get_possible_numbers(board, i, j)
                    if len(possible) == 1:  # Found cell with only one possibility
                        return (i, j)
                    if len(possible) < min_possibilities:
                        min_possibilities = len(possible)
                        best_cell = (i, j)
        
        return best_cell

    def solve_array(self, board):
        """Solve Sudoku from array input"""
        try:
            # Create deep copy to preserve original board
            initial_state = [row[:] for row in board]
            
            # Print the input board in 3x3 format
            print("\nInput Sudoku Board:")
            print("-" * 25)
            for i in range(9):
                if i % 3 == 0 and i != 0:
                    print("-" * 25)
                row = board[i]
                for j in range(9):
                    if j % 3 == 0:
                        print("|", end=" ")
                    print(row[j], end=" ")
                print("|")
            print("-" * 25)
            
            self.load_example(board)  # Load the board into GUI first
            solution = self.solve(board)
            if solution:
                self.visualize(solution, initial_state)
                return solution
            else:
                print("No solution exists!")
                return None
        except ValueError as e:
            print(f"Error: {e}")
            return None

    def load_array_to_gui(self, board):
        """Load array into GUI"""
        if not self.window:
            self.create_gui()
        
        for i in range(9):
            for j in range(9):
                if board[i][j] != ".":
                    self.cells[i][j].setText(board[i][j])

    # # def solve(self, board):
    #     if not self.is_valid_board(board):
    #         raise ValueError("Invalid Sudoku board")
            
    #     find = self.find_empty(board)
    #     if not find:
    #         return board
            
    #     row, col = find
        
    #     for i in range(1,10):
    #         if self.is_valid(board, i, (row, col)):
    #             board[row][col] = str(i)
                
    #             # Update GUI with current number in red
    #             if hasattr(self, 'cells') and self.cells:
    #                 self.cells[row][col].setText(str(i))
    #                 self.cells[row][col].setStyleSheet("""
    #                     QLineEdit {
    #                         font-size: 20px;
    #                         background-color: white;
    #                         border: 1px solid gray;
    #                         color: red;
    #                     }
    #                 """)
    #                 QApplication.processEvents()
    #                 time.sleep(self.delay)
                
    #             if self.solve(board):
    #                 return board
                    
    #             board[row][col] = "."
    #             # Clear cell in GUI if backtracking
    #             if hasattr(self, 'cells') and self.cells:
    #                 self.cells[row][col].setText("")
    #                 self.cells[row][col].setStyleSheet("""
    #                     QLineEdit {
    #                         font-size: 20px;
    #                         background-color: white;
    #                         border: 1px solid gray;
    #                     }
    #                 """)
    #                 QApplication.processEvents()
                
    #     return False

    def load_example(self, custom_board=None):
        # Create GUI if it doesn't exist
        if not self.window:
            self.create_gui()
        
        # Initialize default example board
        example = [
            ["5","3",".",".","7",".",".",".","."],
            ["6",".",".","1","9","5",".",".","."],
            [".","9","8",".",".",".",".","6","."],
            ["8",".",".",".","6",".",".",".","3"],
            ["4",".",".","8",".","3",".",".","1"],
            ["7",".",".",".","2",".",".",".","6"],
            [".","6",".",".",".",".","2","8","."],
            [".",".",".","4","1","9",".",".","5"],
            [".",".",".",".","8",".",".","7","9"]
        ]
        
        board_to_use = example
        
        # Handle custom board if provided
        if custom_board is not None:
            try:
                # Handle boolean input by converting to empty board
                if isinstance(custom_board, bool):
                    board = [["."] * 9 for _ in range(9)]
                else:
                    # Convert rows to lists if needed
                    board = []
                    for row in custom_board:
                        board_row = []
                        for cell in row:
                            # Convert cell to string and handle zeros
                            cell_str = str(cell)
                            board_row.append("." if cell_str == "0" or cell_str == "" else cell_str)
                        board.append(board_row)
                
                # Validate board dimensions
                if len(board) != 9 or any(len(row) != 9 for row in board):
                    raise ValueError("Board must be 9x9")
                
                # Validate cell contents
                for row in board:
                    for cell in row:
                        if not (cell == "." or (cell.isdigit() and 1 <= int(cell) <= 9)):
                            raise ValueError(f"Invalid cell value: {cell}")
                
                # Update GUI with custom board
                self.clear_board()
                for i in range(9):
                    for j in range(9):
                        if board[i][j] != ".":
                            self.cells[i][j].setText(board[i][j])
                            self.cells[i][j].setStyleSheet("""
                                QLineEdit {
                                    font-size: 20px;
                                    background-color: white;
                                    border: 1px solid gray;
                                    color: black;
                                }
                            """)
                
                # Print the board in 9x9 format
                print("\nLoaded Sudoku Board:")
                print("-" * 25)
                for i in range(9):
                    if i % 3 == 0 and i != 0:
                        print("-" * 25)
                    for j in range(9):
                        if j % 3 == 0:
                            print("|", end=" ")
                        print(board[i][j], end=" ")
                    print("|")
                print("-" * 25)
                
                return board
                
            except Exception as e:
                print(f"Error loading custom board: {e}")
        
        # Load default example if no custom board or if custom board failed
        example = [
            ["5","3",".",".","7",".",".",".","."],
            ["6",".",".","1","9","5",".",".","."],
            [".","9","8",".",".",".",".","6","."],
            ["8",".",".",".","6",".",".",".","3"],
            ["4",".",".","8",".","3",".",".","1"],
            ["7",".",".",".","2",".",".",".","6"],
            [".","6",".",".",".",".","2","8","."],
            [".",".",".","4","1","9",".",".","5"],
            [".",".",".",".","8",".",".","7","9"]
        ]
        
        # Clear and update GUI with example
        self.clear_board()
        for i in range(9):
            for j in range(9):
                if example[i][j] != ".":
                    self.cells[i][j].setText(example[i][j])
                    self.cells[i][j].setStyleSheet("""
                        QLineEdit {
                            font-size: 20px;
                            background-color: white;
                            border: 1px solid gray;
                            color: black;
                        }
                    """)

    def clear_board(self):
        """Clear all cells in the GUI"""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].setText("")
                self.cells[i][j].setStyleSheet(self.cells[i][j].styleSheet().replace("red", "black"))

    def is_valid(self, board, num, pos):
        # Check row
        for x in range(len(board[0])):
            if board[pos[0]][x] == str(num) and pos[1] != x:
                return False
                
        # Check column
        for x in range(len(board)):
            if board[x][pos[1]] == str(num) and pos[0] != x:
                return False
                
        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == str(num) and (i,j) != pos:
                    return False
                    
        return True
        
    # def solve(self, board):
    #     if not self.is_valid_board(board):
    #         raise ValueError("Invalid Sudoku board")
            
    #     find = self.find_empty(board)
    #     if not find:
    #         return board
            
    #     row, col = find
        
    #     for i in range(1,10):
    #         if self.is_valid(board, i, (row, col)):
    #             board[row][col] = str(i)
                
    #             # Update GUI with current number in red
    #             if hasattr(self, 'cells') and self.cells:
    #                 self.cells[row][col].setText(str(i))
    #                 self.cells[row][col].setStyleSheet("""
    #                     QLineEdit {
    #                         font-size: 20px;
    #                         background-color: white;
    #                         border: 1px solid gray;
    #                         color: red;
    #                     }
    #                 """)
    #                 QApplication.processEvents()
    #                 time.sleep(self.delay)
                
    #             if self.solve(board):
    #                 return board
                    
    #             board[row][col] = "."
    #             # Clear cell in GUI if backtracking
    #             if hasattr(self, 'cells') and self.cells:
    #                 self.cells[row][col].setText("")
    #                 self.cells[row][col].setStyleSheet("""
    #                     QLineEdit {
    #                         font-size: 20px;
    #                         background-color: white;
    #                         border: 1px solid gray;
    #                     }
    #                 """)
    #                 QApplication.processEvents()
                
    #     return False

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == ".":
                    return (i, j)
        return None
        
    def is_valid_board(self, board):
        # Check rows
        for row in board:
            nums = [x for x in row if x != "."]
            if len(nums) != len(set(nums)):
                return False
                
        # Check columns
        for col in zip(*board):
            nums = [x for x in col if x != "."]
            if len(nums) != len(set(nums)):
                return False
                
        # Check boxes
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                box = []
                for k in range(3):
                    for l in range(3):
                        if board[i+k][j+l] != ".":
                            box.append(board[i+k][j+l])
                if len(box) != len(set(box)):
                    return False
        return True
        
    def is_valid_solution(self, board):
        # Check if board is complete and valid
        for row in board:
            if sorted([str(x) for x in row]) != ['1','2','3','4','5','6','7','8','9']:
                return False
                
        for col in zip(*board):
            if sorted([str(x) for x in col]) != ['1','2','3','4','5','6','7','8','9']:
                return False
                
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                box = []
                for k in range(3):
                    for l in range(3):
                        box.append(board[i+k][j+l])
                if sorted([str(x) for x in box]) != ['1','2','3','4','5','6','7','8','9']:
                    return False
        return True

    def display_solution(self, solution, initial_state):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].setText(solution[i][j])
                # Color solved numbers red, keep original numbers black
                if initial_state[i][j] == ".":
                    self.cells[i][j].setStyleSheet(
                        self.cells[i][j].styleSheet() + "color: red;"
                    )
                    QApplication.processEvents()
                    time.sleep(0.2)

    def visualize(self, board, initial_state):
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Draw grid with thicker lines for 3x3 boxes
        for i in range(10):
            lw = 3 if i % 3 == 0 else 0.5
            ax.axhline(y=i, color='black', linewidth=lw)
            ax.axvline(x=i, color='black', linewidth=lw)
            
        # Fill numbers with different colors
        for i in range(9):
            for j in range(9):
                color = 'black' if initial_state[i][j] != "." else 'red'
                ax.text(j + 0.5, 8.5 - i, board[i][j], 
                       ha='center', va='center', fontsize=20,
                       color=color)
                
        ax.set_title("Sudoku Solution\nRed: Solved Numbers, Black: Given Numbers")
        plt.axis('off')
        plt.show()

    def solve_from_gui(self):
        """Solve Sudoku from GUI input"""
        self.solving = True  # Reset solving flag
        board = []
        initial_state = []  # Store initial state to know which numbers were given
        for i in range(9):
            row = []
            initial_row = []
            for j in range(9):
                val = self.cells[i][j].text()
                row.append(val if val else ".")
                initial_row.append(val if val else ".")
            board.append(row)
            initial_state.append(initial_row)
            
        try:
            start_time = time.time()
            solution = self.solve(board)
            end_time = time.time()
            solve_time = end_time - start_time
            
            if solution and self.solving:  # Check if solving wasn't stopped
                self.display_solution(solution, initial_state)
                self.visualize(solution, initial_state)
                empty_cells = sum(row.count('.') for row in initial_state)
                
                # Calculate solving statistics
                attempts_per_cell = self.solve_attempts / empty_cells if empty_cells > 0 else 0
                backtrack_ratio = self.backtrack_count / self.solve_attempts if self.solve_attempts > 0 else 0
                
                stats_message = (
                    f"Time taken: {solve_time:.3f} seconds\n"
                    f"Empty cells filled: {empty_cells}\n"
                    f"Complexity: O(9^{empty_cells})\n"
                    f"Solution attempts: {self.solve_attempts}\n"
                    f"Backtrack count: {self.backtrack_count}\n"
                    f"Average attempts per cell: {attempts_per_cell:.2f}\n"
                    f"Backtrack ratio: {backtrack_ratio:.2%}"
                )
                
                QMessageBox.information(self.window, "Solution Found", stats_message)
                self.window.setWindowTitle("Sudoku Solver")  # Reset title
            elif not self.solving:
                QMessageBox.information(self.window, "Stopped", "Solving process stopped!")
            else:
                QMessageBox.critical(self.window, "Error", "No solution exists!")
        except ValueError as e:
            QMessageBox.critical(self.window, "Error", str(e))

    def create_gui(self):
        self.window = QMainWindow()
        self.window.setWindowTitle("Sudoku Solver")
        
        # Set window to stay on top initially
        self.window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)
        main_layout.setSpacing(10)  # Space between 3x3 boxes
        
        # Create 9x9 grid organized in 3x3 boxes
        self.cells = []
        for box_i in range(3):
            for box_j in range(3):
                # Create a widget for each 3x3 box
                box_widget = QWidget()
                box_layout = QGridLayout(box_widget)
                box_layout.setSpacing(1)  # Space between cells in a box
                
                for i in range(3):
                    cell_row = []
                    for j in range(3):
                        cell = QLineEdit()
                        cell.setMaxLength(1)
                        cell.setFixedSize(50, 50)
                        cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        cell.setStyleSheet("""
                            QLineEdit {
                                font-size: 20px;
                                background-color: white;
                                border: 1px solid gray;
                            }
                        """)
                        
                        box_layout.addWidget(cell, i, j)
                        cell_row.append(cell)
                        
                        # Set focus to first cell
                        if box_i == 0 and box_j == 0 and i == 0 and j == 0:
                            cell.setFocus()
                    
                    if box_i * 3 + i >= len(self.cells):
                        self.cells.append([])
                    self.cells[box_i * 3 + i].extend(cell_row)
                
                box_widget.setStyleSheet("background-color: #f0f0f0; border: 2px solid black;")
                main_layout.addWidget(box_widget, box_i, box_j)

        # Remove stats label section and directly add buttons
        button_widget = QWidget()
        button_layout = QGridLayout(button_widget)
        
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.solve_from_gui)
        solve_button.setFixedSize(100, 40)
        
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_solving)
        stop_button.setFixedSize(100, 40)
        
        check_button = QPushButton("Check")
        check_button.clicked.connect(self.check_solution)
        check_button.setFixedSize(100, 40)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_board)
        clear_button.setFixedSize(100, 40)
        
        example_button = QPushButton("Load Example")
        example_button.clicked.connect(self.load_example)
        example_button.setFixedSize(100, 40)
        
        button_layout.addWidget(solve_button, 0, 0)
        button_layout.addWidget(stop_button, 0, 1)
        button_layout.addWidget(check_button, 0, 2)
        button_layout.addWidget(clear_button, 0, 3)
        button_layout.addWidget(example_button, 0, 4)
        
        main_layout.addWidget(button_widget, 3, 0, 1, 3)
        
        self.window.show()
        self.window.activateWindow()
        self.window.raise_()  # Bring window to front
        
        # Remove stay on top flag after showing
        self.window.setWindowFlags(Qt.WindowType.Widget)
        self.window.show()

    def stop_solving(self):
        """Stop the solving process"""
        self.solving = False

    def check_solution(self):
        """Check if current board state is valid"""
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].text()
                if not val:  # Board not complete
                    QMessageBox.warning(self.window, "Incomplete", "Please fill all cells!")
                    return
                row.append(val)
            board.append(row)
            
        if self.is_valid_solution(board):
            QMessageBox.information(self.window, "Valid", "Solution is correct!")
        else:
            QMessageBox.warning(self.window, "Invalid", "Solution is incorrect!")

    if __name__ == "__main__":
        sudoku = Sudoku()
        # Start the event loop after creating the instance
        sudoku.app.exec()