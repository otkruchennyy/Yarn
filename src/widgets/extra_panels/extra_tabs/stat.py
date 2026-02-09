"""
Real-time system resource monitoring and visualization panel.

Displays:
- CPU usage history graph (last 60 seconds)
- Memory consumption trends
- Current resource utilization metrics
- Process-specific statistics (handles, threads)
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg
import services.logger as log


class StatPanel(QWidget):
    """
    Real-time system resource monitoring panel.
    
    Features:
    - CPU load graph with configurable history length
    - Memory consumption visualization (RSS)
    - Real-time metrics display with configurable update interval
    - Theme-aware styling for light/dark modes
    - Pausable monitoring when panel is hidden
    
    Note:
        Metrics are collected exclusively for the current application process
        via the MetricsCollector service.
    """
    
    def __init__(self, base_path, theme=None, lang=None):
        """
        Initialize statistics panel with visualization components.
        
        Args:
            base_path (str): Project root directory for resource loading
            theme (dict, optional): Color theme configuration
            lang (dict, optional): Language localization strings
        """
        super().__init__()
        self.base_path = base_path
        self.theme = theme
        self.lang = lang
        
        self._init_theme_properties()
        
        self.setup_ui()
        self.apply_theme()

    def _init_theme_properties(self):
        """init theme properties for setup_ui."""
        if self.theme:
            self.text_main = self.theme.get('text_main', '#FFFFFF')
            self.bg_card = self.theme.get('bg_card', '#2D2D2D')
            self.accent_gray = self.theme.get('accent_gray', '#555555')
        else:
            self.text_main = '#FFFFFF'
            self.bg_card = '#2D2D2D'
            self.accent_gray = '#555555'
    
    def setup_ui(self):
        """
        Construct the panel layout with visualization widgets.
        
        Layout structure:
            - CPU graph (pyqtgraph PlotWidget)
            - Memory graph (pyqtgraph PlotWidget)  
            - Current metrics labels
        """
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        
        # CPU usage graph
        self.cpu_graph = self._create_graph(
            title="CPU Usage",
            y_label="%",
            y_range=(0, 100),
            color="#FF6B6B"  # Red tone for CPU
        )
        
        # Memory usage graph  
        self.memory_graph = self._create_graph(
            title="Memory Usage",
            y_label="MB",
            color="#4ECDC4"  # Teal tone for memory
        )
        
        # Current metrics display
        self.metrics_layout = QVBoxLayout()
        
        self.cpu_label = QLabel("CPU: --%")
        self.memory_label = QLabel("Memory: -- MB")
        self.threads_label = QLabel("Threads: --")
        self.handles_label = QLabel("Handles: --")
        
        self.metrics_layout.addWidget(self.cpu_label)
        self.metrics_layout.addWidget(self.memory_label)
        self.metrics_layout.addWidget(self.threads_label)
        self.metrics_layout.addWidget(self.handles_label)
        
        # Assemble all components
        self.layout.addWidget(self.cpu_graph)
        self.layout.addWidget(self.memory_graph)
        self.layout.addLayout(self.metrics_layout)
    
    def _create_graph(self, title, y_label, y_range=None, color="#FFFFFF"):
        """
        Create a standardized pyqtgraph widget.
        
        Args:
            title (str): Graph title
            y_label (str): Y-axis label
            y_range (tuple, optional): (min, max) Y-axis range
            color (str): Line color in hex format
        
        Returns:
            pg.PlotWidget: Configured graph widget
        """
        graph = pg.PlotWidget()
        graph.setTitle(title, color=self.text_main)
        graph.setLabel('left', y_label)
        graph.setLabel('bottom', 'Time', 's')
        graph.showGrid(x=True, y=True, alpha=0.3)
        
        if y_range:
            graph.setYRange(*y_range)
        
        # Style based on theme
        bg_color = self.bg_card
        text_color = self.text_main
        grid_color = self.accent_gray
        
        graph.setBackground(bg_color)
        graph.getAxis('left').setTextPen(text_color)
        graph.getAxis('bottom').setTextPen(text_color)
        
        # Create plot line
        pen = pg.mkPen(color=color, width=2)
        plot_line = graph.plot(pen=pen)
        
        # Store reference for data updates
        if "CPU" in title:
            self.cpu_plot_line = plot_line
        else:
            self.memory_plot_line = plot_line
        
        return graph
    
    def update_metrics(self, metrics):
        """
        Update all visualizations with new metric data.
        
        Args:
            metrics (dict): System resource data containing:
                - cpu (float): Current CPU usage percentage
                - cpu_history (list): CPU usage history (last 60 seconds)
                - memory_mb (float): Current memory usage in MB
                - memory_history (list): Memory usage history in bytes
                - threads (int): Number of active threads
                - handles (int): Number of open handles/descriptors
        
        Note:
            Memory history is converted from bytes to MB for display.
        """
        try:
            # Update CPU graph
            if 'cpu_history' in metrics and metrics['cpu_history']:
                self.cpu_plot_line.setData(metrics['cpu_history'])
            
            # Update memory graph (convert bytes to MB)
            if 'memory_history' in metrics and metrics['memory_history']:
                memory_mb_history = [mb / 1024 / 1024 for mb in metrics['memory_history']]
                self.memory_plot_line.setData(memory_mb_history)
            
            # Update current values
            if 'cpu' in metrics:
                self.cpu_label.setText(f"CPU: {metrics['cpu']:.1f}%")
            
            if 'memory_mb' in metrics:
                self.memory_label.setText(f"Memory: {metrics['memory_mb']:.1f} MB")
            
            if 'threads' in metrics:
                self.threads_label.setText(f"Threads: {metrics['threads']}")
            
            if 'handles' in metrics:
                self.handles_label.setText(f"Handles: {metrics['handles']}")
                
        except KeyError as e:
            log.error(f"Missing expected metric key: {e}")
        except Exception as e:
            log.error(f"Failed to update metrics display: {e}")
    
    def show_panel(self):
        """Make the statistics panel visible."""
        self.show()
    
    def hide_panel(self):
        """Hide the statistics panel."""
        self.hide()
    
    def apply_theme(self):
        """
        Apply theme colors to panel components.
        
        Extracts colors from theme dictionary and applies them to:
            - Graph backgrounds and text
            - Label text colors
            - Overall panel styling
        """
        if not self.theme:
            return
            
        # Extract theme colors
        self.bg_card = self.theme.get('bg_card', '#2D2D2D')
        self.text_main = self.theme.get('text_main', '#FFFFFF')
        self.text_muted = self.theme.get('text_muted', '#AAAAAA')
        self.accent_gray = self.theme.get('accent_gray', '#555555')
        
        # Apply CSS styling to labels
        self.setStyleSheet(f"""
            QLabel {{
                color: {self.text_main};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px;
                padding: 2px;
            }}
        """)
        
        # Update graph colors if they exist
        if hasattr(self, 'cpu_graph'):
            self.cpu_graph.setBackground(self.bg_card)
            self.cpu_graph.getAxis('left').setTextPen(self.text_main)
            self.cpu_graph.getAxis('bottom').setTextPen(self.text_main)
            
            # Update grid color
            self.cpu_graph.showGrid(x=True, y=True, alpha=0.3)
        
        if hasattr(self, 'memory_graph'):
            self.memory_graph.setBackground(self.bg_card)
            self.memory_graph.getAxis('left').setTextPen(self.text_main)
            self.memory_graph.getAxis('bottom').setTextPen(self.text_main)
        
        # Force UI update
        self.update()