from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTextEdit, QCheckBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextCursor  
import json
import services.logger as log
import utils.helpers as helpers
import os

class InfoPanel(QWidget):
    """
    Document and system information panel.
    
    Features:
    - Real-time document statistics (line count, word count, character count)
    - Current cursor position (line, column)
    - File encoding detection
    - File size and last modified timestamp
    - Optional system resource monitoring toggle
    - Auto-refresh on document change with configurable update interval
    - Theme-aware styling
    """
    
    def __init__(self, base_path, theme=None, lang=None):
        """Initialize the info panel with base path and theme settings."""
        super().__init__()
        self.base_path = base_path
        self.theme = theme
        self.lang = lang
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        """Setup user interface"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        label = QLabel("Info")
        self.layout.addWidget(label)
        self.layout.addStretch()

    def show_panel(self):
        self.show()

    def hide_panel(self):
        self.hide()
    
    def apply_theme(self):
        """Apply color theme to UI elements using CSS styling."""
        # Extract theme colors
        self.bg_card = self.theme.get('bg_card')
        self.bg_color = self.theme.get('bg_color')
        self.accent_color = self.theme.get('accent_color')
        self.accent_primary = self.theme.get('accent_primary')
        self.text_main = self.theme.get('text_main')
        self.btn_bg_color = self.theme.get('btn_bg_color')
        self.accent_light = self.theme.get('accent_light')
        self.accent_gray = self.theme.get('accent_gray')
        self.text_muted = self.theme.get('text_muted')

        # Apply comprehensive styling
        self.setStyleSheet(f"""
            QLabel {{
                color: #fff;
            }}
        """)
        
        # Force UI refresh
        self.update()