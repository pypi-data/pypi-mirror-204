"""
This module provides client and server logging - console and file based

Internal package - does not need to be used
"""

import logging
from dfiibridge_core import LoggingCallback

LOGGER_NAME = "dfii_bridge"
LOGGER_FILE_NAME = "dfii_bridge.log"


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors
    SRC: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    """

    green = "\033[32;1m"
    yellow = "\033[33;1m"
    red = "\033[31;1m"
    reset = "\033[0m"

    FORMATS = {
        logging.DEBUG: green + "[%(levelname)s]" + reset + " %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)",
        logging.INFO: green + "[%(levelname)s]" + reset + " %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)",
        logging.WARNING: yellow + "[%(levelname)s]" + reset + " %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)",
        logging.ERROR: red + "[%(levelname)s]" + reset + " %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)",
        logging.CRITICAL: red + "[%(levelname)s]" + reset + " %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def configure_logger(only_file=False, log_level=logging.INFO) -> None:
    """
    Create and initialize the logger, by setting the log level and adding
    multiple handlers for console and file output
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(log_level)

    if not only_file:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)

    fh = logging.FileHandler(LOGGER_FILE_NAME)
    fh.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

class SimpleStdoutLogger(LoggingCallback):
    """
    Simple implementation of the logging interface LoggingCallback
    """

    def __init__(self, log_level=logging.DEBUG):
        super().__init__()
        self.log_level = log_level

    def log(self, log_level, log_message):
        '''Log the passed message if it matches my log level
           The log levels are descending defined: CRITICAL > ERROR > WARING > INFO > DEBUG
        '''
        if log_level >= self.log_level:
            print(log_message)
