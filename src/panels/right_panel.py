from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSlider, QGroupBox, 
    QRadioButton, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

class RightPanel(QScrollArea):
    # Signal emitted when scale is changed
    scale_changed = pyqtSignal(str, float)
    
    def __init__(self, app_state, grid_view):
        super().__init__()
        self.app_state = app_state
        self.grid_view = grid_view
        
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
        title = QLabel("Properties")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Add scale controls
        self.add_scale_controls(layout)
        
        # Add plane selection
        self.add_plane_selection(layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def add_scale_controls(self, layout):
        """Add scale control sliders"""
        group_box = QGroupBox("Scale")
        group_layout = QVBoxLayout()
        
        # X scale
        x_label = QLabel("X Scale")
        group_layout.addWidget(x_label)
        
        self.x_value_label = QLabel("1.0x")
        group_layout.addWidget(self.x_value_label)
        
        self.x_scale = QSlider(Qt.Orientation.Horizontal)
        self.x_scale.setRange(10, 200)  # 0.1x to 2.0x
        self.x_scale.setValue(100)      # 1.0x default
        self.x_scale.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.x_scale.setTickInterval(10)
        self.x_scale.valueChanged.connect(self.on_x_scale_changed)
        group_layout.addWidget(self.x_scale)
        
        # Y scale
        y_label = QLabel("Y Scale")
        group_layout.addWidget(y_label)
        
        self.y_value_label = QLabel("1.0x")
        group_layout.addWidget(self.y_value_label)
        
        self.y_scale = QSlider(Qt.Orientation.Horizontal)
        self.y_scale.setRange(10, 200)  # 0.1x to 2.0x
        self.y_scale.setValue(100)      # 1.0x default
        self.y_scale.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.y_scale.setTickInterval(10)
        self.y_scale.valueChanged.connect(self.on_y_scale_changed)
        group_layout.addWidget(self.y_scale)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
    
    def add_plane_selection(self, layout):
        """Add plane selection radio buttons"""
        group_box = QGroupBox("Active Plane")
        group_layout = QVBoxLayout()
        
        # Create radio buttons for planes
        self.xy_radio = QRadioButton("XY Plane")
        self.xy_radio.setChecked(True)
        self.xy_radio.clicked.connect(lambda: self.change_plane("xy"))
        group_layout.addWidget(self.xy_radio)
        
        self.yz_radio = QRadioButton("YZ Plane")
        self.yz_radio.clicked.connect(lambda: self.change_plane("yz"))
        group_layout.addWidget(self.yz_radio)
        
        self.zx_radio = QRadioButton("ZX Plane")
        self.zx_radio.clicked.connect(lambda: self.change_plane("zx"))
        group_layout.addWidget(self.zx_radio)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
    
    def on_x_scale_changed(self, value):
        """Handle X scale slider value change"""
        scale = value / 100.0
        self.x_value_label.setText(f"{scale:.1f}x")
        self.scale_changed.emit('x', scale)
    
    def on_y_scale_changed(self, value):
        """Handle Y scale slider value change"""
        scale = value / 100.0
        self.y_value_label.setText(f"{scale:.1f}x")
        self.scale_changed.emit('y', scale)
    
    def change_plane(self, plane):
        """Change the active plane"""
        self.app_state.set_current_plane(plane)
        
        # Update radio buttons to match app state
        self.xy_radio.setChecked(plane == "xy")
        self.yz_radio.setChecked(plane == "yz")
        self.zx_radio.setChecked(plane == "zx")