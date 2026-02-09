import json
import os
import utils.helpers as helpers
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout)
from PySide6.QtCore import Qt

class TermsManager:
    def __init__(self):
        self.base_path = helpers.get_project_root()
        self.config_path = os.path.join(self.base_path, "config", "config.json")
        self._ensure_config_exists()
        self.config_data = helpers.get_json_property(f'{self.config_path}')

        if self.config_data is None:
            self.config_data = { "termsAccepted": false, "theme": "dark_theme", "fonts": "basic_fonts", "current_workspaces": "work", "lang": "rus"}

    def search_termsAccepted(self):
        if self.config_data.get("termsAccepted") == True:
            return True
        else:
            return self.show_terms_dialog()

    def show_terms_dialog(self):
        dialog = TermsDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.config_data["termsAccepted"] = True
            self.save_config()
            return True
        
        return False

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, indent=2, ensure_ascii=False)
    
    def _ensure_config_exists(self):
        """Создаёт config.json с дефолтными значениями, если его нет."""
        if not os.path.exists(self.config_path):
            # Создаём папку config если нужно
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            default_config = {
                "termsAccepted": False,
                "theme": "dark_theme",
                "fonts": "basic_fonts",
                "current_workspaces": [],
                "lang": "eng"
            }
            
            try:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                print(f"Created default config at {self.config_path}")
            except Exception as e:
                print(f"Failed to create config: {e}")
                # Можно создать минимальный конфиг в оперативке
                self.config_data = default_config.copy()
        else:
            # Проверяем что есть обязательное поле termsAccepted
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
                
                if "termsAccepted" not in existing_config:
                    existing_config["termsAccepted"] = False
                    with open(self.config_path, 'w', encoding='utf-8') as f:
                        json.dump(existing_config, f, indent=2, ensure_ascii=False)
            except (json.JSONDecodeError, IOError):
                # Если файл битый - пересоздаём
                self._recreate_config()
    
    def _recreate_config(self):
        """Пересоздаёт config.json при повреждении."""
        backup_path = f"{self.config_path}.bak"
        try:
            os.rename(self.config_path, backup_path)
        except OSError:
            pass
            
        default_config = {
            "termsAccepted": False,
            "theme": "dark_theme",
            "fonts": "basic_fonts",
            "current_workspaces": [],
            "lang": "en"
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print(f"Recreated config (backup at {backup_path})")


class TermsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("License Agreement MIT")
        self.setFixedSize(500, 500)
        self.setModal(True)
        self.base_path = helpers.get_project_root()
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)

        label_title = QLabel("License Agreement MIT")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(label_title)

        license_text = self.load_license_text()
        text_edit = QTextEdit()
        text_edit.setPlainText(license_text)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 10px;
                font-family:'Arial', 'Courier New', monospace;
            }
        """)
        layout.addWidget(text_edit)

        button_layout = QHBoxLayout()
        
        reject_btn = QPushButton("I Disagree")
        reject_btn.clicked.connect(self.reject)
        button_layout.addWidget(reject_btn)

        accept_btn = QPushButton("I Agree")
        accept_btn.clicked.connect(self.accept)
        button_layout.addWidget(accept_btn)

        layout.addLayout(button_layout)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                padding: 10px;
            }
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                padding: 10px 15px;
                font-size: 14px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #99d2ff;
            }
            QPushButton:pressed {
                background-color: #66bcff;
            }
            QPushButton:focus {
                outline: 1px solid #fff;
            }
        """)

    def load_license_text(self):
        try:
            license_path = os.path.join(self.base_path, "LICENSE.txt")
            with open(license_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return """MIT License

Copyright (c) 2025 tsukagahara

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""