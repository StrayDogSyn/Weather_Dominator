"""
Tests for application constants.
"""

import pytest

from src.constants import (  # Application metadata; Window dimensions; Theme classes; API configuration; Enums
    APP_DESCRIPTION, APP_NAME, APP_VERSION, GIJOE_FANDOM_API, GIJOE_WIKI_URL,
    OPENWEATHER_BASE_URL, WINDOW_HEIGHT, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH,
    WINDOW_WIDTH, CobraThemeColors, Faction, FontConfig, LogLevel,
    PredictionType, SearchType, ThemeColors)


class TestModuleLevelConstants:
    """Test module-level application constants."""
    
    def test_app_metadata_exists(self):
        """Test that app metadata constants are defined."""
        assert isinstance(APP_NAME, str)
        assert isinstance(APP_VERSION, str)
        assert isinstance(APP_DESCRIPTION, str)
        assert len(APP_NAME) > 0
        assert len(APP_VERSION) > 0
    
    def test_window_dimensions(self):
        """Test window dimension constants."""
        assert isinstance(WINDOW_WIDTH, int)
        assert isinstance(WINDOW_HEIGHT, int)
        assert isinstance(WINDOW_MIN_WIDTH, int)
        assert isinstance(WINDOW_MIN_HEIGHT, int)
        assert WINDOW_WIDTH > 0
        assert WINDOW_HEIGHT > 0
        assert WINDOW_WIDTH >= WINDOW_MIN_WIDTH
        assert WINDOW_HEIGHT >= WINDOW_MIN_HEIGHT
    
    def test_api_urls(self):
        """Test API URL constants."""
        assert isinstance(OPENWEATHER_BASE_URL, str)
        assert isinstance(GIJOE_FANDOM_API, str)
        assert isinstance(GIJOE_WIKI_URL, str)
        assert OPENWEATHER_BASE_URL.startswith('http')
        assert GIJOE_FANDOM_API.startswith('http')
        assert GIJOE_WIKI_URL.startswith('http')


class TestThemeColors:
    """Test ThemeColors class attributes."""
    
    def test_theme_colors_exist(self):
        """Test that theme color attributes exist."""
        # Background colors
        assert hasattr(ThemeColors, 'WINDOW_BG')
        assert hasattr(ThemeColors, 'CONTAINER_BG')
        assert hasattr(ThemeColors, 'GLASS_BG')
        
        # Accent colors
        assert hasattr(ThemeColors, 'PRIMARY_ACCENT')
        assert hasattr(ThemeColors, 'SECONDARY_ACCENT')
        
        # Text colors
        assert hasattr(ThemeColors, 'TITLE_COLOR')
        assert hasattr(ThemeColors, 'TEXT_COLOR')
    
    def test_theme_colors_are_strings(self):
        """Test that theme colors are hex color strings."""
        colors = [
            ThemeColors.WINDOW_BG,
            ThemeColors.PRIMARY_ACCENT,
            ThemeColors.TEXT_COLOR
        ]
        
        for color in colors:
            assert isinstance(color, str)
            assert color.startswith('#')
    
    def test_cobra_theme_colors(self):
        """Test COBRA theme color overrides."""
        assert hasattr(CobraThemeColors, 'PRIMARY_ACCENT')
        assert isinstance(CobraThemeColors.PRIMARY_ACCENT, str)
        assert CobraThemeColors.PRIMARY_ACCENT.startswith('#')


class TestFontConfig:
    """Test FontConfig class attributes."""
    
    def test_font_config_exists(self):
        """Test that font configuration attributes exist."""
        assert hasattr(FontConfig, 'FONT_FAMILY')
        assert hasattr(FontConfig, 'TITLE_SIZE')
        assert hasattr(FontConfig, 'BODY_SIZE')
        assert hasattr(FontConfig, 'SMALL_SIZE')
    
    def test_font_family(self):
        """Test font family is a string."""
        assert isinstance(FontConfig.FONT_FAMILY, str)
        assert len(FontConfig.FONT_FAMILY) > 0
    
    def test_font_sizes_are_positive(self):
        """Test that font sizes are positive integers."""
        sizes = [
            FontConfig.TITLE_SIZE,
            FontConfig.BODY_SIZE,
            FontConfig.SMALL_SIZE
        ]
        
        for size in sizes:
            assert isinstance(size, int)
            assert size > 0


class TestEnumerations:
    """Test enum classes."""
    
    def test_search_type_enum(self):
        """Test SearchType enumeration."""
        assert hasattr(SearchType, 'WEATHER')
        assert hasattr(SearchType, 'CHARACTER')
    
    def test_prediction_type_enum(self):
        """Test PredictionType enumeration."""
        assert hasattr(PredictionType, 'TEMPERATURE')
        assert hasattr(PredictionType, 'HUMIDITY')
        assert hasattr(PredictionType, 'SEVERE_WEATHER')
    
    def test_log_level_enum(self):
        """Test LogLevel enumeration."""
        assert hasattr(LogLevel, 'DEBUG')
        assert hasattr(LogLevel, 'INFO')
        assert hasattr(LogLevel, 'WARNING')
        assert hasattr(LogLevel, 'ERROR')
        assert hasattr(LogLevel, 'CRITICAL')
    
    def test_faction_enum(self):
        """Test Faction enumeration."""
        assert hasattr(Faction, 'COBRA')
        assert hasattr(Faction, 'GI_JOE')
        assert hasattr(Faction, 'INDEPENDENT')
        assert hasattr(Faction, 'UNKNOWN')


class TestConstantsIntegrity:
    """Test relationships and integrity between constants."""
    
    def test_window_min_dimensions_valid(self):
        """Test that minimum dimensions are reasonable."""
        assert WINDOW_MIN_WIDTH >= 400
        assert WINDOW_MIN_HEIGHT >= 300
    
    def test_font_sizes_ordered(self):
        """Test that font sizes follow logical ordering."""
        assert FontConfig.TITLE_SIZE > FontConfig.BODY_SIZE
        assert FontConfig.BODY_SIZE > FontConfig.SMALL_SIZE
    
    def test_api_urls_complete(self):
        """Test that all required API URLs are defined."""
        assert 'openweathermap.org' in OPENWEATHER_BASE_URL
        assert 'fandom.com' in GIJOE_FANDOM_API or 'wikia.com' in GIJOE_FANDOM_API
