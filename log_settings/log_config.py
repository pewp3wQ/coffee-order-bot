import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # очистить старые обработчики
    logger.handlers.clear()

    # файл с ротацией
    file_handler = RotatingFileHandler(
        "logs_file/app.log",
        maxBytes=5_000_000,
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))

    # консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
