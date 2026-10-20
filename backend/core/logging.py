import logging
import sys


def setup_logging(log_file="logs/logger.logs", level=logging.INFO):
    log_format = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)-3d %(levelname)7s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Логи в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    # Логи в файл
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(log_format)

    # Корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    noisy_loggers = [
        "urllib3",
        "multipart",
        "python-multipart",
        "multipart.multipart",
        "python-multipart.multipart",
        "aiogram",
        "asyncio",
        "sqlalchemy",
        "sqlalchemy.engine",
        "aiosqlite",
        "apscheduler",
    ]

    for name in noisy_loggers:
        logger = logging.getLogger(name)
        logger.setLevel(logging.WARNING)
