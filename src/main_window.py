from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSplitter,
    QToolBar, QStatusBar, QMenuBar, QMenu, QFileDialog, QMessageBox, QColorDialog, QStyle
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QColor

from src.grid_view import GridView
from src.panels.left_panel import LeftPanel
from src.panels.right_panel import RightPanel
from src.dialogs.grid_settings_dialog import GridSettingsDialog
from src.dialogs.about_dialog import AboutDialog
from src.models.app_state import AppState
from src.utils.file_utils import FileManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set up the main window
        self.setWindowTitle("2D Grid Editor")
        self.setMinimumSize(1400, 900)
        
        # Create application state
        self.app_state = AppState()
        
        # Create file manager
        self.file_manager = FileManager(self.app_state)
        
        # Set up the UI
        self.setup_ui()
        
        # Connect signals and slots
        self.connect_signals()
        
    def setup_ui(self):
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Create splitter for panels and grid view
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Create left panel
        self.left_panel = LeftPanel(self.app_state)
        self.splitter.addWidget(self.left_panel)
        
        # Create grid view (main drawing area)
        self.grid_view = GridView(self.app_state)
        self.splitter.addWidget(self.grid_view)
        
        # Create right panel
        self.right_panel = RightPanel(self.app_state, self.grid_view)
        self.splitter.addWidget(self.right_panel)
        
        # Set splitter sizes (left panel, grid view, right panel)
        self.splitter.setSizes([250, 800, 250])
        
        # Create menu bar (after grid_view is initialized)
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        style = self.style()
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        new_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_FileIcon), "New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.clear_all)
        file_menu.addAction(new_action)
        
        open_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton), "Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), "Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export...", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton), "Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        undo_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowBack), "Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowForward), "Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        clear_action = QAction("Clear All", self)
        clear_action.triggered.connect(self.clear_all)
        edit_menu.addAction(clear_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(lambda: self.grid_view.zoom(1.2))
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(lambda: self.grid_view.zoom(0.8))
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.triggered.connect(self.grid_view.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        view_menu.addSeparator()
        
        toggle_grid_action = QAction("Show/Hide Grid", self)
        toggle_grid_action.setShortcut("G")
        toggle_grid_action.triggered.connect(self.grid_view.toggle_grid)
        view_menu.addAction(toggle_grid_action)
        
        grid_settings_action = QAction("Grid Settings...", self)
        grid_settings_action.triggered.connect(self.show_grid_settings)
        view_menu.addAction(grid_settings_action)
        
        # Background color action
        bg_color_action = QAction("Background Color...", self)
        bg_color_action.triggered.connect(self.change_background_color)
        view_menu.addAction(bg_color_action)
        
        view_menu.addSeparator()
        
        # Fullscreen action
        fullscreen_action = QAction("Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence.StandardKey.FullScreen)
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Zen mode action
        zen_mode_action = QAction("Zen Mode", self)
        zen_mode_action.setShortcut("Z")
        zen_mode_action.setCheckable(True)
        zen_mode_action.triggered.connect(self.toggle_zen_mode)
        view_menu.addAction(zen_mode_action)
        
        # Store view actions for toggling
        self.view_actions = {
            "fullscreen": fullscreen_action,
            "zen_mode": zen_mode_action
        }
        
        view_menu.addSeparator()
        
        # Plane submenu
        plane_menu = view_menu.addMenu("Plane")
        
        xy_plane_action = QAction("XY Plane", self)
        xy_plane_action.setCheckable(True)
        xy_plane_action.setChecked(True)
        xy_plane_action.triggered.connect(lambda: self.change_plane("xy"))
        plane_menu.addAction(xy_plane_action)
        
        yz_plane_action = QAction("YZ Plane", self)
        yz_plane_action.setCheckable(True)
        yz_plane_action.triggered.connect(lambda: self.change_plane("yz"))
        plane_menu.addAction(yz_plane_action)
        
        zx_plane_action = QAction("ZX Plane", self)
        zx_plane_action.setCheckable(True)
        zx_plane_action.triggered.connect(lambda: self.change_plane("zx"))
        plane_menu.addAction(zx_plane_action)
        
        self.plane_actions = [xy_plane_action, yz_plane_action, zx_plane_action]
        
        # Tools menu
        tools_menu = menu_bar.addMenu("Tools")
        
        eraser_action = QAction("Eraser", self)
        eraser_action.setCheckable(True)
        eraser_action.setShortcut("E")
        eraser_action.triggered.connect(self.toggle_eraser)
        tools_menu.addAction(eraser_action)
        
        selection_action = QAction("Selection", self)
        selection_action.setCheckable(True)
        selection_action.setShortcut("S")
        selection_action.triggered.connect(self.toggle_selection)
        tools_menu.addAction(selection_action)
        
        tools_menu.addSeparator()
        
        force_action = QAction("Add Force", self)
        force_action.setShortcut("F")
        force_action.triggered.connect(self.add_force)
        tools_menu.addAction(force_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Store tool actions for toggling
        self.tool_actions = {
            "eraser": eraser_action,
            "selection": selection_action
        }
        
    def create_toolbar(self):
        # Create main toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        style = self.style()
        # File section
        new_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_FileIcon), "New", self)
        new_action.triggered.connect(self.clear_all)
        self.toolbar.addAction(new_action)
        
        open_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton), "Open", self)
        open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_action)
        
        save_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), "Save", self)
        save_action.triggered.connect(self.save_file)
        self.toolbar.addAction(save_action)
        
        self.toolbar.addSeparator()
        
        # Edit section
        undo_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowBack), "Undo", self)
        undo_action.triggered.connect(self.undo)
        self.toolbar.addAction(undo_action)
        
        redo_action = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowForward), "Redo", self)
        redo_action.triggered.connect(self.redo)
        self.toolbar.addAction(redo_action)
        
        self.toolbar.addSeparator()
        
        # View section
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(lambda: self.grid_view.zoom(1.2))
        self.toolbar.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(lambda: self.grid_view.zoom(0.8))
        self.toolbar.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.triggered.connect(self.grid_view.reset_zoom)
        self.toolbar.addAction(reset_zoom_action)
        
        self.toolbar.addSeparator()
        
        # Tools section
        eraser_action = QAction("Eraser", self)
        eraser_action.setCheckable(True)
        eraser_action.triggered.connect(self.toggle_eraser)
        self.toolbar.addAction(eraser_action)
        
        selection_action = QAction("Selection", self)
        selection_action.setCheckable(True)
        selection_action.triggered.connect(self.toggle_selection)
        self.toolbar.addAction(selection_action)
        
        # Update tool actions
        self.tool_actions["eraser_tb"] = eraser_action
        self.tool_actions["selection_tb"] = selection_action
    
    def connect_signals(self):
        # Connect application state signals to UI updates
        self.app_state.node_added.connect(self.grid_view.update)
        self.app_state.line_added.connect(self.grid_view.update)
        self.app_state.force_added.connect(self.grid_view.update)
        self.app_state.element_deleted.connect(self.grid_view.update)
        self.app_state.state_changed.connect(self.grid_view.update)
        self.app_state.plane_changed.connect(self.on_plane_changed)
        
        # Connect left panel signals
        self.left_panel.grid_updated.connect(self.grid_view.update_grid)
        
        # Connect right panel signals
        self.right_panel.scale_changed.connect(self.grid_view.update_scale)
    
    def clear_all(self):
        """Clear all elements from the grid"""
        reply = QMessageBox.question(
            self, "Clear All", 
            "Are you sure you want to clear all elements?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.app_state.clear_all()
            self.grid_view.update()
            self.status_bar.showMessage("All elements cleared")
    
    def open_file(self):
        """Open a grid structure file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            success = self.file_manager.load_file(file_path)
            if success:
                self.grid_view.update()
                self.status_bar.showMessage(f"File loaded: {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to load file")
    
    def save_file(self):
        """Save the grid structure to a file"""
        if self.app_state.current_file_path:
            success = self.file_manager.save_file(self.app_state.current_file_path)
            if success:
                self.status_bar.showMessage(f"File saved: {self.app_state.current_file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to save file")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save the grid structure to a new file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            success = self.file_manager.save_file(file_path)
            if success:
                self.app_state.current_file_path = file_path
                self.status_bar.showMessage(f"File saved: {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to save file")
    
    def export_data(self):
        """Export grid structure data"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            success = self.file_manager.export_data(file_path)
            if success:
                self.status_bar.showMessage(f"Data exported: {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to export data")
    
    def undo(self):
        """Undo the last action"""
        if self.app_state.undo():
            self.grid_view.update()
            self.status_bar.showMessage("Undo")
    
    def redo(self):
        """Redo the last undone action"""
        if self.app_state.redo():
            self.grid_view.update()
            self.status_bar.showMessage("Redo")
    
    def change_plane(self, plane):
        """Change the active plane"""
        self.app_state.set_current_plane(plane)
        
        # Update plane actions
        for i, plane_type in enumerate(["xy", "yz", "zx"]):
            self.plane_actions[i].setChecked(plane_type == plane)
        
        self.status_bar.showMessage(f"Changed to {plane.upper()} plane")
    
    def on_plane_changed(self, plane):
        """Handle plane changed signal from app state"""
        # Update plane actions
        for i, plane_type in enumerate(["xy", "yz", "zx"]):
            self.plane_actions[i].setChecked(plane_type == plane)
    
    def toggle_eraser(self, checked=None):
        """Toggle eraser mode"""
        if checked is None:
            checked = not self.app_state.eraser_mode
        
        # Update app state
        self.app_state.eraser_mode = checked
        self.app_state.selection_mode = False
        
        # Update all eraser actions
        self.tool_actions["eraser"].setChecked(checked)
        self.tool_actions["eraser_tb"].setChecked(checked)
        
        # Uncheck selection actions
        self.tool_actions["selection"].setChecked(False)
        self.tool_actions["selection_tb"].setChecked(False)
        
        self.status_bar.showMessage("Eraser mode: " + ("On" if checked else "Off"))
    
    def toggle_selection(self, checked=None):
        """Toggle selection mode"""
        if checked is None:
            checked = not self.app_state.selection_mode
        
        # Update app state
        self.app_state.selection_mode = checked
        self.app_state.eraser_mode = False
        
        # Update all selection actions
        self.tool_actions["selection"].setChecked(checked)
        self.tool_actions["selection_tb"].setChecked(checked)
        
        # Uncheck eraser actions
        self.tool_actions["eraser"].setChecked(False)
        self.tool_actions["eraser_tb"].setChecked(False)
        
        self.status_bar.showMessage("Selection mode: " + ("On" if checked else "Off"))
    
    def add_force(self):
        """Enter force placement mode"""
        # This will be implemented later with a force dialog
        self.grid_view.start_force_placement()
        self.status_bar.showMessage("Click on a node or line to add a force")
    
    def show_grid_settings(self):
        """Show grid settings dialog"""
        dialog = GridSettingsDialog(self, self.app_state)
        if dialog.exec():
            self.grid_view.update_grid()
            self.status_bar.showMessage("Grid settings updated")
    
    def show_about(self):
        """Show about dialog"""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def toggle_fullscreen(self, checked=None):
        """Toggle fullscreen mode"""
        if checked is None:
            checked = not self.isFullScreen()
        
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()
        
        self.view_actions["fullscreen"].setChecked(checked)
        self.status_bar.showMessage("Fullscreen mode: " + ("On" if checked else "Off"))
    
    def toggle_zen_mode(self, checked=None):
        """Toggle zen mode (hide side panels)"""
        if checked is None:
            checked = not self.app_state.zen_mode
        
        # Update app state
        self.app_state.zen_mode = checked
        
        # Show/hide panels
        self.left_panel.setVisible(not checked)
        self.right_panel.setVisible(not checked)
        
        # Adjust splitter sizes
        if checked:
            # Store current sizes for restoration
            self.previous_sizes = self.splitter.sizes()
            # Give all space to grid view
            self.splitter.setSizes([0, self.width(), 0])
        else:
            # Restore previous sizes or use defaults
            if hasattr(self, 'previous_sizes'):
                self.splitter.setSizes(self.previous_sizes)
            else:
                self.splitter.setSizes([250, 800, 250])
        
        self.view_actions["zen_mode"].setChecked(checked)
        self.status_bar.showMessage("Zen mode: " + ("On" if checked else "Off"))
    
    def change_background_color(self):
        """Show color picker dialog to change grid background color"""
        # Get current color
        current_color = QColor(self.app_state.grid_bg_color)
        
        # Show color picker dialog
        color = QColorDialog.getColor(current_color, self, "Choose Background Color")
        
        if color.isValid():
            # Update app state
            self.app_state.grid_bg_color = color.name()
            # Update grid view
            self.grid_view.update_grid()
            self.status_bar.showMessage(f"Background color changed to {color.name()}")
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        # Handle Escape key to exit fullscreen or zen mode
        if event.key() == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.toggle_fullscreen(False)
            elif self.app_state.zen_mode:
                self.toggle_zen_mode(False)
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)