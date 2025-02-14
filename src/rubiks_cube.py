from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QLabel, QSlider
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QIcon  # Add QIcon import
import numpy as np
import sys
from .views.cube_view_3d import CubeView3D
from .views.cube_view_unfolded import CubeViewUnfolded
from .views.cube_view_flat import CubeViewFlat
from .cube_solver import CubeSolver

class RubiksCube:
    def __init__(self, size=3):
        if size < 2 or size > 6:
            raise ValueError("Cube size must be between 2 and 6")
        self.size = size  # Cube size (2x2, 3x3, 4x4, etc.)
        # Initialize cube state (6 faces, each size x size)
        self.state = np.zeros((6, size, size), dtype=int)
        for i in range(6):
            self.state[i] = np.full((size, size), i)
        
        # Initialize solution moves list
        self.moves_to_solve = []
        
        # Define colors for faces
        self.colors = {
            0: QColor('white'),
            1: QColor('yellow'),
            2: QColor('red'),
            3: QColor('orange'),
            4: QColor('blue'),
            5: QColor('green')
        }
        
        # Define moves dictionary
        self.moves = {
            'U': self.rotate_up,
            'D': self.rotate_down,
            'L': self.rotate_left,
            'R': self.rotate_right,
            'F': self.rotate_front,
            'B': self.rotate_back
        }
        
        # Initialize solver
        self.solver = CubeSolver(self)
        
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.setup_ui()

    def setup_ui(self):
        self.window.setWindowTitle("Rubik's Cube Solver")
        self.window.setGeometry(100, 100, 800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.window.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget for different views
        tabs = QTabWidget()
        
        # Add 3D view tab
        view_3d = CubeView3D(self)
        view_3d.setMinimumSize(400, 400)  # Set minimum size for visibility
        tabs.addTab(view_3d, "3D View")
        
        # Add unfolded view tab
        view_unfolded = CubeViewUnfolded(self)
        view_unfolded.setMinimumSize(400, 400)
        tabs.addTab(view_unfolded, "Unfolded View")
        
        # Add flat view tab
        view_flat = CubeViewFlat(self)
        view_flat.setMinimumSize(400, 400)
        tabs.addTab(view_flat, "Flat View")
        
        layout.addWidget(tabs)
        
        # Create layouts
        moves_layout = QHBoxLayout()
        size_layout = QHBoxLayout()  # Add this line
        view_controls = QHBoxLayout()  # Add this line
        
        # Add move buttons
        moves = ['U', 'D', 'L', 'R', 'F', 'B']
        move_descriptions = {
            'U': 'Rotate Up',
            'D': 'Rotate Down',
            'L': 'Rotate Left',
            'R': 'Rotate Right',
            'F': 'Rotate Front',
            'B': 'Rotate Back'
        }
        
        # Store move buttons for enabling/disabling
        self.move_buttons = []
        for move in moves:
            btn = QPushButton(move)
            btn.setToolTip(f"{move_descriptions[move]} clockwise")
            btn.clicked.connect(lambda checked, m=move: self.make_move(m))
            moves_layout.addWidget(btn)
            self.move_buttons.append(btn)
            
            # Add inverse move button
            btn_inv = QPushButton(f"{move}'")
            btn_inv.setToolTip(f"{move_descriptions[move]} counterclockwise")
            btn_inv.clicked.connect(lambda checked, m=move: self.make_move(f"{m}'"))
            moves_layout.addWidget(btn_inv)
            self.move_buttons.append(btn_inv)
    
        # Add utility buttons with tooltips
        scramble_btn = QPushButton()
        scramble_btn.setIcon(QIcon(":/icons/shuffle"))  # Try system icon first
        if scramble_btn.icon().isNull():  # If system icon not found
            scramble_btn.setText("🔀")  # Use Unicode shuffle symbol as fallback
        scramble_btn.setToolTip("Randomly scramble the cube")
        scramble_btn.clicked.connect(self.scramble)
        moves_layout.addWidget(scramble_btn)
        self.scramble_btn = scramble_btn
        
        solve_btn = QPushButton()
        solve_btn.setIcon(QIcon.fromTheme("media-playback-start"))  # Play icon
        if solve_btn.icon().isNull():
            solve_btn.setText("▶️")
        solve_btn.setToolTip("Solve the cube")
        solve_btn.clicked.connect(self.solve)
        moves_layout.addWidget(solve_btn)
        self.solve_btn = solve_btn  # Store reference
        
        self.stop_btn = QPushButton()
        self.stop_btn.setIcon(QIcon.fromTheme("media-playback-pause"))
        if self.stop_btn.icon().isNull():
            self.stop_btn.setText("⏸️")
        self.stop_btn.setToolTip("Stop solving animation")
        self.stop_btn.clicked.connect(self.stop_solving)
        self.stop_btn.setEnabled(False)
        moves_layout.addWidget(self.stop_btn)
        
        self.resume_btn = QPushButton()
        self.resume_btn.setIcon(QIcon.fromTheme("media-skip-forward"))  # Different icon for resume
        if self.resume_btn.icon().isNull():
            self.resume_btn.setText("⏭️")  # Different symbol for resume
        self.resume_btn.setToolTip("Resume solving from where it was stopped")
        self.resume_btn.clicked.connect(self.resume_solving)
        self.resume_btn.setEnabled(False)
        moves_layout.addWidget(self.resume_btn)
        
        reset_btn = QPushButton()
        reset_btn.setIcon(QIcon.fromTheme("edit-undo"))  # Reset/undo icon
        reset_btn.setToolTip("Reset cube to solved state")
        reset_btn.clicked.connect(self.reset)
        moves_layout.addWidget(reset_btn)
        
        # Add size selector with tooltips
        for size in [2, 3, 4, 5, 6]:
            btn = QPushButton(f"{size}x{size}")
            btn.setToolTip(f"Change to {size}x{size} cube")
            btn.clicked.connect(lambda checked, s=size: self.change_size(s))
            size_layout.addWidget(btn)
        
        # Add view controls with tooltips
        transparency_btn = QPushButton("Toggle Transparency")
        transparency_btn.setToolTip("Toggle cube face transparency")
        transparency_btn.clicked.connect(self.toggle_transparency)
        view_controls.addWidget(transparency_btn)
        
        lift_faces_btn = QPushButton("Lift Hidden Faces")
        lift_faces_btn.setToolTip("Show/hide hidden faces of the cube")
        lift_faces_btn.clicked.connect(self.toggle_lift_faces)
        view_controls.addWidget(lift_faces_btn)

         # Add speed control slider
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Animation Speed:")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(13)  # Updated for 14 different speed values
        self.speed_slider.setValue(3)     # 1.0x default (index 3)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setPageStep(1)
        self.speed_slider.setSingleStep(1)
        
        self.speed_values = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        self.speed_value_label = QLabel("1.0x")
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_value_label)
        
        # Update layout
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.addLayout(size_layout)
        controls_layout.addLayout(view_controls)
        controls_layout.addLayout(speed_layout)  # Add speed controls
        controls_layout.addLayout(moves_layout)
        layout.addWidget(controls_widget)
        
        # Set focus policy for keyboard controls
        for view in [view_3d, view_unfolded, view_flat]:
            view.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.window.show()

    def stop_solving(self):
        """Stop the solving animation"""
        self.solving_stopped = True
        self.stop_btn.setEnabled(False)
        self.resume_btn.setEnabled(True)
        self.solve_btn.setEnabled(False)  # Disable solve button when stopped
        # Disable all move buttons during pause
        for btn in self.move_buttons:
            btn.setEnabled(False)

    def resume_solving(self):
        """Resume the solving animation"""
        self.solving_stopped = False
        self.stop_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)
        self.execute_next_move()

    def start_solving(self):
        """Start the solving animation"""
        self.solving_stopped = False
        self.stop_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)

    def update_speed_label(self):
        """Update the speed label when slider value changes"""
        speed = self.speed_values[self.speed_slider.value()]
        self.speed_value_label.setText(f"{speed:.2f}x")

    def change_size(self, new_size):
        self.size = new_size
        # Reinitialize the state array with the new size
        self.state = np.zeros((6, new_size, new_size), dtype=int)
        
        # Reinitialize the solver
        self.solver = CubeSolver(self)
        
        # Reset the cube to solved state
        for i in range(6):
            self.state[i] = np.full((new_size, new_size), i)
        
        # Clear any existing moves
        self.moves_to_solve = []
        
        # Enable buttons for fresh start
        self.scramble_btn.setEnabled(True)
        self.solve_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        
        self.window.update()

    def toggle_transparency(self):
        for view in self.window.findChildren(CubeView3D):
            view.transparency = not view.transparency
            view.update()

    def toggle_lift_faces(self):
        for view in self.window.findChildren(CubeView3D):
            view.lift_faces = not view.lift_faces
            view.update()

    def make_move(self, move):
        # Don't allow moves when solving is paused
        if hasattr(self, 'solving_stopped') and self.solving_stopped:
            return
            
        inverse = False
        layer = 0
        
        # Store original move before parsing
        original_move = move
        
        # Parse move notation
        if move.endswith("'"):
            move = move[:-1]
            inverse = True
        
        if len(move) > 1 and move[0].isdigit():
            layer = int(move[0]) - 1
            move = move[1]        
        
        if move in self.moves:            
            # Execute the move
            if layer > 0:
                for _ in range(3 if inverse else 1):
                    self.rotate_inner_layer(move, layer)
            else:
                for _ in range(3 if inverse else 1):
                    self.moves[move]()

            # Only add to solver stack if not during scramble
            if hasattr(self, 'solver') and not hasattr(self, '_scrambling'):
                # Store the exact move in the stack
                self.solver.move_stack.append(original_move)
                print(f"Move made: {original_move}, Added to stack: {original_move}")
        
        self.window.update()

    def rotate_face(self, face):
        """Rotate a face clockwise"""
        self.state[face] = np.rot90(self.state[face], k=-1)

    # Basic Face Rotations
    def rotate_front(self):
        self.rotate_face(2)
        self._rotate_adjacent_front()

    def rotate_back(self):
        self.rotate_face(3)
        self._rotate_adjacent_back()

    def rotate_up(self):
        self.rotate_face(0)
        self._rotate_adjacent_up()

    def rotate_down(self):
        self.rotate_face(1)
        self._rotate_adjacent_down()

    def rotate_left(self):
        self.rotate_face(4)
        self._rotate_adjacent_left()

    def rotate_right(self):
        self.rotate_face(5)
        self._rotate_adjacent_right()

    # Helper Methods for Adjacent Face Rotations
    def _rotate_adjacent_front(self):
        last_idx = self.size - 1
        temp = self.state[0, last_idx].copy()
        self.state[0, last_idx] = np.flip(self.state[4, :, last_idx])
        self.state[4, :, last_idx] = self.state[1, 0]
        self.state[1, 0] = np.flip(self.state[5, :, 0])
        self.state[5, :, 0] = temp

    def _rotate_adjacent_back(self):
        last_idx = self.size - 1
        temp = self.state[0, 0].copy()
        self.state[0, 0] = np.flip(self.state[4, :, 0])
        self.state[4, :, 0] = self.state[1, last_idx]
        self.state[1, last_idx] = np.flip(self.state[5, :, last_idx])
        self.state[5, :, last_idx] = temp

    def _rotate_adjacent_up(self):
        temp = self.state[2, 0].copy()
        self.state[2, 0] = self.state[5, 0]
        self.state[5, 0] = self.state[3, 0]
        self.state[3, 0] = self.state[4, 0]
        self.state[4, 0] = temp

    def _rotate_adjacent_down(self):
        last_idx = self.size - 1
        temp = self.state[2, last_idx].copy()
        self.state[2, last_idx] = self.state[4, last_idx]
        self.state[4, last_idx] = self.state[3, last_idx]
        self.state[3, last_idx] = self.state[5, last_idx]
        self.state[5, last_idx] = temp

    def _rotate_adjacent_left(self):
        last_idx = self.size - 1
        temp = self.state[0, :, 0].copy()
        self.state[0, :, 0] = self.state[2, :, 0]
        self.state[2, :, 0] = self.state[1, :, 0]
        self.state[1, :, 0] = np.flip(self.state[3, :, last_idx])
        self.state[3, :, last_idx] = np.flip(temp)

    def _rotate_adjacent_right(self):
        last_idx = self.size - 1
        temp = self.state[0, :, last_idx].copy()
        self.state[0, :, last_idx] = np.flip(self.state[3, :, 0])
        self.state[3, :, 0] = np.flip(self.state[1, :, last_idx])
        self.state[1, :, last_idx] = self.state[2, :, last_idx]
        self.state[2, :, last_idx] = temp

    def rotate_inner_layer(self, face_move, layer):
        """Rotate an inner layer of the cube
        Args:
            face_move: The face move character ('U', 'D', 'L', 'R', 'F', 'B')
            layer: The layer number to rotate (0 is outermost)
        """
        if face_move == 'L':
            # Similar to left face rotation but for inner layer
            last_idx = self.size - 1
            temp = self.state[0, :, layer].copy()
            self.state[0, :, layer] = self.state[2, :, layer]
            self.state[2, :, layer] = self.state[1, :, layer]
            self.state[1, :, layer] = np.flip(self.state[3, :, last_idx - layer])
            self.state[3, :, last_idx - layer] = np.flip(temp)
            
        elif face_move == 'R':
            # Similar to right face rotation but for inner layer
            last_idx = self.size - 1
            temp = self.state[0, :, last_idx - layer].copy()
            self.state[0, :, last_idx - layer] = np.flip(self.state[3, :, layer])
            self.state[3, :, layer] = np.flip(self.state[1, :, last_idx - layer])
            self.state[1, :, last_idx - layer] = self.state[2, :, last_idx - layer]
            self.state[2, :, last_idx - layer] = temp
            
        elif face_move == 'U':
            # Similar to up face rotation but for inner layer
            temp = self.state[2, layer].copy()
            self.state[2, layer] = self.state[5, layer]
            self.state[5, layer] = self.state[3, layer]
            self.state[3, layer] = self.state[4, layer]
            self.state[4, layer] = temp
            
        elif face_move == 'D':
            # Similar to down face rotation but for inner layer
            last_idx = self.size - 1
            temp = self.state[2, last_idx - layer].copy()
            self.state[2, last_idx - layer] = self.state[4, last_idx - layer]
            self.state[4, last_idx - layer] = self.state[3, last_idx - layer]
            self.state[3, last_idx - layer] = self.state[5, last_idx - layer]
            self.state[5, last_idx - layer] = temp
            
        elif face_move == 'F':
            # Similar to front face rotation but for inner layer
            last_idx = self.size - 1
            temp = self.state[0, last_idx - layer].copy()
            self.state[0, last_idx - layer] = np.flip(self.state[4, :, last_idx - layer])
            self.state[4, :, last_idx - layer] = self.state[1, layer]
            self.state[1, layer] = np.flip(self.state[5, :, layer])
            self.state[5, :, layer] = temp
            
        elif face_move == 'B':
            # Similar to back face rotation but for inner layer
            last_idx = self.size - 1
            temp = self.state[0, layer].copy()
            self.state[0, layer] = np.flip(self.state[4, :, layer])
            self.state[4, :, layer] = self.state[1, last_idx - layer]
            self.state[1, last_idx - layer] = np.flip(self.state[5, :, last_idx - layer])
            self.state[5, :, last_idx - layer] = temp


    def is_solved(self):
        """Check if the cube is in solved state"""
        # Check each face for uniform color
        for face in range(6):
            center_color = self.state[face, self.size//2, self.size//2]
            if not np.all(self.state[face] == center_color):
                return False
        
        # Enable all buttons when solved
        self.scramble_btn.setEnabled(True)
        self.solve_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        
        # Enable all move buttons
        for btn in self.move_buttons:
            btn.setEnabled(True)
        
        return True

    def scramble(self):
        """Perform a random scramble with appropriate number of moves"""
        # Disable scramble button and reset solver
        self.scramble_btn.setEnabled(False)
        
        # Store existing moves instead of resetting
        existing_moves = self.solver.move_stack.copy() if hasattr(self, 'solver') else []
        self.solver.reset()
        self.solver.move_stack = existing_moves  # Restore existing moves
        
        self.moves_to_solve = []

        # Set scrambling flag
        self._scrambling = True
        
        basic_moves = ['U', 'D', 'L', 'R', 'F', 'B']
        moves = basic_moves.copy()
        
        # Add slice moves for 4x4 and larger cubes
        if self.size >= 4:
            for i in range(2, self.size):
                for m in basic_moves:
                    moves.append(f"{i}{m}")
        
        # Scale move count with cube size: more moves for larger cubes
        move_count = max(20, self.size * self.size * 3)  # Increased scaling factor
        last_face = None
        last_layer = None
        
        for _ in range(move_count):
            # Avoid same face and layer moves in sequence
            available_moves = []
            for m in moves:
                current_face = m[0] if m[0] not in '123456' else m[1]
                current_layer = m[0] if m[0] in '123456' else None
                
                if (current_face != last_face or 
                    (current_layer is not None and current_layer != last_layer)):
                    available_moves.append(m)
            
            move = np.random.choice(available_moves)
            
            # 50% chance of inverse move
            if np.random.random() < 0.5:
                move = f"{move}'"
            
            # Execute the move and add to solver stack
            self.make_move(move)
            self.solver.add_move(move)
            
            # Update last face and layer
            last_face = move[0] if move[0] not in '123456' else move[1]
            last_layer = move[0] if move[0] in '123456' else None
            
            # Animation delay
            speed_multiplier = self.speed_values[self.speed_slider.value()]
            delay = int(400 / speed_multiplier)
            self.window.update()
            self.app.processEvents()
            QTimer.singleShot(delay, lambda: None)
        
        # Remove scrambling flag
        delattr(self, '_scrambling')
        
        print(f"\nScramble complete with {len(self.solver.move_stack)} moves")

    def solve(self):
        """Solve the cube using the solver"""
        if not hasattr(self, 'solver'):
            print("Solver not initialized")
            return
            
        if self.is_solved():
            print("Cube is already solved!")
            # Clean up the stack when cube is already solved
            self.solver.move_stack = []
            self.moves_to_solve = []
            return
        
        # Store initial state and clear previous moves
        initial_state = self.state.copy()
        self.moves_to_solve = []
        
        try:
            # For cubes larger than 3x3, solve centers and edges first
            if self.size > 3:
                # Store the scramble moves
                scramble_moves = self.solver.move_stack.copy()
                self.solver.move_stack = []
                
                # Solve centers and edges
                self.solver.solve_centers()
                self.solver.solve_edges()
                
                # Combine all moves
                self.moves_to_solve = scramble_moves
            else:
                # For 3x3 and smaller, just use the scramble moves
                self.moves_to_solve = self.solver.move_stack.copy()
            
            # Clear solver stack and start solving
            self.solver.move_stack = []
            
            if not self.moves_to_solve:
                print("No moves to solve")
                self.solve_btn.setEnabled(True)  # Re-enable solve button
                return
            
            self.solve_btn.setEnabled(False)    
            print(f"Starting solve with {len(self.moves_to_solve)} moves")
            self.start_solving()
            self.execute_next_move()
            
        except Exception as e:
            print(f"Solving failed: {e}")
            self.state = initial_state.copy()
            self.solver.move_stack = []
            self.moves_to_solve = []
            self.solve_btn.setEnabled(True)  # Re-enable solve button on failure

    def execute_next_move(self):
        if not self.moves_to_solve or self.solving_stopped:
            if self.solving_stopped:
                self.resume_btn.setEnabled(True)
            else:
                # Re-enable all move buttons when solution is complete
                for btn in self.move_buttons:
                    btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            
            if not self.moves_to_solve and not self.solving_stopped:
                self.is_solved()
            return
        
        try:
            move = self.moves_to_solve.pop()
            inverse_move = move[:-1] if move.endswith("'") else f"{move}'"
            
            # Handle moves with layer numbers (e.g., "2R", "3L")
            if len(move) > 1 and move[0].isdigit():
                layer = int(move[0]) - 1
                face_move = move[1]
                if inverse_move.endswith("'"):
                    for _ in range(3):  # Triple rotation for inverse
                        self.rotate_inner_layer(face_move, layer)
                else:
                    self.rotate_inner_layer(face_move, layer)
            
            # Handle basic moves
            elif move[0] in ['U', 'D', 'L', 'R', 'F', 'B']:
                if inverse_move.endswith("'"):
                    base_move = inverse_move[:-1]
                    self.moves[base_move]()
                    self.moves[base_move]()
                    self.moves[base_move]()
                else:
                    self.moves[inverse_move]()
            
            # Handle middle slice moves
            elif move.startswith('M'):
                layer = self.size // 2 - 1
                if inverse_move.endswith("'"):
                    for _ in range(3):
                        self.rotate_inner_layer('L', layer)
                else:
                    self.rotate_inner_layer('L', layer)
            elif move.startswith('E'):
                layer = self.size // 2 - 1
                if inverse_move.endswith("'"):
                    for _ in range(3):
                        self.rotate_inner_layer('D', layer)
                else:
                    self.rotate_inner_layer('D', layer)
            elif move.startswith('S'):
                layer = self.size // 2 - 1
                if inverse_move.endswith("'"):
                    for _ in range(3):
                        self.rotate_inner_layer('F', layer)
                else:
                    self.rotate_inner_layer('F', layer)
            
            self.window.update()
            print("Remaining moves:", len(self.moves_to_solve))

            speed_multiplier = self.speed_values[self.speed_slider.value()]
            delay = int(400 / speed_multiplier)
            QTimer.singleShot(delay, self.execute_next_move)
            
        except Exception as e:
            print(f"Solving failed: {e}")
            self.state = initial_state.copy()

        # Remove this line as it causes duplicate execution
        # self.execute_next_move()

    def reset(self):
        """Reset cube to solved state"""
        # Reset to solved state using current cube size
        for i in range(6):
            self.state[i] = np.full((self.size, self.size), i)
        
        # Reset the solver state
        if hasattr(self, 'solver'):
            self.solver.reset()
        
        # Clear any solving states
        self.moves_to_solve = []
        if hasattr(self, 'solving_stopped'):
            delattr(self, 'solving_stopped')
        if hasattr(self, '_scrambling'):
            delattr(self, '_scrambling')
        
        # Enable all buttons when reset
        self.scramble_btn.setEnabled(True)
        self.solve_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        
        # Enable all move buttons
        for btn in self.move_buttons:
            btn.setEnabled(True)
        
        # Update the display
        self.window.update()
                    
if __name__ == "__main__":
    cube = RubiksCube()
    sys.exit(cube.app.exec())