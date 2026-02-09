"""
Main application window orchestrating all UI components.

Coordinates:
- Window management (frameless, resize, minimize/maximize/close)
- Theme and language configuration
- Layout assembly from modular widgets
- Signal routing between components
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication
)
from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import Signal

from widgets.window_resize import ResizeHandler, toggle_maximize
import utils.helpers as helpers
from widgets.header import header
from widgets.tabs import tabs
from widgets.extra_panels.extra_panels_manager import ExtraPanel
import widgets.aside as aside
import widgets.text_editor as te
import manifests.platform_manifests as manifests
from utils.aside_manager import show_aside
import utils.aside_manager as am
import services.logger as log


class MainWindow(QMainWindow):
    """
    Primary application window container.
    
    Attributes:
        metrics_updated (Signal[dict]): Emits system metrics to subscribed panels
        resize_handler (ResizeHandler): Manages frameless window resizing
        base_path (str): Root directory of the project
        current_lang (str): Currently selected language code
        lang_data (dict): Loaded language strings
        theme_default (dict): Current color theme configuration
    """
    
    metrics_updated = Signal(dict)
    
    def __init__(self):
        """
        Initialize main window with frameless design and modular widgets.
        
        Initialization order:
        1. Window properties and platform manifests
        2. Theme and language configuration
        3. UI widget assembly
        4. Signal connections
        """
        super().__init__()
        self.resize_handler = ResizeHandler(self)
        self.base_path = helpers.get_project_root()
        
        # Platform-specific initialization
        manifests.set_platform_manifest(self.base_path)
        
        # Window icon and styling
        icon_path = os.path.join(
            self.base_path, "resources", "icons", "ico", "Yarn-256.ico"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        # Language configuration
        self.current_lang = helpers.get_json_property(
            os.path.join(helpers.get_project_root(), 'config', 'config.json'), 
            "lang"
        )
        log.info(msg=f'Selected language: "{self.current_lang}"')
        self.lang_data = helpers.get_json_property(
            os.path.join(self.base_path, "resources", "language", 
                        f'{self.current_lang}.json')
        )
        
        # Window geometry and theme
        self.setup_main_app()
        self.config_path = os.path.join(
            helpers.get_project_root(), 'config', 'config.json'
        )
        self.themes_path = os.path.join(
            helpers.get_project_root(), 'resources', 'themes'
        )
        self.theme_default = helpers.load_theme()
        
        # Build UI components
        self.create_widgets()
        
        # Restore panel states from config
        if helpers.get_json_property(
            os.path.join(helpers.get_project_root(), "config", 
                        "btn_settings_config.json"), 
            'aside_is_open'
        ):
            show_aside()
        
        # Establish signal connections
        self.setup_signals()
    
    def setup_signals(self):
        """
        Connect internal signals between window components.
        
        Routes:
            metrics_updated → ExtraPanel.metrics_updated
        """
        if hasattr(self, 'extra_panel'):
            self.metrics_updated.connect(self.extra_panel.metrics_updated)
    
    def update_metrics(self, metrics):
        """
        Forward system metrics to subscribed panels.
        
        Args:
            metrics (dict): System resource usage data from MetricsCollector
        """
        self.metrics_updated.emit(metrics)
    
    # Frameless window event handling
    def mousePressEvent(self, event):
        """Delegate mouse press events to resize handler."""
        if self.resize_handler.mouse_press(event):
            return
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Delegate mouse move events to resize handler."""
        if self.resize_handler.mouse_move(event):
            return
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Delegate mouse release events to resize handler."""
        if self.resize_handler.mouse_release(event):
            return
        super().mouseReleaseEvent(event)
    
    def setup_main_app(self):
        """
        Configure main window geometry and central widget.
        
        Sets:
            - Centered initial position
            - Minimum size constraints
            - Mouse tracking for custom resize handles
        """
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        width, height = 1200, 500
        x = (geometry.width() - width) // 2
        y = (geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)
        self.setWindowTitle("Yarn")
        self.setMinimumSize(400, 300)
        
        # Enable mouse tracking for custom resize areas
        self.setMouseTracking(True)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setMouseTracking(True)
        
        # Main vertical layout
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
    
    def create_widgets(self):
        """
        Assemble all UI widgets into the main layout.
        
        Hierarchy:
            Header (window controls)
            Tabs (document management)
            Main Content Area:
                - Aside panel (navigation/sidebar)
                - Right panel:
                    - Text editor
                    - Extra panels (logs, stats, info)
        """
        # Window header with control buttons
        self.header = header(theme=self.theme_default, parent=self)
        self.header.setMouseTracking(True)
        self.layout.addWidget(self.header)
        self.header.minimize_btn.clicked.connect(self.showMinimized)
        self.header.maximize_btn.clicked.connect(self.toggle_maximize_window)
        self.header.close_btn.clicked.connect(self.close)
        
        # Document tabs
        self.tabs = tabs(theme=self.theme_default, parent=self, lang=self.lang_data)
        self.tabs.setMouseTracking(True)
        self.layout.addWidget(self.tabs)
        
        # Main content area (aside + editor + panels)
        main_content = QHBoxLayout()
        
        # Right panel container
        self.right_panel = QWidget()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Text editor
        self.text_editor = te.textEditor(
            parent=self, 
            theme=self.theme_default
        )
        
        # Extra panels (logs, stats, info)
        self.extra_panel = ExtraPanel(
            parent=self, 
            theme=self.theme_default, 
            lang=self.lang_data
        )
        self.extra_panel.reload_requested.connect(self.extra_panel.reload_widget)
        am.set_extra_panel_signal(self.extra_panel.reload_requested)
        
        right_layout.addWidget(self.text_editor)
        right_layout.addWidget(self.extra_panel)
        
        # Aside navigation panel
        self.aside = aside.aside(
            parent=self, 
            theme=self.theme_default, 
            tabs_widget=self.tabs, 
            base_path=self.base_path, 
            lang=self.lang_data
        )
        
        # Assemble main content
        main_content.addWidget(self.aside)
        main_content.addWidget(self.right_panel)
        self.layout.addLayout(main_content)
    
    def toggle_maximize_window(self):
        """Toggle between windowed and maximized states."""
        toggle_maximize(self)
    
    def on_close(self):
        """Close the main window (connected to header close button)."""
        self.close()