"""
Logging configuration for Weather Dominator application.

This module provides centralized logging configuration with support for
console and file handlers, log rotation, and structured logging.
"""

import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    # Emoji prefixes for better visual identification
    ICONS = {
        "DEBUG": "🔍",
        "INFO": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🚨",
    }

    def format(self, record):
        """
        Format log record with colors and icons.

        Args:
            record: LogRecord instance

        Returns:
            Formatted log string
        """
        # Add color
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}"
                f"{self.ICONS.get(levelname, '')} {levelname}"
                f"{self.COLORS['RESET']}"
            )

        return super().format(record)


class WeatherDominatorLogger:
    """
    Centralized logger for Weather Dominator application.

    Provides logging to both console and file with rotation,
    different log levels, and structured formatting.
    """

    def __init__(
        self,
        name: str = "WeatherDominator",
        log_dir: str = "logs",
        log_file: str = "weather_dominator.log",
        level: int = logging.INFO,
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5,
        console_output: bool = True,
        colored_console: bool = True,
    ):
        """
        Initialize logger.

        Args:
            name: Logger name
            log_dir: Directory for log files
            log_file: Log filename
            level: Logging level
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            console_output: Whether to output to console
            colored_console: Whether to use colors in console output
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_file = log_file
        self.level = level
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.console_output = console_output
        self.colored_console = colored_console

        # Create logger
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up logger with handlers and formatters.

        Returns:
            Configured Logger instance
        """
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()

        # File handler with rotation
        if self._setup_file_handler(logger):
            pass  # File handler added successfully

        # Console handler
        if self.console_output:
            self._setup_console_handler(logger)

        return logger

    def _setup_file_handler(self, logger: logging.Logger) -> bool:
        """
        Set up rotating file handler.

        Args:
            logger: Logger instance

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create log directory if it doesn't exist
            self.log_dir.mkdir(parents=True, exist_ok=True)

            log_path = self.log_dir / self.log_file

            # Rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding="utf-8",
            )

            # Detailed format for file logs
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(module)s:%(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(self.level)

            logger.addHandler(file_handler)
            return True

        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
            return False

    def _setup_console_handler(self, logger: logging.Logger):
        """
        Set up console handler.

        Args:
            logger: Logger instance
        """
        console_handler = logging.StreamHandler(sys.stdout)

        # Choose formatter based on color setting
        if self.colored_console and sys.stdout.isatty():
            console_formatter: logging.Formatter = ColoredFormatter(
                "%(levelname)s - %(message)s"
            )
        else:
            console_formatter = logging.Formatter("%(levelname)s - %(message)s")

        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(self.level)

        logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            Logger instance
        """
        return self.logger

    def set_level(self, level: int):
        """
        Set logging level.

        Args:
            level: Logging level (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def add_handler(self, handler: logging.Handler):
        """
        Add custom handler to logger.

        Args:
            handler: logging.Handler instance
        """
        self.logger.addHandler(handler)

    def log_startup(self):
        """Log application startup information."""
        self.logger.info("=" * 60)
        self.logger.info("Weather Dominator Application Starting")
        self.logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Log Level: {logging.getLevelName(self.level)}")
        self.logger.info(f"Log Directory: {self.log_dir}")
        self.logger.info("=" * 60)

    def log_shutdown(self):
        """Log application shutdown information."""
        self.logger.info("=" * 60)
        self.logger.info("Weather Dominator Application Shutting Down")
        self.logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 60)


# Global logger instance
_logger_instance: Optional[WeatherDominatorLogger] = None


def setup_logging(
    level: int = logging.INFO,
    log_dir: str = "logs",
    console_output: bool = True,
    colored: bool = True,
) -> logging.Logger:
    """
    Set up global logging configuration.

    Args:
        level: Logging level
        log_dir: Directory for log files
        console_output: Whether to output to console
        colored: Whether to use colored console output

    Returns:
        Configured logger instance
    """
    global _logger_instance

    if _logger_instance is None:
        _logger_instance = WeatherDominatorLogger(
            level=level,
            log_dir=log_dir,
            console_output=console_output,
            colored_console=colored,
        )
        _logger_instance.log_startup()

    return _logger_instance.get_logger()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get logger instance.

    Args:
        name: Optional logger name. If None, returns root logger.

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"WeatherDominator.{name}")

    if _logger_instance is None:
        return setup_logging()

    return _logger_instance.get_logger()


def log_exception(logger: logging.Logger, exc: Exception, context: str = ""):
    """
    Log exception with full traceback.

    Args:
        logger: Logger instance
        exc: Exception to log
        context: Optional context message
    """
    if context:
        logger.error(f"{context}: {type(exc).__name__}: {exc}", exc_info=True)
    else:
        logger.error(f"{type(exc).__name__}: {exc}", exc_info=True)


def log_function_call(func):
    """
    Decorator to log function calls.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """

    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__}(*{args}, **{kwargs})")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}", exc_info=True)
            raise

    return wrapper


# Example usage
if __name__ == "__main__":
    # Setup logging
    logger = setup_logging(level=logging.DEBUG)

    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Test exception logging
    try:
        raise ValueError("Test exception")
    except Exception as e:
        log_exception(logger, e, "Testing exception logging")

    # Test function decorator
    @log_function_call
    def test_function(x, y):
        return x + y

    result = test_function(5, 3)
    logger.info(f"Result: {result}")

    # Shutdown
    if _logger_instance:
        _logger_instance.log_shutdown()
