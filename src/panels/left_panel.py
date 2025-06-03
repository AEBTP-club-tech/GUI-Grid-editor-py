from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton, QGroupBox, 
    QFormLayout, QLineEdit, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.models.constants import NodeType

class LeftPanel(QScrollArea):
    # Signal emitted when grid settings are updated
    grid_updated = pyqtSignal()
    
    def __init__(self, app_state):
        super().__init__()
        self.app_state = app_state
        
        # Configure scroll area
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create content widget
        content = QWidget()
        self.setWidget(content)
        
        # Create main layout
        layout = QVBoxLayout(content)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(16)
        
        # Add panel title
        title = QLabel("Drawing Tools")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Add node types group
        self.add_node_types_group(layout)
        
        # Add force value group
        self.add_force_value_group(layout)
        
        # Add grid spacing group
        self.add_grid_spacing_group(layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def add_node_types_group(self, layout):
        """Add node types selection group"""
        group_box = QGroupBox("Node Types")
        group_layout = QVBoxLayout()
        
        # Create radio buttons for node types
        self.simple_radio = QRadioButton("Simple")
        self.simple_radio.setChecked(True)
        self.simple_radio.clicked.connect(lambda: self.set_node_type(NodeType.SIMPLE))
        group_layout.addWidget(self.simple_radio)
        
        self.fixed_radio = QRadioButton("Fixed Support")
        self.fixed_radio.clicked.connect(lambda: self.set_node_type(NodeType.FIXED))
        group_layout.addWidget(self.fixed_radio)
        
        self.hinge_radio = QRadioButton("Hinge")
        self.hinge_radio.clicked.connect(lambda: self.set_node_type(NodeType.HINGE))
        group_layout.addWidget(self.hinge_radio)
        
        self.elastic_radio = QRadioButton("Elastic")
        self.elastic_radio.clicked.connect(lambda: self.set_node_type(NodeType.ELASTIC))
        group_layout.addWidget(self.elastic_radio)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
    
    def add_force_value_group(self, layout):
        """Add force value input group"""
        group_box = QGroupBox("Force Value")
        group_layout = QFormLayout()
        
        # Force value input
        self.force_value = QLineEdit("0.0")
        self.force_value.setPlaceholderText("Enter force value (kN)")
        self.force_value.textChanged.connect(self.update_force_value)
        group_layout.addRow("Value (kN):", self.force_value)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
    
    def add_grid_spacing_group(self, layout):
        """Add grid spacing inputs"""
        group_box = QGroupBox("Grid Spacing")
        group_layout = QFormLayout()
        
        # Horizontal spacing input
        self.h_spacing = QLineEdit("1 2 5 6")
        self.h_spacing.setPlaceholderText("Enter horizontal spacings separated by spaces")
        group_layout.addRow("Horizontal:", self.h_spacing)
        
        # Vertical spacing input
        self.v_spacing = QLineEdit("7 8 4 5")
        self.v_spacing.setPlaceholderText("Enter vertical spacings separated by spaces")
        group_layout.addRow("Vertical:", self.v_spacing)
        
        # Update button
        update_button = QPushButton("Update Grid")
        update_button.clicked.connect(self.update_grid_spacing)
        group_layout.addRow(update_button)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
    
    def set_node_type(self, node_type):
        """Set the current node type"""
        self.app_state.current_node_type = node_type
    
    def update_force_value(self):
        """Update the current force value"""
        try:
            value = float(self.force_value.text())
            self.app_state.current_force_value = value
        except ValueError:
            # Invalid input, ignore
            pass
    
    def update_grid_spacing(self):
        """Update grid spacing based on input fields"""
        # Parse horizontal spacings
        try:
            h_spacings = [float(x) for x in self.h_spacing.text().split() if x.strip()]
            if h_spacings:
                self.app_state.h_spacings = h_spacings
        except ValueError:
            # Invalid input, ignore
            pass
        
        # Parse vertical spacings
        try:
            v_spacings = [float(x) for x in self.v_spacing.text().split() if x.strip()]
            if v_spacings:
                self.app_state.v_spacings = v_spacings
        except ValueError:
            # Invalid input, ignore
            pass
        
        # Emit signal to update grid
        self.grid_updated.emit()