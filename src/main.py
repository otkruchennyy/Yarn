"""
Yarn - Lightweight Text Editor
Main application entry point and orchestration.

Handles:
- Application initialization and lifecycle
- License agreement verification
- Main window creation
- System metrics collection service management
"""

import sys
import os
from utils.terms_manager import TermsManager
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
import services.logger as log
import utils.helpers as helpers
from services.metrics_collector import MetricsCollector


class Yarn:
    """
    Main application controller.
    
    Responsibilities:
    - Initialize Qt application and set up global properties
    - Manage application lifecycle (startup, shutdown)
    - Coordinate between different services (metrics, UI, licensing)
    - Handle cross-cutting concerns (logging, configuration)
    """
    
    def __init__(self):
        """
        Initialize the Yarn application.
        
        Steps:
        1. Set up application icon
        2. Create Qt application instance
        3. Initialize terms manager for license agreement
        4. Schedule initial terms check
        """
        self.icon_path = os.path.join(
            helpers.get_project_root(), 
            "resources", "icons", "ico", "Yarn-256.ico"
        )
        self.app = QApplication(sys.argv)
        
        if os.path.exists(self.icon_path):
            self.app.setWindowIcon(QIcon(self.icon_path))
            
        self.terms_manager = TermsManager()
        # Schedule terms check to run after event loop starts
        QTimer.singleShot(0, self.check_terms)
    
    def check_terms(self):
        """
        Verify user has accepted license terms.
        
        If terms are not accepted:
        - Application quits immediately
        - No windows are created
        
        If terms are accepted:
        - Proceeds to launch main window
        """
        if not self.terms_manager.search_termsAccepted():
            self.app.quit()
            return
        
        self.launch_main_window()
    
    def launch_main_window(self):
        """
        Create and display the main application window.
        
        Steps:
        1. Import and instantiate MainWindow (lazy import to reduce startup time)
        2. Start metrics collection service
        3. Connect cleanup signals
        """
        from app.main_window import MainWindow
        
        self.main_window = MainWindow()
        self.main_window.show()
        
        self.start_metrics_collection()
        # Ensure metrics are stopped when application quits
        self.app.aboutToQuit.connect(self.stop_metrics_collection)
    
    def run(self):
        """
        Execute the main application event loop.
        
        Returns:
            int: Application exit code
            
        Ensures:
            - Metrics collection is stopped even on crash
            - Critical errors are logged before exit
        """
        try:
            return self.app.exec()
        except Exception as e:
            log.critical(f"Application crashed: {e}")
            raise
        finally:
            # Safety cleanup in case normal shutdown fails
            self.stop_metrics_collection()
    
    def start_metrics_collection(self):
        """
        Start the system metrics collection service.
        
        The service runs in a separate thread and emits
        metrics_updated signals with system resource usage data.
        """
        self.metrics_collector = MetricsCollector(update_interval=1000)
        self.metrics_collector.metrics_updated.connect(self.on_metrics_updated)
        self.metrics_collector.start()
        log.info(msg="Metrics collection started")
    
    def on_metrics_updated(self, metrics):
        """
        Handle incoming metrics data from collection service.
        
        Args:
            metrics (dict): Dictionary containing CPU, memory, and system metrics
            
        Forwards metrics to main window if it's ready to receive them.
        Otherwise, metrics are dropped (window may be initializing or closing).
        """
        if self.main_window and hasattr(self.main_window, 'update_metrics'):
            self.main_window.update_metrics(metrics)
        # Metrics are intentionally not logged here to avoid console spam
        # during normal operation. Debug logging is handled in the collector.
    
    def stop_metrics_collection(self):
        """
        Stop and clean up the metrics collection service.
        
        Ensures:
            - Thread is properly stopped
            - Resources are released
            - No dangling threads remain after application exit
        """
        if hasattr(self, 'metrics_collector') and self.metrics_collector:
            self.metrics_collector.stop()
            self.metrics_collector.wait()
            self.metrics_collector = None
            log.info(msg="Metrics collection stopped")


if __name__ == "__main__":
    """
    Application entry point.
    
    Creates the Yarn application instance and starts the event loop.
    Exit code is propagated to the operating system.
    """
    log.info('Starting Yarn application')
    yarn_app = Yarn()
    sys.exit(yarn_app.run())