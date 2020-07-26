import logging

import settings



def _get_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(settings.COSOLE_FORMATTER)
    return console_handler


def _get_file_handler():
    file_handler = TimedRotatingFileHandler(settings.LOG_FILE, when='midnight')
    file_handler.setFormatter(settings.FILE_FORMATTER)
    return file_handler


def get_logger(logger_name, console_log=True, file_log=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(settings.LOGGING_LEVEL)

    if console_log:
        logger.addHandler(_get_console_handler())

    if file_log:
        logger.addHandler(_get_file_handler())

    logger.propagate = False
    return logger
