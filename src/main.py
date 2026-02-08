import sys
import os
from utils.terms_manager import TermsManager
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
import services.logger as log
import utils.helpers as helpers

class Yarn:
    def __init__(self):
        self.icon_path = os.path.join(helpers.get_project_root(), "resources", "icons", "ico", "Yarn-256.ico")
        self.app = QApplication(sys.argv)
        if os.path.exists(self.icon_path):
            self.app.setWindowIcon(QIcon(self.icon_path))
        self.terms_manager = TermsManager()
        QTimer.singleShot(0, self.check_terms)

    def check_terms(self):
        if not self.terms_manager.search_termsAccepted():
            self.app.quit()
            return
        
        self.launch_main_window()
    
    def launch_main_window(self):
        from app.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
    
    def run(self):
        return self.app.exec()

if __name__ == "__main__":
    log.info('Run application')
    yarn_app = Yarn()
    sys.exit(yarn_app.run())