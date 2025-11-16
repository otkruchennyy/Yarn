import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QPushButton, QTextEdit, QListWidget, QApplication)
from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import QRect

from widgets.window_resize import ResizeHandler
import utils.helpers as helpers
from widgets.header import CustomHeader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize_handler = ResizeHandler(self)
        self.base_path = helpers.get_project_root()
        self.setup_main_app()

        self.config_path = os.path.join(self.base_path, 'config', 'config.json')
        self.themes_path = os.path.join(self.base_path, 'resources', 'themes')
        self.fonts_path = os.path.join(self.base_path, 'resources', 'fonts')

        self.theme_default = self.load_theme()

        self.theme_default = self.theme_default or {}
        if not self.theme_default:
            self.theme_default = {
                'isDark': True, 
                'bg_dark': '#111111', 
                'bg_card': '#121212', 
                'accent_primary': '#202020', 
                'accent_secondary': '#252525', 
                'accent_light': '#7a7a7a', 
                'text_main': '#e0e0e0', 
                'text_muted': '#a0a0a0'
            }
        self.font_default = self.load_font()

        self.font_default = self.font_default or {}
        if not self.font_default:
            self.font_default = {
                'isDark': True, 
                'bg_dark': '#111111', 
                'bg_card': '#121212', 
                'accent_primary': '#202020', 
                'accent_secondary': '#252525', 
                'accent_light': '#7a7a7a', 
                'text_main': '#e0e0e0', 
                'text_muted': '#a0a0a0'
            }
            
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.create_widgets()

        self.main_font_style = self.font_default["main"]
        self.monospace_font_style = self.font_default["monospace"]
        self.is_color_suitable = (self.theme_default["isDark"] == self.main_font_style["fontIsDark"])
        if self.is_color_suitable:
            dialog = helpers.colors_is_suitable(self.theme_default, self.main_font_style, self.base_path, parent=self)
            dialog.exec()

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

    def load_theme(self):
        theme_name = helpers.get_json_property(self.config_path, "theme") or "default"
        theme_file = os.path.join(self.themes_path, f"{theme_name}.json")
        return helpers.get_json_property(theme_file) or self.get_fallback_theme()

    def load_font(self):
        font_name = helpers.get_json_property(self.config_path, "fonts") or "default"  
        font_file = os.path.join(self.fonts_path, f"{font_name}.json")
        return helpers.get_json_property(font_file) or self.get_fallback_font()

    def get_fallback_theme(self):
        return {
            "isDark": True,
            "bg_dark": "#111111",
            "bg_card": "#121212", 
            "accent_primary": "#202020",
            "accent_secondary": "#252525",
            "accent_light": "#7a7a7a",
            "text_main": "#e0e0e0",
            "text_muted": "#a0a0a0"
        }

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
        width, height = 400, 300
        x = (geometry.width() - width) // 2
        y = (geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)
        self.setWindowTitle("Yarn")
        self.setMinimumSize(400, 300)
        
        icon_path = os.path.join(self.base_path, "resources", "icons", "ico", "Yarn-256.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setMouseTracking(True)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setMouseTracking(True)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    
    def create_widgets(self):
        self.header = CustomHeader(theme=self.theme_default, parent=self)
        self.header.setMouseTracking(True)
        self.layout.addWidget(self.header)
        self.header.minimize_btn.clicked.connect(self.showMinimized)
        self.header.maximize_btn.clicked.connect(self.toggle_maximize)
        self.header.close_btn.clicked.connect(self.close)

        main_content = QHBoxLayout()
    
        self.block1 = QWidget()
        self.block2 = QWidget()
        self.block3 = QWidget()

        self.block1.setMouseTracking(True)
        self.block2.setMouseTracking(True)
        self.block3.setMouseTracking(True)

        self.block1_layout = QVBoxLayout(self.block1)
        self.block2_layout = QVBoxLayout(self.block2)
        self.block3_layout = QVBoxLayout(self.block3)

        self.block1_layout.addWidget(QLabel("Блок 1"))
        self.block1_layout.addWidget(QPushButton("Кнопка 1"))

        self.block2_layout.addWidget(QLabel("Блок 2"))
        self.block2_layout.addWidget(QTextEdit())

        self.block3_layout.addWidget(QLabel("Блок 3"))
        self.block3_layout.addWidget(QListWidget())

        main_content.addWidget(self.block1)
        main_content.addWidget(self.block2)
        main_content.addWidget(self.block3)
        
        self.layout.addLayout(main_content)
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()  
    
    def on_close(self):
        self.close()