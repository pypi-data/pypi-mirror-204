import logging

class CustomLogger(object):
    def __init__(self, logger_name, log_format, extra=None):
        logging.basicConfig(format=log_format)
        self.logger = logging.getLogger(logger_name)
        self.extra = extra

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, extra=self.extra, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, extra=self.extra, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, extra=self.extra, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, extra=self.extra, **kwargs)