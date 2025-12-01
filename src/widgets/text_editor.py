from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt
# from PySide6.QtGui import

class textEditor(QWidget):
    def __init__(self, parent=None, theme=None):
        super().__init__(parent)
        self.theme = theme
        self.setMouseTracking(True)
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.content_frame = QFrame()
        label = QLabel("textEditor")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 10)

        content_layout.addWidget(label)
        main_layout.addWidget(self.content_frame)

    def apply_theme(self):
        self.bg_card = self.theme.get('bg_card')
        self.bg_color = self.theme.get('bg_color')
        self.accent_color = self.theme.get('accent_color')
        self.accent_primary = self.theme.get('accent_primary')
        self.text_main = self.theme.get('text_main')
        self.btn_bg_color = self.theme.get('btn_bg_color')
        self.accent_light = self.theme.get('accent_light')
        self.accent_gray = self.theme.get('accent_gray')
        self.text_muted = self.theme.get('text_muted')
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.bg_card};
                border: 1px solid {self.accent_gray};
                border-width: 0 1px;
                color: {self.text_main}
            }}
            QLabel {{
                border: None
            }}
        """)