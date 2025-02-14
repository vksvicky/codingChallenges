from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRectF, Qt  # Added Qt import
from PyQt6.QtGui import QPainter, QPen

class CubeViewFlat(QWidget):
    def __init__(self, cube):
        super().__init__()
        self.cube = cube
        
        # Initialize zoom parameters
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate cell size based on widget size and cube size
        width = self.width()
        height = self.height()
        cube_size = self.cube.size
        
        # Adjust spacing and cell size for better fit
        spacing = min(width, height) / (12 * cube_size)  # Reduced spacing
        cell_size = min(
            (width - spacing * (4 * cube_size)) / (3 * cube_size),
            (height - spacing * (4 * cube_size)) / (4.5 * cube_size)  # Adjusted ratio
        ) * 1.2  # Slightly smaller overall size
        
        # Adjust starting positions to center the view better
        start_x = (width - cell_size * 3 * cube_size - spacing * (2 * cube_size)) / 2
        start_y = (height - cell_size * 4 * cube_size - spacing * (3 * cube_size)) / 3  # Changed from /2 to /3
        
        # Rearrange faces for better visibility
        faces = [
            (1, 0, 0),  # Up (White)
            (0, 1, 4),  # Left (Blue)
            (1, 1, 2),  # Front (Red)
            (2, 1, 5),  # Right (Green)
            (1, 2, 3),  # Back (Orange)
            (1, 3, 1),  # Down (Yellow)
        ]
        
        for col, row, face in faces:
            x = start_x + col * (cube_size * cell_size + spacing)
            y = start_y + row * (cube_size * cell_size + spacing)
            
            # Draw each cell of the face
            for i in range(cube_size):
                for j in range(cube_size):
                    cell_x = int(x + j * cell_size)
                    cell_y = int(y + i * cell_size)
                    cell_width = int(cell_size - 2)  # Slightly larger gap
                    cell_height = int(cell_size - 2)  # Slightly larger gap
                    
                    color = self.cube.colors[self.cube.state[face, i, j]]
                    painter.fillRect(
                        cell_x,
                        cell_y,
                        cell_width,
                        cell_height,
                        color
                    )

    def wheelEvent(self, event):
        # Add zoom functionality with mouse wheel
        delta = event.angleDelta().y()
        zoom_factor = 0.1  # Adjust zoom speed
        
        # Update zoom level
        self.zoom = max(self.min_zoom, min(self.max_zoom, 
                                         self.zoom + (delta * zoom_factor / 120)))
        self.update()

    def keyPressEvent(self, event):
        # Arrow key controls
        if event.key() == Qt.Key.Key_Left:
            self.rotation[1] -= 5
        elif event.key() == Qt.Key.Key_Right:
            self.rotation[1] += 5
        elif event.key() == Qt.Key.Key_Up:
            self.rotation[0] -= 5
        elif event.key() == Qt.Key.Key_Down:
            self.rotation[0] += 5
        self.update()
