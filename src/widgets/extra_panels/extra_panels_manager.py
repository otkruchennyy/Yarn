from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Signal
import os
import json
import services.logger as log
import utils.helpers as helpers

class ExtraPanel(QFrame):
    reload_requested = Signal()
    def __init__(self, parent=None, theme=None):
        super().__init__(parent)
        self.base_path = helpers.get_project_root()
        self.theme = theme
        self.extra_panels_config_path = os.path.join(self.base_path, "config", "extra_panel.json")
        self.extra_panels_data = self.get_extra_panels_status()
        self.panel_container_layout = QVBoxLayout(self)
        self.isOpen = self.extra_panels_data["isOpen"]
        self.setFrameShape(QFrame.StyledPanel)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #000000; border: 2px solid red;")
        self.reload_widget()
        self.setFixedHeight(200)
        self.setMouseTracking(True)
        self.apply_theme()
        if not self.isOpen: self.hide()
        else: self.show()

    def reload_widget(self):
        self.extra_panels_data = self.get_extra_panels_status()
        self.isOpen = self.extra_panels_data["isOpen"]
        if self.isOpen:
            self.show()
            self.load_extra_panels(self.extra_panels_data, self.isOpen)
        else:
            self.hide()

    def get_extra_panels_status(self):
        try:
            with open(self.extra_panels_config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            log.error(f'Extra panels not found, but now created in file "{self.extra_panels_config_path}"')
            data = {
                "isOpen": False,
                "logs": False
            }
            with open(self.extra_panels_config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except:
            log.error('Extra panels are not loading')
            return {"isOpen": False}
        return data
    
    def load_extra_panels(self, extra_panels_data, isOpen):
        if isOpen is True:
            self.panel_container_layout.addStretch()
        else:
            pass # TODO: Hide widget if it was previously open
    
    def ensure_single_active_button(self):
        """Ensures only one button is active, returns its name or empty string"""
        extra_panels_data = self.get_extra_panels_status()
        isOpen = extra_panels_data["isOpen"]
        active_button = ''
        
        for name in extra_panels_data:
            if name == "isOpen": 
                continue
            
            is_active = extra_panels_data[name] == True
            if is_active:
                active_button = name
            extra_panels_data[name] = is_active
        
        helpers.save_config(self.extra_panels_config_path, extra_panels_data)

        return active_button
    
    def set_active_button(self, button_name):
        """Set only specified button as active, others to False (skip 'isOpen')"""
        self.extra_panels_data = self.get_extra_panels_status()
        
        for name in self.extra_panels_data:
            if name == "isOpen":
                continue
            
            self.extra_panels_data[name] = (name == button_name)
        
        helpers.save_config(self.extra_panels_config_path, self.extra_panels_data)
    
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
        self.accent_light = self.theme.get('accent_light')
        self.accent_gray = self.theme.get('accent_gray')
        self.text_muted = self.theme.get('text_muted')
        # Refresh UI
        self.update()

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.bg_card};
                border: 1px solid {self.accent_gray};
                border-width: 0px 1px 1px 1px
            }}
        """)
    def close(self):
        self.hide()