"""
Configuration management for Weather Dominator application.

This module provides centralized configuration management with support for
JSON config files, environment variables, and default values.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class APIKeys:
    """API key configuration."""
    openweather: Optional[str] = None
    fandom: Optional[str] = None


@dataclass
class Preferences:
    """User preferences configuration."""
    temperature_unit: str = "F"
    wind_unit: str = "mph"
    pressure_unit: str = "hPa"
    theme: str = "default"


@dataclass
class CacheSettings:
    """Cache configuration."""
    max_age_days: int = 7
    max_size_mb: int = 50


@dataclass
class DatabaseSettings:
    """Database configuration."""
    path: str = "weather_dominator.db"
    cleanup_days: int = 30


@dataclass
class AppConfig:
    """Main application configuration."""
    api_keys: APIKeys = field(default_factory=APIKeys)
    preferences: Preferences = field(default_factory=Preferences)
    cache: CacheSettings = field(default_factory=CacheSettings)
    database: DatabaseSettings = field(default_factory=DatabaseSettings)


class ConfigManager:
    """
    Centralized configuration manager.
    
    Handles loading, saving, and accessing configuration from multiple sources:
    1. JSON configuration file
    2. Environment variables
    3. Default values
    
    Attributes:
        config: Current application configuration
        config_path: Path to configuration file
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        self.config_path = self._resolve_config_path(config_path)
        self.config = self._load_config()
    
    def _resolve_config_path(self, config_path: Optional[str]) -> Path:
        """
        Resolve configuration file path.
        
        Args:
            config_path: Optional configuration path
            
        Returns:
            Resolved Path object
        """
        if config_path:
            return Path(config_path)
        
        # Check multiple locations
        possible_paths = [
            Path("config/config.json"),
            Path("config.json"),
            Path.home() / ".weather_dominator" / "config.json"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # Default to first location
        return possible_paths[0]
    
    def _load_config(self) -> AppConfig:
        """
        Load configuration from file and environment variables.
        
        Returns:
            Loaded application configuration
        """
        config = AppConfig()
        
        # Load from JSON file if exists
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                config = self._dict_to_config(data)
                logger.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}. Using defaults.")
        else:
            logger.info(f"Config file not found at {self.config_path}. Using defaults.")
        
        # Override with environment variables
        config = self._load_from_environment(config)
        
        return config
    
    def _dict_to_config(self, data: Dict[str, Any]) -> AppConfig:
        """
        Convert dictionary to AppConfig object.
        
        Args:
            data: Configuration dictionary
            
        Returns:
            AppConfig object
        """
        api_keys = APIKeys(**data.get('api_keys', {}))
        preferences = Preferences(**data.get('preferences', {}))
        cache = CacheSettings(**data.get('cache', {}))
        database = DatabaseSettings(**data.get('database', {}))
        
        return AppConfig(
            api_keys=api_keys,
            preferences=preferences,
            cache=cache,
            database=database
        )
    
    def _load_from_environment(self, config: AppConfig) -> AppConfig:
        """
        Load configuration from environment variables.
        
        Environment variables override JSON configuration.
        
        Args:
            config: Current configuration
            
        Returns:
            Updated configuration
        """
        # API Keys
        if openweather_key := os.getenv('OPENWEATHER_API_KEY'):
            config.api_keys.openweather = openweather_key
            logger.info("OpenWeather API key loaded from environment")
        
        if fandom_key := os.getenv('FANDOM_API_KEY'):
            config.api_keys.fandom = fandom_key
            logger.info("Fandom API key loaded from environment")
        
        # Preferences
        if temp_unit := os.getenv('TEMP_UNIT'):
            config.preferences.temperature_unit = temp_unit
        
        if wind_unit := os.getenv('WIND_UNIT'):
            config.preferences.wind_unit = wind_unit
        
        if theme := os.getenv('APP_THEME'):
            config.preferences.theme = theme
        
        # Database
        if db_path := os.getenv('DATABASE_PATH'):
            config.database.path = db_path
        
        return config
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dictionary
            config_dict = {
                'api_keys': asdict(self.config.api_keys),
                'preferences': asdict(self.config.preferences),
                'cache': asdict(self.config.cache),
                'database': asdict(self.config.database)
            }
            
            # Write to file
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def get_api_key(self, service: str) -> Optional[str]:
        """
        Get API key for a service.
        
        Args:
            service: Service name ('openweather' or 'fandom')
            
        Returns:
            API key or None if not configured
        """
        return getattr(self.config.api_keys, service, None)
    
    def set_api_key(self, service: str, key: str) -> bool:
        """
        Set API key for a service.
        
        Args:
            service: Service name
            key: API key value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            setattr(self.config.api_keys, service, key)
            return self.save_config()
        except Exception as e:
            logger.error(f"Failed to set API key: {e}")
            return False
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get user preference value.
        
        Args:
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value or default
        """
        return getattr(self.config.preferences, key, default)
    
    def set_preference(self, key: str, value: Any) -> bool:
        """
        Set user preference.
        
        Args:
            key: Preference key
            value: Preference value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            setattr(self.config.preferences, key, value)
            return self.save_config()
        except Exception as e:
            logger.error(f"Failed to set preference: {e}")
            return False
    
    def get_database_path(self) -> str:
        """
        Get database file path.
        
        Returns:
            Database path string
        """
        return self.config.database.path
    
    def is_api_configured(self, service: str) -> bool:
        """
        Check if API key is configured for a service.
        
        Args:
            service: Service name
            
        Returns:
            True if configured, False otherwise
        """
        key = self.get_api_key(service)
        return key is not None and len(key) > 0
    
    def validate_config(self) -> Dict[str, bool]:
        """
        Validate configuration.
        
        Returns:
            Dictionary with validation results for each component
        """
        return {
            'openweather_api': self.is_api_configured('openweather'),
            'fandom_api': self.is_api_configured('fandom'),
            'database_path': bool(self.config.database.path),
            'valid_units': self.config.preferences.temperature_unit in ['F', 'C'],
        }
    
    def get_config_summary(self) -> Dict[str, Any]:
        """
        Get configuration summary for display.
        
        Returns:
            Dictionary with configuration summary
        """
        return {
            'config_file': str(self.config_path),
            'config_exists': self.config_path.exists(),
            'openweather_configured': self.is_api_configured('openweather'),
            'fandom_configured': self.is_api_configured('fandom'),
            'temperature_unit': self.config.preferences.temperature_unit,
            'theme': self.config.preferences.theme,
            'database_path': self.config.database.path,
        }
    
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.config = AppConfig()
            return self.save_config()
        except Exception as e:
            logger.error(f"Failed to reset configuration: {e}")
            return False


# Singleton instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """
    Get singleton configuration manager instance.
    
    Args:
        config_path: Optional configuration path (only used on first call)
        
    Returns:
        ConfigManager instance
    """
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    
    return _config_manager


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create config manager
    config = ConfigManager()
    
    # Display config summary
    print("Configuration Summary:")
    print("=" * 50)
    summary = config.get_config_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Validation
    print("\nValidation Results:")
    print("=" * 50)
    validation = config.validate_config()
    for key, valid in validation.items():
        status = "✅" if valid else "❌"
        print(f"  {status} {key}")
