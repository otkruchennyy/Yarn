import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
import utils.helpers as helpers

class tabs(QWidget):
    def __init__(self, theme=None, parent=None):
        super().__init__(parent)
        self.bg_color = None
        self.theme = theme
        self.path_tabs = os.path.join(helpers.get_project_root(), "config", "tabs_config.json")
        self.property_tabs = helpers.get_json_property(self.path_tabs)
        self.count_tabs = len(self.property_tabs)
        self.setup_ui()
        self.apply_theme()
        # print(self.path_tabs)
        # print(self.property_tabs)
        # print(self.count_tabs)
    
    def setup_ui(self):
        self.setObjectName("tabs")
        layout = QHBoxLayout(self)
        self.setFixedHeight(30)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.installEventFilter(self)
        self.tabs = {}
        for i in range(self.count_tabs):
            name = list(self.property_tabs.keys())[i]
            self.btn = QPushButton(f'{name}')
            self.btn.setFixedSize(200, 25)
            self.btn.setCursor(Qt.PointingHandCursor)
            self.btn.setProperty("class", "tab")
            self.tabs[name] = self.btn
            layout.addWidget(self.tabs[name])
    
    def apply_theme(self):
        self.bg_color = self.theme.get('bg_card', '#121212')
        self.text_color = self.theme.get('text_main', '#e0e0e0')
        self.accent_color = self.theme.get('accent_primary', '#202020')

        self.update()

        #
        self.setStyleSheet(f"""
            QPushButton[class="tab"] {{
                color: {self.text_color};
                border: none;
                border-radius: 3px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton[class="tab"]:hover {{
                background-color: #ff555555;
            }}
        """)
        
    
    def paintEvent(self, event):
        if self.bg_color and self.accent_color:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(self.bg_color))

            painter.setPen(QColor(self.accent_color))
            painter.drawLine(0, 0, self.width(), 0)
            
            painter.drawLine(0, self.height()-1, self.width(), self.height()-1)
        super().paintEvent(event)