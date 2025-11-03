import logging
from typing import Any

from apps.core.helpers.get_slug import get_slug


class LoggingService:
    _prefix: str = ""
    logger: logging.Logger

    def debug(self, message: Any) -> None:
        formatted_message = f"{self._prefix} {message}" if self._prefix else message
        self.logger.debug(formatted_message)

    def info(self, message: str) -> None:
        formatted_message = f"{self._prefix} {message}" if self._prefix else message
        self.logger.info(formatted_message)

    def warning(self, message: str) -> None:
        formatted_message = f"{self._prefix} {message}" if self._prefix else message
        self.logger.warning(formatted_message)

    def error(self, message: str) -> None:
        formatted_message = f"{self._prefix} {message}" if self._prefix else message
        self.logger.error(formatted_message)

    def critical(self, message: str) -> None:
        formatted_message = f"{self._prefix} {message}" if self._prefix else message
        self.logger.critical(formatted_message)

    def setup(self, name: str) -> None:
        logger_name = get_slug(name)
        self.logger = logging.getLogger(logger_name)

    def setup_prefix(self, prefix: str) -> None:
        self._prefix = prefix
