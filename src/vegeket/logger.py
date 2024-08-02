import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import threading
import time
import pytz
import traceback

class SingletonMeta(type):
    """シングルトンパターンを実装するためのメタクラス
       開発時に意識する必要はなし
    """
    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class MyLogger(metaclass=SingletonMeta):
    """ロガークラス(シングルトン)
       後でロガーを変更しやすいように実装している。
    """
    def __init__(self, log_dir_path="logs", log_level=logging.DEBUG, max_bytes=5*1024*1024, backup_count=100):
        self.logger = logging.getLogger(__name__)
        self._log_level = log_level
        self.logger.setLevel(log_level)
        self.log_dir_path = log_dir_path
        self._max_bytes = max_bytes
        self._backup_count = backup_count

    def _create_file_handler(self, filename):
        handler = LockedRotatingFileHandler(os.path.join(self.log_dir_path, filename), maxBytes=self._max_bytes, backupCount=self._backup_count)
        handler.setFormatter(self._create_formatter())
        return handler

    def _create_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._log_level)
        console_handler.setFormatter(self._create_formatter())
        return console_handler

    def setup_logger(self, filename="app"):
        self._create_dir(self.log_dir_path)
        filename = f"{filename}.log"
        self.logger.addHandler(self._create_file_handler(filename=filename))
        self.logger.addHandler(self._create_console_handler())
        return self.logger

    def _create_formatter(self):
        formatter = CustomFormatter('%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
        return formatter

    def _create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @property
    def log_dir_path(self):
        return self._log_dir_path

    @log_dir_path.setter
    def log_dir_path(self, path):
        self._log_dir_path = path

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level):
        self._log_level = level
        self.logger.setLevel(self._log_level)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exc_info=True):
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message, exc_info=True):
        self.logger.critical(message, exc_info=exc_info)

class LockedRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()

    def emit(self, record):
        with self._lock:
            super().emit(record)

class CustomFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc)
        return dt.astimezone(pytz.timezone('Asia/Tokyo'))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

def create_logger():
    """ロガー作成

    Returns:
        MyLogger: 設定済みのMyLoggerインスタンス
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    log_dir_path = os.path.join(current_path, "logs")
    level = logging.DEBUG
    max_size = 200 * 1024  # 200KB
    backup_count = 5
    filename = "yolo"

    logger_setup = MyLogger(log_dir_path=log_dir_path, log_level=level, max_bytes=max_size, backup_count=backup_count)
    logger_setup.setup_logger(filename=filename)

    return logger_setup


# 動作確認

if __name__ == '__main__':
    # シングルトンの動作確認
    logger1 = create_logger()
    logger2 = create_logger()
    
    print("シングルトンの確認:")
    print(f"logger1 のID: {id(logger1)}")
    print(f"logger2 のID: {id(logger2)}")
    print(f"logger1 と logger2 は同じインスタンス: {logger1 is logger2}")
    
    print("\nロガーの動作確認:")
    
    # 異なるスレッドでロガーを使用
    def log_in_thread(thread_name):
        thread_logger = create_logger()
        thread_logger.info(f"This is a log from {thread_name}")
        print(f"{thread_name} のロガーID: {id(thread_logger)}")
    
    thread1 = threading.Thread(target=log_in_thread, args=("Thread 1",))
    thread2 = threading.Thread(target=log_in_thread, args=("Thread 2",))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    # スタックトレースを生成する再帰関数
    def recursive_function(n):
        if n == 0:
            raise RecursionError("This is a sample recursion error")
        recursive_function(n - 1)
    
    # メインスレッドでのログ出力
    for i in range(3):
        logger1.debug(f"Debug message {i}")
        logger1.info(f"Info message {i}")
        logger1.warning(f"Warning message {i}")
        try:
            if i == 1:
                recursive_function(10)  # スタックトレースを生成するエラーを発生させる
        except RecursionError as e:
            logger1.error(f"An error occurred: {str(e)}")
        logger1.critical(f"Critical message {i}")
        time.sleep(1)