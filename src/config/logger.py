# in your_app/logging_utils.py

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from threading import Lock
from typing import Any

# 現在の実装は、基本的に複数のクライアントからのアクセスに対応できます。以下の理由から：
# シングルトンパターンを使用しているため、同じプロセス内で複数のロガーインスタンスが作成されることを防いでいます。
# ログメッセージにプロセスIDが含まれているため、異なるプロセスからのログを区別できます。
# RotatingFileHandlerは、ファイルへの書き込みをスレッドセーフに行います。
# ただし、非常に高負荷な環境や、多数の同時接続がある場合には、以下の点に注意が必要です：
# ファイルI/Oがボトルネックになる可能性があります。
# ログローテーション時に短時間のブロッキングが発生する可能性があります。
# 改善案：
# 非同期ロギングを導入する（例：QueueHandlerとQueueListenerを使用）
# TODO: 2024-08-02 分散ロギングシステムを使用する（例：ELK スタック）


class SingletonMeta(type):
    _instances: dict[Any, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DjangoLoggingStrategy(metaclass=SingletonMeta):
    def __init__(
        self,
        name,
        log_dir_path="logs",
        log_level=logging.DEBUG,
        max_bytes=5 * 1024 * 1024,
        backup_count=100,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        self.log_dir_path = log_dir_path
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._setup_handlers()

    def _setup_handlers(self):
        if not os.path.exists(self.log_dir_path):
            os.makedirs(self.log_dir_path)

        # ファイルハンドラの設定
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir_path, "app.log"),
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
        )

        # コンソールハンドラの設定
        console_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _log(self, level, message, exc_info=False):
        self.logger.log(level, message, exc_info=exc_info)

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


_logger_instances = {}


def get_logger(name="django"):
    if name not in _logger_instances:
        strategy = DjangoLoggingStrategy(name)
        _logger_instances[name] = DjangoLogger(strategy)
    return _logger_instances[name]


# Usage in your Django views or anywhere in your Django project:
# from your_app.logging_utils import get_logger

# logger = get_logger('my_app')
# logger.info("This is an info message")
# logger.error("This is an error message")
