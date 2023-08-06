"""
Logger class for logging to log server
"""
import logging


class Logger(object):
    """
    Logger class for logging to log server
        .log(message) - log message
        .error(message) - log error message
        .warning(message) - log warning message
        .send_log() - send log to log server
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.logger = logging.getLogger(f"{session_id}-LOG")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(f"{session_id}_log.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log(self, message: str):
        print(message)
        self.logger.info(message)

    def error(self, message: str):
        print(message)
        self.logger.error(message)

    def warning(self, message: str):
        print(message)
        self.logger.warning(message)

    def send_log(self):
        """
        Send log to log server
        """
        with open(f"{self.session_id}_log.log", "r") as log_file:
            lines = log_file.readlines()
            print(lines)
