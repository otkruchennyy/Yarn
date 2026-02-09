import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication)
from PySide6.QtGui import QIcon, Qt
# from PySide6.QtCore import

from widgets.window_resize import ResizeHandler, toggle_maximize
import utils.helpers as helpers
from widgets.header import header
import widgets.window_resize
from widgets.tabs import tabs
from widgets.extra_panels.extra_panels_manager import ExtraPanel
import widgets.aside as aside
import widgets.text_editor as te
import manifests.platform_manifests as manifests
from utils.aside_manager import show_aside
import utils.aside_manager as am
import services.logger as log

class MainWindow(QMainWindow):
    """Launches all UI elements of the page that are separated into individual scripts"""
    def __init__(self):
        super().__init__()
        self.resize_handler = ResizeHandler(self)
        self.base_path = helpers.get_project_root()

        manifests.set_platform_manifest(self.base_path)

        icon_path = os.path.join(self.base_path, "resources", "icons", "ico", "Yarn-256.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.current_lang = helpers.get_json_property(os.path.join(helpers.get_project_root(), 'config', 'config.json'), "lang")
        log.info(msg=f'Selected language: "{self.current_lang}"')
        self.lang_data = helpers.get_json_property(os.path.join(self.base_path, "resources", "language", f'{self.current_lang}.json'))

        self.setup_main_app()
        self.config_path = os.path.join(helpers.get_project_root(), 'config', 'config.json')
        self.themes_path =os.path.join(helpers.get_project_root(), 'resources', 'themes')

        self.theme_default = helpers.load_theme()

        self.create_widgets()
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

    def setup_main_app(self):
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        width, height = 1200, 500
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

        self.tabs = tabs(theme=self.theme_default, parent=self, lang=self.lang_data)
        self.tabs.setMouseTracking(True)
        self.layout.addWidget(self.tabs)

        main_content = QHBoxLayout()

        self.right_panel = QWidget()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        self.text_editor = te.textEditor(parent=self, theme=self.theme_default)
        self.extra_panel = ExtraPanel(parent=self, theme=self.theme_default, lang=self.lang_data)
        self.extra_panel.reload_requested.connect(self.extra_panel.reload_widget)
        am.set_extra_panel_signal(self.extra_panel.reload_requested)
        right_layout.addWidget(self.text_editor)
        right_layout.addWidget(self.extra_panel)

        self.aside = aside.aside(parent=self, theme=self.theme_default, tabs_widget=self.tabs, base_path=self.base_path, lang=self.lang_data)
        
        main_content.addWidget(self.aside)
        main_content.addWidget(self.right_panel)
        
        self.layout.addLayout(main_content)
    
    def toggle_maximize_window(self):
        toggle_maximize(self)
    
    def on_close(self):
        self.close()