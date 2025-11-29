from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import os
import utils.helpers as helpers

class ToolsPanel(QWidget):
    def __init__(self, base_path, theme):
        super().__init__()
        self.theme = theme
        self.base_path = base_path
        self.tools_widgets = {}
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.font = QFont("Segoe UI", 10) # TODO: current font
        
        name_property = QLabel("tools")
        self.layout.addWidget(name_property)
        self.tools_widgets["name_property"] = name_property

        self.add_btn("Search emails", "Search for email addresses in the document")
        self.add_btn("Extract URLs", "Find and extract all web links from the document")
        self.add_btn("Find Phone Numbers", "Search for phone numbers in various formats")
        
        self.layout.addStretch()

    def add_btn(self, name, tooltip_text=None, connect=None):
        try:
            btn = QPushButton(name)
            btn.setFixedSize(246, 30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(self.font)
            btn.setProperty("class", "tool")
            if isinstance(tooltip_text, str) and tooltip_text.strip():
                btn.setToolTip(tooltip_text)
            btn.setStyleSheet("margin: 2px; padding: 0px;")
            # btn.clicked.connect(connect)
            self.layout.addWidget(btn)
            self.tools_widgets[name] = btn
        
        except TypeError: print("TypeError: invalid name")
        except: print(f'no function named {connect}') # TODO: Implement an error counter in the widget

    def on_tools_clicked(self, path, name_btn):
        """Tools click handler"""

        # Reload panel
        self.reload_tools()

    def reload_tools(self):
        for widget in self.tools_widgets.values():
            widget.deleteLater()
        self.tools_widgets.clear()
        
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