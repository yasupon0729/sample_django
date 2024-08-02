# in your_app/logging_utils.py

import logging
from logging.handlers import RotatingFileHandler
import os
import threading
import uuid
from django.conf import settings

class DjangoLoggingStrategy:
    def __init__(self, name, log_dir_path=None, log_level=logging.DEBUG, max_bytes=5*1024*1024, backup_count=100):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.instance_id = str(uuid.uuid4())
        
        if log_dir_path is None:
            log_dir_path = getattr(settings, 'LOG_DIR', 'logs')
        
        self.log_dir_path = log_dir_path
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._setup_handlers()

    def _setup_handlers(self):
        if not os.path.exists(self.log_dir_path):
            os.makedirs(self.log_dir_path)
        
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir_path, f"app_{self.instance_id}.log"),
            maxBytes=self.max_bytes,
            backupCount=self.backup_count
        )
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - [%(instance_id)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)

    def _log(self, level, message, exc_info=False):
        extra = {'instance_id': self.instance_id}
        self.logger.log(level, message, exc_info=exc_info, extra=extra)

    def debug(self, message):
        self._log(logging.DEBUG, message)

    def info(self, message):
        self._log(logging.INFO, message)

    def warning(self, message):
        self._log(logging.WARNING, message)

    def error(self, message, exc_info=True):
        self._log(logging.ERROR, message, exc_info=exc_info)

    def critical(self, message, exc_info=True):
        self._log(logging.CRITICAL, message, exc_info=exc_info)

class SingletonMeta(type):
    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class DjangoLogger(metaclass=SingletonMeta):
    def __init__(self, logging_strategy: DjangoLoggingStrategy):
        self.logging_strategy = logging_strategy

    def debug(self, message):
        self.logging_strategy.debug(message)

    def info(self, message):
        self.logging_strategy.info(message)

    def warning(self, message):
        self.logging_strategy.warning(message)

    def error(self, message, exc_info=True):
        self.logging_strategy.error(message, exc_info=exc_info)

    def critical(self, message, exc_info=True):
        self.logging_strategy.critical(message, exc_info=exc_info)

def get_logger(name='django'):
    strategy = DjangoLoggingStrategy(name)
    return DjangoLogger(strategy)

# Usage in your Django views or anywhere in your Django project:
# from your_app.logging_utils import get_logger

# logger = get_logger('my_app')
# logger.info("This is an info message")
# logger.error("This is an error message")