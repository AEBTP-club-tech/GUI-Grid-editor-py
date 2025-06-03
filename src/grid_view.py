from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSlot, QEvent
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QMouseEvent, QWheelEvent

from src.models.constants import NodeType, ForceType
from src.utils.geometry import calculate_distance
from src.utils.drawing import draw_node, draw_force

class GridView(QGraphicsView):
    def __init__(self, app_state):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        
        self.app_state = app_state
        
        # Configure view
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMouseTracking(True)
        
        # Set background color
        self.setBackgroundBrush(QBrush(QColor(self.app_state.grid_bg_color)))
        
        # Drawing state
        self.current_line = None
        self.start_node = None
        self.temp_force = None
        self.selection_highlight = None
        self.is_dragging = False
        self.drag_start_pos = None
        
        # Initialize the view
        self.reset_transform()
        self.update_grid()
    
    def reset_transform(self):
        """Reset zoom and pan"""
        self.resetTransform()
        self.scale(1.0, 1.0)
        self.app_state.zoom_level = 1.0
    
    def update_grid(self):
        """Update and draw the grid"""
        self.scene.clear()
        
        # Update background color
        self.setBackgroundBrush(QBrush(QColor(self.app_state.grid_bg_color)))
        
        # Draw coordinate system
        self.draw_coordinate_system()
        
        # Draw grid lines
        self.draw_grid()
        
        # Draw nodes, lines, and forces
        self.draw_elements()
    
    def update(self):
        """Update the view"""
        self.scene.clear()
        
        # Draw coordinate system and grid
        self.draw_coordinate_system()
        self.draw_grid()
        
        # Draw nodes, lines, and forces
        self.draw_elements()
    
    def draw_coordinate_system(self):
        """Draw the coordinate system with axes and labels"""
        # Get coordinate system parameters
        origin_x = self.app_state.origin_x
        origin_y = self.app_state.origin_y
        
        # Calculate axes lengths
        h_length = self.app_state.calculate_axis_length(self.app_state.h_spacings, self.app_state.scale_factor_x)
        v_length = self.app_state.calculate_axis_length(self.app_state.v_spacings, self.app_state.scale_factor_y)
        
        # Get current plane labels
        if self.app_state.current_plane == "xy":
            h_label, v_label = "X", "Y"
        elif self.app_state.current_plane == "yz":
            h_label, v_label = "Y", "Z"
        else:  # zx
            h_label, v_label = "Z", "X"
        
        # Draw X axis
        x_axis_pen = QPen(QColor(0, 0, 0))
        x_axis_pen.setWidth(2)
        self.scene.addLine(origin_x, origin_y, origin_x + h_length, origin_y, x_axis_pen)
        
        # Draw Y axis
        y_axis_pen = QPen(QColor(0, 0, 0))
        y_axis_pen.setWidth(2)
        self.scene.addLine(origin_x, origin_y, origin_x, origin_y - v_length, y_axis_pen)
        
        # Add axis labels
        self.scene.addText(h_label).setPos(origin_x + h_length + 20, origin_y - 10)
        self.scene.addText(v_label).setPos(origin_x - 10, origin_y - v_length - 30)
        self.scene.addText("O").setPos(origin_x - 20, origin_y + 10)
        
        # Add graduations on horizontal axis
        x = origin_x
        total_distance = 0
        for spacing in self.app_state.h_spacings:
            x += spacing * self.app_state.scale_factor_x * self.app_state.zoom_level
            total_distance += spacing
            
            # Graduation line
            self.scene.addLine(x, origin_y - 5, x, origin_y + 5, x_axis_pen)
            
            # Graduation label
            label = self.scene.addText(f"{total_distance:.1f}")
            label.setPos(x - 10, origin_y + 10)
        
        # Add graduations on vertical axis
        y = origin_y
        total_distance = 0
        for spacing in self.app_state.v_spacings:
            y -= spacing * self.app_state.scale_factor_y * self.app_state.zoom_level
            total_distance += spacing
            
            # Graduation line
            self.scene.addLine(origin_x - 5, y, origin_x + 5, y, y_axis_pen)
            
            # Graduation label
            label = self.scene.addText(f"{total_distance:.1f}")
            label.setPos(origin_x - 30, y - 10)
    
    def draw_grid(self):
        """Draw the grid lines"""
        origin_x = self.app_state.origin_x
        origin_y = self.app_state.origin_y
        
        # Calculate axes lengths
        h_length = self.app_state.calculate_axis_length(self.app_state.h_spacings, self.app_state.scale_factor_x)
        v_length = self.app_state.calculate_axis_length(self.app_state.v_spacings, self.app_state.scale_factor_y)
        
        # Set grid line style
        grid_pen = QPen(QColor("#404040"))
        grid_pen.setWidth(1)
        grid_pen.setStyle(Qt.PenStyle.DashLine)
        
        # Set main grid line style (thicker)
        main_grid_pen = QPen(QColor("#606060"))
        main_grid_pen.setWidth(2)
        
        # Draw vertical grid lines
        x = origin_x
        for i, spacing in enumerate(self.app_state.h_spacings):
            x += spacing * self.app_state.scale_factor_x * self.app_state.zoom_level
            
            # Use thicker pen for every 5th line
            pen = main_grid_pen if (i + 1) % 5 == 0 else grid_pen
            self.scene.addLine(x, origin_y, x, origin_y - v_length, pen)
        
        # Draw horizontal grid lines
        y = origin_y
        for i, spacing in enumerate(self.app_state.v_spacings):
            y -= spacing * self.app_state.scale_factor_y * self.app_state.zoom_level
            
            # Use thicker pen for every 5th line
            pen = main_grid_pen if (i + 1) % 5 == 0 else grid_pen
            self.scene.addLine(origin_x, y, origin_x + h_length, y, pen)
    
    def draw_elements(self):
        """Draw all nodes, lines, and forces"""
        # Draw lines first (so they're behind nodes)
        for i, (x1, y1, x2, y2) in enumerate(self.app_state.line_positions):
            # Convert real coordinates to screen coordinates
            screen_x1 = self.app_state.origin_x + (x1 - self.app_state.origin_x) * self.app_state.zoom_level
            screen_y1 = self.app_state.origin_y + (y1 - self.app_state.origin_y) * self.app_state.zoom_level
            screen_x2 = self.app_state.origin_x + (x2 - self.app_state.origin_x) * self.app_state.zoom_level
            screen_y2 = self.app_state.origin_y + (y2 - self.app_state.origin_y) * self.app_state.zoom_level
            
            # Draw line
            line_pen = QPen(QColor("blue"))
            line_pen.setWidth(max(2, int(3 * self.app_state.zoom_level)))
            self.scene.addLine(screen_x1, screen_y1, screen_x2, screen_y2, line_pen)
        
        # Draw nodes
        for i, (x, y) in enumerate(self.app_state.node_positions):
            # Convert real coordinates to screen coordinates
            screen_x = self.app_state.origin_x + (x - self.app_state.origin_x) * self.app_state.zoom_level
            screen_y = self.app_state.origin_y + (y - self.app_state.origin_y) * self.app_state.zoom_level
            
            # Draw node
            node_type = self.app_state.node_types[i]
            draw_node(self.scene, screen_x, screen_y, node_type, self.app_state.zoom_level)
        
        # Draw forces
        for i, (x, y) in enumerate(self.app_state.force_positions):
            # Convert real coordinates to screen coordinates
            screen_x = self.app_state.origin_x + (x - self.app_state.origin_x) * self.app_state.zoom_level
            screen_y = self.app_state.origin_y + (y - self.app_state.origin_y) * self.app_state.zoom_level
            
            # Draw force
            force_type = self.app_state.force_types[i]
            force_value = self.app_state.force_values[i]
            draw_force(self.scene, screen_x, screen_y, force_type, force_value, self.app_state.zoom_level)
        
        # Draw temporary line during drawing
        if self.current_line and self.start_node is not None:
            start_node_idx = self.app_state.nodes.index(self.start_node)
            start_x, start_y = self.app_state.node_positions[start_node_idx]
            
            # Convert to screen coordinates
            screen_x = self.app_state.origin_x + (start_x - self.app_state.origin_x) * self.app_state.zoom_level
            screen_y = self.app_state.origin_y + (start_y - self.app_state.origin_y) * self.app_state.zoom_level
            
            # Draw temporary line
            temp_pen = QPen(QColor("red"))
            temp_pen.setWidth(2)
            temp_pen.setStyle(Qt.PenStyle.DashLine)
            self.scene.addLine(screen_x, screen_y, self.current_line[0], self.current_line[1], temp_pen)
    
    def update_scale(self, axis, value):
        """Update scale for an axis"""
        if axis == 'x':
            self.app_state.scale_factor_x = 100 * value
        else:
            self.app_state.scale_factor_y = 100 * value
        
        self.update()
    
    def zoom(self, factor):
        """Zoom the view"""
        # Update zoom level
        self.app_state.zoom_level *= factor
        
        # Limit zoom between 0.1 and 5.0
        self.app_state.zoom_level = max(0.1, min(5.0, self.app_state.zoom_level))
        
        # Update the view
        self.update()
    
    def reset_zoom(self):
        """Reset zoom to original level"""
        self.app_state.zoom_level = 1.0
        self.update()
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.app_state.grid_visible = not self.app_state.grid_visible
        self.update()
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events"""
        # Get mouse position
        pos = self.mapToScene(event.pos())
        x, y = pos.x(), pos.y()
        
        # Left button
        if event.button() == Qt.MouseButton.LeftButton:
            if self.app_state.force_placement_mode:
                self.place_force(x, y)
            elif self.app_state.selection_mode:
                self.select_element(x, y)
            else:
                self.start_drawing(x, y)
        
        # Middle button (pan)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.is_dragging = True
            self.drag_start_pos = pos
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        
        # Right button (erase)
        elif event.button() == Qt.MouseButton.RightButton:
            if self.app_state.eraser_mode:
                self.erase_element(x, y)
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events"""
        pos = self.mapToScene(event.pos())
        x, y = pos.x(), pos.y()
        
        # Update current line if drawing
        if self.current_line and event.buttons() & Qt.MouseButton.LeftButton:
            self.current_line = (x, y)
            self.update()
        
        # Pan view if middle button is pressed
        if self.is_dragging and event.buttons() & Qt.MouseButton.MiddleButton:
            delta = pos - self.drag_start_pos
            self.app_state.origin_x += delta.x()
            self.app_state.origin_y += delta.y()
            
            # Update all node positions
            for i in range(len(self.app_state.node_positions)):
                x, y = self.app_state.node_positions[i]
                self.app_state.node_positions[i] = (x + delta.x(), y + delta.y())
            
            # Update all line positions
            for i in range(len(self.app_state.line_positions)):
                x1, y1, x2, y2 = self.app_state.line_positions[i]
                self.app_state.line_positions[i] = (x1 + delta.x(), y1 + delta.y(), 
                                                  x2 + delta.x(), y2 + delta.y())
            
            # Update view
            self.drag_start_pos = pos
            self.update()
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events"""
        pos = self.mapToScene(event.pos())
        x, y = pos.x(), pos.y()
        
        # Finish drawing line
        if self.current_line and event.button() == Qt.MouseButton.LeftButton:
            self.finish_line(x, y)
            self.current_line = None
        
        # End panning
        if self.is_dragging and event.button() == Qt.MouseButton.MiddleButton:
            self.is_dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle zoom with mouse wheel"""
        # Zoom in or out based on wheel direction
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.zoom(factor)
    
    def find_closest_node(self, x, y, max_distance=30):
        """Find the closest node to the given position"""
        min_distance = float('inf')
        closest_node = None
        closest_idx = -1
        
        for i, (node_x, node_y) in enumerate(self.app_state.node_positions):
            # Convert to screen coordinates
            screen_x = self.app_state.origin_x + (node_x - self.app_state.origin_x) * self.app_state.zoom_level
            screen_y = self.app_state.origin_y + (node_y - self.app_state.origin_y) * self.app_state.zoom_level
            
            # Calculate distance
            distance = calculate_distance(x, y, screen_x, screen_y)
            
            if distance < min_distance and distance < max_distance:
                min_distance = distance
                closest_node = i
                closest_idx = i
        
        return closest_node, closest_idx
    
    def find_grid_intersection(self, x, y, snap_distance=10):
        """Find the closest grid intersection to the given position"""
        origin_x = self.app_state.origin_x
        origin_y = self.app_state.origin_y
        
        # Find closest x coordinate
        closest_x = origin_x
        min_x_dist = float('inf')
        
        curr_x = origin_x
        for spacing in self.app_state.h_spacings:
            curr_x += spacing * self.app_state.scale_factor_x * self.app_state.zoom_level
            dist = abs(x - curr_x)
            if dist < min_x_dist:
                min_x_dist = dist
                closest_x = curr_x
        
        # Find closest y coordinate
        closest_y = origin_y
        min_y_dist = float('inf')
        
        curr_y = origin_y
        for spacing in self.app_state.v_spacings:
            curr_y -= spacing * self.app_state.scale_factor_y * self.app_state.zoom_level
            dist = abs(y - curr_y)
            if dist < min_y_dist:
                min_y_dist = dist
                closest_y = curr_y
        
        # Return intersection if close enough
        if min_x_dist < snap_distance and min_y_dist < snap_distance:
            return closest_x, closest_y
        
        return None
    
    def start_drawing(self, x, y):
        """Start drawing a line or node"""
        # Save state for undo
        self.app_state.save_state()
        
        # Find closest node
        closest_node, closest_idx = self.find_closest_node(x, y)
        
        if closest_node is not None:
            # Start a line from this node
            self.start_node = closest_node
            self.current_line = (x, y)
        else:
            # Find grid intersection
            intersection = self.find_grid_intersection(x, y)
            
            if intersection:
                grid_x, grid_y = intersection
                
                # Convert to real coordinates
                real_x = self.app_state.origin_x + (grid_x - self.app_state.origin_x) / self.app_state.zoom_level
                real_y = self.app_state.origin_y + (grid_y - self.app_state.origin_y) / self.app_state.zoom_level
                
                # Create new node
                self.app_state.add_node(real_x, real_y, self.app_state.current_node_type)
                
                # Start a line from this node
                self.start_node = len(self.app_state.nodes) - 1
                self.current_line = (grid_x, grid_y)
        
        self.update()
    
    def finish_line(self, x, y):
        """Finish drawing a line"""
        if self.start_node is None:
            return
        
        # Find closest node
        end_node, end_idx = self.find_closest_node(x, y)
        
        if end_node is not None and end_node != self.start_node:
            # Get start and end positions
            start_x, start_y = self.app_state.node_positions[self.start_node]
            end_x, end_y = self.app_state.node_positions[end_node]
            
            # Add line
            self.app_state.add_line(start_x, start_y, end_x, end_y)
        
        self.start_node = None
        self.current_line = None
        self.update()
    
    def select_element(self, x, y):
        """Select an element at the given position"""
        # Clear current selection
        if self.selection_highlight:
            self.scene.removeItem(self.selection_highlight)
            self.selection_highlight = None
        
        # Find closest node
        node, node_idx = self.find_closest_node(x, y)
        
        if node is not None:
            # Highlight the node
            node_x, node_y = self.app_state.node_positions[node]
            
            # Convert to screen coordinates
            screen_x = self.app_state.origin_x + (node_x - self.app_state.origin_x) * self.app_state.zoom_level
            screen_y = self.app_state.origin_y + (node_y - self.app_state.origin_y) * self.app_state.zoom_level
            
            # Create highlight
            size = 16 * self.app_state.zoom_level
            highlight_pen = QPen(QColor("yellow"))
            highlight_pen.setWidth(2)
            highlight_pen.setStyle(Qt.PenStyle.DashLine)
            
            self.selection_highlight = self.scene.addEllipse(
                screen_x - size, screen_y - size, size * 2, size * 2, 
                highlight_pen, QBrush(Qt.BrushStyle.NoBrush)
            )
            
            # Set selected element
            self.app_state.selected_element = ("node", node)
            
            # Show force dialog or handle selection action
            # (This would be implemented in a separate method)
        
        self.update()
    
    def erase_element(self, x, y):
        """Erase an element at the given position"""
        # Save state for undo
        self.app_state.save_state()
        
        # Find closest node
        node, node_idx = self.find_closest_node(x, y)
        
        if node is not None:
            # Remove node and all connected lines
            self.app_state.delete_node(node)
            self.update()
        
        # TODO: Add support for erasing lines and forces
    
    def place_force(self, x, y):
        """Place a force at the given position"""
        # TODO: Implement force placement logic
        pass
    
    def start_force_placement(self):
        """Enter force placement mode"""
        self.app_state.force_placement_mode = True
        self.setCursor(Qt.CursorShape.CrossCursor)