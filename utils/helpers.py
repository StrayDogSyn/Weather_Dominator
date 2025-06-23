"""
utils/helpers.py - Utility functions for data formatting, image loading, and API response parsing
Write a function to format temperature units (F/C), apply theme styles to widgets, and cache images locally.
"""

import os
import json
import urllib.request
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import tkinter as tk
import io

# Try to import PIL, but provide fallbacks if not available
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    print("⚠️ PIL (Pillow) not available. Image features will be disabled.")
    PIL_AVAILABLE = False
    # Create fallback classes
    class MockImage:
        class Resampling:
            LANCZOS = None
        
        @staticmethod
        def open(*args, **kwargs):
            return MockImageInstance()
        @staticmethod
        def new(*args, **kwargs):
            return MockImageInstance()
    
    class MockImageInstance:
        def resize(self, *args, **kwargs):
            return self
    
    class MockImageTk:
        @staticmethod
        def PhotoImage(*args, **kwargs):
            return None
    
    Image = MockImage()
    ImageTk = MockImageTk()

class TemperatureConverter:
    """Utility class for temperature conversions and formatting"""
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius"""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def kelvin_to_fahrenheit(kelvin: float) -> float:
        """Convert Kelvin to Fahrenheit"""
        return (kelvin - 273.15) * 9/5 + 32
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius"""
        return kelvin - 273.15
    
    @staticmethod
    def format_temperature(temp: float, unit: str = "F", decimals: int = 0) -> str:
        """
        Format temperature with proper unit symbol
        
        Args:
            temp: Temperature value
            unit: Unit ("F", "C", or "K")
            decimals: Number of decimal places
            
        Returns:
            Formatted temperature string
        """
        if temp is None:
            return "--°"
        
        unit_symbols = {"F": "°F", "C": "°C", "K": "K"}
        symbol = unit_symbols.get(unit.upper(), "°")
        
        return f"{temp:.{decimals}f}{symbol}"
    
    @staticmethod
    def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
        """
        Convert temperature between units
        
        Args:
            temp: Temperature value
            from_unit: Source unit ("F", "C", "K")
            to_unit: Target unit ("F", "C", "K")
            
        Returns:
            Converted temperature
        """
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()
        
        if from_unit == to_unit:
            return temp
        
        # Convert to Celsius first
        if from_unit == "F":
            celsius = TemperatureConverter.fahrenheit_to_celsius(temp)
        elif from_unit == "K":
            celsius = TemperatureConverter.kelvin_to_celsius(temp)
        else:
            celsius = temp
        
        # Convert from Celsius to target
        if to_unit == "F":
            return TemperatureConverter.celsius_to_fahrenheit(celsius)
        elif to_unit == "K":
            return celsius + 273.15
        else:
            return celsius

class ThemeStyler:
    """Utility class for applying consistent theme styles to widgets"""
    
    def __init__(self, theme_config):
        """
        Initialize with theme configuration
        
        Args:
            theme_config: Theme configuration object
        """
        self.theme = theme_config
    
    def style_label(self, label: tk.Label, style_type: str = "default") -> tk.Label:
        """
        Apply theme styling to a label
        
        Args:
            label: Tkinter Label widget
            style_type: Style type ("default", "title", "subtitle", "muted")
            
        Returns:
            Styled label widget
        """
        styles = {
            "default": {
                "fg": self.theme.TEXT_COLOR,
                "bg": self.theme.CONTENT_BG,
                "font": self.theme.BODY_FONT
            },
            "title": {
                "fg": self.theme.TITLE_COLOR,
                "bg": self.theme.CONTENT_BG,
                "font": self.theme.TITLE_FONT
            },
            "subtitle": {
                "fg": self.theme.SUBTITLE_COLOR,
                "bg": self.theme.CONTENT_BG,
                "font": self.theme.SUBTITLE_FONT
            },
            "muted": {
                "fg": self.theme.MUTED_TEXT,
                "bg": self.theme.CONTENT_BG,
                "font": self.theme.BODY_FONT
            }
        }
        
        style = styles.get(style_type, styles["default"])
        label.configure(**style)
        return label
    
    def style_button(self, button: tk.Button, style_type: str = "primary") -> tk.Button:
        """
        Apply theme styling to a button
        
        Args:
            button: Tkinter Button widget
            style_type: Style type ("primary", "secondary", "danger")
            
        Returns:
            Styled button widget
        """
        styles = {
            "primary": {
                "bg": self.theme.PRIMARY_ACCENT,
                "fg": "#ffffff",
                "activebackground": self.theme.HIGHLIGHT,
                "font": self.theme.BUTTON_FONT
            },
            "secondary": {
                "bg": self.theme.BUTTON_BG,
                "fg": self.theme.TEXT_COLOR,
                "activebackground": self.theme.BUTTON_HOVER_BG,
                "font": self.theme.BUTTON_FONT
            },
            "danger": {
                "bg": self.theme.DANGER_COLOR,
                "fg": "#ffffff",
                "activebackground": "#c82333",
                "font": self.theme.BUTTON_FONT
            }
        }
        
        style = styles.get(style_type, styles["primary"])
        common_style = {
            "relief": "flat",
            "bd": 0,
            "padx": 15,
            "pady": 8,
            "cursor": "hand2"
        }
        
        button.configure(**style, **common_style)
        return button
    
    def style_frame(self, frame: tk.Frame, style_type: str = "default") -> tk.Frame:
        """
        Apply theme styling to a frame
        
        Args:
            frame: Tkinter Frame widget
            style_type: Style type ("default", "glass", "container")
            
        Returns:
            Styled frame widget
        """
        styles = {
            "default": {
                "bg": self.theme.CONTENT_BG,
                "relief": "flat",
                "bd": 0
            },
            "glass": {
                "bg": self.theme.GLASS_BG,
                "relief": "raised",
                "bd": self.theme.BORDER_WIDTH,
                "highlightbackground": self.theme.BORDER,
                "highlightthickness": 1
            },
            "container": {
                "bg": self.theme.CONTAINER_BG,
                "relief": "flat",
                "bd": 0
            }
        }
        
        style = styles.get(style_type, styles["default"])
        frame.configure(**style)
        return frame

class ImageCache:
    """Utility class for caching and loading images locally"""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize image cache
        
        Args:
            cache_dir: Directory to store cached images
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.loaded_images = {}  # In-memory cache
    
    def get_image_from_url(self, url: str, size: tuple = (64, 64)) -> Optional[Any]:
        """
        Get image from URL with local caching
        
        Args:
            url: Image URL
            size: Desired image size (width, height)
            
        Returns:
            PhotoImage object or None if failed
        """
        if not url or not PIL_AVAILABLE:
            return None
        
        # Create cache filename
        filename = self._url_to_filename(url)
        cache_path = os.path.join(self.cache_dir, filename)
        
        # Check in-memory cache first
        cache_key = f"{url}_{size[0]}x{size[1]}"
        if cache_key in self.loaded_images:
            return self.loaded_images[cache_key]
        
        try:
            # Try to load from disk cache
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    image_data = f.read()
            else:
                # Download and cache
                with urllib.request.urlopen(url, timeout=10) as response:
                    image_data = response.read()
                
                # Save to cache
                with open(cache_path, 'wb') as f:
                    f.write(image_data)
              # Load and resize image
            image = Image.open(io.BytesIO(image_data))
            image = image.resize(size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo_image = ImageTk.PhotoImage(image)
            
            # Cache in memory
            self.loaded_images[cache_key] = photo_image
            
            return photo_image
            
        except Exception as e:
            print(f"⚠️ Error loading image from {url}: {e}")
            return None
    
    def get_placeholder_image(self, size: tuple = (64, 64), color: str = "#4a6fa5") -> Any:
        """
        Create a placeholder image
        
        Args:
            size: Image size (width, height)
            color: Background color
            
        Returns:
            Placeholder PhotoImage
        """
        if not PIL_AVAILABLE:
            return None
            
        cache_key = f"placeholder_{size[0]}x{size[1]}_{color}"
        
        if cache_key in self.loaded_images:
            return self.loaded_images[cache_key]
        
        try:
            # Create placeholder image
            image = Image.new('RGB', size, color)
            photo_image = ImageTk.PhotoImage(image)
            
            # Cache in memory
            self.loaded_images[cache_key] = photo_image
            
            return photo_image
            
        except Exception as e:
            print(f"⚠️ Error creating placeholder image: {e}")
            return None
    
    def clear_cache(self, max_age_days: int = 7):
        """
        Clear old cached images
        
        Args:
            max_age_days: Maximum age in days before clearing
        """
        try:
            cutoff_time = datetime.now() - timedelta(days=max_age_days)
            
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        print(f"🗑️ Removed old cached image: {filename}")
            
            # Clear in-memory cache
            self.loaded_images.clear()
            print("✅ Image cache cleared")
            
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")
    
    def _url_to_filename(self, url: str) -> str:
        """Convert URL to safe filename"""
        import hashlib
        
        # Create hash of URL for filename
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        # Try to get file extension from URL
        try:
            extension = url.split('.')[-1].split('?')[0]
            if extension.lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                return f"{url_hash}.{extension}"
        except:
            pass
        
        return f"{url_hash}.png"

class DataFormatter:
    """Utility class for formatting various data types"""
    
    @staticmethod
    def format_wind_speed(speed: float, unit: str = "mph") -> str:
        """
        Format wind speed with unit
        
        Args:
            speed: Wind speed value
            unit: Unit ("mph", "kmh", "ms")
            
        Returns:
            Formatted wind speed string
        """
        if speed is None:
            return "-- mph"
        
        unit_labels = {"mph": "mph", "kmh": "km/h", "ms": "m/s"}
        label = unit_labels.get(unit, "mph")
        
        return f"{speed:.1f} {label}"
    
    @staticmethod
    def format_pressure(pressure: float, unit: str = "hPa") -> str:
        """
        Format atmospheric pressure
        
        Args:
            pressure: Pressure value
            unit: Unit ("hPa", "inHg", "mmHg")
            
        Returns:
            Formatted pressure string
        """
        if pressure is None:
            return "-- hPa"
        
        if unit == "inHg":
            pressure = pressure * 0.02953  # Convert hPa to inHg
        elif unit == "mmHg":
            pressure = pressure * 0.75006  # Convert hPa to mmHg
        
        return f"{pressure:.1f} {unit}"
    
    @staticmethod
    def format_humidity(humidity: int) -> str:
        """Format humidity percentage"""
        if humidity is None:
            return "--%"
        return f"{humidity}%"
    
    @staticmethod
    def format_visibility(visibility: float, unit: str = "km") -> str:
        """
        Format visibility distance
        
        Args:
            visibility: Visibility in km
            unit: Unit ("km" or "mi")
            
        Returns:
            Formatted visibility string
        """
        if visibility is None:
            return "-- km"
        
        if unit == "mi":
            visibility = visibility * 0.621371  # Convert km to miles
        
        return f"{visibility:.1f} {unit}"
    
    @staticmethod
    def format_time_ago(timestamp: str) -> str:
        """
        Format timestamp as 'time ago' string
        
        Args:
            timestamp: Timestamp string
            
        Returns:
            Human-readable time ago string
        """
        try:
            time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            diff = now - time_obj
            
            if diff.days > 0:
                return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                return "Just now"
                
        except:
            return "Unknown"

class ConfigManager:
    """Utility class for managing application configuration"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize configuration manager
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "api_keys": {
                "openweather": None
            },
            "preferences": {
                "temperature_unit": "F",
                "wind_unit": "mph",
                "pressure_unit": "hPa",
                "theme": "default"
            },
            "cache": {
                "max_age_days": 7,
                "max_size_mb": 50
            },
            "database": {
                "path": "weather_dominator.db",
                "cleanup_days": 30
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                
                # Merge with defaults
                default_config.update(loaded_config)
            
            return default_config
            
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
            return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print("✅ Configuration saved")
            
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Configuration key path (e.g., "preferences.temperature_unit")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key_path: Configuration key path
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to parent key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value

# Convenience functions
def format_temp(temp: float, unit: str = "F") -> str:
    """Convenience function to format temperature"""
    return TemperatureConverter.format_temperature(temp, unit)

def convert_temp(temp: float, from_unit: str, to_unit: str) -> float:
    """Convenience function to convert temperature"""
    return TemperatureConverter.convert_temperature(temp, from_unit, to_unit)

def create_styler(theme_config):
    """Convenience function to create theme styler"""
    return ThemeStyler(theme_config)

def create_image_cache(cache_dir: str = "cache"):
    """Convenience function to create image cache"""
    return ImageCache(cache_dir)

def create_config_manager(config_file: str = "config.json"):
    """Convenience function to create config manager"""
    return ConfigManager(config_file)

# Example usage and testing
if __name__ == "__main__":
    print("🛠️ Testing utility functions...")
    
    # Test temperature conversion
    print(f"72°F = {TemperatureConverter.fahrenheit_to_celsius(72):.1f}°C")
    print(f"25°C = {TemperatureConverter.celsius_to_fahrenheit(25):.1f}°F")
    print(f"Temperature format: {TemperatureConverter.format_temperature(72.5, 'F', 1)}")
    
    # Test data formatting
    print(f"Wind speed: {DataFormatter.format_wind_speed(15.5)}")
    print(f"Pressure: {DataFormatter.format_pressure(1013.25)}")
    print(f"Humidity: {DataFormatter.format_humidity(65)}")
    print(f"Visibility: {DataFormatter.format_visibility(10.5)}")
    
    # Test config manager
    config = ConfigManager("test_config.json")
    print(f"Default temp unit: {config.get('preferences.temperature_unit')}")
    config.set('preferences.temperature_unit', 'C')
    print(f"Updated temp unit: {config.get('preferences.temperature_unit')}")
    
    print("🛠️ Utility functions test completed!")
