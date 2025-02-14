import numpy as np
from PyQt6.QtCore import QTimer
import sys
from datetime import datetime

class CubeSolver:
    def __init__(self, cube):
        self.cube = cube
        self.move_stack = []
        self._initialize_inverse_moves()
        
    def solve_centers(self):
        """Solve centers for cubes larger than 3x3"""
        if self.cube.size <= 3:
            return
            
        # Solve centers in a specific order: white, yellow, red, orange, blue, green
        center_order = [0, 1, 2, 3, 4, 5]
        
        for face in center_order:
            center_color = self.cube.state[face, self.cube.size//2, self.cube.size//2]
            
            # Solve center pieces in a spiral pattern
            for layer in range(1, self.cube.size // 2):
                # Top row
                for col in range(layer, self.cube.size - layer - 1):
                    if self.cube.state[face, layer, col] != center_color:
                        self._move_center_piece(face, layer, col, center_color)
                
                # Right column
                for row in range(layer, self.cube.size - layer - 1):
                    if self.cube.state[face, row, self.cube.size - layer - 1] != center_color:
                        self._move_center_piece(face, row, self.cube.size - layer - 1, center_color)
                
                # Bottom row
                for col in range(self.cube.size - layer - 1, layer - 1, -1):
                    if self.cube.state[face, self.cube.size - layer - 1, col] != center_color:
                        self._move_center_piece(face, self.cube.size - layer - 1, col, center_color)
                
                # Left column
                for row in range(self.cube.size - layer - 1, layer - 1, -1):
                    if self.cube.state[face, row, layer] != center_color:
                        self._move_center_piece(face, row, layer, center_color)

    def _move_center_piece(self, face, row, col, target_color):
        """Move center pieces to their correct positions"""
        # Find the target piece
        found = False
        for f in range(6):
            if f != face:
                for i in range(1, self.cube.size - 1):
                    for j in range(1, self.cube.size - 1):
                        if self.cube.state[f, i, j] == target_color:
                            # Move piece to target position
                            self._align_and_move_center(f, i, j, face, row, col)
                            found = True
                            break
                    if found:
                        break
            if found:
                break

    def _align_and_move_center(self, src_face, src_row, src_col, dst_face, dst_row, dst_col):
        """Align and move center pieces using commutator sequences"""
        # Map face numbers to moves
        face_moves = {
            0: 'U', 1: 'D', 2: 'F', 3: 'B', 4: 'L', 5: 'R'
        }
        
        # Calculate relative positions
        src_layer = src_row + 1
        dst_layer = dst_row + 1
        
        # Different sequences based on source and destination faces
        if src_face in [0, 1] and dst_face in [0, 1]:  # Up/Down faces
            moves = [
                f"{src_layer}F", "R",
                f"{dst_layer}F'", "R'",
                f"{src_layer}F'", "R",
                f"{dst_layer}F", "R'"
            ]
        elif src_face in [2, 3] and dst_face in [2, 3]:  # Front/Back faces
            moves = [
                f"{src_layer}U", "R",
                f"{dst_layer}U'", "R'",
                f"{src_layer}U'", "R",
                f"{dst_layer}U", "R'"
            ]
        else:  # Other face combinations
            moves = [
                f"{src_layer}{face_moves[dst_face]}", 
                f"{dst_layer}{face_moves[src_face]}", 
                f"{src_layer}{face_moves[dst_face]}'",
                f"{dst_layer}{face_moves[src_face]}'"
            ]
        
        for move in moves:
            self.add_move(move)

    def solve_edges(self):
        """Pair up edges for cubes larger than 3x3"""
        if self.cube.size <= 3:
            return
            
        # Solve edges on each face
        for face in range(6):
            # Solve middle edges first
            for layer in range(1, self.cube.size - 1):
                self._pair_edge(face, layer)

    def _pair_edge(self, face, layer):
        """Pair up edges using slice moves"""
        # Different sequences based on the face and layer
        if face in [0, 1]:  # Up/Down faces
            moves = [
                f"{layer}F", "R",  # Move edge piece to working area
                "U", f"{layer}F'",  # Position second edge piece
                "U'", "R'",  # Complete pairing
                f"{layer}F", "U",  # Restore first edge
                f"{layer}F'", "U'"  # Final alignment
            ]
        elif face in [2, 3]:  # Front/Back faces
            moves = [
                f"{layer}R", "U",  # Setup move
                f"{layer}R'", "F",  # Position first edge
                "U'", f"{layer}R",  # Position second edge
                "F'", f"{layer}R'"  # Complete pairing
            ]
        else:  # Left/Right faces
            moves = [
                f"{layer}U", "F",  # Setup move
                f"{layer}U'", "R",  # Position first edge
                "F'", f"{layer}U",  # Position second edge
                "R'", f"{layer}U'"  # Complete pairing
            ]
        
        for move in moves:
            self.add_move(move)

    def _initialize_inverse_moves(self):
        """Initialize inverse moves dictionary including layer moves"""
        self.inverse_moves = {
            'R': "R'", "R'": 'R', 'R2': 'R2',
            'L': "L'", "L'": 'L', 'L2': 'L2',
            'U': "U'", "U'": 'U', 'U2': 'U2',
            'D': "D'", "D'": 'D', 'D2': 'D2',
            'F': "F'", "F'": 'F', 'F2': 'F2',
            'B': "B'", "B'": 'B', 'B2': 'B2'
        }
        
        # Add layer-specific moves for larger cubes
        for i in range(1, 7):  # Support up to 6x6
            for move in ['R', 'L', 'U', 'D', 'F', 'B']:
                self.inverse_moves[f"{i}{move}"] = f"{i}{move}'"
                self.inverse_moves[f"{i}{move}'"] = f"{i}{move}"

    def add_move(self, move):
        """Add a move to the move stack"""
        self.move_stack.append(move)

    def reset(self):
        """Reset the solver state"""
        self.move_stack = []
        if hasattr(self.cube, 'solution_moves'):
            self.cube.solution_moves = []

    def solve(self):
        """Solve cube by reversing the moves in the stack"""
        if not self.move_stack:
            print("Stack is empty, nothing to solve", flush=True)
            return

        try:
            # Store initial state and moves
            initial_state = self.cube.state.copy()
            moves_to_reverse = self.move_stack.copy()
            self.cube.solution_moves = []
            
            # Create solution sequence
            solution = []
            for move in reversed(moves_to_reverse):
                # Handle layer moves correctly
                if len(move) > 1 and move[0].isdigit():
                    layer = move[0]
                    base_move = move[1:]
                    inverse_base = self.inverse_moves.get(base_move, base_move)
                    inverse_move = f"{layer}{inverse_base}"
                else:
                    inverse_move = self.inverse_moves.get(move, move)
                solution.append(inverse_move)
            
            # Clear the move stack before executing solution
            self.move_stack = []
            
            # Execute solution sequence
            for move in solution:
                self.cube.solution_moves.append(move)
                self.cube.make_move(move)
                self.cube.window.update()
                self.cube.app.processEvents()
                QTimer.singleShot(100, lambda: None)

        except Exception as e:
            print(f"Solving failed: {e}")
            self.cube.state = initial_state.copy()
            self.cube.solution_moves = []
            self.move_stack = []