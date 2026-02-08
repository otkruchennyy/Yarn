from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTextEdit, QCheckBox
from PySide6.QtCore import Qt, QTimer
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
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_logs)
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
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

        for checkbox in [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, 
                        self.error_checkbox, self.critical_checkbox]:
            self.filter_layout.addWidget(checkbox)
            checkbox.stateChanged.connect(self.on_filter_changed)

        self.btn_select_all = QPushButton("All")
        self.btn_select_all.setFixedWidth(50)
        self.btn_select_none = QPushButton("None")
        self.btn_select_none.setFixedWidth(50)

        self.btn_auto_refresh = QPushButton("🔄 Auto")
        self.btn_auto_refresh.setCheckable(True)
        self.btn_auto_refresh.setChecked(True)
        self.btn_auto_refresh.setFixedWidth(70)
        self.btn_auto_refresh.clicked.connect(self.toggle_auto_refresh)

        self.btn_select_all.clicked.connect(self.select_all_levels)
        self.btn_select_none.clicked.connect(self.deselect_all_levels)
        
        self.filter_layout.addWidget(self.btn_select_all)
        self.filter_layout.addWidget(self.btn_select_none)
        self.filter_layout.addWidget(self.btn_auto_refresh)
        self.filter_layout.addStretch()

        self.load_filter_settings()

        self.logsTextArea = QTextEdit()
        self.logsTextArea.setReadOnly(True)
        self.logsTextArea.setLineWrapMode(QTextEdit.NoWrap)
        self.logsTextArea.setUndoRedoEnabled(False)
        self.logsTextArea.setAcceptRichText(False)
        self.logsTextArea.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        
        self.log_line_count = 0
        try:
            log_path = os.path.join(self.base_path, "app.log")
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = f.readlines()
                self.log_line_count = len(log_data)
                self.logsTextArea.setPlainText(''.join(log_data))
                log.debug(msg=f'log_line_count: "{self.log_line_count}"')
        except FileNotFoundError:
            log.debug(msg=f"File not found: {log_path}")
        except PermissionError:
            log.debug(msg=f"Permission denied: {log_path}")
        except UnicodeDecodeError:
            log.debug(msg=f"Encoding error in {log_path}")
        except Exception as e:
            log.debug(msg=f"Error loading logs: {str(e)}\tType: {type(e).__name__}")

        self.load_logs()
        self.layout.addWidget(self.logsTextArea)

    def toggle_auto_refresh(self):
        """ON/OFF autorefresh"""
        log.debug(msg='def"toggle_auto_refresh" signal')
        if self.btn_auto_refresh.isChecked():
            self.btn_auto_refresh.setText("🔄 Auto")
            if self.isVisible():
                self.refresh_timer.start(1000)
        else:
            self.btn_auto_refresh.setText("⏸ Pause")
            self.refresh_timer.stop()

    def on_filter_changed(self):
        self.save_filter_settings()
        self.load_logs()

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
        
        checkboxes = [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, self.error_checkbox, self.critical_checkbox]
        
        for cb in checkboxes:
            cb.blockSignals(True)
        
        self.debug_checkbox.setChecked(settings.get("debug", True))
        self.info_checkbox.setChecked(settings.get("info", True))
        self.warning_checkbox.setChecked(settings.get("warning", True))
        self.error_checkbox.setChecked(settings.get("error", True))
        self.critical_checkbox.setChecked(settings.get("critical", True))
        
        for cb in checkboxes:
            cb.blockSignals(False)

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
        checkboxes = [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, self.error_checkbox, self.critical_checkbox]
        
        for cb in checkboxes:
            cb.blockSignals(True)
        
        self.debug_checkbox.setChecked(True)
        self.info_checkbox.setChecked(True)
        self.warning_checkbox.setChecked(True)
        self.error_checkbox.setChecked(True)
        self.critical_checkbox.setChecked(True)
        
        for cb in checkboxes:
            cb.blockSignals(False)
        
        self.save_filter_settings()
        self.load_logs()

    def deselect_all_levels(self):
        """Deselect all levels"""
        checkboxes = [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, self.error_checkbox, self.critical_checkbox]
        
        for cb in checkboxes:
            cb.blockSignals(True)
        
        self.debug_checkbox.setChecked(False)
        self.info_checkbox.setChecked(False)
        self.warning_checkbox.setChecked(False)
        self.error_checkbox.setChecked(False)
        self.critical_checkbox.setChecked(False)
        
        for cb in checkboxes:
            cb.blockSignals(False)
        
        self.save_filter_settings()
        self.load_logs()

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
        """Load logs with current filters"""
        log_path = os.path.join(self.base_path, "app.log")
        
        try:
            active_filters = self.get_active_filters()
            
            if not active_filters:
                self.logsTextArea.setPlainText("All filters are disabled. No logs to display.")
                return
            
            if not os.path.exists(log_path):
                self.logsTextArea.setPlainText(f"Log file not found: {log_path}")
                return
            
            with open(log_path, 'r', encoding='utf-8') as f:
                # self.log_line_count
                log_data = f.readlines()
                len_log_data = len(log_data)
                if len_log_data == self.log_line_count: pass
                else:
                    for line in log_data[self.log_line_count:]:
                        self.logsTextArea.append(line.replace('\n', ''))
                    self.log_line_count = len_log_data
                # if len(active_filters) == 5:
                #     log_data = f.read()
                #     self.logsTextArea.setPlainText(log_data)
                # else:
                #     all_lines = f.readlines()
                #     filtered_lines = []
                    
                #     for line in all_lines:
                #         line_upper = line.upper()
                #         for log_level in active_filters:
                #             if log_level in line_upper:
                #                 filtered_lines.append(line)
                #                 break
                    
                #     result_text = ''.join(filtered_lines)
                #     self.logsTextArea.setPlainText(result_text)
        
        except FileNotFoundError:
            self.logsTextArea.setPlainText(f"File not found: {log_path}")
        except PermissionError:
            self.logsTextArea.setPlainText(f"Permission denied: {log_path}")
        except UnicodeDecodeError:
            self.logsTextArea.setPlainText(f"Encoding error in {log_path}")
        except Exception as e:
            self.logsTextArea.setPlainText(f"Error loading logs: {str(e)}\tType: {type(e).__name__}")

    def show_panel(self):
        self.show()
        if self.btn_auto_refresh.isChecked():
            self.refresh_timer.start(1000)

    def hide_panel(self):
        self.hide()
        self.refresh_timer.stop()
    
    def apply_theme(self):
        """
        Applies color theme to UI elements using CSS styling.
        Updates main widget and button styles with theme colors.
        """
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
                color: {self.text_main}
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {self.accent_primary};
                border: 1px solid {self.accent_gray};
            }}
            
            QCheckBox::indicator:disabled {{
                background-color: {self.accent_gray};
                border: 1px solid {self.accent_gray};
            }}
            QCheckBox {{
                color: {self.text_main}
            }}
            QScrollBar:vertical {{
                background-color: #1a1a1a;
                width: 14px;
                margin: 0px;
                border-radius: 7px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.accent_gray};
                min-height: 25px;
                border-radius: 7px;
                border: 2px solid #2a2a2a;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.accent_primary};
            }}
            
            QScrollBar::handle:vertical:pressed {{
                background-color: {self.accent_primary};
            }}
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
                border: none;
                background: none;
            }}
            
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
            
            QScrollBar:horizontal {{
                background-color: #1a1a1a;
                height: 14px;
                margin: 0px;
                border-radius: 7px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {self.accent_gray};
                min-width: 25px;
                border-radius: 7px;
                border: 2px solid #2a2a2a;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {self.accent_primary};
            }}
            
            QScrollBar::handle:horizontal:pressed {{
                background-color: {self.accent_primary};
            }}
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {{
                width: 0px;
                border: none;
                background: none;
            }}
            
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}
        """)
        
        # Refresh UI
        self.update()