import os
import json

def get_json_property(path, preference_name=""):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if preference_name=="":
                return json.load(f)
            return json.load(f).get(preference_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON файл не найден: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в файле {path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла {path}: {e}")
    
    
from PySide6.QtWidgets import (QDialog, QVBoxLayout,
                            QLabel, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt

class colors_is_suitable(QDialog):
    def __init__(self, theme_default, main_font_style, path):
        super().__init__()
        self.setWindowTitle("Проверка контрасности шрифта на фоне")
        self.setFixedSize(1000, 500)
        self.setModal(True)
        self.theme_default = theme_default
        self.main_font_style = main_font_style
        self.path = path

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        label_title = QLabel("Проверка контрасности шрифта на фоне")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(label_title)

        label_text = QLabel(f'Параметр "isDark" в {self.path + "/resources/themes/" + f'{get_json_property("./config/config.json", "theme")}' + ".json"} равен параметру {'\n'} "fontIsDark" в {self.path + "/resources/themes/" + f'{get_json_property("./config/config.json", "fonts")}' + ".json"}, что означает плохую контрасность текста')

        label_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_text.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px;")
        layout.addWidget(label_text)

        example_title = QLabel("вот так будет выглядеть ваш стиль, если он читаем - вы вольны его оставить")
        example_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        example_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px;")
        layout.addWidget(example_title)

        example = QLabel("example example example example example")
        example.setAlignment(Qt.AlignmentFlag.AlignLeft)
        example.setStyleSheet(f'font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px; background:{self.theme_default["bg_card"]}; color:{self.main_font_style["color"]};')
        layout.addWidget(example)

        button_layout = QHBoxLayout()

        reject_btn = QPushButton("поменять")
        reject_btn.clicked.connect(self.reject)
        button_layout.addWidget(reject_btn)

        accept_btn = QPushButton("оставить")
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