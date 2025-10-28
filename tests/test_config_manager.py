"""
Tests for configuration management.
"""

import json
import os
import tempfile
from pathlib import Path
from threading import Thread

import pytest

from src.config_manager import (APIKeys, AppConfig, CacheSettings,
                                ConfigManager, DatabaseSettings, Preferences,
                                get_config_manager)
from src.exceptions import ConfigurationError


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    config_data = {
        'api_keys': {
            'openweather': 'test_weather_key_123',
            'fandom': 'test_fandom_key_456'
        },
        'preferences': {
            'temperature_unit': 'F',
            'wind_unit': 'mph',
            'pressure_unit': 'hPa',
            'theme': 'cobra'
        },
        'cache': {
            'max_age_days': 7,
            'max_size_mb': 50
        },
        'database': {
            'path': 'test_weather.db',
            'cleanup_days': 30
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
    except:
        pass


class TestConfigManager:
    """Test ConfigManager class."""
    
    def test_multiple_instances(self):
        """Test that ConfigManager can create multiple independent instances."""
        config1 = ConfigManager()
        config2 = ConfigManager()
        assert config1 is not config2
    
    def test_get_config_manager_function(self):
        """Test get_config_manager() helper function."""
        manager = get_config_manager()
        assert isinstance(manager, ConfigManager)
    
    def test_load_config_success(self, temp_config_file):
        """Test successful configuration loading."""
        config_manager = ConfigManager(temp_config_file)
        assert config_manager.config is not None
        assert hasattr(config_manager.config, 'api_keys')
        assert hasattr(config_manager.config, 'preferences')
    
    def test_get_api_key(self, temp_config_file):
        """Test getting API key."""
        config_manager = ConfigManager(temp_config_file)
        key = config_manager.get_api_key('openweather')
        assert key == 'test_weather_key_123'
    
    def test_get_missing_api_key(self, temp_config_file):
        """Test getting non-existent API key returns None."""
        config_manager = ConfigManager(temp_config_file)
        key = config_manager.get_api_key('nonexistent')
        assert key is None
    
    def test_set_api_key(self, temp_config_file):
        """Test setting API key."""
        config_manager = ConfigManager(temp_config_file)
        result = config_manager.set_api_key('openweather', 'new_key_789')
        assert result is True
        assert config_manager.get_api_key('openweather') == 'new_key_789'
    
    def test_get_preference(self, temp_config_file):
        """Test getting preference value."""
        config_manager = ConfigManager(temp_config_file)
        value = config_manager.get_preference('temperature_unit')
        assert value == 'F'
    
    def test_get_preference_with_default(self, temp_config_file):
        """Test getting non-existent preference with default."""
        config_manager = ConfigManager(temp_config_file)
        value = config_manager.get_preference('nonexistent', default='default_value')
        assert value == 'default_value'
    
    def test_set_preference(self, temp_config_file):
        """Test setting preference."""
        config_manager = ConfigManager(temp_config_file)
        result = config_manager.set_preference('temperature_unit', 'C')
        assert result is True
        assert config_manager.get_preference('temperature_unit') == 'C'
    
    def test_get_database_path(self, temp_config_file):
        """Test getting database path."""
        config_manager = ConfigManager(temp_config_file)
        path = config_manager.get_database_path()
        assert path == 'test_weather.db'
    
    def test_is_api_configured(self, temp_config_file):
        """Test checking if API is configured."""
        config_manager = ConfigManager(temp_config_file)
        assert config_manager.is_api_configured('openweather') is True
        assert config_manager.is_api_configured('nonexistent') is False
    
    def test_save_config(self, temp_config_file):
        """Test saving configuration."""
        config_manager = ConfigManager(temp_config_file)
        config_manager.set_api_key('openweather', 'updated_key')
        result = config_manager.save_config()
        assert result is True
        
        # Reload to verify
        new_manager = ConfigManager(temp_config_file)
        assert new_manager.get_api_key('openweather') == 'updated_key'
    
    def test_validate_config(self, temp_config_file):
        """Test configuration validation."""
        config_manager = ConfigManager(temp_config_file)
        validation = config_manager.validate_config()
        
        assert isinstance(validation, dict)
        assert 'openweather_api' in validation
        assert 'fandom_api' in validation
        assert validation['openweather_api'] is True
    
    def test_get_config_summary(self, temp_config_file):
        """Test getting config summary."""
        config_manager = ConfigManager(temp_config_file)
        summary = config_manager.get_config_summary()
        
        assert isinstance(summary, dict)
        assert 'config_file' in summary
        assert 'openweather_configured' in summary
        assert summary['temperature_unit'] == 'F'
    
    def test_reset_to_defaults(self, temp_config_file):
        """Test resetting configuration to defaults."""
        config_manager = ConfigManager(temp_config_file)
        config_manager.set_api_key('openweather', 'test_key')
        
        result = config_manager.reset_to_defaults()
        assert result is True
        assert config_manager.get_api_key('openweather') is None
    
    def test_invalid_config_file(self):
        """Test handling of invalid JSON config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json {{{")
            temp_path = f.name
        
        try:
            # Should use defaults on invalid file
            config_manager = ConfigManager(temp_path)
            assert isinstance(config_manager.config, AppConfig)
            assert config_manager.get_api_key('openweather') is None
        finally:
            os.unlink(temp_path)
    
    def test_missing_config_file(self):
        """Test handling of missing config file."""
        config_manager = ConfigManager('/nonexistent/path/config.json')
        # Should use defaults
        assert isinstance(config_manager.config, AppConfig)
        assert config_manager.get_api_key('openweather') is None
    
    def test_environment_variable_override(self, temp_config_file, monkeypatch):
        """Test environment variables override config file."""
        monkeypatch.setenv('OPENWEATHER_API_KEY', 'env_key_from_env')
        
        config_manager = ConfigManager(temp_config_file)
        key = config_manager.get_api_key('openweather')
        assert key == 'env_key_from_env'
    
    def test_thread_safety(self, temp_config_file):
        """Test concurrent access to ConfigManager."""
        results = []
        
        def create_manager():
            manager = ConfigManager(temp_config_file)
            results.append(manager)
        
        threads = [Thread(target=create_manager) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Should have 10 independent instances
        assert len(results) == 10
        assert len(set(id(r) for r in results)) == 10


class TestDataClasses:
    """Test configuration dataclasses."""
    
    def test_api_keys_dataclass(self):
        """Test APIKeys dataclass."""
        keys = APIKeys(openweather='key1', fandom='key2')
        assert keys.openweather == 'key1'
        assert keys.fandom == 'key2'
    
    def test_preferences_dataclass(self):
        """Test Preferences dataclass."""
        prefs = Preferences(temperature_unit='C', theme='cobra')
        assert prefs.temperature_unit == 'C'
        assert prefs.theme == 'cobra'
    
    def test_app_config_dataclass(self):
        """Test AppConfig dataclass."""
        config = AppConfig()
        assert isinstance(config.api_keys, APIKeys)
        assert isinstance(config.preferences, Preferences)
        assert isinstance(config.cache, CacheSettings)
        assert isinstance(config.database, DatabaseSettings)
