from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTextEdit, QCheckBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextCursor  
import json
import services.logger as log
import utils.helpers as helpers
import os

class LogsPanel(QWidget):
    """
    Panel for displaying and filtering application logs with auto-refresh functionality.
    
    Features:
    - Real-time log monitoring with configurable refresh interval
    - Filter logs by severity level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Persist filter settings across sessions
    - Auto-scroll to newest log entries
    - Theme-aware styling
    """
    
    def __init__(self, base_path, theme=None, lang=None):
        """Initialize the logs panel with base path and theme settings."""
        super().__init__()
        self.base_path = base_path
        self.theme = theme
        self.lang = lang
        self.log_path = os.path.join(self.base_path, "app.log")
        self.logs_widgets = {}
        self.path_logs = log.get_log_path()  # Path for logger service
        self.setup_ui()
        self.apply_theme()
        
        # Timer for auto-refresh functionality
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_logs)
        
        # Start auto-refresh if enabled by default
        if self.btn_auto_refresh.isChecked():
            self.refresh_timer.start(500)  # 500ms refresh interval

    def setup_ui(self):
        """Setup the user interface with filter controls and log display area."""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        # Filter controls container
        self.filter_widget = QWidget()
        self.layout.addWidget(self.filter_widget)

        self.filter_layout = QHBoxLayout(self.filter_widget)
        self.filter_layout.setContentsMargins(5, 5, 5, 5)
        self.filter_layout.setSpacing(20)

        self.filter_label = QLabel(self.lang["Filter levels"])
        self.filter_layout.addWidget(self.filter_label)

        # Create severity level checkboxes
        self.debug_checkbox = QCheckBox("DEBUG")
        self.info_checkbox = QCheckBox("INFO")
        self.warning_checkbox = QCheckBox("WARNING")
        self.error_checkbox = QCheckBox("ERROR")
        self.critical_checkbox = QCheckBox("CRITICAL")

        for checkbox in [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, 
                        self.error_checkbox, self.critical_checkbox]:
            self.filter_layout.addWidget(checkbox)
            checkbox.stateChanged.connect(self.on_filter_changed)

        # Filter control buttons
        self.btn_select_all = QPushButton(self.lang["All"])
        self.btn_select_all.setFixedWidth(50)
        self.btn_select_none = QPushButton(self.lang["None"])
        self.btn_select_none.setFixedWidth(50)

        # Auto-refresh toggle button
        self.btn_auto_refresh = QPushButton(self.lang["Auto"])
        self.btn_auto_refresh.setCheckable(True)
        self.btn_auto_refresh.setChecked(True)  # Enabled by default
        self.btn_auto_refresh.setFixedWidth(70)
        self.btn_auto_refresh.clicked.connect(self.toggle_auto_refresh)

        self.btn_select_all.clicked.connect(self.select_all_levels)
        self.btn_select_none.clicked.connect(self.deselect_all_levels)
        
        self.filter_layout.addWidget(self.btn_select_all)
        self.filter_layout.addWidget(self.btn_select_none)
        self.filter_layout.addWidget(self.btn_auto_refresh)
        self.filter_layout.addStretch()  # Push everything to the left

        # Load saved filter settings
        self.load_filter_settings()

        # Main log display area
        self.logsTextArea = QTextEdit()
        self.logsTextArea.setReadOnly(True)
        self.logsTextArea.setLineWrapMode(QTextEdit.NoWrap)
        self.logsTextArea.setUndoRedoEnabled(False)
        self.logsTextArea.setAcceptRichText(False)
        self.logsTextArea.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)

        # State tracking for incremental updates
        self.log_line_count = 0  # Track number of lines in log file
        self.last_modified_time = 0  # Track file modification time
        
        # Load initial log data
        self.initial_load()

        self.layout.addWidget(self.logsTextArea)
    
    def initial_load(self):
        """Load initial log data on panel initialization with current filters applied."""
        try:
            if not os.path.exists(self.log_path):
                log.debug(msg=f"Log file not found on init: {self.log_path}")
                return
            
            # Track file modification time for change detection
            self.last_modified_time = os.path.getmtime(self.log_path)
            
            # Load entire log file on startup
            with open(self.log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.log_line_count = len(lines)
                
                # Apply current filter settings
                active_filters = self.get_active_filters()
                if len(active_filters) == 5:  # All filters active
                    self.logsTextArea.setPlainText(''.join(lines))
                else:
                    # Filter lines based on active severity levels
                    filtered_lines = []
                    for line in lines:
                        line_upper = line.upper()
                        if any(filter_level in line_upper for filter_level in active_filters):
                            filtered_lines.append(line)
                    self.logsTextArea.setPlainText(''.join(filtered_lines))
                
                # Auto-scroll to show newest entries at bottom
                cursor = self.logsTextArea.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.logsTextArea.setTextCursor(cursor)
                
                log.debug(msg=f'Initial log load: {self.log_line_count} lines')
                
        except Exception as e:
            log.debug(msg=f"Error in initial_load: {str(e)}")

    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality on/off."""
        if self.btn_auto_refresh.isChecked():
            log.debug(msg='"auto_refresh" active')
            self.btn_auto_refresh.setText(self.lang["Auto"])
            self.refresh_timer.start(500)
        else:
            log.debug(msg='"auto_refresh" pause')
            self.btn_auto_refresh.setText(self.lang["Pause"])
            self.refresh_timer.stop()

    def on_filter_changed(self):
        """Handler for filter checkbox changes - saves settings and reloads logs."""
        self.save_filter_settings()
        self.log_line_count = 0  # Reset line count for full reload
        self.load_logs_with_filters()

    def load_filter_settings(self):
        """Load filter settings from JSON configuration file."""
        log_config_path = os.path.join(self.base_path, "config", "log_filters.json")
        
        # Default settings if config doesn't exist
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
            # Save default settings if file doesn't exist
            with open(log_config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        
        checkboxes = [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, 
                    self.error_checkbox, self.critical_checkbox]
        
        # Prevent signal emission during initialization
        for cb in checkboxes:
            cb.blockSignals(True)
        
        # Apply loaded settings to checkboxes
        self.debug_checkbox.setChecked(settings.get("debug", True))
        self.info_checkbox.setChecked(settings.get("info", True))
        self.warning_checkbox.setChecked(settings.get("warning", True))
        self.error_checkbox.setChecked(settings.get("error", True))
        self.critical_checkbox.setChecked(settings.get("critical", True))
        
        # Re-enable signals after initialization
        for cb in checkboxes:
            cb.blockSignals(False)

    def save_filter_settings(self):
        """Save current filter settings to JSON configuration file."""
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
        """Select all log severity level filters."""
        checkboxes = [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, 
                    self.error_checkbox, self.critical_checkbox]
        
        # Block signals during batch update
        for cb in checkboxes:
            cb.blockSignals(True)
        
        self.debug_checkbox.setChecked(True)
        self.info_checkbox.setChecked(True)
        self.warning_checkbox.setChecked(True)
        self.error_checkbox.setChecked(True)
        self.critical_checkbox.setChecked(True)
        
        # Re-enable signals and trigger update
        for cb in checkboxes:
            cb.blockSignals(False)
        
        self.save_filter_settings()
        self.log_line_count = 0  # Reset for full reload
        self.load_logs_with_filters()

    def deselect_all_levels(self):
        """Deselect all log severity level filters."""
        checkboxes = [self.debug_checkbox, self.info_checkbox, self.warning_checkbox, 
                    self.error_checkbox, self.critical_checkbox]
        
        # Block signals during batch update
        for cb in checkboxes:
            cb.blockSignals(True)
        
        self.debug_checkbox.setChecked(False)
        self.info_checkbox.setChecked(False)
        self.warning_checkbox.setChecked(False)
        self.error_checkbox.setChecked(False)
        self.critical_checkbox.setChecked(False)
        
        # Re-enable signals and trigger update
        for cb in checkboxes:
            cb.blockSignals(False)
        
        self.save_filter_settings()
        self.log_line_count = 0  # Reset for full reload
        self.load_logs_with_filters()

    def get_active_filters(self):
        """Return list of currently active log severity filters."""
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
        """
        Timer-based incremental log loading - only processes new lines.
        
        This method is called periodically by the refresh timer and only
        reads new log entries that have been added since the last check.
        """
        try:
            # Check if log file exists
            if not os.path.exists(self.log_path):
                return
            
            # Check if file has been modified since last read
            current_modified_time = os.path.getmtime(self.log_path)
            if current_modified_time <= self.last_modified_time:
                return  # No changes detected
            
            self.last_modified_time = current_modified_time
            
            # Get current filter settings
            active_filters = self.get_active_filters()
            if not active_filters:
                return  # No filters active, nothing to display
            
            # Read new log entries
            with open(self.log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                total_lines = len(lines)
                
                # If no new lines, update counter and exit
                if total_lines <= self.log_line_count:
                    self.log_line_count = total_lines
                    return
                
                # Extract only new lines since last check
                new_lines = lines[self.log_line_count:]
                
                # Apply filters to new lines
                filtered_new_lines = []
                if len(active_filters) == 5:  # All filters active
                    filtered_new_lines = new_lines
                else:
                    for line in new_lines:
                        line_upper = line.upper()
                        if any(filter_level in line_upper for filter_level in active_filters):
                            filtered_new_lines.append(line)
                
                # Append filtered new lines to display
                if filtered_new_lines:
                    current_text = self.logsTextArea.toPlainText()
                    new_text = ''.join(filtered_new_lines)
                    
                    self.logsTextArea.setPlainText(current_text + new_text)
                    
                    # Auto-scroll to newest entries
                    cursor = self.logsTextArea.textCursor()
                    cursor.movePosition(QTextCursor.End)
                    self.logsTextArea.setTextCursor(cursor)
                
                # Update line counter for next incremental read
                self.log_line_count = total_lines
                
        except Exception as e:
            log.debug(msg=f"Error in timer load_logs: {str(e)}")
    
    def load_logs_with_filters(self):
        """Complete reload of all logs with current filter settings applied."""
        try:
            if not os.path.exists(self.log_path):
                self.logsTextArea.setPlainText(f"Log file not found: {self.log_path}")
                return
            
            active_filters = self.get_active_filters()
            if not active_filters:
                self.logsTextArea.setPlainText("All filters are disabled. No logs to display.")
                return
            
            # Read and filter entire log file
            with open(self.log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.log_line_count = len(lines)
                self.last_modified_time = os.path.getmtime(self.log_path)
                
                if len(active_filters) == 5:
                    self.logsTextArea.setPlainText(''.join(lines))
                else:
                    # Apply filters to all lines
                    filtered_lines = []
                    for line in lines:
                        line_upper = line.upper()
                        if any(filter_level in line_upper for filter_level in active_filters):
                            filtered_lines.append(line)
                    self.logsTextArea.setPlainText(''.join(filtered_lines))
                
                # Auto-scroll to bottom
                cursor = self.logsTextArea.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.logsTextArea.setTextCursor(cursor)
                
        except Exception as e:
            log.debug(msg=f"Error in load_logs_with_filters: {str(e)}")

    def show_panel(self):
        """Show the panel and start auto-refresh if enabled."""
        self.show()
        if self.btn_auto_refresh.isChecked():
            self.refresh_timer.start(500)

    def hide_panel(self):
        """Hide the panel and stop auto-refresh timer."""
        self.hide()
        self.refresh_timer.stop()
    
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
            /* Custom scrollbar styling for dark theme */
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
            QPushButton {{
                background-color: {self.accent_gray};
                border: 1px solid {self.accent_color};
                color: {self.text_main}
            }}
        """)
        
        # Force UI refresh
        self.update()