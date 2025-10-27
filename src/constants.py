"""
Constants and configuration values for Weather Dominator application.

This module contains all magic numbers, strings, and configuration
values used throughout the application.
"""

from enum import Enum
from typing import Final

# ============================================================================
# Application Metadata
# ============================================================================
APP_NAME: Final[str] = "COBRA Weather Dominator"
APP_VERSION: Final[str] = "2.0.0"
APP_DESCRIPTION: Final[str] = "Advanced Weather Control System"
APP_AUTHOR: Final[str] = "Stray Dog Syndicate"

# ============================================================================
# Window Configuration
# ============================================================================
WINDOW_WIDTH: Final[int] = 1200
WINDOW_HEIGHT: Final[int] = 800
WINDOW_MIN_WIDTH: Final[int] = 900
WINDOW_MIN_HEIGHT: Final[int] = 600
WINDOW_ALPHA: Final[float] = 0.95

# ============================================================================
# API Configuration
# ============================================================================
OPENWEATHER_BASE_URL: Final[str] = "http://api.openweathermap.org/data/2.5"
OPENWEATHER_ICON_URL: Final[str] = "http://openweathermap.org/img/w"
OPENWEATHER_GEO_URL: Final[str] = "http://api.openweathermap.org/geo/1.0"

GIJOE_FANDOM_API: Final[str] = "https://gijoe.fandom.com/api.php"
GIJOE_WIKI_URL: Final[str] = "https://gijoe.fandom.com/wiki"

# ============================================================================
# Database Configuration
# ============================================================================
DEFAULT_DB_PATH: Final[str] = "weather_dominator.db"
MAX_CACHE_AGE_DAYS: Final[int] = 7
MAX_DB_SIZE_MB: Final[int] = 50
DATA_CLEANUP_DAYS: Final[int] = 30


# ============================================================================
# Theme Colors - Blue (Default)
# ============================================================================
class ThemeColors:
    """Default blue glassmorphic theme colors."""

    # Backgrounds
    WINDOW_BG: Final[str] = "#000000"
    CONTAINER_BG: Final[str] = "#1a1a2e"
    GLASS_BG: Final[str] = "#16213e"
    CONTENT_BG: Final[str] = "#16213e"

    # Accents
    PRIMARY_ACCENT: Final[str] = "#4a9eff"
    SECONDARY_ACCENT: Final[str] = "#7bb3ff"
    HIGHLIGHT: Final[str] = "#4a6fa5"
    BORDER: Final[str] = "#0f3460"

    # Gradient colors for glassmorphic effect
    GRADIENT_COLORS: Final[tuple] = ("#16213e", "#1a1a2e", "#0f3460")

    # Text
    TITLE_COLOR: Final[str] = "#4a9eff"
    SUBTITLE_COLOR: Final[str] = "#7bb3ff"
    TEXT_COLOR: Final[str] = "#ffffff"
    MUTED_TEXT: Final[str] = "#b0b0b0"

    # Buttons
    BUTTON_BG: Final[str] = "#2d4059"
    BUTTON_FG: Final[str] = "#ffffff"
    BUTTON_ACTIVE_BG: Final[str] = "#4a6fa5"
    BUTTON_HOVER_BG: Final[str] = "#3a5068"

    # Status
    DANGER_COLOR: Final[str] = "#ff6b6b"
    SUCCESS_COLOR: Final[str] = "#51cf66"
    WARNING_COLOR: Final[str] = "#ffd43b"
    INFO_COLOR: Final[str] = "#4a9eff"

    # Input
    INPUT_BG: Final[str] = "#1a2451"
    INPUT_FG: Final[str] = "#ffffff"
    INPUT_BORDER: Final[str] = "#4a6fa5"


# ============================================================================
# COBRA Theme Colors - Red
# ============================================================================
class CobraThemeColors:
    """COBRA red theme colors."""

    PRIMARY_ACCENT: Final[str] = "#dc143c"
    SECONDARY_ACCENT: Final[str] = "#ff6b6b"
    HIGHLIGHT: Final[str] = "#8b0000"
    TITLE_COLOR: Final[str] = "#dc143c"
    SUBTITLE_COLOR: Final[str] = "#ff6b6b"


# ============================================================================
# Font Configuration
# ============================================================================
class FontConfig:
    """Font family and sizes."""

    FONT_FAMILY: Final[str] = "Arial"

    TITLE_SIZE: Final[int] = 24
    SUBTITLE_SIZE: Final[int] = 12
    LARGE_SIZE: Final[int] = 18
    BODY_SIZE: Final[int] = 10
    SMALL_SIZE: Final[int] = 8

    LABEL_SIZE: Final[int] = 9
    BUTTON_SIZE: Final[int] = 10
    SECTION_SIZE: Final[int] = 12

    # Font tuples for tkinter (family, size, weight)
    TITLE_FONT: Final[tuple] = (FONT_FAMILY, TITLE_SIZE, "bold")
    SUBTITLE_FONT: Final[tuple] = (FONT_FAMILY, SUBTITLE_SIZE)
    BODY_FONT: Final[tuple] = (FONT_FAMILY, BODY_SIZE)
    BUTTON_FONT: Final[tuple] = (FONT_FAMILY, BUTTON_SIZE)
    SECTION_FONT: Final[tuple] = (FONT_FAMILY, SECTION_SIZE, "bold")
    LABEL_FONT: Final[tuple] = (FONT_FAMILY, LABEL_SIZE)
    SMALL_FONT: Final[tuple] = (FONT_FAMILY, SMALL_SIZE)
    LARGE_FONT: Final[tuple] = (FONT_FAMILY, LARGE_SIZE)


# ============================================================================
# Spacing and Layout
# ============================================================================
class Spacing:
    """Spacing constants for consistent layout."""

    PADDING_LARGE: Final[int] = 20
    PADDING_MEDIUM: Final[int] = 10
    PADDING_SMALL: Final[int] = 5
    PADDING_TINY: Final[int] = 2

    BORDER_WIDTH: Final[int] = 1
    SEPARATOR_HEIGHT: Final[int] = 1
    GLASS_HIGHLIGHT_HEIGHT: Final[int] = 2
    GRADIENT_FRAME_HEIGHT: Final[int] = 1


# ============================================================================
# API Request Configuration
# ============================================================================
class APIConfig:
    """API request configuration."""

    REQUEST_TIMEOUT: Final[int] = 10
    MAX_RETRIES: Final[int] = 3
    RETRY_DELAY: Final[int] = 1

    # Weather units
    TEMP_UNIT_IMPERIAL: Final[str] = "imperial"
    TEMP_UNIT_METRIC: Final[str] = "metric"

    # Wind units
    WIND_UNIT_MPH: Final[str] = "mph"
    WIND_UNIT_MS: Final[str] = "m/s"

    # Pressure units
    PRESSURE_UNIT_HPA: Final[str] = "hPa"
    PRESSURE_UNIT_INHG: Final[str] = "inHg"


# ============================================================================
# Weather Thresholds
# ============================================================================
class WeatherThresholds:
    """Thresholds for weather condition classification."""

    # Wind speed thresholds (mph)
    HIGH_WIND_MPH: Final[float] = 25.0
    HIGH_WIND_MS: Final[float] = 11.0  # meters per second

    # Temperature thresholds (Fahrenheit)
    EXTREME_COLD_F: Final[float] = 0.0
    EXTREME_HOT_F: Final[float] = 100.0

    # Visibility threshold (km)
    LOW_VISIBILITY_KM: Final[float] = 1.0


# ============================================================================
# Character Data
# ============================================================================
class CobraCharacters:
    """Known COBRA character names."""

    COMMANDERS: Final[list[str]] = ["Cobra Commander", "Serpentor", "Golobulus"]

    HIGH_COMMAND: Final[list[str]] = [
        "Destro",
        "Baroness",
        "Dr. Mindbender",
        "Tomax",
        "Xamot",
    ]

    FIELD_OPERATIVES: Final[list[str]] = [
        "Storm Shadow",
        "Firefly",
        "Zartan",
        "Major Bludd",
        "Wild Weasel",
    ]

    SPECIALISTS: Final[list[str]] = [
        "Scrap-Iron",
        "Copperhead",
        "Croc Master",
        "Crystal Ball",
        "Gnawgahyde",
    ]

    TROOPS: Final[list[str]] = [
        "Viper",
        "Crimson Guard",
        "Alley-Viper",
        "Range-Viper",
        "Night-Viper",
        "Snow Serpent",
        "Techno-Viper",
    ]


# ============================================================================
# Severe Weather Keywords
# ============================================================================
SEVERE_WEATHER_KEYWORDS: Final[list[str]] = [
    "storm",
    "thunderstorm",
    "hail",
    "tornado",
    "hurricane",
    "blizzard",
    "extreme",
    "severe",
    "warning",
    "advisory",
]


# ============================================================================
# File Paths
# ============================================================================
class FilePaths:
    """Default file paths and directories."""

    CONFIG_DIR: Final[str] = "config"
    DATA_DIR: Final[str] = "data"
    SCHEMAS_DIR: Final[str] = "schemas"
    EXPORTS_DIR: Final[str] = "data/exports"
    BACKUPS_DIR: Final[str] = "data/backups"

    CONFIG_FILE: Final[str] = "config/config.json"
    FAVORITES_FILE: Final[str] = "data/favorite_cities.json"
    ALERTS_FILE: Final[str] = "data/weather_alerts.json"
    JOURNAL_FILE: Final[str] = "data/weather_journal.json"
    SETTINGS_FILE: Final[str] = "data/user_settings.json"


# ============================================================================
# Logging Configuration
# ============================================================================
class LogConfig:
    """Logging configuration."""

    LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
    LOG_FILE: Final[str] = "weather_dominator.log"
    MAX_LOG_SIZE: Final[int] = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT: Final[int] = 5


# ============================================================================
# Status Messages
# ============================================================================
class StatusMessages:
    """Standard status messages."""

    # Success
    SUCCESS_WEATHER_FETCH: Final[str] = "✅ Weather data retrieved successfully"
    SUCCESS_CHARACTER_FOUND: Final[str] = "✅ Character data retrieved successfully"
    SUCCESS_DB_INIT: Final[str] = "✅ Database initialized successfully"

    # Errors
    ERROR_NO_API_KEY: Final[str] = "❌ API key not configured"
    ERROR_NETWORK: Final[str] = "❌ Network error occurred"
    ERROR_NOT_FOUND: Final[str] = "❌ Data not found"
    ERROR_DB: Final[str] = "❌ Database error occurred"

    # Warnings
    WARN_NO_MODULES: Final[str] = "⚠️ Some modules not available"
    WARN_DEMO_MODE: Final[str] = "⚠️ Running in demo mode"

    # Info
    INFO_LOADING: Final[str] = "Loading..."
    INFO_SEARCHING: Final[str] = "Searching..."


# ============================================================================
# Error Messages
# ============================================================================
class ErrorMessages:
    """Detailed error messages."""

    INPUT_REQUIRED: Final[str] = "Input Required"
    CITY_NAME_REQUIRED: Final[str] = "Please enter a city name."
    CHARACTER_NAME_REQUIRED: Final[str] = "Please enter a character name."

    API_KEY_MISSING: Final[str] = (
        "API key not configured. Add your API key to config.json"
    )
    NETWORK_ERROR: Final[str] = "Network error: Unable to connect to API"
    DATA_PARSE_ERROR: Final[str] = "Data parsing error: Unable to process response"

    DB_INIT_ERROR: Final[str] = "Database initialization error"
    DB_WRITE_ERROR: Final[str] = "Database write error"
    DB_READ_ERROR: Final[str] = "Database read error"


# ============================================================================
# Tab Names
# ============================================================================
class TabNames:
    """Tab display names."""

    WEATHER_INTEL: Final[str] = "⛈️ WEATHER INTEL"
    COBRA_INTEL: Final[str] = "🐍 COBRA INTEL"
    INTERACTIVE: Final[str] = "🎯 INTERACTIVE"
    SMART_AI: Final[str] = "🧠 SMART AI"


# ============================================================================
# Button Labels
# ============================================================================
class ButtonLabels:
    """Button text labels."""

    FETCH_WEATHER: Final[str] = "🌍 ACQUIRE WEATHER DATA"
    SEARCH_CHARACTER: Final[str] = "🔍 INTERROGATE DATABASE"
    CLEAR: Final[str] = "Clear"
    SAVE: Final[str] = "Save"
    EXPORT: Final[str] = "Export"
    CLOSE: Final[str] = "✕"


# ============================================================================
# Enum Types
# ============================================================================
class SearchType(Enum):
    """Search type enumeration."""

    WEATHER = "weather"
    CHARACTER = "character"


class PredictionType(Enum):
    """ML prediction type enumeration."""

    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    SEVERE_WEATHER = "severe_weather"


class LogLevel(Enum):
    """Log level enumeration."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"


class Faction(Enum):
    """Character faction enumeration."""

    COBRA = "Cobra"
    GI_JOE = "G.I. Joe"
    INDEPENDENT = "Independent"
    UNKNOWN = "Unknown"
