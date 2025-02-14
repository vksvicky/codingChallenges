from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter, QPen

class CubeViewUnfolded(QWidget):
    def __init__(self, cube):
        super().__init__()
        self.cube = cube

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Adjust cell size for better fit
        cell_size = min(self.width() // 4, self.height() // 5) * 1.1  # Reduced multiplier and increased vertical divisions
        
        # Center the layout with more vertical space
        start_x = (self.width() - cell_size * 3) / 2
        start_y = (self.height() - cell_size * 4.5) / 2  # Increased vertical space
        
        # Draw unfolded layout in cross pattern
        layouts = [
            (1, 0, 0),  # Up
            (0, 1, 4),  # Left
            (1, 1, 2),  # Front
            (2, 1, 5),  # Right
            (1, 2, 3),  # Back
            (1, 3, 1)   # Down
        ]
        
        for face, (x, y, idx) in enumerate(layouts):
            for i in range(self.cube.size):
                for j in range(self.cube.size):
                    rect = QRectF(
                        start_x + x * cell_size + j * (cell_size / self.cube.size),
                        start_y + y * cell_size + i * (cell_size / self.cube.size),
                        cell_size / self.cube.size - 1,  # Add small gap
                        cell_size / self.cube.size - 1   # Add small gap
                    )
                    color = self.cube.colors[self.cube.state[idx, i, j]]
                    painter.fillRect(rect, color)
                    # Set darker border
                    pen = QPen(color.darker(150))
                    pen.setWidth(1)
                    painter.setPen(pen)
                    painter.drawRect(rect)
