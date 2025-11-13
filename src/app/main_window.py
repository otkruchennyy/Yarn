import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import QRect
import utils.helpers as helpers
from widgets.header import CustomHeader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_main_app()
        self.path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
        
        self.resize_margin = 8
        self.resize_dragging = False
        self.resize_direction = None
        self.setMouseTracking(True)

        self.theme_default = helpers.get_json_property(
            self.path + '/resources/themes/' + 
            f'{helpers.get_json_property('./config/config.json', "theme")}' + 
            '.json'
        )

        self.font_default = helpers.get_json_property(
            self.path + '/resources/fonts/' + 
            f'{helpers.get_json_property('./config/config.json', "fonts")}' + 
            '.json'
        )
        self.main_font_style = self.font_default["main"]
        self.monospace_font_style = self.font_default["monospace"]

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.create_widgets()

        self.is_color_suitable = (self.theme_default["isDark"] == self.main_font_style["fontIsDark"])
        if self.is_color_suitable:
            dialog = helpers.colors_is_suitable(self.theme_default, self.main_font_style, self.path)
            dialog.exec()

    def setup_main_app(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Yarn")
        self.setMinimumSize(200, 150)
        
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                "resources", "icons", "ico", "Yarn-256.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        central_widget = QWidget()
        central_widget.setMouseTracking(True)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position().toPoint()
            self.resize_direction = self.get_resize_direction(pos)
            if self.resize_direction:
                self.resize_dragging = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_geometry = self.geometry()
                return
                
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        width = self.width()
        height = self.height()
        x, y = pos.x(), pos.y()
        
        if not self.resize_dragging:
            new_cursor = Qt.ArrowCursor
            
            if x <= 10 and y <= 10:
                new_cursor = Qt.SizeFDiagCursor
            elif x >= width - 10 and y <= 10:
                new_cursor = Qt.SizeBDiagCursor
            elif x <= 10 and y >= height - 10:
                new_cursor = Qt.SizeBDiagCursor
            elif x >= width - 10 and y >= height - 10:
                new_cursor = Qt.SizeFDiagCursor
            elif x <= 10:
                new_cursor = Qt.SizeHorCursor
            elif x >= width - 10:
                new_cursor = Qt.SizeHorCursor
            elif y <= 10:
                new_cursor = Qt.SizeVerCursor
            elif y >= height - 10:
                new_cursor = Qt.SizeVerCursor
            
            if self.cursor().shape() != new_cursor:
                self.unsetCursor()
                self.setCursor(new_cursor)
        else:
            self.handle_resize(event.globalPosition().toPoint())
            
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.resize_dragging = False
            self.resize_direction = None
            self.setCursor(Qt.ArrowCursor)
            
        super().mouseReleaseEvent(event)
    
    def get_resize_direction(self, pos):
        width = self.width()
        height = self.height()
        x, y = pos.x(), pos.y()
        margin = 10
        
        if x <= margin and y <= margin:
            return 'top_left'
        elif x >= width - margin and y <= margin:
            return 'top_right'
        elif x <= margin and y >= height - margin:
            return 'bottom_left'
        elif x >= width - margin and y >= height - margin:
            return 'bottom_right'
        elif x <= margin:
            return 'left'
        elif x >= width - margin:
            return 'right'
        elif y <= margin:
            return 'top'
        elif y >= height - margin:
            return 'bottom'
        return None
    
    def handle_resize(self, global_pos):
        if not self.resize_dragging or not self.resize_direction:
            return
            
        delta = global_pos - self.resize_start_pos
        new_geometry = QRect(self.resize_start_geometry)
        
        direction = self.resize_direction
        
        if 'left' in direction:
            new_geometry.setLeft(new_geometry.left() + delta.x())
        if 'right' in direction:
            new_geometry.setRight(new_geometry.right() + delta.x())
        if 'top' in direction:
            new_geometry.setTop(new_geometry.top() + delta.y())
        if 'bottom' in direction:
            new_geometry.setBottom(new_geometry.bottom() + delta.y())
        
        if new_geometry.width() >= 200 and new_geometry.height() >= 150:
            self.setGeometry(new_geometry)
    
    def create_widgets(self):
        pass
        # self.header = CustomHeader(theme=self.theme_default, parent=self)
        # self.layout.addWidget(self.header)
        # self.header.close_btn.clicked.connect(self.close)
    
    def on_close(self):
        self.close()
    
    def run(self):
        self.show()