from PyQt6.QtCore import QObject, pyqtSignal
import copy

from src.models.constants import NodeType, ForceType

class AppState(QObject):
    """Manages the application state and emits signals when it changes"""
    # Signals
    node_added = pyqtSignal(int)  # Node index
    line_added = pyqtSignal(int)  # Line index
    force_added = pyqtSignal(int)  # Force index
    element_deleted = pyqtSignal(str, int)  # Type, index
    state_changed = pyqtSignal()  # Generic state change
    plane_changed = pyqtSignal(str)  # New plane
    
    def __init__(self):
        super().__init__()
        
        # Grid properties
        self.grid_visible = True
        self.grid_bg_color = "#f0f0f0"
        self.h_spacings = [1.0, 2.0, 5.0, 6.0]
        self.v_spacings = [7.0, 8.0, 4.0, 5.0]
        
        # Coordinate system
        self.origin_x = 100
        self.origin_y = 700
        self.zoom_level = 1.0
        self.scale_factor_x = 100
        self.scale_factor_y = 100
        
        # Active plane
        self.current_plane = "xy"
        
        # Elements
        self.nodes = []  # Nodes (as indexes)
        self.node_types = []  # Node types corresponding to nodes
        self.node_positions = []  # (x, y) positions
        self.lines = []  # Lines (as indexes)
        self.line_positions = []  # (x1, y1, x2, y2) positions
        self.forces = []  # Forces (as indexes)
        self.force_positions = []  # (x, y) positions
        self.force_types = []  # Force types
        self.force_values = []  # Force values
        
        # Current state
        self.current_node_type = NodeType.SIMPLE
        self.current_force_type = ForceType.POINT
        self.current_force_value = 0.0
        
        # Modes
        self.selection_mode = False
        self.eraser_mode = False
        self.force_placement_mode = False
        
        # Selection
        self.selected_element = None  # (type, index)
        
        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo_steps = 50
        
        # File management
        self.current_file_path = None
        
        # Zen mode
        self.zen_mode = False
    
    def save_state(self):
        """Save current state for undo"""
        state = {
            "nodes": self.nodes.copy(),
            "node_types": self.node_types.copy(),
            "node_positions": [(x, y) for x, y in self.node_positions],
            "lines": self.lines.copy(),
            "line_positions": [(x1, y1, x2, y2) for x1, y1, x2, y2 in self.line_positions],
            "forces": self.forces.copy(),
            "force_positions": [(x, y) for x, y in self.force_positions],
            "force_types": self.force_types.copy(),
            "force_values": self.force_values.copy(),
            "origin_x": self.origin_x,
            "origin_y": self.origin_y,
            "zoom_level": self.zoom_level,
            "scale_factor_x": self.scale_factor_x,
            "scale_factor_y": self.scale_factor_y
        }
        
        self.undo_stack.append(state)
        self.redo_stack.clear()
        
        # Limit undo stack size
        if len(self.undo_stack) > self.max_undo_steps:
            self.undo_stack.pop(0)
    
    def undo(self):
        """Undo the last action"""
        if not self.undo_stack:
            return False
        
        # Save current state for redo
        current_state = {
            "nodes": self.nodes.copy(),
            "node_types": self.node_types.copy(),
            "node_positions": [(x, y) for x, y in self.node_positions],
            "lines": self.lines.copy(),
            "line_positions": [(x1, y1, x2, y2) for x1, y1, x2, y2 in self.line_positions],
            "forces": self.forces.copy(),
            "force_positions": [(x, y) for x, y in self.force_positions],
            "force_types": self.force_types.copy(),
            "force_values": self.force_values.copy(),
            "origin_x": self.origin_x,
            "origin_y": self.origin_y,
            "zoom_level": self.zoom_level,
            "scale_factor_x": self.scale_factor_x,
            "scale_factor_y": self.scale_factor_y
        }
        
        self.redo_stack.append(current_state)
        
        # Restore previous state
        state = self.undo_stack.pop()
        self.restore_state(state)
        
        # Emit signal
        self.state_changed.emit()
        
        return True
    
    def redo(self):
        """Redo the last undone action"""
        if not self.redo_stack:
            return False
        
        # Save current state for undo
        current_state = {
            "nodes": self.nodes.copy(),
            "node_types": self.node_types.copy(),
            "node_positions": [(x, y) for x, y in self.node_positions],
            "lines": self.lines.copy(),
            "line_positions": [(x1, y1, x2, y2) for x1, y1, x2, y2 in self.line_positions],
            "forces": self.forces.copy(),
            "force_positions": [(x, y) for x, y in self.force_positions],
            "force_types": self.force_types.copy(),
            "force_values": self.force_values.copy(),
            "origin_x": self.origin_x,
            "origin_y": self.origin_y,
            "zoom_level": self.zoom_level,
            "scale_factor_x": self.scale_factor_x,
            "scale_factor_y": self.scale_factor_y
        }
        
        self.undo_stack.append(current_state)
        
        # Restore next state
        state = self.redo_stack.pop()
        self.restore_state(state)
        
        # Emit signal
        self.state_changed.emit()
        
        return True
    
    def restore_state(self, state):
        """Restore state from saved state"""
        self.nodes = state["nodes"].copy()
        self.node_types = state["node_types"].copy()
        self.node_positions = [(x, y) for x, y in state["node_positions"]]
        self.lines = state["lines"].copy()
        self.line_positions = [(x1, y1, x2, y2) for x1, y1, x2, y2 in state["line_positions"]]
        self.forces = state["forces"].copy()
        self.force_positions = [(x, y) for x, y in state["force_positions"]]
        self.force_types = state["force_types"].copy()
        self.force_values = state["force_values"].copy()
        self.origin_x = state["origin_x"]
        self.origin_y = state["origin_y"]
        self.zoom_level = state["zoom_level"]
        self.scale_factor_x = state["scale_factor_x"]
        self.scale_factor_y = state["scale_factor_y"]
    
    def add_node(self, x, y, node_type):
        """Add a new node"""
        node_id = len(self.nodes)
        self.nodes.append(node_id)
        self.node_types.append(node_type)
        self.node_positions.append((x, y))
        
        # Emit signal
        self.node_added.emit(node_id)
        
        return node_id
    
    def add_line(self, x1, y1, x2, y2):
        """Add a new line"""
        line_id = len(self.lines)
        self.lines.append(line_id)
        self.line_positions.append((x1, y1, x2, y2))
        
        # Emit signal
        self.line_added.emit(line_id)
        
        return line_id
    
    def add_force(self, x, y, force_type, force_value):
        """Add a new force"""
        force_id = len(self.forces)
        self.forces.append(force_id)
        self.force_positions.append((x, y))
        self.force_types.append(force_type)
        self.force_values.append(force_value)
        
        # Emit signal
        self.force_added.emit(force_id)
        
        return force_id
    
    def delete_node(self, node_id):
        """Delete a node and all connected lines"""
        if node_id >= len(self.nodes):
            return False
        
        # Find and delete all connected lines
        lines_to_remove = []
        for i, (x1, y1, x2, y2) in enumerate(self.line_positions):
            node_x, node_y = self.node_positions[node_id]
            if (abs(x1 - node_x) < 1 and abs(y1 - node_y) < 1) or \
               (abs(x2 - node_x) < 1 and abs(y2 - node_y) < 1):
                lines_to_remove.append(i)
        
        # Remove lines in reverse order to avoid index issues
        for i in sorted(lines_to_remove, reverse=True):
            del self.lines[i]
            del self.line_positions[i]
            self.element_deleted.emit("line", i)
        
        # Remove the node
        del self.nodes[node_id]
        del self.node_types[node_id]
        del self.node_positions[node_id]
        
        # Emit signal
        self.element_deleted.emit("node", node_id)
        
        return True
    
    def delete_line(self, line_id):
        """Delete a line"""
        if line_id >= len(self.lines):
            return False
        
        # Remove the line
        del self.lines[line_id]
        del self.line_positions[line_id]
        
        # Emit signal
        self.element_deleted.emit("line", line_id)
        
        return True
    
    def delete_force(self, force_id):
        """Delete a force"""
        if force_id >= len(self.forces):
            return False
        
        # Remove the force
        del self.forces[force_id]
        del self.force_positions[force_id]
        del self.force_types[force_id]
        del self.force_values[force_id]
        
        # Emit signal
        self.element_deleted.emit("force", force_id)
        
        return True
    
    def clear_all(self):
        """Clear all elements"""
        # Save state for undo
        self.save_state()
        
        # Clear all lists
        self.nodes = []
        self.node_types = []
        self.node_positions = []
        self.lines = []
        self.line_positions = []
        self.forces = []
        self.force_positions = []
        self.force_types = []
        self.force_values = []
        
        # Emit signal
        self.state_changed.emit()
    
    def set_current_plane(self, plane):
        """Set the active plane"""
        if plane in ["xy", "yz", "zx"] and plane != self.current_plane:
            self.current_plane = plane
            self.plane_changed.emit(plane)
    
    def calculate_axis_length(self, spacings, scale_factor):
        """Calculate the length of an axis in pixels"""
        # Calculate total length of spacings
        total_length = sum(spacings)
        # Calculate pixel length with zoom and scale factor
        return total_length * scale_factor * self.zoom_level