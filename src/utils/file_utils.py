import json
import os
import math

class FileManager:
    def __init__(self, app_state):
        self.app_state = app_state
    
    def save_file(self, file_path):
        """Save the grid structure to a file"""
        try:
            data = {
                "nodes": [],
                "lines": []
            }
            
            # Save nodes
            for i, (x, y) in enumerate(self.app_state.node_positions):
                # Convert to real-world coordinates
                x_meters = (x - self.app_state.origin_x) / self.app_state.scale_factor_x
                y_meters = (self.app_state.origin_y - y) / self.app_state.scale_factor_y
                
                node_data = {
                    "id": i + 1,
                    "type": self.app_state.node_types[i],
                    "coordinates": {
                        "x": round(x_meters, 2),
                        "y": round(y_meters, 2)
                    }
                }
                data["nodes"].append(node_data)
            
            # Save lines
            for i, (x1, y1, x2, y2) in enumerate(self.app_state.line_positions):
                # Convert to real-world coordinates
                x1_meters = (x1 - self.app_state.origin_x) / self.app_state.scale_factor_x
                y1_meters = (self.app_state.origin_y - y1) / self.app_state.scale_factor_y
                x2_meters = (x2 - self.app_state.origin_x) / self.app_state.scale_factor_x
                y2_meters = (self.app_state.origin_y - y2) / self.app_state.scale_factor_y
                
                # Calculate length
                length = math.sqrt((x2_meters - x1_meters) ** 2 + (y2_meters - y1_meters) ** 2)
                
                line_data = {
                    "id": i + 1,
                    "start_node": {
                        "x": round(x1_meters, 2),
                        "y": round(y1_meters, 2)
                    },
                    "end_node": {
                        "x": round(x2_meters, 2),
                        "y": round(y2_meters, 2)
                    },
                    "length": round(length, 2)
                }
                data["lines"].append(line_data)
            
            # Save to file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            # Update current file path
            self.app_state.current_file_path = file_path
            
            return True
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return False
    
    def load_file(self, file_path):
        """Load the grid structure from a file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Clear current structure
            self.app_state.clear_all()
            
            # Load nodes
            for node_data in data["nodes"]:
                # Convert from real-world coordinates to screen coordinates
                x = self.app_state.origin_x + node_data["coordinates"]["x"] * self.app_state.scale_factor_x
                y = self.app_state.origin_y - node_data["coordinates"]["y"] * self.app_state.scale_factor_y
                
                # Add node
                self.app_state.nodes.append(len(self.app_state.nodes))
                self.app_state.node_types.append(node_data["type"])
                self.app_state.node_positions.append((x, y))
            
            # Load lines
            for line_data in data["lines"]:
                # Convert from real-world coordinates to screen coordinates
                x1 = self.app_state.origin_x + line_data["start_node"]["x"] * self.app_state.scale_factor_x
                y1 = self.app_state.origin_y - line_data["start_node"]["y"] * self.app_state.scale_factor_y
                x2 = self.app_state.origin_x + line_data["end_node"]["x"] * self.app_state.scale_factor_x
                y2 = self.app_state.origin_y - line_data["end_node"]["y"] * self.app_state.scale_factor_y
                
                # Add line
                self.app_state.lines.append(len(self.app_state.lines))
                self.app_state.line_positions.append((x1, y1, x2, y2))
            
            # Update current file path
            self.app_state.current_file_path = file_path
            
            # Signal that the state has changed
            self.app_state.state_changed.emit()
            
            return True
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return False
    
    def export_data(self, file_path):
        """Export grid structure data in a format suitable for analysis"""
        try:
            # Create data structure
            data = {
                "nodes": [],
                "lines": []
            }
            
            # Add node data
            for i, (x, y) in enumerate(self.app_state.node_positions):
                # Convert to real-world coordinates
                x_meters = (x - self.app_state.origin_x) / self.app_state.scale_factor_x
                y_meters = (self.app_state.origin_y - y) / self.app_state.scale_factor_y
                
                node_data = {
                    "id": i + 1,
                    "type": self.app_state.node_types[i],
                    "coordinates": {
                        "x": round(x_meters, 2),
                        "y": round(y_meters, 2)
                    }
                }
                data["nodes"].append(node_data)
            
            # Add line data
            for i, (x1, y1, x2, y2) in enumerate(self.app_state.line_positions):
                # Convert to real-world coordinates
                x1_meters = (x1 - self.app_state.origin_x) / self.app_state.scale_factor_x
                y1_meters = (self.app_state.origin_y - y1) / self.app_state.scale_factor_y
                x2_meters = (x2 - self.app_state.origin_x) / self.app_state.scale_factor_x
                y2_meters = (self.app_state.origin_y - y2) / self.app_state.scale_factor_y
                
                # Calculate length
                length = math.sqrt((x2_meters - x1_meters) ** 2 + (y2_meters - y1_meters) ** 2)
                
                line_data = {
                    "id": i + 1,
                    "start_node": {
                        "x": round(x1_meters, 2),
                        "y": round(y1_meters, 2)
                    },
                    "end_node": {
                        "x": round(x2_meters, 2),
                        "y": round(y2_meters, 2)
                    },
                    "length": round(length, 2)
                }
                data["lines"].append(line_data)
            
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            os.makedirs("data/grille", exist_ok=True)
            
            # Save to file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return False