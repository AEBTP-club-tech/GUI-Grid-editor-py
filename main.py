import sys
from PyQt6.QtWidgets import QApplication
from src.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())