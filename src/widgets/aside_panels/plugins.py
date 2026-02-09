from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import os
import utils.helpers as helpers

class PluginsPanel(QWidget):
    def __init__(self, base_path, theme, lang=None):
        super().__init__()
        self.base_path = base_path
        self.theme = theme
        self.lang = lang
        self.plugins_widgets = {}
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.font = QFont("Segoe UI", 10) # TODO: current font 
                # font-family: Unbouded;

        self.load_plugins()

        self.layout.addStretch()

    def load_plugins(self):
        name_property = QLabel(self.lang["Plugins"])
        self.layout.addWidget(name_property)
        self.plugins_widgets["name_property"] = name_property

    def on_plugins_clicked(self, path, name_btn):
        """Plugins click handler"""

        self.reload_plugins()

    def reload_plugins(self):
        """Reload panel plugins"""
        # Delite all widgets
        for widget in self.plugins_widgets.values():
            widget.deleteLater()
        self.plugins_widgets.clear()
        
        # Cleaning layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_panel(self):
        self.show()

    def hide_panel(self):
        self.hide()
    
    def apply_theme(self):
        """
        Applies color theme to UI elements using CSS styling.
        Updates main widget and button styles with theme colors.
        """
        # Extract theme colors
        self.bg_card = self.theme.get('bg_card')
        self.bg_card = self.theme.get('bg_card')
        self.bg_color = self.theme.get('bg_color')
        self.accent_color = self.theme.get('accent_color')
        self.accent_primary = self.theme.get('accent_primary')
        self.text_main = self.theme.get('text_main')
        self.btn_bg_color = self.theme.get('btn_bg_color')
        self.accent_light = self.theme.get('accent_light')
        self.btn_hover_bg_color = self.theme.get('btn_hover_bg_color')
        self.text_muted = self.theme.get('text_muted')

        # Refresh UI
        self.update()