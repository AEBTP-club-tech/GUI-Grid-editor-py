from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QFormLayout, QColorDialog, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class ColorPreview(QFrame):
    def __init__(self, color="#f0f0f0"):
        super().__init__()
        self.setFixedSize(50, 50)
        self.setColor(color)
    
    def setColor(self, color):
        self.color = color
        self.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

class GridSettingsDialog(QDialog):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        
        # Set up dialog properties
        self.setWindowTitle("Grid Settings")
        self.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Spacing group
        self.create_spacing_group(layout)
        
        # Color group
        self.create_color_group(layout)
        
        # Button group
        button_layout = QHBoxLayout()
        
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_settings)
        button_layout.addWidget(apply_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def create_spacing_group(self, layout):
        """Create grid spacing input group"""
        group_box = QGroupBox("Grid Spacing")
        group_layout = QFormLayout()
        
        # Horizontal spacing input
        self.h_spacing = QLineEdit()
        self.h_spacing.setText(" ".join(map(str, self.app_state.h_spacings)))
        self.h_spacing.setPlaceholderText("Enter horizontal spacings separated by spaces")
        group_layout.addRow("Horizontal:", self.h_spacing)
        
        # Vertical spacing input
        self.v_spacing = QLineEdit()
        self.v_spacing.setText(" ".join(map(str, self.app_state.v_spacings)))
        self.v_spacing.setPlaceholderText("Enter vertical spacings separated by spaces")
        group_layout.addRow("Vertical:", self.v_spacing)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
    
    def create_color_group(self, layout):
        """Create grid color settings group"""
        group_box = QGroupBox("Grid Colors")
        group_layout = QVBoxLayout()
        
        # Background color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Background Color:"))
        
        self.color_preview = ColorPreview(self.app_state.grid_bg_color)
        color_layout.addWidget(self.color_preview)
        
        color_button = QPushButton("Choose Color")
        color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(color_button)
        
        group_layout.addLayout(color_layout)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
    
    def choose_color(self):
        """Open color dialog to choose background color"""
        color = QColorDialog.getColor(QColor(self.app_state.grid_bg_color), self, "Choose Grid Background Color")
        
        if color.isValid():
            self.color_preview.setColor(color.name())
    
    def apply_settings(self):
        """Apply settings and close dialog"""
        # Parse horizontal spacings
        try:
            h_spacings = [float(x) for x in self.h_spacing.text().split() if x.strip()]
            if h_spacings:
                self.app_state.h_spacings = h_spacings
        except ValueError:
            pass
        
        # Parse vertical spacings
        try:
            v_spacings = [float(x) for x in self.v_spacing.text().split() if x.strip()]
            if v_spacings:
                self.app_state.v_spacings = v_spacings
        except ValueError:
            pass
        
        # Set background color
        self.app_state.grid_bg_color = self.color_preview.color
        
        self.accept()