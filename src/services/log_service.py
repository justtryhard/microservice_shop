import logging
from datetime import datetime


class LogService:
    def __init__(self, log_file: str = 'app.log'):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)

    def info(self, message: str, **kwargs):
        """Логирование информационного сообщения"""
        self.logger.info(f"{message} | {kwargs}")

    def error(self, message: str, **kwargs):
        """Логирование ошибки"""
        self.logger.error(f"{message} | {kwargs}")

    def warning(self, message: str, **kwargs):
        """Логирование предупреждения"""
        self.logger.warning(f"{message} | {kwargs}")

    def critical(self, message: str, **kwargs):
        """Логирование критической ошибки"""
        self.logger.critical(f"{message} | {kwargs}")
        # Можно добавить отправку алерта




log_service = LogService()