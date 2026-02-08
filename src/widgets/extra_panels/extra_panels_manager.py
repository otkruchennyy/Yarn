from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QTabWidget, QTextEdit
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
import os
import json
import services.logger as log
import utils.helpers as helpers
import widgets.extra_panels.extra_tabs.logs as lp

class ExtraPanel(QFrame):
    reload_requested = Signal()
    def __init__(self, parent=None, theme=None, lang=None):
        super().__init__(parent)
        self.base_path = helpers.get_project_root()
        self.theme = theme
        self.lang = lang
        self.extra_panels_config_path = os.path.join(self.base_path, "config", "extra_panel.json")
        self.extra_panels_data = self.get_extra_panels_status()
        self.isOpen = self.extra_panels_data["isOpen"]
        self.active_tab = self.get_active_tab()
        self.setup_ui()
        self.apply_theme()
        if not self.isOpen: self.hide()
        else: self.show()
        log.debug(msg=f'Currently active tab in extra panels is "{self.active_tab}"')

    def reload_widget(self):
        self.extra_panels_data = self.get_extra_panels_status()
        self.isOpen = self.extra_panels_data["isOpen"]
        if self.isOpen:
            self.show()
            self.active_tab = self.get_active_tab()
            self.set_initial_tab()
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
                json.dump(data, f, ensure_ascii=False, indent=2)
                log.warning(msg='File "extra_panels.json" successfully created')
        except:
            log.error('Extra panels are not loading')
            return {"isOpen": False}
        return data
    
    def load_extra_panels(self, extra_panels_data, isOpen):
        if isOpen is True:
            self.active_tab = self.get_active_tab()
            self.set_initial_tab()
    
    def get_active_tab(self):
        for tab_name in self.extra_panels_data:
            if tab_name == "isOpen":
                continue
            else:
                if self.extra_panels_data[tab_name] == False:
                    continue
                else: return tab_name
        return 'log'
    
    def setup_ui(self):
        """Initialize UI components and layout"""
        # Create main layout
        self.panel_container_layout = QVBoxLayout(self)
        self.panel_container_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_container_layout.setSpacing(0)
        
        # Set frame properties
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(400)
        self.setMouseTracking(True)
        
        # Create tab container (QTabWidget for different panels)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # Create tab pages
        self.logs_tab = lp.LogsPanel(self.base_path, self.theme, lang=self.lang)

        self.stats_tab = QWidget()

        self.info_tab = QWidget()
        
        # Add tabs to tab widget
        
        self.tab_widget.addTab(self.logs_tab, f"{self.lang["Logs"]}")
        self.tab_widget.addTab(self.stats_tab, f"{self.lang["Stats"]}")
        self.tab_widget.addTab(self.info_tab, f"{self.lang["Info"]}")
        
        # Add tab widget to main layout
        self.panel_container_layout.addWidget(self.tab_widget)
        
        # Set initial tab based on config
        self.set_initial_tab()
    
    def set_initial_tab(self):
        """Set the active tab based on configuration"""
        if self.active_tab == "logs":
            self.tab_widget.setCurrentIndex(0)
            log.debug(msg='Logs panel open in extra panels')
        elif self.active_tab == "stats":
            self.tab_widget.setCurrentIndex(1)
            log.debug(msg='Stats panel open in extra panels')
        elif self.active_tab == "info":
            self.tab_widget.setCurrentIndex(2)
            log.debug(msg='Info panel open in extra panels')
    
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
                border-width: 0px 0px 0px 1px;
            }}
            
            /* Tab widget styling - only the tab bar */
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            
            QTabBar::tab {{
                background-color: {self.btn_bg_color};
                color: {self.text_muted};
                padding: 2px 12px;
                margin-right: 2px;
                border-radius: 4px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {self.accent_color};
                color: white;
                font-weight: bold;
            }}
            
            QTabBar::tab:hover {{
                background-color: {self.accent_light};
            }}
        """)
    def close(self):
        self.hide()