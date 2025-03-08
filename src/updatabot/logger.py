import logging
import os

logger = logging.getLogger("updatabot")

level = os.environ.get('UPDATABOT_LOG_LEVEL', 'WARNING')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(level)
