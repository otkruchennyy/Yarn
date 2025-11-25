from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import utils.helpers as helpers
import utils.aside_manager as al
import os
# from PySide6.QtGui import

class aside(QWidget):
    def __init__(self, parent=None, theme=None, tabs_widget=None, base_path=None):
        super().__init__(parent)
        self.theme = theme
        self.base_path = base_path
        
        self.tabs = tabs_widget

        self.setMouseTracking(True)
        self.setFixedWidth(50)
        
        self.widget1 = QFrame()
        self.btn_toggle = QPushButton(">>")
        
        al.init_widget(self)
        
        self.setup_ui()
        self.apply_theme()
        self.reload_workspaces()
    
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

        # left control panel
        self.widget1.setFixedWidth(50)

        self.btn_toggle = QPushButton(">>")
        self.btn_toggle.setToolTip("Aside panel")
        self.btn_toggle.clicked.connect(al.aside_state)
        self.btn_toggle.setProperty("class", "workspaces")

        self.btn_workspaces = QPushButton("🗂")
        self.btn_workspaces.setToolTip("Workspaces")
        self.btn_workspaces.clicked.connect(al.btn_workspaces_clicked)
        self.btn_workspaces.setProperty("class", "workspaces")

        self.btn_tools = QPushButton("🛠") 
        self.btn_tools.setToolTip("Tools")
        self.btn_tools.clicked.connect(al.btn_tools_clicked)
        self.btn_tools.setProperty("class", "workspaces")

        self.btn_plugins = QPushButton("🧩")
        self.btn_plugins.setToolTip("Plugins")
        self.btn_plugins.clicked.connect(al.btn_plugins_clicked)
        self.btn_plugins.setProperty("class", "workspaces")

        self.btn_settings = QPushButton("⚙")
        self.btn_settings.setToolTip("Settings")
        self.btn_settings.clicked.connect(al.btn_settings_clicked)
        self.btn_settings.setProperty("class", "workspaces")
        
        widget1_layout = QVBoxLayout(self.widget1)
        widget1_layout.setAlignment(Qt.AlignTop)
        widget1_layout.addWidget(self.btn_toggle)
        widget1_layout.addWidget(self.btn_workspaces)
        widget1_layout.addWidget(self.btn_tools)
        widget1_layout.addWidget(self.btn_plugins)
        widget1_layout.addWidget(self.btn_settings)
        widget1_layout.addStretch()
        
        # right side panel 
        self.widget2 = QFrame()
        self.widget2.hide()
        
        self.widget2_layout = QVBoxLayout(self.widget2)
        self.widget2_layout.setAlignment(Qt.AlignTop)

        # Workspaces
        workspaces_path = os.path.join(self.base_path, "config", "workspaces")
        workspaces = helpers.get_files_from_directory(workspaces_path, 'json')
        font = QFont("Monospace", 10) # TODO: get font from property

        self.workspaces_btn = {}

        for name in workspaces:
            btn = QPushButton(name)
            btn.setFixedSize(200, 18)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("class", "workspaces")
            btn.setFont(font)
            btn.setToolTip(f'{workspaces[name]}')
            btn.setStyleSheet("margin: 0px; padding: 0px;")
            btn.clicked.connect(lambda checked, n=name: self.on_workspaces_clicked(workspaces[n], name)) 
            self.workspaces_btn[name]= btn
            self.widget2_layout.addWidget(btn)
        
        self.widget2_layout.addStretch()
        
        # add_widgets_to_main_layout 
        content_layout.addWidget(self.widget1)
        content_layout.addWidget(self.widget2)
        
        main_layout.addWidget(self.content_frame)

    def on_workspaces_clicked(self, path, name_btn):
        """Load the file into the editor when clicking on the tab"""
        current_workspaces = helpers.get_json_property(os.path.join(self.base_path, "config", "config.json"), "current_workspaces")
        value = (path.split('\\')[-1])[:-5]
        if current_workspaces == value: return
        if os.access(path, os.R_OK):
            helpers.replace_json_content(os.path.join(self.base_path, "config", "tabs_config.json"),
                                         os.path.join(self.base_path, "workspaces", current_workspaces + '.json'))
            
            helpers.add_json_property(os.path.join(self.base_path, "config", "config.json"), "current_workspaces", value, replace=True)

            helpers.replace_json_content(os.path.join(self.base_path, "config", "workspaces", value + '.json'),
                                         os.path.join(self.base_path, "config", "tabs_config.json"))   
             
            if self.tabs:
                self.tabs.reload_tabs()

            self.reload_workspaces()

    def reload_workspaces(self):
        """reload style buttons"""
        for btn in self.workspaces_btn.values():
            btn.deleteLater()
        self.workspaces_btn.clear()
        
        # cleaning layout
        while self.widget2_layout.count():
            child = self.widget2_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # create button
        workspaces_path = os.path.join(self.base_path, "config", "workspaces")
        workspaces = helpers.get_files_from_directory(workspaces_path, 'json')
        font = QFont("Monospace", 10)
        current_workspace = helpers.get_json_property(
            os.path.join(self.base_path, "config", "config.json"), 
            "current_workspaces"
        )

        for name in workspaces:
            btn = QPushButton(name)
            btn.setFixedSize(200, 18)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFont(font)
            btn.setToolTip(f'{workspaces[name]}')
            btn.setStyleSheet("margin: 0px; padding: 0px;")
            btn.clicked.connect(lambda checked, n=name: self.on_workspaces_clicked(workspaces[n], n))
            
            # set style for buttons
            if name == current_workspace:
                btn.setProperty("class", "active_workspaces")
            else:
                btn.setProperty("class", "workspaces")
            
            self.workspaces_btn[name] = btn
            self.widget2_layout.addWidget(btn)
        
        self.widget2_layout.addStretch()



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
        self.btn_hover_bg_color = self.theme.get('btn_hover_bg_color')

        # Refresh UI
        self.update()
        
        # Apply main widget styling
        self.setStyleSheet(f"""
                background-color: {self.bg_card}; 
                color: {self.text_main};
            """)
    
    # Apply button styling to content frame
        self.content_frame.setStyleSheet(f"""
            QPushButton[class="workspaces"]{{
                background-color: {self.btn_bg_color};
                color: {self.text_main};
                border: 1px solid {self.accent_color};
                padding: 5px;
                border-radius: 3px;
            }}
            
            QPushButton[class="workspaces"]:hover {{
                background-color: {self.btn_hover_bg_color};
                border: 1px solid {self.accent_primary};
            }}
            
            QPushButton[class="workspaces"]:pressed {{
                background-color: {self.accent_primary};
                color: {self.accent_color}
            }}
            QPushButton[class="active_workspaces"] {{
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