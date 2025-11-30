import logging
import utils.helpers as helpers
import os
import inspect

log_path = os.path.join(helpers.get_project_root(), "app.log")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ])

logger = logging.getLogger(__name__)

def _get_caller_info(level):
    frame = inspect.currentframe()
    for _ in range(level):
        frame = frame.f_back
        if frame is None:
            break
    return frame.f_code.co_filename, frame.f_lineno

def debug(msg, level=2):
    filename, lineno = _get_caller_info(level)
    logger.debug(f"{os.path.basename(filename)}:{lineno} - {msg}")

def info(msg, level=2):
    filename, lineno = _get_caller_info(level)  
    logger.info(f"{os.path.basename(filename)}:{lineno} - {msg}")

def warning(msg, level=2):
    filename, lineno = _get_caller_info(level)  
    logger.warning(f"{os.path.basename(filename)}:{lineno} - {msg}")

def error(msg, level=2):
    filename, lineno = _get_caller_info(level)  
    logger.error(f"{os.path.basename(filename)}:{lineno} - {msg}")

def clear_logs():
    open('app.log', 'w').close()
    info("Логи очищены пользователем")