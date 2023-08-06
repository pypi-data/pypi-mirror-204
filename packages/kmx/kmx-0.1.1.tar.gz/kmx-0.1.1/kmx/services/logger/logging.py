import logging


class LoggingLogger:
    """
    Logging throw python "logging" module
    """
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)

    def debug(self, text: str):
        self.logger.debug(text)

    def info(self, text: str):
        self.logger.info(text)

    def warning(self, text: str):
        self.logger.warning(text)

    def error(self, text: str):
        self.logger.error(text)

    def exception(self, text: str):
        self.logger.exception(text)
