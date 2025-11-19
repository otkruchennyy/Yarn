import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QColor, QFont
import utils.helpers as helpers

class tabs(QWidget):
    def __init__(self, theme=None, parent=None):
        super().__init__(parent)
        self.bg_color = None
        self.theme = theme
        self.path_tabs = os.path.join(helpers.get_project_root(), "config", "tabs_config.json")
        self.setup_ui()
        self.apply_theme()
        self.scroll_area.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.scroll_area and event.type() == QEvent.Wheel:
            scroll_bar = self.scroll_area.horizontalScrollBar()
            delta = event.angleDelta().y()
            scroll_bar.setValue(scroll_bar.value() - delta)
            return True
        return super().eventFilter(obj, event)

    def setup_ui(self):
        self.property_tabs = helpers.get_json_property(self.path_tabs)
        self.count_tabs = len(self.property_tabs)
        self.setObjectName("tabs")
        layout = QHBoxLayout(self)
        self.setFixedHeight(23)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        add_tab_btn = QPushButton("+")
        add_tab_btn.setFixedSize(50, 18)
        add_tab_btn.setCursor(Qt.PointingHandCursor)
        add_tab_btn.setProperty("class", "tab")
        add_tab_btn.setFont(QFont("Monospace", 10))
        layout.addWidget(add_tab_btn)
        
        self.tabs_container = QWidget()
        self.tabs_container.setFixedHeight(20)
        self.tabs_layout = QHBoxLayout(self.tabs_container)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(0)
        self.tabs_width = 0
        self.tabs = {}
        for i in range(self.count_tabs):
            name = list(self.property_tabs.keys())[i]
            if len(name) > 15:
                display_name = name[:15] + '..'
            else:
                display_name = name
            self.tabs_width += len(display_name) * 11
            btn = QPushButton(display_name)
            btn.setFixedHeight(18)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("class", "tab")
            btn.setFont(QFont("Monospace", 10))
            self.tabs[display_name] = btn
            self.tabs_layout.addWidget(btn)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFixedHeight(23)
        self.scroll_area.setWidget(self.tabs_container)

        self.scroll_area.setWidgetResizable(False)
        
        layout.addWidget(self.scroll_area)
    
    def reload_tabs(self):
        for i in reversed(range(self.tabs_layout.count())):
            widget = self.tabs_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.tabs.clear()
        self.tabs_width = 0
        self.property_tabs = helpers.get_json_property(self.path_tabs)
        self.count_tabs = len(self.property_tabs)
        
        for i in range(self.count_tabs):
            name = list(self.property_tabs.keys())[i]
            if len(name) > 15:
                display_name = name[:15] + '..'
            else:
                display_name = name
            self.tabs_width += len(display_name) * 11
            
            btn = QPushButton(display_name)
            btn.setFixedHeight(18)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("class", "tab")
            btn.setFont(QFont("Monospace", 10))
            btn.setFixedWidth(len(display_name) * 15)
            self.tabs[display_name] = btn
            self.tabs_layout.addWidget(btn)
        
        self.tabs_container.setMinimumWidth(self.tabs_width + 30)
    
    def apply_theme(self):
        self.bg_card = self.theme.get('bg_card')
        self.bg_color = self.theme.get('bg_color')
        self.accent_color = self.theme.get('accent_color')
        self.text_main = self.theme.get('text_main')
        self.btn_bg_color = self.theme.get('btn_bg_color')
        self.btn_hover_bg_color = self.theme.get('btn_hover_bg_color')

        self.update()        
        self.setStyleSheet(f"""
            QPushButton[class="tab"] {{
                color: {self.text_main};
                background: transparent;
                padding-left: 5px;
                padding-right: 5px;
                border: none;
                border-radius: 3px;
                font-weight: 600;
            }}
            QPushButton[class="tab"]:hover {{ 
                background-color: #292929;
            }}
        """)

        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollArea::viewport {{
                background: {self.bg_card};
            }}
            QPushButton {{
                color: {self.text_main};
                background: {self.bg_card};
                padding-left: 5px;
                padding-right: 5px;
                border: none;
                border-radius: 3px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: #292929;
            }}
            QScrollBar:horizontal {{
                background: white;
                border: none;
                height: 3px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.accent_color};
            }}
            QScrollBar::add-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)
        
    
    def paintEvent(self, event):
        if self.bg_color and self.accent_color:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(self.bg_color))

            painter.setPen(QColor(self.accent_color))
            painter.drawLine(0, 0, self.width(), 0)
            
            painter.drawLine(0, self.height()-1, self.width(), self.height()-1)
            from PySide6.QtGui import QPalette

            palette = self.tabs_container.palette()
            palette.setColor(QPalette.Window, QColor(self.bg_color))
            self.tabs_container.setPalette(palette)
            self.tabs_container.setAutoFillBackground(True)
        super().paintEvent(event)