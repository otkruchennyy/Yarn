import os
import sys
import json
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog)
from PySide6.QtCore import Qt
import services.logger as log

"""The script is primarily for manipulating JSON files. Its functions are widely used"""

def load_theme():
    config_path = os.path.join(get_project_root(), 'config', 'config.json')
    themes_path =os.path.join(get_project_root(), 'resources', 'themes')
    theme_name = get_json_property(config_path, "theme") or "default"
    theme_file = os.path.join(themes_path, f"{theme_name}.json")
    
    log.debug(f'Selected theme: {theme_name}')
     # TODO: make debug on get_json_property()
    return get_json_property(theme_file) or get_fallback_theme()

def get_fallback_theme():
    return {
        "isDark": True,
        "bg_color": "#111111", 
        "bg_card": "#121212", 
        "accent_color": "202020",
        "accent_primary": "#FFB300",
        "btn_bg_color": "#202020",
        "accent_gray": "#292929",
        "accent_light": "#7a7a7a",
        "text_main": "#e0e0e0",
        "text_muted": "#a0a0a0"
    }

def open_file_dialog(self):
    """Function needed to display error dialogs"""
    file_path, _ = QFileDialog.getOpenFileName(
        self, 
        "Select File",
        "",
        "All Files (*)"
    )
    
    if file_path:
        file_name = os.path.basename(file_path)
        directory = os.path.dirname(file_path) + '/' + file_name
        
        return file_name, directory
    return None, None

def get_project_root():
    """Returns the project root folder"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_json_property(path, preference_name=""):
    """Returns values from JSON file:

    - If "preference_name" specified, returns only that key's value
    - Otherwise returns a list"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if preference_name == "":
                return json.load(f)
            return json.load(f).get(preference_name)
    except FileNotFoundError:
        log.debug(msg=f"JSON file not found: {path}")
    except json.JSONDecodeError as e:
        log.debug(msg=f"JSON parsing error in file {path}: {e}")
    except Exception as e:
        log.debug(msg=f"Error reading file {path}: {e}")
    
def replace_json_content(path_from, path_to):
    """Completely replaces contents of one JSON file with another JSON file"""
    try:
        if not os.path.exists(path_from):
            return 'error: Source file not found'
        
        with open(path_from, 'r', encoding='utf-8') as source_file:
            data_to_copy = json.load(source_file)
        
        with open(path_to, 'w', encoding='utf-8') as target_file:
            json.dump(data_to_copy, target_file, indent=2, ensure_ascii=False)
        
        return 'success'
    
    except FileNotFoundError:
        return 'error: JSON file not found'
    except json.JSONDecodeError as e:
        return f'error: JSON parsing error: {e}'
    except Exception as e:
        return f'error: File operation error: {e}'
    
def add_json_property(path, property, value):
    """If "property" already exists in JSON file, replaces its value; otherwise adds "property": "value" to dictionary"""
    try:
        if not property or not isinstance(property, str):
            return 'invalid_key_name'
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data[property] = value

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return 'success'

    except FileNotFoundError:
        return 'error: JSON file not found'
    except json.JSONDecodeError as e:
        return f'error: JSON parsing error: {e}'
    except Exception as e:
        return f'error: File operation error: {e}'
    
def remove_json_property(path, property):
    """Deletes key and its corresponding value from JSON file"""
    # TODO: Clean up unused tab paths after removal
    try:
        if not property or not isinstance(property, str):
            return 'invalid_key_name'

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if property in data:
            del data[property]
        else:
            return 'property_not_found'
        
        for j in list(data.keys()):
            count = 0
            if f'{property[property.find("/") + 1:]}' in j:
                count += 1

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return 'success'

    except FileNotFoundError:
        return 'error: JSON file not found'
    except json.JSONDecodeError as e:
        return f'error: JSON parsing error: {e}'
    except Exception as e:
        return f'error: File operation error: {e}'

def save_config(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except FileNotFoundError:
        log.error(f'file not found "{path}"')
    except Exception as e:
        log.error(f'file not found. eroor: "{e}"')
    
def get_files_from_directory(folder_path, endswith=None):
    """Returns files from directory. If endswith provided, filters by file extension"""
    current_files = {}
    
    if not os.path.exists(folder_path):
        return current_files
    
    if endswith and not endswith.startswith('.'):
        endswith = '.' + endswith
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            name_without_extension = os.path.splitext(filename)[0]
            
            if endswith:
                if filename.endswith(endswith):
                    current_files[name_without_extension] = file_path
            else:
                current_files[name_without_extension] = file_path
    
    return current_files

class ColorContrastCheckDialog(QDialog):
    """A dialog window that appears only when the font lacks contrast against the background"""
    def __init__(self, theme_default, main_font_style, base_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Font Color Contrast Check")
        self.setFixedSize(1000, 500)
        self.setModal(True)
        self.theme_default = theme_default
        self.main_font_style = main_font_style
        self.base_path = base_path

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        label_title = QLabel("Font Color Contrast Check")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(label_title)

        config_path = os.path.join(self.base_path, 'config', 'config.json')
        theme_name = get_json_property(config_path, "theme") or "default"
        fonts_name = get_json_property(config_path, "fonts") or "default"

        theme_file_path = os.path.join(self.base_path, "resources", "themes", f"{theme_name}.json")
        fonts_file_path = os.path.join(self.base_path, "resources", "fonts", f"{fonts_name}.json")

        label_text = QLabel(
            f'The "isDark" parameter in {theme_file_path} equals the\n'
            f'"fontIsDark" parameter in {fonts_file_path}, indicating poor text contrast'
        )

        label_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_text.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px;")
        layout.addWidget(label_text)

        example_title = QLabel("This is how your style will look. If it's readable - you can keep it")
        example_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        example_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px;")
        layout.addWidget(example_title)

        example = QLabel("example example example example example")
        example.setAlignment(Qt.AlignmentFlag.AlignLeft)
        example.setStyleSheet(f'font-size: 16px; font-weight: bold; padding: 10px, 2px; margin: 20px; background:{self.theme_default["bg_card"]}; color:{self.main_font_style["color"]};')
        layout.addWidget(example)

        button_layout = QHBoxLayout()

        reject_btn = QPushButton("Change")
        reject_btn.clicked.connect(self.reject)
        button_layout.addWidget(reject_btn)

        accept_btn = QPushButton("Keep")
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