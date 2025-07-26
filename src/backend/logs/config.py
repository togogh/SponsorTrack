import logging
from logging.handlers import TimedRotatingFileHandler
import os


def get_logger(name):
    LOG_DIR = r"src\backend\logs"
    LOG_FILE = "app.log"

    log_path = os.path.join(LOG_DIR, LOG_FILE)

    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    file_handler = TimedRotatingFileHandler(
        log_path, when="midnight", interval=1, backupCount=7, encoding="utf-8", delay=True
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger
