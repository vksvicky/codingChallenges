from PyQt6.QtWidgets import QWidget, QToolTip
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QPen, QCursor
import numpy as np

class CubeView3D(QWidget):
    def __init__(self, cube):
        super().__init__()
        self.cube = cube
        self.rotation = [30, 45, 0]
        self.setMouseTracking(True)
        self.last_pos = None
        self.mouse_pressed = False
        self.zoom = 1.0  # Initial zoom level
        self.min_zoom = 1.0  # Minimum zoom level
        self.max_zoom = 2.0  # Maximum zoom level
        self.transparency = False
        self.lift_faces = False
        self.zoom_buttons = {'+': QRectF(10, 10, 30, 30), '-': QRectF(10, 50, 30, 30)}

    # In the paintEvent method, update the pen color and width
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Draw the cube first
        width = self.width()
        height = self.height()
        
        # Draw zoom controls first (before translation)
        tooltips = {'+': 'Zoom in', '-': 'Zoom out'}
        cursor_pos = QPointF(self.mapFromGlobal(QCursor.pos()))  # Convert QPoint to QPointF
        for text, rect in self.zoom_buttons.items():
            painter.setPen(QPen(Qt.GlobalColor.black))
            painter.setBrush(QColor(220, 220, 220))
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
            if rect.contains(cursor_pos):  # Use the converted point
                QToolTip.showText(QCursor.pos(), tooltips[text])
        
        # Now translate for cube drawing
        painter.translate(width / 2, height / 2)

        # Calculate scale based on widget size and zoom
        base_scale = min(width, height) / 6
        scale = base_scale * self.zoom * (1.0 + self.rotation[2] / 200.0)

        # Calculate rotation matrices
        rx = np.radians(self.rotation[0])
        ry = np.radians(self.rotation[1])

        # Define cube vertices with proper size and orientation
        size = 0.8  # Slightly smaller cube for better visibility
        vertices = np.array([
            [-size, -size, -size],  # 0: front bottom left
            [size, -size, -size],   # 1: front bottom right
            [size, size, -size],    # 2: front top right
            [-size, size, -size],   # 3: front top left
            [-size, -size, size],   # 4: back bottom left
            [size, -size, size],    # 5: back bottom right
            [size, size, size],     # 6: back top right
            [-size, size, size]     # 7: back top left
        ])

        # Define faces with correct winding order and orientation
        faces = [
            (0, 1, 2, 3),  # Front (Z-)
            (5, 4, 7, 6),  # Back (Z+)
            (4, 0, 3, 7),  # Left (X-)
            (1, 5, 6, 2),  # Right (X+)
            (3, 2, 6, 7),  # Top (Y+)
            (4, 5, 1, 0)   # Bottom (Y-)
        ]

        # Map faces to cube state indices (matching the actual cube state)
        face_indices = [2, 3, 4, 5, 0, 1]  # Front, Back, Left, Right, Top, Bottom

        # Project vertices with proper perspective
        projected = []
        for v in vertices:
            # Rotate around Y
            x = v[0] * np.cos(ry) - v[2] * np.sin(ry)
            z = v[0] * np.sin(ry) + v[2] * np.cos(ry)
            
            # Rotate around X
            y = v[1] * np.cos(rx) - z * np.sin(rx)
            z2 = v[1] * np.sin(rx) + z * np.cos(rx)
            
            # Apply perspective projection
            d = 5.0  # Perspective strength
            f = d / (d + z2)
            x_proj = x * scale * f
            y_proj = y * scale * f
            projected.append((x_proj, y_proj, z2))

        # Sort faces by depth for proper rendering
        face_depths = []
        for i, face in enumerate(faces):
            z = sum(projected[v][2] for v in face) / 4
            face_depths.append((z, i))
        face_depths.sort(reverse=True)  # Draw back-to-front

        # Draw faces with subdivisions
        for _, face_idx in face_depths:
            face = faces[face_idx]
            points = [projected[v] for v in face]
            state_idx = face_indices[face_idx]

            # Apply lift effect for hidden faces
            if self.lift_faces:
                # Determine if this is a hidden face based on current rotation
                is_hidden = False
                angle = (self.rotation[1] % 360)  # Get angle between 0 and 360
                
                if 0 <= angle < 90:  # Viewing from front-right
                    is_hidden = face_idx in [1, 2]  # Back and Left faces
                elif 90 <= angle < 180:  # Viewing from back-right
                    is_hidden = face_idx in [0, 2]  # Front and Left faces
                elif 180 <= angle < 270:  # Viewing from back-left
                    is_hidden = face_idx in [0, 3]  # Front and Right faces
                else:  # Viewing from front-left
                    is_hidden = face_idx in [1, 3]  # Back and Right faces
                
                if is_hidden:
                    offset = 0.3  # Reduced offset distance for subtler effect
                    # Calculate offset direction based on face position
                    dx = offset * np.cos(ry) * scale
                    dy = offset * np.sin(rx) * scale
                    dz = offset * scale
                    
                    # Apply offset to all points of the face
                    points = [(x + dx, y + dy, z + dz) for x, y, z in points]

            # Draw each cubelet
            for i in range(self.cube.size):
                for j in range(self.cube.size):
                    sub_points = self._get_subdivision(points, i, j)
                    
                    path = QPainterPath()
                    path.moveTo(sub_points[0][0], sub_points[0][1])
                    for point in sub_points[1:]:
                        path.lineTo(point[0], point[1])
                    path.closeSubpath()
                    
                    color_idx = self.cube.state[state_idx, i, j]
                    color = QColor(self.cube.colors[color_idx])  # Create new QColor instance
                    
                    # Apply transparency to hidden faces
                    if self.transparency:
                        if state_idx in [0, 1, 2, 3, 4, 5]:  # All faces including white (0)
                            color.setAlpha(32)  # Make more transparent
                    
                    # Draw filled cubelet with darker border
                    painter.setBrush(color)
                    pen = QPen(color.darker(150))
                    pen.setWidth(2)
                    painter.setPen(pen)
                    painter.drawPath(path)

    def _get_subdivision(self, face_points, i, j):
        size = self.cube.size
        points = []
        x = [p[0] for p in face_points]
        y = [p[1] for p in face_points]
        
        for u, v in [(j/size, i/size), ((j+1)/size, i/size), 
                     ((j+1)/size, (i+1)/size), (j/size, (i+1)/size)]:
            px = (1-v)*((1-u)*x[0] + u*x[1]) + v*((1-u)*x[3] + u*x[2])
            py = (1-v)*((1-u)*y[0] + u*y[1]) + v*((1-u)*y[3] + u*y[2])
            points.append((px, py))
        return points

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.rotation[2] = max(-50, min(50, self.rotation[2] + delta * 0.1))
        self.update()

    def mousePressEvent(self, event):
        pos = QPointF(event.pos())
        for text, rect in self.zoom_buttons.items():
            if rect.contains(pos):
                if text == '+':
                    self.zoom = min(self.max_zoom, self.zoom + 0.1)
                else:
                    self.zoom = max(self.min_zoom, self.zoom - 0.1)
                self.update()
                return

        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            self.last_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
            self.last_pos = None  # Reset last position

    def mouseMoveEvent(self, event):
        if not self.mouse_pressed or self.last_pos is None:
            return
            
        dx = event.pos().x() - self.last_pos.x()
        dy = event.pos().y() - self.last_pos.y()
        
        # Update rotation angles
        self.rotation[1] += dx * 0.5
        self.rotation[0] += dy * 0.5
        self.rotation[0] = max(-90, min(90, self.rotation[0]))
        
        self.last_pos = event.pos()
        self.update()

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
