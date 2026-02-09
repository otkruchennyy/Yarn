import psutil
import os
from collections import deque
from PySide6.QtCore import QThread, Signal, QTimer

class MetricsCollector(QThread):
    """Потоковый сборщик метрик системы для текущего процесса."""
    metrics_updated = Signal(dict)  # Сигнал с новыми данными
    
    def __init__(self, update_interval=1000):
        super().__init__()
        self.update_interval = update_interval
        self.process = psutil.Process(os.getpid())
        self._stop_flag = False
        
        # История для графиков
        self.cpu_history = deque(maxlen=60)
        self.memory_history = deque(maxlen=60)
        
        # Первый вызов для калибровки CPU
        self.process.cpu_percent(interval=None)
        
    def run(self):
        """Основной цикл сбора метрик."""
        timer = QTimer()
        timer.timeout.connect(self._collect)
        timer.start(self.update_interval)
        
        # Запускаем event loop потока
        self.exec_()
        
    def _collect(self):
        """Сбор одной порции метрик."""
        try:
            # CPU
            cpu = self.process.cpu_percent(interval=None)
            self.cpu_history.append(cpu)
            
            # Memory
            mem_bytes = self.process.memory_info().rss
            self.memory_history.append(mem_bytes)
            
            # Threads и handles (кросс-платформенно)
            threads = self.process.num_threads()
            if hasattr(self.process, 'num_handles'):
                handles = self.process.num_handles()
            else:
                handles = self.process.num_fds()
            
            metrics = {
                'cpu': cpu,
                'cpu_history': list(self.cpu_history),
                'memory_bytes': mem_bytes,
                'memory_history': list(self.memory_history),
                'memory_mb': mem_bytes / 1024 / 1024,
                'threads': threads,
                'handles': handles
            }
            
            self.metrics_updated.emit(metrics)
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Процесс завершился или нет прав
            self.stop()
            
    def stop(self):
        """Остановка сбора."""
        self._stop_flag = True
        self.quit()