"""
ui/visual_features.py - Visual Features for Weather Dominator
Implements Temperature Graph, Weather Icons, and Theme Switcher
as specified in the project requirements.
"""

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    plt = None
    mdates = None
    FigureCanvasTkAgg = None
    Figure = None
    MATPLOTLIB_AVAILABLE = False

import tkinter as tk
from tkinter import ttk
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import requests
from io import BytesIO

from ..data.weather_features import WeatherFeatures

class VisualFeatures:
    """Visual features for weather data presentation"""
    
    def __init__(self, parent_widget=None):
        """
        Initialize visual features system
        
        Args:
            parent_widget: Parent tkinter widget for embedding graphs
        """
        self.parent = parent_widget
        self.weather_features = WeatherFeatures()
        self.current_theme = "light"
        
        # Weather icon mappings
        self.weather_icons = {
            "clear sky": "☀️",
            "few clouds": "🌤️",
            "scattered clouds": "⛅",
            "broken clouds": "☁️",
            "overcast clouds": "☁️",
            "light rain": "🌦️",
            "moderate rain": "🌧️",
            "heavy rain": "⛈️",
            "thunderstorm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️",
            "fog": "🌫️",
            "drizzle": "🌦️",
            "default": "🌡️"
        }
        
        # Color schemes for different themes
        self.color_schemes = {
            "light": {
                "background": "#FFFFFF",
                "text": "#000000",
                "primary": "#2E86AB",
                "secondary": "#A23B72",
                "accent": "#F18F01",
                "grid": "#E0E0E0",
                "temp_line": "#FF6B6B",
                "humidity_line": "#4ECDC4",
                "pressure_line": "#45B7D1"
            },
            "dark": {
                "background": "#2C3E50",
                "text": "#FFFFFF",
                "primary": "#3498DB",
                "secondary": "#E74C3C",
                "accent": "#F39C12",
                "grid": "#34495E",
                "temp_line": "#E74C3C",
                "humidity_line": "#1ABC9C",
                "pressure_line": "#3498DB"
            },
            "weather_based": {
                "sunny": {"bg": "#FFE4B5", "text": "#8B4513", "accent": "#FF8C00"},
                "cloudy": {"bg": "#D3D3D3", "text": "#2F4F4F", "accent": "#708090"},
                "rainy": {"bg": "#B0C4DE", "text": "#191970", "accent": "#4169E1"},
                "snowy": {"bg": "#F0F8FF", "text": "#483D8B", "accent": "#6495ED"}
            }
        }
    
    # =============================================================================
    # 1. TEMPERATURE GRAPH
    # =============================================================================
      def create_temperature_graph(self, city: str, days: int = 7, 
                               graph_type: str = "line") -> Any:
        """
        Create line graph of temperature history
        
        Args:
            city: City name for temperature data
            days: Number of days to display
            graph_type: Type of graph ("line", "bar", "area")
            
        Returns:
            Matplotlib figure object or None if matplotlib not available
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available. Please install matplotlib to use graphing features.")
            return None
            
        # Get temperature data
        weather_data = self.weather_features.display_last_7_days(city)
        
        if not weather_data:
            return self._create_no_data_graph(f"No temperature data for {city}")
        
        # Extract data for plotting
        dates = []
        temperatures = []
        feels_like = []
        descriptions = []
        
        for record in sorted(weather_data, key=lambda x: x['timestamp']):
            if record.get('temperature'):
                dates.append(datetime.fromisoformat(record['timestamp']))
                temperatures.append(record['temperature'])
                feels_like.append(record.get('feels_like', record['temperature']))
                descriptions.append(record.get('description', 'Unknown'))
        
        if not dates:
            return self._create_no_data_graph(f"No valid temperature readings for {city}")
        
        # Create figure with current theme colors
        colors = self.color_schemes[self.current_theme]
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor(colors["background"])
        ax.set_facecolor(colors["background"])
        
        # Plot based on graph type
        if graph_type == "line":
            ax.plot(dates, temperatures, 
                   color=colors["temp_line"], linewidth=2, 
                   marker='o', markersize=6, label='Temperature')
            ax.plot(dates, feels_like, 
                   color=colors["secondary"], linewidth=1, 
                   linestyle='--', alpha=0.7, label='Feels Like')
        
        elif graph_type == "bar":
            ax.bar(dates, temperatures, 
                  color=colors["temp_line"], alpha=0.7, label='Temperature')
        
        elif graph_type == "area":
            ax.fill_between(dates, temperatures, 
                           color=colors["temp_line"], alpha=0.3)
            ax.plot(dates, temperatures, 
                   color=colors["temp_line"], linewidth=2)
        
        # Customize the graph
        ax.set_title(f'Temperature History - {city} (Last {days} days)', 
                    color=colors["text"], fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', color=colors["text"], fontsize=12)
        ax.set_ylabel('Temperature (°F)', color=colors["text"], fontsize=12)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Style the graph
        ax.grid(True, color=colors["grid"], alpha=0.3)
        ax.tick_params(colors=colors["text"])
        ax.spines['bottom'].set_color(colors["text"])
        ax.spines['top'].set_color(colors["text"])
        ax.spines['right'].set_color(colors["text"])
        ax.spines['left'].set_color(colors["text"])
        
        if graph_type == "line":
            ax.legend(facecolor=colors["background"], 
                     edgecolor=colors["text"], labelcolor=colors["text"])
        
        plt.tight_layout()
        return fig
    
    def embed_graph_in_tkinter(self, parent_frame: tk.Widget, 
                              city: str, days: int = 7) -> FigureCanvasTkAgg:
        """
        Embed matplotlib graph in Tkinter widget
        
        Args:
            parent_frame: Tkinter frame to embed graph in
            city: City name for data
            days: Number of days to display
            
        Returns:
            Canvas object with embedded graph
        """
        fig = self.create_temperature_graph(city, days)
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return canvas
    
    def create_multi_metric_graph(self, city: str, days: int = 7) -> plt.Figure:
        """
        Create graph showing multiple weather metrics
        
        Args:
            city: City name
            days: Number of days to display
            
        Returns:
            Figure with multiple subplots
        """
        weather_data = self.weather_features.display_last_7_days(city)
        
        if not weather_data:
            return self._create_no_data_graph(f"No data for {city}")
        
        # Extract data
        dates = []
        temperatures = []
        humidity = []
        pressure = []
        wind_speed = []
        
        for record in sorted(weather_data, key=lambda x: x['timestamp']):
            dates.append(datetime.fromisoformat(record['timestamp']))
            temperatures.append(record.get('temperature', 0))
            humidity.append(record.get('humidity', 0))
            pressure.append(record.get('pressure', 0))
            wind_speed.append(record.get('wind_speed', 0))
        
        colors = self.color_schemes[self.current_theme]
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.patch.set_facecolor(colors["background"])
        
        # Temperature plot
        ax1.plot(dates, temperatures, color=colors["temp_line"], linewidth=2, marker='o')
        ax1.set_title('Temperature', color=colors["text"], fontweight='bold')
        ax1.set_ylabel('°F', color=colors["text"])
        self._style_subplot(ax1, colors)
        
        # Humidity plot
        ax2.plot(dates, humidity, color=colors["humidity_line"], linewidth=2, marker='s')
        ax2.set_title('Humidity', color=colors["text"], fontweight='bold')
        ax2.set_ylabel('%', color=colors["text"])
        self._style_subplot(ax2, colors)
        
        # Pressure plot
        ax3.plot(dates, pressure, color=colors["pressure_line"], linewidth=2, marker='^')
        ax3.set_title('Pressure', color=colors["text"], fontweight='bold')
        ax3.set_ylabel('inHg', color=colors["text"])
        self._style_subplot(ax3, colors)
        
        # Wind speed plot
        ax4.plot(dates, wind_speed, color=colors["accent"], linewidth=2, marker='d')
        ax4.set_title('Wind Speed', color=colors["text"], fontweight='bold')
        ax4.set_ylabel('mph', color=colors["text"])
        self._style_subplot(ax4, colors)
        
        plt.tight_layout()
        return fig
    
    # =============================================================================
    # 2. WEATHER ICONS
    # =============================================================================
    
    def get_weather_icon(self, weather_description: str, size: int = 64) -> str:
        """
        Get Unicode weather icon for description
        
        Args:
            weather_description: Weather condition description
            size: Icon size (for future image-based icons)
            
        Returns:
            Unicode weather icon
        """
        description_lower = weather_description.lower()
        
        for condition, icon in self.weather_icons.items():
            if condition in description_lower:
                return icon
        
        return self.weather_icons["default"]
    
    def create_canvas_weather_representation(self, weather_data: Dict[str, Any], 
                                           width: int = 300, height: int = 200) -> Image.Image:
        """
        Create canvas-based weather representation
        
        Args:
            weather_data: Weather data dictionary
            width: Canvas width
            height: Canvas height
            
        Returns:
            PIL Image object
        """
        # Create image
        img = Image.new('RGB', (width, height), self._get_weather_background_color(weather_data))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font_large = ImageFont.truetype("arial.ttf", 48)
            font_medium = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Get weather info
        temp = weather_data.get('temperature', 'N/A')
        description = weather_data.get('description', 'Unknown')
        city = weather_data.get('city', 'Unknown')
        icon = self.get_weather_icon(description)
        
        # Draw weather icon (large)
        icon_x = width // 2 - 30
        icon_y = 20
        draw.text((icon_x, icon_y), icon, font=font_large, fill='white')
        
        # Draw temperature
        temp_text = f"{temp}°F" if temp != 'N/A' else 'N/A'
        temp_bbox = draw.textbbox((0, 0), temp_text, font=font_medium)
        temp_width = temp_bbox[2] - temp_bbox[0]
        temp_x = width // 2 - temp_width // 2
        draw.text((temp_x, 90), temp_text, font=font_medium, fill='white')
        
        # Draw description
        desc_bbox = draw.textbbox((0, 0), description.title(), font=font_small)
        desc_width = desc_bbox[2] - desc_bbox[0]
        desc_x = width // 2 - desc_width // 2
        draw.text((desc_x, 130), description.title(), font=font_small, fill='white')
        
        # Draw city name
        city_bbox = draw.textbbox((0, 0), city, font=font_small)
        city_width = city_bbox[2] - city_bbox[0]
        city_x = width // 2 - city_width // 2
        draw.text((city_x, 160), city, font=font_small, fill='lightgray')
        
        return img
    
    def create_color_coded_conditions(self, weather_data: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
        """
        Create color-coded condition indicators
        
        Args:
            weather_data: List of weather records
            
        Returns:
            List of (condition, color) tuples
        """
        conditions = []
        
        for record in weather_data:
            temp = record.get('temperature', 0)
            description = record.get('description', '').lower()
            
            # Temperature-based colors
            if temp >= 80:
                temp_color = "#FF4444"  # Hot - Red
            elif temp >= 70:
                temp_color = "#FF8800"  # Warm - Orange
            elif temp >= 60:
                temp_color = "#FFDD00"  # Mild - Yellow
            elif temp >= 40:
                temp_color = "#44AA44"  # Cool - Green
            else:
                temp_color = "#4488FF"  # Cold - Blue
            
            # Weather condition colors
            if any(word in description for word in ['rain', 'drizzle', 'shower']):
                condition_color = "#6699FF"  # Rainy - Light Blue
            elif any(word in description for word in ['storm', 'thunder']):
                condition_color = "#8844AA"  # Stormy - Purple
            elif any(word in description for word in ['snow', 'blizzard']):
                condition_color = "#FFFFFF"  # Snowy - White
            elif any(word in description for word in ['cloud', 'overcast']):
                condition_color = "#AAAAAA"  # Cloudy - Gray
            elif any(word in description for word in ['clear', 'sunny']):
                condition_color = "#FFAA00"  # Sunny - Gold
            else:
                condition_color = "#888888"  # Unknown - Dark Gray
            
            date = record.get('timestamp', '')[:10]
            conditions.append((f"{date}: {temp}°F - {description.title()}", temp_color))
        
        return conditions
    
    def create_simple_animations(self, weather_type: str) -> List[str]:
        """
        Create simple text-based animations for weather types
        
        Args:
            weather_type: Type of weather
            
        Returns:
            List of animation frames
        """
        animations = {
            "sunny": ["☀️", "🌞", "☀️", "🌞"],
            "cloudy": ["☁️", "⛅", "☁️", "⛅"],
            "rainy": ["🌦️", "🌧️", "⛈️", "🌧️"],
            "snowy": ["❄️", "🌨️", "❄️", "🌨️"],
            "windy": ["💨", "🌪️", "💨", "🌪️"],
            "foggy": ["🌫️", "🌁", "🌫️", "🌁"]
        }
        
        weather_lower = weather_type.lower()
        for condition, frames in animations.items():
            if condition in weather_lower:
                return frames
        
        return ["🌡️", "📊", "🌡️", "📊"]  # Default animation
    
    # =============================================================================
    # 3. THEME SWITCHER
    # =============================================================================
    
    def set_day_night_mode(self, mode: str) -> Dict[str, str]:
        """
        Set day/night mode themes
        
        Args:
            mode: "day", "night", or "auto"
            
        Returns:
            Current theme colors
        """
        if mode == "day":
            self.current_theme = "light"
        elif mode == "night":
            self.current_theme = "dark"
        elif mode == "auto":
            # Auto-detect based on time
            current_hour = datetime.now().hour
            if 6 <= current_hour <= 18:
                self.current_theme = "light"
            else:
                self.current_theme = "dark"
        
        return self.color_schemes[self.current_theme]
    
    def apply_weather_based_colors(self, weather_condition: str) -> Dict[str, str]:
        """
        Apply weather-based color themes
        
        Args:
            weather_condition: Current weather condition
            
        Returns:
            Weather-based theme colors
        """
        condition_lower = weather_condition.lower()
        weather_themes = self.color_schemes["weather_based"]
        
        if any(word in condition_lower for word in ['clear', 'sunny']):
            return weather_themes["sunny"]
        elif any(word in condition_lower for word in ['rain', 'storm', 'drizzle']):
            return weather_themes["rainy"]
        elif any(word in condition_lower for word in ['snow', 'blizzard']):
            return weather_themes["snowy"]
        elif any(word in condition_lower for word in ['cloud', 'overcast']):
            return weather_themes["cloudy"]
        else:
            return self.color_schemes[self.current_theme]
    
    def save_user_preferences(self, preferences: Dict[str, Any]) -> bool:
        """
        Save user theme preferences
        
        Args:
            preferences: User preference dictionary
            
        Returns:
            Success status
        """
        try:
            prefs_file = "data/user_preferences.json"
            os.makedirs(os.path.dirname(prefs_file), exist_ok=True)
            
            # Load existing preferences
            existing_prefs = {}
            if os.path.exists(prefs_file):
                with open(prefs_file, 'r') as f:
                    existing_prefs = json.load(f)
            
            # Update with new preferences
            existing_prefs.update(preferences)
            
            # Save updated preferences
            with open(prefs_file, 'w') as f:
                json.dump(existing_prefs, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
    
    def load_user_preferences(self) -> Dict[str, Any]:
        """
        Load user theme preferences
        
        Returns:
            User preferences dictionary
        """
        try:
            prefs_file = "data/user_preferences.json"
            if os.path.exists(prefs_file):
                with open(prefs_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading preferences: {e}")
        
        # Return default preferences
        return {
            "theme": "light",
            "auto_theme": False,
            "weather_based_colors": True,
            "animation_enabled": True,
            "graph_type": "line"
        }
    
    def create_theme_selector_widget(self, parent: tk.Widget) -> ttk.Frame:
        """
        Create theme selector widget
        
        Args:
            parent: Parent widget
            
        Returns:
            Theme selector frame
        """
        frame = ttk.Frame(parent)
        
        # Theme selection
        ttk.Label(frame, text="Theme:").grid(row=0, column=0, padx=5, pady=5)
        
        theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(frame, textvariable=theme_var, 
                                  values=["light", "dark", "auto"],
                                  state="readonly")
        theme_combo.grid(row=0, column=1, padx=5, pady=5)
        
        def on_theme_change(*args):
            new_theme = theme_var.get()
            self.set_day_night_mode(new_theme)
            self.save_user_preferences({"theme": new_theme})
        
        theme_combo.bind('<<ComboboxSelected>>', on_theme_change)
        
        # Weather-based colors checkbox
        weather_colors_var = tk.BooleanVar(value=True)
        weather_colors_check = ttk.Checkbutton(
            frame, text="Weather-based colors", 
            variable=weather_colors_var
        )
        weather_colors_check.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        def on_weather_colors_change():
            self.save_user_preferences({
                "weather_based_colors": weather_colors_var.get()
            })
        
        weather_colors_check.configure(command=on_weather_colors_change)
        
        return frame
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _create_no_data_graph(self, message: str) -> plt.Figure:
        """Create a graph showing no data message"""
        colors = self.color_schemes[self.current_theme]
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(colors["background"])
        ax.set_facecolor(colors["background"])
        
        ax.text(0.5, 0.5, message, transform=ax.transAxes,
                ha='center', va='center', fontsize=16,
                color=colors["text"], fontweight='bold')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        return fig
    
    def _style_subplot(self, ax: plt.Axes, colors: Dict[str, str]):
        """Apply consistent styling to subplot"""
        ax.set_facecolor(colors["background"])
        ax.grid(True, color=colors["grid"], alpha=0.3)
        ax.tick_params(colors=colors["text"])
        
        for spine in ax.spines.values():
            spine.set_color(colors["text"])
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, color=colors["text"])
    
    def _get_weather_background_color(self, weather_data: Dict[str, Any]) -> Tuple[int, int, int]:
        """Get background color based on weather condition"""
        description = weather_data.get('description', '').lower()
        temp = weather_data.get('temperature', 70)
        
        if 'rain' in description or 'storm' in description:
            return (70, 130, 180)  # Steel Blue
        elif 'snow' in description:
            return (176, 196, 222)  # Light Steel Blue
        elif 'cloud' in description:
            return (119, 136, 153)  # Light Slate Gray
        elif 'clear' in description or 'sunny' in description:
            if temp >= 80:
                return (255, 165, 0)  # Orange
            else:
                return (135, 206, 235)  # Sky Blue
        else:
            return (105, 105, 105)  # Dim Gray
    
    def export_graph_image(self, figure: plt.Figure, filename: str = None) -> str:
        """
        Export graph as image file
        
        Args:
            figure: Matplotlib figure to export
            filename: Optional custom filename
            
        Returns:
            Path to exported image
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weather_graph_{timestamp}.png"
        
        filepath = os.path.join("data", "exports", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        figure.savefig(filepath, dpi=300, bbox_inches='tight')
        return filepath

# Convenience functions for easy use
def create_temperature_plot(city: str, days: int = 7, theme: str = "light") -> plt.Figure:
    """Create temperature plot with specified theme"""
    visual = VisualFeatures()
    visual.current_theme = theme
    return visual.create_temperature_graph(city, days)

def get_weather_emoji(description: str) -> str:
    """Get weather emoji for condition"""
    visual = VisualFeatures()
    return visual.get_weather_icon(description)

def create_weather_widget(parent: tk.Widget, weather_data: Dict[str, Any]) -> tk.Label:
    """Create weather display widget"""
    visual = VisualFeatures()
    icon = visual.get_weather_icon(weather_data.get('description', ''))
    temp = weather_data.get('temperature', 'N/A')
    
    text = f"{icon} {temp}°F"
    return tk.Label(parent, text=text, font=('Arial', 16))

# Example usage and testing
if __name__ == "__main__":
    # Test Visual Features
    visual = VisualFeatures()
    
    print("🎨 Visual Features Test")
    print("=" * 30)
    
    test_city = "New York"
    
    # Test 1: Temperature Graph
    print(f"\n📈 Testing Temperature Graph for {test_city}:")
    try:
        fig = visual.create_temperature_graph(test_city, 7)
        export_path = visual.export_graph_image(fig, "test_temp_graph.png")
        print(f"✅ Temperature graph created and exported to: {export_path}")
        plt.close(fig)
    except Exception as e:
        print(f"❌ Temperature graph error: {e}")
    
    # Test 2: Weather Icons
    print(f"\n🌤️ Testing Weather Icons:")
    test_conditions = ["clear sky", "light rain", "snow", "thunderstorm"]
    for condition in test_conditions:
        icon = visual.get_weather_icon(condition)
        print(f"✅ {condition}: {icon}")
    
    # Test 3: Theme Switching
    print(f"\n🎨 Testing Theme Switching:")
    themes = ["light", "dark"]
    for theme in themes:
        colors = visual.set_day_night_mode(theme)
        print(f"✅ {theme.title()} theme: background={colors['background']}")
    
    # Test 4: Weather-based Colors
    print(f"\n🌈 Testing Weather-based Colors:")
    weather_conditions = ["sunny", "rainy", "snowy", "cloudy"]
    for condition in weather_conditions:
        colors = visual.apply_weather_based_colors(condition)
        print(f"✅ {condition}: {colors}")
    
    # Test 5: User Preferences
    print(f"\n⚙️ Testing User Preferences:")
    test_prefs = {
        "theme": "dark",
        "weather_based_colors": True,
        "animation_enabled": False
    }
    
    success = visual.save_user_preferences(test_prefs)
    print(f"✅ Preferences saved: {success}")
    
    loaded_prefs = visual.load_user_preferences()
    print(f"✅ Preferences loaded: {len(loaded_prefs)} settings")
    
    print(f"\n🎨 Visual Features Test Complete!")
