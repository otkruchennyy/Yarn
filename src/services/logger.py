import logging
import time
import functools
import os
import sys
import inspect

def get_project_root():
    """Returns the project root folder"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
def get_log_path():
    return os.path.join(get_project_root(), "app.log")

log_path = get_log_path()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ])

logger = logging.getLogger(__name__)

def _get_caller_info():
    """Automatically detect caller filename and line number in the call stack."""
    # Get the current stack
    stack = inspect.stack()
    
    # Direct approach: frame 2 is always the caller of info/debug/etc
    if len(stack) > 2:
        frame_info = stack[2]  # 0=_get_caller_info, 1=info/debug, 2=caller
        filename = os.path.basename(frame_info.filename)
        lineno = frame_info.lineno
        return filename, lineno
    
    # Fallback
    return "unknown", 0

def get_logs():
    with open(log_path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def log(msg=None, mode="debug", call_level=3):  # debug, info, error
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if mode == "debug":
                # DEBUG: time_measurement
                start = time.time()
                result = func(*args, **kwargs)
                duration = (time.time() - start) * 1000
                message = msg or f"PERF: {func.__name__} took {duration:.2f}ms"
                debug(message)
                return result
                
            elif mode == "info":
                # INFO: call_arguments
                message = msg or f"CALL: {func.__name__} with args={args}, kwargs={kwargs}"
                info(message)
                return func(*args, **kwargs)
                
            elif mode == "error":
                # ERROR: log_exceptions
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    message = msg or f"ERROR in {func.__name__}: {e}"
                    error(message)
                    raise
            elif mode == "critical":
                # CRITICAL: log_exceptions
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    message = msg or f"CRITICAL in {func.__name__}: {e}"
                    critical(message)
                    raise
            else: 
                error(f"ШАКАЛ: неизвестный mode='{mode}' в декораторе @log")
                return func(*args, **kwargs) 
                    
        return wrapper
    return decorator

def debug(msg):
    """Log debug level message with automatic caller detection."""
    filename, lineno = _get_caller_info()
    logger.debug(f"{filename}:{lineno} - {msg}")

def info(msg):
    """Log info level message with automatic caller detection."""
    filename, lineno = _get_caller_info()
    logger.info(f"{filename}:{lineno} - {msg}")

def warning(msg):
    """Log warning level message with automatic caller detection."""
    filename, lineno = _get_caller_info()
    logger.warning(f"{filename}:{lineno} - {msg}")

def error(msg):
    """Log error level message with automatic caller detection."""
    filename, lineno = _get_caller_info()
    logger.error(f"{filename}:{lineno} - {msg}")

def critical(msg):
    """Log critical level message with automatic caller detection."""
    filename, lineno = _get_caller_info()
    logger.critical(f"{filename}:{lineno} - {msg}")

def clear_logs():
    """Clear all log entries from the log file."""
    open(log_path, 'w').close()
    info("Логи очищены пользователем")