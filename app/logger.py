from loguru import logger
from datetime import datetime

def configure_log() -> logger:
    '''
    Configures a logging system and returns the logger instance.

    This function sets up logging by creating a logger instance, specifying a log file with a name
    based on the current date, enabling log rotation when the file reaches 20 MB in size, and setting
    the log level to "TRACE."

    Returns:
        logger: The configured logger instance for logging purposes.
    '''
    FILE_OUT_LOG = f"./app_{datetime.today().strftime('%Y_%m_%d')}.log"
    logger.remove()
    logger.add(FILE_OUT_LOG, rotation="20 MB",level="TRACE")
    return logger