from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import os
import utils.helpers as helpers

class ToolsPanel(QWidget):
    def __init__(self, base_path, theme):
        super().__init__()
        self.theme = theme
        self.base_path = base_path
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        font = QFont("Segoe UI", 10) # TODO: current font

        email_btn = QPushButton("Search emails")
        email_btn.setFixedSize(246, 30)
        email_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        email_btn.setFont(font)
        email_btn.setProperty("class", "tool")
        email_btn.setToolTip("Search for email addresses in the document")
        email_btn.setStyleSheet("margin: 2px; padding: 0px;")
        # btn.clicked.connect()
        self.layout.addWidget(email_btn)

        url_btn = QPushButton("Extract URLs")
        url_btn.setFixedSize(246, 30)
        url_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        url_btn.setFont(font)
        url_btn.setProperty("class", "tool")
        url_btn.setToolTip("Find and extract all web links from the document")
        url_btn.setStyleSheet("margin: 2px; padding: 0px;")
        # btn.clicked.connect()
        self.layout.addWidget(url_btn)

        phone_btn = QPushButton("Find Phone Numbers")
        phone_btn.setFixedSize(246, 30)
        phone_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        phone_btn.setFont(font)
        phone_btn.setProperty("class", "tool")
        phone_btn.setToolTip("Search for phone numbers in various formats")
        phone_btn.setStyleSheet("margin: 2px; padding: 0px;")
        # btn.clicked.connect()
        self.layout.addWidget(phone_btn)

        
        self.layout.addStretch()

    def on_tools_clicked(self, path, name_btn):
        """Tools click handler"""

        # Reload panel
        self.reload_tools()

    def reload_tools(self):
        """Reload panel tools"""
        # Delite all
        # TODO: delete widgets
        # Cleaning layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Reload
        # self.load_tools()

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

        self.setStyleSheet(f"""
            QPushButton[class="tool"]{{
                background-color: {self.bg_color};
                color: {self.text_main};
                padding: 5px;
                border-radius: 3px;
            }}
            
            QPushButton[class="tool"]:hover {{
                background-color: {self.btn_hover_bg_color};
                color: {self.text_main};
            }}
            
            QPushButton[class="tool"]:pressed {{
                background-color: {self.btn_hover_bg_color};
                color: {self.text_main};
            }}
            QPushButton[class="active_tool"] {{
                background-color: {self.bg_card};
                border: 1px solid {self.accent_light};
                color: {self.text_main};
            }}
            QToolTip {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
            }}
            """)