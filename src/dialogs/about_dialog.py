from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Set up dialog properties
        self.setWindowTitle("About")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Add title
        title = QLabel("2D Grid Editor")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Add version
        version = QLabel("Version 1.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        # Add description
        description = QTextEdit()
        description.setReadOnly(True)
        description.setHtml("""
        <p style="text-align: center;">A powerful tool for creating and analyzing 2D structures.</p>
        <p style="text-align: center;">Built with PyQt6.</p>
        <br>
        <p><b>Features:</b></p>
        <ul>
            <li>Interactive grid drawing</li>
            <li>Multiple node types</li>
            <li>Force application</li>
            <li>Data export and analysis</li>
            <li>Undo/redo functionality</li>
        </ul>
        """)
        layout.addWidget(description)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)