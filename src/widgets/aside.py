from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
from PySide6.QtCore import Qt
import utils.aside_manager as al
import os
# from widgets.aside_panels.logs import LogsPanel
from widgets.aside_panels.tools import ToolsPanel
from widgets.aside_panels.plugins import PluginsPanel  
from widgets.aside_panels.settings import SettingsPanel
from widgets.aside_panels.workspaces import WorkspacesPanel
from widgets.extra_panels.extra_panels_manager import ExtraPanel

class aside(QWidget):
    """Aside widget"""
    def __init__(self, parent=None, theme=None, tabs_widget=None, base_path=None):
        super().__init__(parent)
        self.theme = theme
        self.base_path = base_path
        self.tabs = tabs_widget
        
        self.setMouseTracking(True)
        self.setFixedWidth(50)
        
        self.widget1 = QFrame()
        self.widget2 = QFrame()
        self.btn_toggle = QPushButton(">>")
        
        al.init_widget(self)
        
        self.create_panels()
        
        self.setup_ui()
        self.apply_theme()
    
    def create_panels(self):
        """Create and register all content panels"""
        # Workspaces panel
        self.workspaces_panel = WorkspacesPanel(self.base_path, self.tabs, self.theme)
        al.register_panel('workspaces', self.workspaces_panel)
        
        # Tools panel
        self.tools_panel = ToolsPanel(self.base_path, self.theme)
        al.register_panel('tools', self.tools_panel)
        
        # Plugins panel 
        self.plugins_panel = PluginsPanel(self.base_path, self.theme)
        al.register_panel('plugins', self.plugins_panel)
        
        # Settings panel
        self.settings_panel = SettingsPanel(self.base_path, self.theme)
        al.register_panel('settings', self.settings_panel)

        # self.logs_panel = LogsPanel(self.base_path, self.theme)
        # al.register_panel('logs', self.logs_panel)
    
    def setup_ui(self):
        """
Creates a layout with two main panels:
- Left panel (widget1): fixed control panel with buttons
- Right panel (widget2): hidden by default side panel with content

UI Architecture:
┌────────────────────────────────────────┐
│ main_layout (QVBoxLayout)              │
│ ┌────────────────────────────────────┐ │
│ │ content_frame (QFrame)             │ │
│ │ ┌─────────────┐ ┌────────────────┐ │ │
│ │ │ widget1     │ │ widget2        │ │ │
│ │ │ (50px wide) │ │ (aside panel)  │ │ │
│ │ │ ┌─────────┐ │ │ ┌────────────┐ │ │ │
│ │ │ │ btn_a   │ │ │ │ label2     │ │ │ │
│ │ │ │ btn_b   │ │ │ │            │ │ │ │
│ │ │ │ ...     │ │ │ │            │ │ │ │
│ │ │ └─────────┘ │ │ └────────────┘ │ │ │
│ │ └─────────────┘ └────────────────┘ │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘

Widgets:
- self.btn_a: button to toggle side panel visibility
- btn_b, btn_c, btn_d, btn_e: additional buttons (placeholders)
- self.widget2: hidden side panel, controlled by btn_a

States:
- Default: widget1 visible, widget2 hidden
- When btn_a is clicked: widget2 appears/disappears
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.content_frame = QFrame()
        
        content_layout = QHBoxLayout(self.content_frame)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Left control panel
        self.widget1.setFixedWidth(50)

        self.btn_toggle = QPushButton(">>")
        self.btn_toggle.setToolTip("Aside panel")
        self.btn_toggle.clicked.connect(al.aside_state)
        self.btn_toggle.setProperty("class", "main")

        self.btn_workspaces = QPushButton("🗂") # TODO: replace emoji with img
        self.btn_workspaces.setToolTip("Workspaces")
        self.btn_workspaces.clicked.connect(al.btn_workspaces_clicked)
        self.btn_workspaces.setProperty("class", "main")

        self.btn_tools = QPushButton("🛠") # TODO: replace emoji with img
        self.btn_tools.setToolTip("Tools")
        self.btn_tools.clicked.connect(al.btn_tools_clicked)
        self.btn_tools.setProperty("class", "main")

        self.btn_plugins = QPushButton("🧩") # TODO: replace emoji with img
        self.btn_plugins.setToolTip("Plugins")
        self.btn_plugins.clicked.connect(al.btn_plugins_clicked)
        self.btn_plugins.setProperty("class", "main")

        self.btn_settings = QPushButton("⚙") # TODO: replace emoji with img
        self.btn_settings.setToolTip("Settings")
        self.btn_settings.clicked.connect(al.btn_settings_clicked)
        self.btn_settings.setProperty("class", "main")

        self.btn_logs = QPushButton("📋") # TODO: replace emoji with img
        self.btn_logs.setToolTip("View logs")
        self.btn_logs.clicked.connect(al.btn_logs_clicked)
        self.btn_logs.setProperty("class", "secondary")
        
        widget1_layout = QVBoxLayout(self.widget1)
        widget1_layout.setAlignment(Qt.AlignTop)
        widget1_layout.addWidget(self.btn_toggle)
        widget1_layout.addWidget(self.btn_workspaces)
        widget1_layout.addWidget(self.btn_tools)
        widget1_layout.addWidget(self.btn_plugins)
        widget1_layout.addWidget(self.btn_settings)
        widget1_layout.addStretch()
        widget1_layout.addWidget(self.btn_logs)
        
        # Right side panel 
        self.widget2.hide()
        
        self.widget2_layout = QVBoxLayout(self.widget2)
        self.widget2_layout.setAlignment(Qt.AlignTop)
        self.widget2_layout.setContentsMargins(0, 0, 0, 0)
        self.widget2_layout.setSpacing(0)
        
        self.widget2_layout.addWidget(self.workspaces_panel)
        self.widget2_layout.addWidget(self.tools_panel)
        self.widget2_layout.addWidget(self.plugins_panel)
        self.widget2_layout.addWidget(self.settings_panel)
        # self.widget2_layout.addWidget(self.logs_panel)
        
        self.workspaces_panel.hide()
        self.tools_panel.hide()
        self.plugins_panel.hide()
        self.settings_panel.hide()
        # self.logs_panel.hide()
        
        # add_widgets_to_main_layout 
        content_layout.addWidget(self.widget1)
        content_layout.addWidget(self.widget2)
        
        main_layout.addWidget(self.content_frame)


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
        self.accent_gray = self.theme.get('accent_gray')

        # Refresh UI
        self.update()
        
        # Apply main widget styling
        self.setStyleSheet(f"""
                background-color: {self.bg_card}; 
                color: {self.text_main};
            """)
    
    # Apply button styling to content frame
        self.content_frame.setStyleSheet(f"""
            QPushButton[class="main"]{{
                background-color: {self.btn_bg_color};
                color: {self.text_main};
                border: 1px solid {self.accent_color};
                padding: 5px;
                border-radius: 3px;
            }}
            
            QPushButton[class="main"]:hover {{
                background-color: {self.accent_gray};
                border: 1px solid {self.accent_primary};
            }}
            
            QPushButton[class="main"]:pressed {{
                background-color: {self.accent_primary};
                color: {self.accent_color}
            }}
            QPushButton[class="active_main"] {{
                background-color: {self.accent_primary};
                color: {self.accent_color}
            }}
            QPushButton[class="secondary"]{{
                background-color: transparent;
                color: {self.text_main};
                border: 1px solid {self.accent_color};
                padding: 5px;
                border-radius: 3px;
            }}
            QPushButton[class="secondary"]:hover{{
                background-color: {self.accent_gray};
                border: 1px solid {self.accent_primary};
            }}
            QPushButton[class="secondary"]:pressed{{
                background-color: {self.accent_primary};
                color: {self.accent_color}
            }}
            QToolTip {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
            }}
            """)