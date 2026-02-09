"""
Extra panels container widget with tabbed interface.

Manages:
- Logs panel (system and application logging)
- Statistics panel (real-time system metrics)
- Info panel (document metadata and statistics)
- Dynamic tab switching based on configuration
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QTabWidget
from PySide6.QtCore import Signal, Qt
import os
import json
import services.logger as log
import utils.helpers as helpers
import widgets.extra_panels.extra_tabs.logs as lp
import widgets.extra_panels.extra_tabs.stat as sp
import widgets.extra_panels.extra_tabs.info as ip


class ExtraPanel(QFrame):
    """
    Tabbed container for auxiliary panels below the text editor.
    
    Attributes:
        metrics_updated (Signal[dict]): Forwards system metrics to statistics panel
        reload_requested (Signal): Triggers UI refresh from external components
        stat_panel (StatPanel): Reference to statistics panel for metric forwarding
    """
    
    metrics_updated = Signal(dict)
    reload_requested = Signal()
    
    def __init__(self, parent=None, theme=None, lang=None):
        """
        Initialize extra panels container.
        
        Args:
            parent: Parent widget
            theme: Color theme dictionary
            lang: Language configuration dictionary or string
        
        Initialization flow:
            1. Load panel configuration from JSON
            2. Set up signal connections
            3. Build UI components
            4. Apply theme styling
        """
        super().__init__(parent)
        self.base_path = helpers.get_project_root()
        self.theme = theme
        self.lang = lang
        
        # Configuration paths and data
        self.extra_panels_config_path = os.path.join(
            self.base_path, "config", "extra_panel.json"
        )
        self.extra_panels_data = self.get_extra_panels_status()
        self.isOpen = self.extra_panels_data["isOpen"]
        self.active_tab = self.get_active_tab()
        
        # Metrics forwarding setup
        self.metrics_updated.connect(self._forward_metrics)
        self.stat_panel = None  # Will be set in setup_ui
        
        # UI initialization
        self.setup_ui()
        self.apply_theme()
        
        # Initial visibility based on config
        if not self.isOpen:
            self.hide()
        else:
            self.show()
        
        log.debug(
            msg=f'Currently active tab in extra panels is "{self.active_tab}"'
        )
    
    def _forward_metrics(self, metrics):
        """
        Route incoming metrics to the statistics panel.
        
        Args:
            metrics (dict): System resource usage data from MetricsCollector
        
        Note:
            If statistics panel is not loaded, metrics are logged at debug level.
        """
        if self.stat_panel and hasattr(self.stat_panel, 'update_metrics'):
            self.stat_panel.update_metrics(metrics)
        else:
            log.debug(msg="StatPanel not found or missing update_metrics method")
    
    def reload_widget(self):
        """
        Reload panel configuration and update UI state.
        
        Triggered by:
            - Configuration file changes
            - Manual refresh requests
            - Theme/language updates
        """
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
        """
        Load panel configuration from JSON file.
        
        Returns:
            dict: Configuration data with panel states
            
        Creates default configuration file if none exists.
        """
        try:
            with open(self.extra_panels_config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            log.error(
                f'Extra panels config not found, creating: "{self.extra_panels_config_path}"'
            )
            data = {
                "isOpen": False,
                "logs": False
            }
            with open(self.extra_panels_config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                log.warning(msg='File "extra_panels.json" successfully created')
        except Exception:
            log.error('Failed to load extra panels configuration')
            return {"isOpen": False}
        return data
    
    def load_extra_panels(self, extra_panels_data, isOpen):
        """
        Apply loaded configuration to UI.
        
        Args:
            extra_panels_data (dict): Configuration dictionary
            isOpen (bool): Whether panels should be visible
        """
        if isOpen is True:
            self.active_tab = self.get_active_tab()
            self.set_initial_tab()
    
    def get_active_tab(self):
        """
        Determine which tab should be active based on configuration.
        
        Returns:
            str: Tab identifier ('logs', 'stats', 'info', or 'log' as default)
        """
        for tab_name in self.extra_panels_data:
            if tab_name == "isOpen":
                continue
            if self.extra_panels_data[tab_name] is True:
                return tab_name
        return 'log'  # Default tab
    
    def setup_ui(self):
        """
        Construct the tabbed panel interface.
        
        Creates three panels:
            1. LogsPanel: Application and system log viewer
            2. StatPanel: Real-time system metrics visualization
            3. InfoPanel: Document metadata and statistics
        """
        # Main container layout
        self.panel_container_layout = QVBoxLayout(self)
        self.panel_container_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_container_layout.setSpacing(0)
        
        # Frame properties
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(400)
        self.setMouseTracking(True)
        
        # Tab widget for panel switching
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # Create individual panels
        self.logs_tab = lp.LogsPanel(self.base_path, self.theme, lang=self.lang)
        self.stats_tab = sp.StatPanel(self.base_path, self.theme, lang=self.lang)
        self.info_tab = ip.InfoPanel(self.base_path, self.theme, lang=self.lang)
        
        # Store reference for metrics forwarding
        self.stat_panel = self.stats_tab
        
        # Add tabs with localized names
        self.tab_widget.addTab(self.logs_tab, f"{self.lang['Logs']}")
        self.tab_widget.addTab(self.stats_tab, f"{self.lang['Stats']}")
        self.tab_widget.addTab(self.info_tab, f"{self.lang['Info']}")
        
        # Assemble UI
        self.panel_container_layout.addWidget(self.tab_widget)
        self.set_initial_tab()
    
    def set_initial_tab(self):
        """
        Activate the tab specified in configuration.
        
        Logs panel state changes for debugging purposes.
        """
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
        Apply color theme using CSS stylesheets.
        
        Colors extracted from theme dictionary:
            - bg_card: Panel background
            - accent_*: Interactive element colors
            - text_*: Text colors for different states
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

        # Apply CSS styles
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
                color: {self.bg_card};
            }}
        """)
    
    def close(self):
        """Hide the extra panels (soft close preserving state)."""
        self.hide()