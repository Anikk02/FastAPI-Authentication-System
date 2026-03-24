import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'app.log')
os.makedirs(LOG_FILE, exist_ok=True)

def setup_logger():
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger
    
    #formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=3)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

settings = setup_logger()