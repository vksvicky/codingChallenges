from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

class CubeControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Move buttons
        moves_layout = QHBoxLayout()
        self.move_buttons = {}
        for move in ['U', 'D', 'L', 'R', 'F', 'B']:
            # Regular move button
            btn = QPushButton(move)
            moves_layout.addWidget(btn)
            self.move_buttons[move] = btn

            # Inverse move button
            btn_inv = QPushButton(f"{move}'")
            moves_layout.addWidget(btn_inv)
            self.move_buttons[f"{move}'"] = btn_inv

        layout.addLayout(moves_layout)

        # Control buttons
        controls_layout = QHBoxLayout()
        
        self.scramble_btn = QPushButton('🔀')
        self.solve_btn = QPushButton('▶️')
        self.stop_btn = QPushButton('⏸️')
        self.resume_btn = QPushButton('⏭️')
        
        self.stop_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        
        controls_layout.addWidget(self.scramble_btn)
        controls_layout.addWidget(self.solve_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.resume_btn)
        
        layout.addLayout(controls_layout)

    def stop_solving(self):
        """Stop the solving process"""
        self.stop_btn.setEnabled(False)
        self.resume_btn.setEnabled(True)
        self.solve_btn.setEnabled(False)
        for btn in self.move_buttons.values():
            btn.setEnabled(False)

    def resume_solving(self):
        """Resume the solving process"""
        self.stop_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)
        self.solve_btn.setEnabled(False)
        for btn in self.move_buttons.values():
            btn.setEnabled(True)