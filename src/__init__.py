"""
Weather Dominator - Source Package

A sophisticated Python application combining real-time weather intelligence,
character database, and machine learning predictions.
"""

__version__ = "2.0.0"
__author__ = "Stray Dog Syndicate"
__email__ = "support@straydogsyndicate.com"

from src.config_manager import ConfigManager, get_config_manager
from src.exceptions import (
    APIKeyMissingError,
    ConfigurationError,
    DatabaseError,
    WeatherDominatorError,
)
from src.logger import get_logger, setup_logging

__all__ = [
    "ConfigManager",
    "get_config_manager",
    "setup_logging",
    "get_logger",
    "WeatherDominatorError",
    "APIKeyMissingError",
    "ConfigurationError",
    "DatabaseError",
]
