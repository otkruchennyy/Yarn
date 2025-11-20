from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt
# from PySide6.QtGui import

class aside(QWidget):
    def __init__(self, parent=None, theme=None):
        super().__init__(parent)
        self.theme = theme
        self.setMouseTracking(True)
        self.setFixedWidth(300)
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.content_frame = QFrame()
        label = QLabel("aside")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 10)

        content_layout.addWidget(label)
        main_layout.addWidget(self.content_frame)

    def apply_theme(self):
        self.bg_color = self.theme.get('bg_card')
        self.text_color = self.theme.get('text_main')
        
        self.setStyleSheet("""
            background-color: %s; 
            color: %s;
            border: 1px solid #444;
        """ % (self.bg_color, self.text_color))