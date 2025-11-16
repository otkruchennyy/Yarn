import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QColor, QPixmap
import utils.helpers as helpers

class CustomHeader(QWidget):
    def __init__(self, theme=None, parent=None):
        super().__init__(parent)
        self.bg_color = None
        self.dragging = False
        self.theme = theme
        self.logo_img_path = os.path.join(helpers.get_project_root(), "resources", "icons", "png", "Yarn-32.png")
        self.setup_ui()
        self.apply_theme()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton and not self.is_in_resize_zone(event.pos()):
                self.dragging = True
                self.drag_position = event.globalPos() - self.window().frameGeometry().topLeft()
                if hasattr(self.window(), 'resize_handler'):
                    self.window().resize_handler.moving = True
                self.grabMouse()
                return True
            return False
            
        elif event.type() == QEvent.MouseMove:
            if self.dragging and event.buttons() == Qt.LeftButton:
                global_pos = event.globalPos()
                screen = self.window().screen().availableGeometry()
                
                if (global_pos.y() <= 5 or 
                    global_pos.x() <= 5 or  
                    global_pos.x() >= screen.width() - 5):
                    
                    local_pos = event.pos()
                    new_x = global_pos.x() - local_pos.x() - self.width() // 2
                    new_y = global_pos.y() - local_pos.y() - self.height() // 2
                    
                    new_x = max(screen.left(), min(new_x, screen.right() - self.window().width()))
                    new_y = max(screen.top(), min(new_y, screen.bottom() - self.window().height()))
                    
                    self.window().move(new_x, new_y)
                else:
                    self.window().move(global_pos - self.drag_position)
                return True
            return False
            
        elif event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self.dragging = False
                if hasattr(self.window(), 'resize_handler'):
                    self.window().resize_handler.moving = False
                self.releaseMouse()
            return False
            
        return super().eventFilter(obj, event)
    
    def is_in_resize_zone(self, pos):
        x, y = pos.x(), pos.y()
        width = self.width()
        return (x <= 5 or x >= width - 5 or y <= 5)
    
    def setup_ui(self):
        self.setObjectName("CustomHeader")
        layout = QHBoxLayout(self)
        self.setFixedHeight(35)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # layout.setContentsMargins(10, 5, 10, 5)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.installEventFilter(self)
        
        self.title_label = QLabel("Yarn")
        self.title_label.setContentsMargins(5, 0, 5, 0)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        

        self.logo_label = QLabel()
        self.logo_label.setContentsMargins(5, 0, 5, 0)
        self.logo_pixmap = QPixmap(self.logo_img_path)
        if not self.logo_pixmap.isNull():
            self.logo_label.setPixmap(self.logo_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            print(self.logo_img_path)
        
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.minimize_btn = QPushButton("_")
        self.minimize_btn.setFixedSize(50, 25)
        self.minimize_btn.setCursor(Qt.PointingHandCursor)

        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(50, 25)
        self.maximize_btn.setCursor(Qt.PointingHandCursor)

        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(50, 25)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)
    
    def apply_theme(self):
        self.bg_color = self.theme.get('bg_card', '#121212')
        text_color = self.theme.get('text_main', '#e0e0e0')
        accent_color = self.theme.get('accent_primary', '#202020')

        self.update()

        self.title_label.setStyleSheet(f"""
            color: {text_color};
            font-weight: bold;
            font-size: 12px;
            background: transparent;
        """)

        self.minimize_btn.setStyleSheet(f"""
            QPushButton {{
                color: {text_color};
                border: none;
                border-radius: 3px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ff555555;
            }}
        """)
        
        self.maximize_btn.setStyleSheet(f"""
            QPushButton {{
                color: {text_color};
                border: none;
                border-radius: 3px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ff555555;
            }}
        """)

        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                color: {text_color};
                border: none;
                border-radius: 3px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ff555555;
            }}
        """)
    
    def paintEvent(self, event):
        if self.bg_color:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(self.bg_color))
        super().paintEvent(event)