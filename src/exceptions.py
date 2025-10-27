"""
Custom exceptions for Weather Dominator application.

This module defines custom exception classes for better error handling
and more specific error messages throughout the application.
"""


class WeatherDominatorError(Exception):
    """Base exception class for all Weather Dominator errors."""
    
    def __init__(self, message: str, details: str = None):
        """
        Initialize exception.
        
        Args:
            message: Error message
            details: Optional additional details
        """
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return string representation."""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


# ============================================================================
# Configuration Errors
# ============================================================================

class ConfigurationError(WeatherDominatorError):
    """Raised when there's a configuration error."""
    pass


class APIKeyMissingError(ConfigurationError):
    """Raised when required API key is missing."""
    
    def __init__(self, service: str):
        super().__init__(
            f"API key missing for {service}",
            f"Please configure the API key in config.json or environment variables"
        )
        self.service = service


class InvalidConfigError(ConfigurationError):
    """Raised when configuration is invalid."""
    pass


# ============================================================================
# API Errors
# ============================================================================

class APIError(WeatherDominatorError):
    """Base class for API-related errors."""
    pass


class WeatherAPIError(APIError):
    """Raised when weather API request fails."""
    pass


class CharacterAPIError(APIError):
    """Raised when character API request fails."""
    pass


class NetworkError(APIError):
    """Raised when network connection fails."""
    pass


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""
    
    def __init__(self, service: str, retry_after: int = None):
        message = f"Rate limit exceeded for {service}"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(message)
        self.service = service
        self.retry_after = retry_after


class InvalidResponseError(APIError):
    """Raised when API response cannot be parsed."""
    pass


# ============================================================================
# Database Errors
# ============================================================================

class DatabaseError(WeatherDominatorError):
    """Base class for database errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails."""
    pass


class DatabaseInitializationError(DatabaseError):
    """Raised when database initialization fails."""
    pass


class DatabaseQueryError(DatabaseError):
    """Raised when database query fails."""
    pass


class DatabaseWriteError(DatabaseError):
    """Raised when database write operation fails."""
    pass


# ============================================================================
# Data Errors
# ============================================================================

class DataError(WeatherDominatorError):
    """Base class for data-related errors."""
    pass


class DataNotFoundError(DataError):
    """Raised when requested data is not found."""
    
    def __init__(self, data_type: str, identifier: str):
        super().__init__(
            f"{data_type} not found",
            f"No data found for {identifier}"
        )
        self.data_type = data_type
        self.identifier = identifier


class DataValidationError(DataError):
    """Raised when data validation fails."""
    pass


class DataParsingError(DataError):
    """Raised when data cannot be parsed."""
    pass


# ============================================================================
# UI Errors
# ============================================================================

class UIError(WeatherDominatorError):
    """Base class for UI-related errors."""
    pass


class WindowInitializationError(UIError):
    """Raised when window initialization fails."""
    pass


class ThemeLoadError(UIError):
    """Raised when theme cannot be loaded."""
    pass


# ============================================================================
# ML Errors
# ============================================================================

class MLError(WeatherDominatorError):
    """Base class for machine learning errors."""
    pass


class ModelNotTrainedError(MLError):
    """Raised when attempting to use untrained model."""
    pass


class PredictionError(MLError):
    """Raised when prediction fails."""
    pass


class InsufficientDataError(MLError):
    """Raised when there's insufficient data for training/prediction."""
    
    def __init__(self, required: int, available: int):
        super().__init__(
            "Insufficient data for operation",
            f"Required: {required}, Available: {available}"
        )
        self.required = required
        self.available = available


# ============================================================================
# Validation Errors
# ============================================================================

class ValidationError(WeatherDominatorError):
    """Base class for validation errors."""
    pass


class InvalidInputError(ValidationError):
    """Raised when user input is invalid."""
    pass


class InvalidCityError(InvalidInputError):
    """Raised when city name is invalid."""
    
    def __init__(self, city: str):
        super().__init__(
            "Invalid city name",
            f"'{city}' is not a valid city name"
        )
        self.city = city


class InvalidCharacterError(InvalidInputError):
    """Raised when character name is invalid."""
    
    def __init__(self, character: str):
        super().__init__(
            "Invalid character name",
            f"'{character}' is not a valid character name"
        )
        self.character = character


# ============================================================================
# File Errors
# ============================================================================

class FileError(WeatherDominatorError):
    """Base class for file-related errors."""
    pass


class FileNotFoundError(FileError):
    """Raised when required file is not found."""
    pass


class FileWriteError(FileError):
    """Raised when file write operation fails."""
    pass


class FileReadError(FileError):
    """Raised when file read operation fails."""
    pass


# ============================================================================
# Cache Errors
# ============================================================================

class CacheError(WeatherDominatorError):
    """Base class for cache-related errors."""
    pass


class CacheFullError(CacheError):
    """Raised when cache is full."""
    
    def __init__(self, current_size: float, max_size: float):
        super().__init__(
            "Cache is full",
            f"Current: {current_size}MB, Max: {max_size}MB"
        )
        self.current_size = current_size
        self.max_size = max_size


class CacheInvalidError(CacheError):
    """Raised when cached data is invalid or expired."""
    pass


# ============================================================================
# Helper Functions
# ============================================================================

def handle_error(error: Exception, fallback_message: str = "An error occurred") -> str:
    """
    Convert exception to user-friendly error message.
    
    Args:
        error: Exception instance
        fallback_message: Message to use if error is generic
        
    Returns:
        User-friendly error message
    """
    if isinstance(error, WeatherDominatorError):
        return str(error)
    return f"{fallback_message}: {str(error)}"


def is_recoverable(error: Exception) -> bool:
    """
    Check if error is recoverable.
    
    Args:
        error: Exception instance
        
    Returns:
        True if error is recoverable, False otherwise
    """
    recoverable_errors = (
        NetworkError,
        RateLimitError,
        CacheError,
        DataNotFoundError
    )
    return isinstance(error, recoverable_errors)


# Example usage
if __name__ == "__main__":
    # Demonstrate custom exceptions
    try:
        raise APIKeyMissingError("OpenWeatherMap")
    except WeatherDominatorError as e:
        print(f"Caught error: {e}")
        print(f"Recoverable: {is_recoverable(e)}")
    
    try:
        raise DataNotFoundError("Weather", "New York")
    except WeatherDominatorError as e:
        print(f"Caught error: {e}")
        print(f"Recoverable: {is_recoverable(e)}")
    
    try:
        raise InsufficientDataError(required=100, available=50)
    except WeatherDominatorError as e:
        print(f"Caught error: {e}")
        print(f"Recoverable: {is_recoverable(e)}")
