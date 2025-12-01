from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import os
import utils.helpers as helpers

class WorkspacesPanel(QWidget):
    def __init__(self, base_path, tabs_manager, theme):
        super().__init__()
        self.theme = theme
        self.base_path = base_path
        self.tabs = tabs_manager
        self.workspaces_widgets = {}
        self.workspaces_path = os.path.join(self.base_path, "config", "workspaces")
        self.workspaces = helpers.get_files_from_directory(self.workspaces_path, 'json')
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.load_workspaces()

    def load_workspaces(self):
        """Loading workspaces"""
        font = QFont("Segoe UI", 10) # TODO: current font

        name_property = QLabel("workspaces")
        self.layout.addWidget(name_property)
        self.workspaces_widgets["name_property"] = name_property

        for name in self.workspaces:
            btn = QPushButton(name)
            btn.setFixedSize(200, 30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(font)
            btn.setToolTip(f'{self.workspaces[name]}')
            btn.setStyleSheet("margin: 2px; padding: 0px;")
            btn.clicked.connect(lambda checked, n=name: self.on_workspaces_clicked(self.workspaces[n], n))
            
            # set button style
            current_workspace = helpers.get_json_property(
                os.path.join(self.base_path, "config", "config.json"), 
                "current_workspaces"
            )
            if name == current_workspace:
                btn.setProperty("class", "active_workspaces")
            else:
                btn.setProperty("class", "workspaces")
            
            self.workspaces_widgets[name] = btn
            self.layout.addWidget(btn)
        
        self.layout.addStretch()

    def on_workspaces_clicked(self, path, name_btn):
        """Workspace click handler"""
        current_workspaces = helpers.get_json_property(
            os.path.join(self.base_path, "config", "config.json"), 
            "current_workspaces"
        )
        value = (path.split('\\')[-1])[:-5]
        
        if current_workspaces == value: 
            return
            
        if os.access(path, os.R_OK):
            # Save config
            helpers.replace_json_content(
                os.path.join(self.base_path, "config", "tabs_config.json"),
                os.path.join(self.base_path, "config", "workspaces", current_workspaces + '.json')
            )
            
            # Reload сurrent workspace
            helpers.add_json_property(
                os.path.join(self.base_path, "config", "config.json"), 
                "current_workspaces", 
                value
            )

            # Load new config
            helpers.replace_json_content(
                os.path.join(self.base_path, "config", "workspaces", value + '.json'),
                os.path.join(self.base_path, "config", "tabs_config.json")
            )
            
            # Reload tabs
            if self.tabs:
                self.tabs.reload_tabs()

            # Reload panel
            self.reload_workspaces()

    def reload_workspaces(self):
        """Reload panel workspaces"""
        # Delite all widgets
        for widget in self.workspaces_widgets.values():
            widget.deleteLater()
        self.workspaces_widgets.clear()
        
        # Cleaning layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Reload
        self.load_workspaces()

    def show_panel(self):
        self.show()

    def hide_panel(self):
        self.hide()

    def toggle_panel(self):
        """Toggle panel visibility"""
        self.setVisible(not self.isVisible())
    
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

        # Refresh UI
        self.update()
        
        # Apply main widget styling
        self.setStyleSheet(f"""
                background-color: {self.bg_card}; 
                color: {self.text_main};
            """)
    
        # Apply button styling to content frame
        self.setStyleSheet(f"""
            QPushButton[class="workspaces"]{{
                background-color: {self.btn_bg_color};
                color: {self.text_muted};
                padding: 5px;
                border-radius: 3px;
            }}
            
            QPushButton[class="workspaces"]:hover {{
                color: {self.text_muted};
            }}
            
            QPushButton[class="workspaces"]:pressed {{
                background-color: {self.accent_gray};
                color: {self.text_muted};
            }}
            QPushButton[class="active_workspaces"] {{
                background-color: {self.bg_card};
                border: 1px solid {self.accent_light};
                color: {self.text_main};
            }}
            QToolTip {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
            }}
            """)