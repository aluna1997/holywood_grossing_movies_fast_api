from loguru import logger
from datetime import datetime

def configure_log():
    FILE_OUT_LOG = f"./app_{datetime.today().strftime('%Y_%m_%d')}.log"
    logger.remove()
    logger.add(FILE_OUT_LOG, rotation="20 MB",level="TRACE")
    return logger