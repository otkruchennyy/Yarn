import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy, QScrollArea, QMessageBox
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics
import utils.helpers as helpers

class tabs(QWidget):
    """Tab manager"""
    def __init__(self, theme=None, parent=None):
        super().__init__(parent)
        self.bg_color = None
        self.theme = theme
        self.path_tabs = os.path.join(helpers.get_project_root(), "config", "tabs_config.json")
        self.setup_ui()
        self.apply_theme()
        self.scroll_area.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.scroll_area and event.type() == QEvent.Wheel:
            scroll_bar = self.scroll_area.horizontalScrollBar()
            delta = event.angleDelta().y()
            scroll_bar.setValue(scroll_bar.value() - delta)
            return True
        return super().eventFilter(obj, event)

    def setup_ui(self):
        self.property_tabs = helpers.get_json_property(self.path_tabs)
        self.count_tabs = len(self.property_tabs)
        self.setObjectName("tabs")
        layout = QHBoxLayout(self)
        self.setFixedHeight(25)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.add_tab_btn = QPushButton("+")
        self.add_tab_btn.setFixedSize(50, 18)
        self.add_tab_btn.setCursor(Qt.PointingHandCursor)
        self.add_tab_btn.setProperty("class", "add_btn")
        self.add_tab_btn.setFont(QFont("Monospace", 10))
        self.add_tab_btn.setToolTip("Add tab")
        self.add_tab_btn.clicked.connect(self.on_add_tab_clicked)
        layout.addWidget(self.add_tab_btn)
        
        self.tabs_container = QWidget()
        self.tabs_layout = QHBoxLayout(self.tabs_container)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(0)
        self.tabs_layout.setAlignment(Qt.AlignLeft)
        self.tabs_width = 0
        self.tabs = {}

        self.add_tab()
        
        self.tabs_container.setFixedSize(self.tabs_width + 30, 20)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFixedHeight(23)
        self.scroll_area.setWidget(self.tabs_container)

        self.scroll_area.setWidgetResizable(False)
        
        layout.addWidget(self.scroll_area)

    def on_add_tab_clicked(self):
        # TODO: load file
        file_name, directory = helpers.open_file_dialog(self)
        helpers.add_json_property(self.path_tabs, file_name, directory)
        self.reload_tabs()

    def check_file_access(self, path):
        """except file load"""
        except_msg = (f"File exists: {os.path.exists(path)}\n")
        except_msg += (f"Readable: {os.access(path, os.R_OK)}\n")
        except_msg += (f"Writable: {os.access(path, os.W_OK)}\n")
        except_msg += (f"Executable: {os.access(path, os.X_OK)}")

        return except_msg
    
    def on_tab_clicked(self, path):
        """Load the file into the editor when clicking on the tab"""
        if os.access(path, os.R_OK):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # TODO: Transfer the content to the editor
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Read Error", 
                    f"Cannot read file: {path}\nError: {e}"
                ) # TODO: realisation in main window
        else:
            QMessageBox.critical(
                self,
                "Read Access Denied",
                f"No read permission: {path}\n-------\n{self.check_file_access(path)}"
            ) # TODO: realisation in main window

    def on_remove_tab_clicked(self, name):
        # add: save file
        helpers.remove_json_property(self.path_tabs, name)
        self.reload_tabs()
        

    def reload_tabs(self):
        for i in reversed(range(self.tabs_layout.count())):
            widget = self.tabs_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.tabs.clear()
        self.tabs_width = 0
        self.property_tabs = helpers.get_json_property(self.path_tabs)
        self.count_tabs = len(self.property_tabs)
        
        self.add_tab()
        
        self.tabs_container.setMinimumWidth(self.tabs_width)
        
        # TODO: reload tabs_width
    
    def add_tab(self):
        font = QFont("Monospace", 10)
        metrics = QFontMetrics(font)
        
        for i in range(self.count_tabs):
            name = list(self.property_tabs.keys())[i]
            
            text_width = int(metrics.horizontalAdvance(name) * 1.25)
            btn_width = text_width
            
            tab_widget = QWidget()
            tab_widget.setProperty("class", "tab_widget")
            tab_widget.setStyleSheet("margin-right: 10px;")
            tabs_layout = QHBoxLayout(tab_widget)
            tabs_layout.setAlignment(Qt.AlignLeft)
            tabs_layout.setContentsMargins(0, 0, 0, 0)
            
            btn = QPushButton(name)
            btn.setFixedSize(btn_width, 18)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("class", "tab")
            btn.setFont(font)
            btn.setToolTip(f'{self.property_tabs[name]}')
            btn.setStyleSheet("margin: 0px; padding: 0px;")
            btn.clicked.connect(lambda checked, n=name: self.on_tab_clicked(self.property_tabs[n])) 
            
            btn_remove = QPushButton('x')
            btn_remove.setFixedSize(20, 18)
            btn_remove.setCursor(Qt.PointingHandCursor)
            btn_remove.setProperty("class", "tab")
            btn_remove.setFont(QFont("Monospace", 10))
            btn_remove.setStyleSheet("margin: 0px; padding: 0px;")
            btn_remove.clicked.connect(lambda checked, n=name: self.on_remove_tab_clicked(n))
            
            tabs_layout.addWidget(btn)
            tabs_layout.addWidget(btn_remove)
            
            tab_width = btn_width + 40
            self.tabs_width += tab_width
            
            tab_widget.setFixedSize(tab_width, 20)
            
            self.tabs_layout.addWidget(tab_widget)
            
            self.tabs[name] = {'container': tab_widget, 'btn': btn, 'btn_remove': btn_remove}
    
    def apply_theme(self):
        self.bg_card = self.theme.get('bg_card')
        self.bg_color = self.theme.get('bg_color')
        self.accent_color = self.theme.get('accent_color')
        self.accent_primary =  self.theme.get('accent_primary')
        self.text_main = self.theme.get('text_main')
        self.btn_bg_color = self.theme.get('btn_bg_color')
        self.btn_hover_bg_color = self.theme.get('btn_hover_bg_color')

        self.update()        
        self.setStyleSheet(f"""
            QPushButton[class="add_btn"] {{
                background-color: {self.btn_bg_color};
                color: {self.text_main};
                border: 1px solid {self.accent_color};
                margin: 0px 5px;
                border-radius: 3px;
            }}
            
            QPushButton[class="add_btn"]:hover {{
                background-color: {self.btn_hover_bg_color};
                border: 1px solid {self.accent_primary};
            }}
            
            QPushButton[class="add_btn"]:pressed {{
                background-color: {self.accent_primary};
                color: {self.accent_color}
            }}
            QPushButton[class="tab"] {{
                background-color: transparent;
                color: {self.text_main};
                border-radius: 3px;
                font-weight: 600;
            }}
            QWidget[class="tab_widget"] {{
                background-color: {self.btn_bg_color};
                border-radius: 3px;
                padding: 0px 10px;
                border-radius: 3px;
            }}
            QWidget[class="tab_widget"]:hover {{
                border: 1px solid #fff;
            }}
            QToolTip {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
            }}
        """)
        
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollArea::viewport {{
                background: {self.bg_card};
            }}
            QScrollBar:horizontal {{
                background: white;
                border: none;
                height: 3px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.accent_color};
            }}
            QScrollBar::add-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)
    
    def paintEvent(self, event):
        if self.bg_color and self.accent_color:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(self.bg_color))

            painter.setPen(QColor(self.accent_color))
            painter.drawLine(0, 0, self.width(), 0)
            
            painter.drawLine(0, self.height()-1, self.width(), self.height()-1)
            from PySide6.QtGui import QPalette

            palette = self.tabs_container.palette()
            palette.setColor(QPalette.Window, QColor(self.bg_color))
            self.tabs_container.setPalette(palette)
            self.tabs_container.setAutoFillBackground(True)
        super().paintEvent(event)