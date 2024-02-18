import logging
import os
from logging.handlers import RotatingFileHandler

from scripts.constants import app_configuration

if not os.path.exists(app_configuration.LOG_BASE_PATH):
    os.makedirs(app_configuration.LOG_BASE_PATH)

def get_logger():
    logger = logging.getLogger(app_configuration.LOG_NAME)
    logger.setLevel(app_configuration.LOG_LEVEL)
    formatter = logging.Formatter(
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        datefmt = "%Y-%m-%dT%H:%M:%SZ"
    )

    if "console" in app_configuration.LOG_HANDLERS:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    if "rotating" in app_configuration.LOG_HANDLERS:
        rotating_handler = RotatingFileHandler(
            filename = app_configuration.LOG_BASE_PATH + app_configuration.LOG_FILE_NAME,
            maxBytes = int(app_configuration.LOG_MAX_FILE_SIZE),
            backupCount = int(app_configuration.LOG_MAX_FILE_BACKUPS),
            encoding = "utf-8"
        )
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)

    return logger

logger = get_logger()
