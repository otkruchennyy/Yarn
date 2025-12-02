from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
# from PySide6.QtGui import QFont
# from PySide6.QtCore import Qt
import services.logger as log
import utils.helpers as helpers
import os

class LogsPanel(QWidget):
    def __init__(self, base_path, theme):
        super().__init__()
        self.base_path = base_path
        self.theme = theme
        self.logs_widgets = {}
        self.path_logs = log.get_log_path()

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.load_logs()

        self.layout.addStretch()

    def load_logs(self):
        name_property = QLabel("logs")
        self.layout.addWidget(name_property)
        self.logs_widgets["name_property"] = name_property

    def on_logs_clicked(self, path, name_btn):
        """logs click handler"""

    def reload_logs(self):
        """Reload panel logs"""
        # Delite all widgets
        for widget in self.logs_widgets.values():
            widget.deleteLater()
        self.logs_widgets.clear()
        
        # Cleaning layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_panel(self):
        self.show()

    def hide_panel(self):
        self.hide()

    def toggle_panel(self):
        """Toggle panel visibility"""
        self.setVisible(not self.isVisible())
    
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
        self.accent_gray = self.theme.get('accent_gray')
        self.text_muted = self.theme.get('text_muted')

        # Refresh UI
        self.update()