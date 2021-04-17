import logging
from logging import handlers

logger = logging.getLogger('framework')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
file_handler = handlers.TimedRotatingFileHandler("framework/log/framework.log", 'D', 1, backupCount=7, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
