import sys
import os
from utils.terms_manager import TermsManager
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

class Yarn:
    def __init__(self):
        self.app = QApplication(sys.argv)
        # print("Запуск приложения...")
        self.terms_manager = TermsManager()
        QTimer.singleShot(0, self.check_terms)

    def check_terms(self):
        # print("Проверяем лицензию...")
        if not self.terms_manager.search_termsAccepted():
            # print("Лицензия не принята, закрываем приложение")
            self.app.quit()
            return
        
        # print("Лицензия принята, открываем главное окно")
        self.launch_main_window()
    
    def launch_main_window(self):
        from app.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
    
    def run(self):
        return self.app.exec()

if __name__ == "__main__":
    yarn_app = Yarn()
    sys.exit(yarn_app.run())