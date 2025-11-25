import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication)
from PySide6.QtGui import QIcon, Qt
# from PySide6.QtCore import

from widgets.window_resize import ResizeHandler, toggle_maximize
import utils.helpers as helpers
from widgets.header import header
import widgets.window_resize
from widgets.tabs import tabs
import widgets.aside as aside
import widgets.text_editor as te
import manifests.platform_manifests as manifests
from utils.aside_manager import show_aside

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize_handler = ResizeHandler(self)
        self.base_path = helpers.get_project_root()

        manifests.set_platform_manifest(self.base_path)

        icon_path = os.path.join(self.base_path, "resources", "icons", "ico", "Yarn-256.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.setup_main_app()
        self.config_path = os.path.join(helpers.get_project_root(), 'config', 'config.json')
        self.themes_path =os.path.join(helpers.get_project_root(), 'resources', 'themes')
        self.fonts_path = os.path.join(self.base_path, 'resources', 'fonts')

        self.theme_default = helpers.load_theme()
        self.font_default = self.load_font() or self.get_fallback_font()

        self.create_widgets()

        self.main_font_style = self.font_default["main"]
        self.monospace_font_style = self.font_default["monospace"]
        self.is_color_suitable = (self.theme_default["isDark"] == self.main_font_style["fontIsDark"])
        if self.is_color_suitable:
            dialog = helpers.colors_is_suitable(self.theme_default, self.main_font_style, self.base_path, parent=self)
            dialog.exec()
        if helpers.get_json_property(os.path.join(helpers.get_project_root(), "config", "btn_settings_config.json"), 'aside_is_open'):
            show_aside()

    def mousePressEvent(self, event):
        if self.resize_handler.mouse_press(event):
            return
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.resize_handler.mouse_move(event):
            return  
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        if self.resize_handler.mouse_release(event):
            return
        super().mouseReleaseEvent(event)

    def load_font(self):
        font_name = helpers.get_json_property(self.config_path, "fonts") or "default"  
        font_file = os.path.join(self.fonts_path, f"{font_name}.json")
        return helpers.get_json_property(font_file) or self.get_fallback_font()

    def get_fallback_font(self):
        return {
            "main": {
                "family": "Segoe UI",
                "size": 12,
                "weight": "normal",
                "style": "normal", 
                "line_height": 1.4,
                "letter_spacing": 0,
                "color": "#e0e0e0",
                "fontIsDark": False
            },
            "monospace": {
                "family": "Consolas", 
                "size": 12,
                "weight": "normal",
                "style": "normal",
                "line_height": 1.2,
                "letter_spacing": 0,
                "color": "#e0e0e0"
            }
        }

    def setup_main_app(self):
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        width, height = 900, 500
        x = (geometry.width() - width) // 2
        y = (geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)
        self.setWindowTitle("Yarn")
        self.setMinimumSize(400, 300)
        
        self.setMouseTracking(True)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setMouseTracking(True)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    
    def create_widgets(self):
        self.header = header(theme=self.theme_default, parent=self)
        self.header.setMouseTracking(True)
        self.layout.addWidget(self.header)
        self.header.minimize_btn.clicked.connect(self.showMinimized)
        self.header.maximize_btn.clicked.connect(self.toggle_maximize_window)
        self.header.close_btn.clicked.connect(self.close)

        self.tabs = tabs(theme=self.theme_default, parent=self)
        self.tabs.setMouseTracking(True)
        self.layout.addWidget(self.tabs)

        main_content = QHBoxLayout()
    
        self.aside = aside.aside(parent=self, theme=self.theme_default, tabs_widget=self.tabs)
        self.text_editor = te.textEditor(parent=self, theme=self.theme_default)
        
        main_content.addWidget(self.aside)
        main_content.addWidget(self.text_editor)
        
        self.layout.addLayout(main_content)
    
    def toggle_maximize_window(self):
        toggle_maximize(self)
    
    def on_close(self):
        self.close()