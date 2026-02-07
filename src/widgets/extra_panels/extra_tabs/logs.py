from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTextEdit, QCheckBox
from PySide6.QtCore import Qt
import json
import services.logger as log
import utils.helpers as helpers
import os

class LogsPanel(QWidget):
    def __init__(self, base_path, theme=None):
        super().__init__()
        self.base_path = base_path
        self.theme = theme
        self.logs_widgets = {}
        self.path_logs = log.get_log_path()
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
# 
        self.filter_widget = QWidget()
        self.layout.addWidget(self.filter_widget)

        self.filter_layout = QHBoxLayout(self.filter_widget)
        self.filter_layout.setContentsMargins(5, 5, 5, 5)
        self.filter_layout.setSpacing(20)

        self.filter_label = QLabel("Filter levels:")
        self.filter_layout.addWidget(self.filter_label)

        self.debug_checkbox = QCheckBox("DEBUG")
        self.info_checkbox = QCheckBox("INFO")
        self.warning_checkbox = QCheckBox("WARNING")
        self.error_checkbox = QCheckBox("ERROR")
        self.critical_checkbox = QCheckBox("CRITICAL")

        for checkbox in [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, self.error_checkbox, self.critical_checkbox]:
            self.filter_layout.addWidget(checkbox)
            checkbox.stateChanged.connect(self.save_filter_settings)

        self.btn_select_all = QPushButton("All")
        self.btn_select_all.setFixedWidth(50)
        self.btn_select_none = QPushButton("None")
        self.btn_select_none.setFixedWidth(50)

        self.btn_select_all.clicked.connect(self.select_all_levels)
        self.btn_select_none.clicked.connect(self.deselect_all_levels)
        
        self.filter_layout.addWidget(self.btn_select_all)
        self.filter_layout.addWidget(self.btn_select_none)

        self.load_filter_settings()
    
        self.filter_layout.addStretch()

        self.logsTextArea = QTextEdit()
        self.logsTextArea.setReadOnly(True)
        self.logsTextArea.setLineWrapMode(QTextEdit.NoWrap)
        self.logsTextArea.setUndoRedoEnabled(False)
        self.logsTextArea.setAcceptRichText(False)
        self.logsTextArea.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.load_logs()
        self.layout.addWidget(self.logsTextArea)
    
    def load_filter_settings(self):
        """Load filter settings from JSON (log_filters.json)"""
        log_config_path = os.path.join(self.base_path, "config", "log_filters.json")
        
        default_settings = {
            "debug": True,
            "info": True,
            "warning": True,
            "error": True,
            "critical": True
        }
        
        try:
            with open(log_config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = default_settings
            # Save default settings
            with open(log_config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        
        # Applying Settings to QCheckBox
        self.debug_checkbox.setChecked(settings.get("debug", True))
        self.info_checkbox.setChecked(settings.get("info", True))
        self.warning_checkbox.setChecked(settings.get("warning", True))
        self.error_checkbox.setChecked(settings.get("error", True))
        self.critical_checkbox.setChecked(settings.get("critical", True))

    def save_filter_settings(self):
        """Save filters settings to JSON (log_filters.json)"""
        settings = {
            "debug": self.debug_checkbox.isChecked(),
            "info": self.info_checkbox.isChecked(),
            "warning": self.warning_checkbox.isChecked(),
            "error": self.error_checkbox.isChecked(),
            "critical": self.critical_checkbox.isChecked()
        }
        
        config_path = os.path.join(self.base_path, "config", "log_filters.json")
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving filter settings: {e}")

    def select_all_levels(self):
        """Select all levels"""
        self.debug_checkbox.setChecked(True)
        self.info_checkbox.setChecked(True)
        self.warning_checkbox.setChecked(True)
        self.error_checkbox.setChecked(True)
        self.critical_checkbox.setChecked(True)

    def deselect_all_levels(self):
        """Deselect all levels"""
        self.debug_checkbox.setChecked(False)
        self.info_checkbox.setChecked(False)
        self.warning_checkbox.setChecked(False)
        self.error_checkbox.setChecked(False)
        self.critical_checkbox.setChecked(False)

    def get_active_filters(self):
        """Get a list of active filters"""
        active_filters = []
        if self.debug_checkbox.isChecked():
            active_filters.append("DEBUG")
        if self.info_checkbox.isChecked():
            active_filters.append("INFO")
        if self.warning_checkbox.isChecked():
            active_filters.append("WARNING")
        if self.error_checkbox.isChecked():
            active_filters.append("ERROR")
        if self.critical_checkbox.isChecked():
            active_filters.append("CRITICAL")
        return active_filters

    def load_logs(self):
        """Load logs"""
        # TODO

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
        self.accent_gray = self.theme.get('accent_gray')
        self.text_muted = self.theme.get('text_muted')

        self.setStyleSheet(f"""
            QLabel {{
                color: #fff;
            }}
            QTextEdit {{
                background-color: #000;
                border: 1px solid {self.accent_gray};
                border-width: 1px 1px 0px 0px;
            }}
            
            /* Активный чекбокс */
            QCheckBox::indicator:checked {{
                background-color: {self.accent_primary};
                border: 1px solid {self.accent_gray};
            }}
            
            /* Отключенный чекбокс */
            QCheckBox::indicator:disabled {{
                background-color: {self.accent_gray};
                border: 1px solid {self.accent_gray};
            }}
            QCheckBox {{
                color: {self.text_main}
            }}
        """)
        
        # Refresh UI
        self.update()