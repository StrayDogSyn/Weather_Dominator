"""
ui/glass_ui.py - Glassmorphic UI components for Weather Dominator
Implement glassmorphic panels for weather display, Cobra intelligence, and alert system.
Create a widget factory for consistent glass-styled components.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional
import io

# Try to import PIL, but provide fallbacks if not available
try:
    from PIL import Image, ImageTk # type: ignore
    PIL_AVAILABLE = True
except ImportError:
    print("⚠️ PIL (Pillow) not available. Image features will be disabled.")
    PIL_AVAILABLE = False
    # Create fallback classes
    class MockImage:
        @staticmethod
        def open(*args, **kwargs):
            return None
        @staticmethod
        def new(*args, **kwargs):
            return None
    
    class MockImageTk:
        @staticmethod
        def PhotoImage(*args, **kwargs):
            return None
    
    Image = MockImage()
    ImageTk = MockImageTk()

class GlassPanel(tk.Frame):
    """Base class for glassmorphic panels"""
    
    def __init__(self, parent, theme, title: str = "", **kwargs):
        super().__init__(parent, bg=theme.GLASS_BG, relief='raised', bd=1, **kwargs)
        self.theme = theme
        self.title = title
        
        # Add glassmorphic styling
        self.config(
            highlightbackground=theme.BORDER,
            highlightcolor=theme.BORDER,
            highlightthickness=1
        )
        
        if title:
            self.create_title_section()
    
    def create_title_section(self):
        """Create title section for the panel"""
        title_frame = tk.Frame(self, bg=self.theme.GLASS_BG)
        title_frame.pack(fill='x', pady=(10, 5))
        
        title_label = tk.Label(
            title_frame,
            text=self.title,
            font=self.theme.SECTION_FONT,
            fg=self.theme.PRIMARY_ACCENT,
            bg=self.theme.GLASS_BG
        )
        title_label.pack()
        
        # Separator
        separator = tk.Frame(
            title_frame,
            bg=self.theme.HIGHLIGHT,
            height=1
        )
        separator.pack(fill='x', pady=(5, 0), padx=20)

class WeatherDisplayPanel(GlassPanel):
    """Glassmorphic panel for weather data display"""
    
    def __init__(self, parent, theme):
        super().__init__(parent, theme, "⛈️ WEATHER INTELLIGENCE")
        self.create_weather_widgets()
    
    def create_weather_widgets(self):
        """Create weather-specific widgets"""
        # Input section
        input_frame = tk.Frame(self, bg=self.theme.GLASS_BG)
        input_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            input_frame,
            text="Target Location:",
            font=self.theme.LABEL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        ).pack(anchor='w')        
        self.city_entry = tk.Entry(
            input_frame,
            font=self.theme.BODY_FONT,
            bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG,
            insertbackground=self.theme.INPUT_FG,
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.theme.INPUT_BORDER,
            highlightbackground=self.theme.INPUT_BORDER
        )
        self.city_entry.pack(fill='x', pady=(5, 10))
        
        self.fetch_button = tk.Button(
            input_frame,
            text="🌍 ACQUIRE WEATHER DATA",
            font=self.theme.BUTTON_FONT,
            bg=self.theme.PRIMARY_ACCENT,
            fg='white',
            activebackground=self.theme.SECONDARY_ACCENT,
            relief='flat',
            bd=0,
            pady=8
        )
        self.fetch_button.pack(fill='x')
        
        # Display section
        display_frame = tk.Frame(self, bg=self.theme.GLASS_BG)
        display_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Weather icon placeholder
        self.icon_label = tk.Label(
            display_frame,
            text="🌤️",
            font=('Arial', 32),
            bg=self.theme.GLASS_BG,
            fg=self.theme.PRIMARY_ACCENT
        )
        self.icon_label.pack(pady=(0, 10))
        
        # Temperature display
        self.temp_label = tk.Label(
            display_frame,
            text="-- °F",
            font=self.theme.LARGE_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        )
        self.temp_label.pack()
        
        # Description
        self.desc_label = tk.Label(
            display_frame,
            text="Awaiting target coordinates...",
            font=self.theme.BODY_FONT,
            fg=self.theme.SUBTITLE_COLOR,
            bg=self.theme.GLASS_BG,
            wraplength=200
        )
        self.desc_label.pack(pady=5)
        
        # Additional info frame
        info_frame = tk.Frame(display_frame, bg=self.theme.GLASS_BG)
        info_frame.pack(fill='x', pady=10)
        
        # Humidity
        self.humidity_label = tk.Label(
            info_frame,
            text="Humidity: --",
            font=self.theme.SMALL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        )
        self.humidity_label.pack(anchor='w')
        
        # Wind
        self.wind_label = tk.Label(
            info_frame,
            text="Wind: --",
            font=self.theme.SMALL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        )
        self.wind_label.pack(anchor='w')
        
        # Pressure
        self.pressure_label = tk.Label(
            info_frame,
            text="Pressure: --",
            font=self.theme.SMALL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        )
        self.pressure_label.pack(anchor='w')
        
        # Forecast section
        forecast_frame = tk.Frame(display_frame, bg=self.theme.GLASS_BG)
        forecast_frame.pack(fill='x', pady=(15, 0))
        
        forecast_title = tk.Label(
            forecast_frame,
            text="📊 TACTICAL FORECAST",
            font=self.theme.LABEL_FONT,
            fg=self.theme.PRIMARY_ACCENT,
            bg=self.theme.GLASS_BG
        )
        forecast_title.pack()
        
        # Sun times
        self.sun_times_label = tk.Label(
            forecast_frame,
            text="☀️ Sunrise: -- | 🌅 Sunset: --",
            font=self.theme.SMALL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        )
        self.sun_times_label.pack(pady=(5, 0))
        
        # Last updated
        self.updated_label = tk.Label(
            forecast_frame,
            text="Last Intel: --",
            font=('Arial', 8),
            fg=self.theme.MUTED_TEXT,
            bg=self.theme.GLASS_BG
        )
        self.updated_label.pack(pady=(5, 0))
    
    def update_weather_data(self, data: Dict[str, Any]):
        """Update the weather display with new data"""
        if "error" in data:
            self.temp_label.config(text="ERROR", fg=self.theme.DANGER_COLOR)
            self.desc_label.config(text=data["error"])
            self.humidity_label.config(text="Humidity: --")
            self.wind_label.config(text="Wind: --")
            self.pressure_label.config(text="Pressure: --")
            self.icon_label.config(text="⚠️")
            return
        
        # Update temperature with city name
        temp = data.get('temp', '--')
        city = data.get('city', 'Unknown')
        country = data.get('country', '')
        location = f"{city}, {country}" if country else city
        self.temp_label.config(text=f"{temp}°F", fg=self.theme.TEXT_COLOR)
        
        # Update description with location
        desc = data.get('description', 'Unknown conditions')
        self.desc_label.config(text=f"{desc}\n{location}")
        
        # Update additional info with more details
        humidity = data.get('humidity', '--')
        self.humidity_label.config(text=f"💧 Humidity: {humidity}%")
        
        wind_speed = data.get('wind_speed', '--')
        feels_like = data.get('feels_like', '--')
        self.wind_label.config(text=f"💨 Wind: {wind_speed} mph | Feels like: {feels_like}°F")
        
        pressure = data.get('pressure', '--')
        visibility = data.get('visibility', '--')
        self.pressure_label.config(text=f"📊 Pressure: {pressure} hPa | Visibility: {visibility} km")
          # Update weather icon based on condition
        icon_code = data.get('icon', '')
        weather_icons = {
            '01d': '☀️', '01n': '🌙', '02d': '⛅', '02n': '☁️',
            '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
            '09d': '🌦️', '09n': '🌧️', '10d': '🌦️', '10n': '🌧️',
            '11d': '⛈️', '11n': '⛈️', '13d': '❄️', '13n': '❄️',
            '50d': '🌫️', '50n': '🌫️'
        }
        icon = weather_icons.get(icon_code, '🌤️')
        self.icon_label.config(text=icon)
        
        # Update sun times if available
        sunrise = data.get('sunrise', '--')
        sunset = data.get('sunset', '--')
        self.sun_times_label.config(text=f"☀️ Sunrise: {sunrise} | 🌅 Sunset: {sunset}")
          # Update timestamp
        timestamp = data.get('timestamp', '--')
        self.updated_label.config(text=f"Last Intel: {timestamp}")

class CobraIntelPanel(GlassPanel):
    """Glassmorphic panel for Cobra intelligence data"""
    
    def __init__(self, parent, theme):
        super().__init__(parent, theme, "🐍 COBRA INTELLIGENCE")
        self.create_cobra_widgets()
    
    def create_cobra_widgets(self):
        """Create Cobra intelligence widgets"""
        # Search section
        search_frame = tk.Frame(self, bg=self.theme.GLASS_BG)
        search_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            search_frame,
            text="Target Subject:",
            font=self.theme.LABEL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        ).pack(anchor='w')        
        self.character_entry = tk.Entry(
            search_frame,
            font=self.theme.BODY_FONT,
            bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG,
            insertbackground=self.theme.INPUT_FG,
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.theme.INPUT_BORDER,
            highlightbackground=self.theme.INPUT_BORDER
        )
        self.character_entry.pack(fill='x', pady=(5, 10))
        
        self.search_button = tk.Button(
            search_frame,
            text="🔍 INTERROGATE DATABASE",
            font=self.theme.BUTTON_FONT,
            bg="#dc143c",  # Cobra red
            fg='white',
            activebackground="#b8001a",
            relief='flat',
            bd=0,
            pady=8
        )
        self.search_button.pack(fill='x')
        
        # Character display section
        display_frame = tk.Frame(self, bg=self.theme.GLASS_BG)
        display_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Character image placeholder
        self.char_image_label = tk.Label(
            display_frame,
            text="👤",
            font=('Arial', 32),
            bg=self.theme.GLASS_BG,
            fg="#dc143c"
        )
        self.char_image_label.pack(pady=(0, 10))
        
        # Character name
        self.char_name_label = tk.Label(
            display_frame,
            text="UNKNOWN SUBJECT",
            font=self.theme.SECTION_FONT,
            fg="#dc143c",
            bg=self.theme.GLASS_BG
        )
        self.char_name_label.pack()
        
        # Character bio
        self.char_bio_label = tk.Label(
            display_frame,
            text="Intelligence files awaiting access...",
            font=self.theme.SMALL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG,
            wraplength=200,
            justify='left'
        )
        self.char_bio_label.pack(pady=10, fill='x')
        
        # Character affiliation
        self.char_affiliation_label = tk.Label(
            display_frame,
            text="Affiliation: CLASSIFIED",
            font=self.theme.SMALL_FONT,
            fg=self.theme.SUBTITLE_COLOR,
            bg=self.theme.GLASS_BG
        )
        self.char_affiliation_label.pack(anchor='w')
        
        # Status section
        status_frame = tk.Frame(display_frame, bg=self.theme.GLASS_BG)
        status_frame.pack(fill='x', pady=(15, 0))
        
        status_title = tk.Label(
            status_frame,
            text="📊 OPERATIONAL STATUS",
            font=self.theme.LABEL_FONT,
            fg="#dc143c",
            bg=self.theme.GLASS_BG
        )
        status_title.pack()
        
        # Database status
        self.db_status_label = tk.Label(
            status_frame,
            text="🗃️ Database: ONLINE",
            font=self.theme.SMALL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        )
        self.db_status_label.pack(anchor='w', pady=(5, 0))
        
        # Security level
        self.security_label = tk.Label(
            status_frame,
            text="🔒 Security Level: CLASSIFIED",
            font=self.theme.SMALL_FONT,
            fg="#dc143c",
            bg=self.theme.GLASS_BG
        )
        self.security_label.pack(anchor='w')
        
        # Last operation
        self.last_op_label = tk.Label(
            status_frame,
            text="Last Operation: --",
            font=('Arial', 8),
            fg=self.theme.MUTED_TEXT,
            bg=self.theme.GLASS_BG
        )
        self.last_op_label.pack(anchor='w', pady=(5, 0))
    
    def update_character_data(self, data: Dict[str, Any]):
        """Update the character display with new data"""
        if "error" in data:
            self.char_name_label.config(text="ACCESS DENIED", fg=self.theme.DANGER_COLOR)
            self.char_bio_label.config(text=data["error"])
            self.char_affiliation_label.config(text="Affiliation: UNKNOWN")
            self.char_image_label.config(text="❌")
            return
        
        # Update character info
        name = data.get('name', 'Unknown Subject')
        self.char_name_label.config(text=name.upper(), fg="#dc143c")
        
        bio = data.get('biography', data.get('bio', 'No intelligence available.'))
        if len(bio) > 150:
            bio = bio[:150] + "..."
        self.char_bio_label.config(text=bio)
        
        affiliation = data.get('affiliation', data.get('team', 'Unknown'))
        speciality = data.get('speciality', data.get('specialty', ''))
        
        affiliation_text = f"🎖️ Team: {affiliation}"
        if speciality:
            affiliation_text += f"\n⚡ Specialty: {speciality}"
        
        self.char_affiliation_label.config(text=affiliation_text)
          # Update character image/icon based on affiliation
        if 'cobra' in affiliation.lower():
            self.char_image_label.config(text="🐍")
        elif 'joe' in affiliation.lower() or 'gi joe' in affiliation.lower():
            self.char_image_label.config(text="🪖")
        elif 'villain' in str(data).lower():
            self.char_image_label.config(text="😈")
        else:
            self.char_image_label.config(text="👤")
        
        # Update status information
        self.db_status_label.config(text="🗃️ Database: INTEL ACQUIRED")
        
        # Set security level based on affiliation
        if 'cobra' in affiliation.lower():
            self.security_label.config(text="🔒 Security Level: COBRA EYES ONLY")
        elif 'joe' in affiliation.lower():
            self.security_label.config(text="🔒 Security Level: CLASSIFIED")
        else:
            self.security_label.config(text="🔒 Security Level: RESTRICTED")
          # Update last operation timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.last_op_label.config(text=f"Last Operation: {timestamp}")

class CobraAlertSystem:
    """Glassmorphic alert system for COBRA-style notifications"""
    
    def __init__(self, parent):
        self.parent = parent
        self.alerts = []
    
    def trigger_alert(self, message: str, alert_type: str = "warning"):
        """Display a COBRA-style alert"""
        alert_window = tk.Toplevel(self.parent)
        alert_window.title("COBRA ALERT")
        alert_window.geometry("400x200")
        alert_window.configure(bg="#1a1a1a")
        alert_window.transient(self.parent)
        alert_window.grab_set()
        
        # Center the alert
        alert_window.update_idletasks()
        x = (alert_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (alert_window.winfo_screenheight() // 2) - (200 // 2)
        alert_window.geometry(f"400x200+{x}+{y}")
        
        # Alert content
        main_frame = tk.Frame(alert_window, bg="#dc143c", relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Alert header
        header_frame = tk.Frame(main_frame, bg="#dc143c")
        header_frame.pack(fill='x', pady=10)
        
        tk.Label(
            header_frame,
            text="⚠️ COBRA ALERT ⚠️",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg="#dc143c"
        ).pack()
        
        # Alert message
        message_frame = tk.Frame(main_frame, bg="white")
        message_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        tk.Label(
            message_frame,
            text=message,
            font=('Arial', 10),
            fg="#dc143c",
            bg="white",
            wraplength=350,
            justify='center'
        ).pack(expand=True)
        
        # Close button
        close_button = tk.Button(
            main_frame,
            text="ACKNOWLEDGE",
            font=('Arial', 10, 'bold'),
            bg="white",
            fg="#dc143c",
            command=alert_window.destroy,
            relief='flat',
            bd=0,
            pady=5
        )
        close_button.pack(pady=(0, 10))
        
        # Auto-close after 5 seconds
        alert_window.after(5000, alert_window.destroy)

def create_glass_widget(parent, widget_type: str, theme, **kwargs):
    """
    Factory function for creating glassmorphic widgets
    
    Args:
        parent: Parent widget
        widget_type: Type of widget ("button", "label", "entry", "frame")
        theme: Theme configuration
        **kwargs: Additional widget options
    """
    if widget_type == "button":
        return tk.Button(
            parent,
            bg=theme.PRIMARY_ACCENT,
            fg='white',
            activebackground=theme.SECONDARY_ACCENT,
            relief='flat',
            bd=0,
            font=theme.BUTTON_FONT,
            **kwargs
        )
    elif widget_type == "label":
        return tk.Label(
            parent,
            bg=theme.GLASS_BG,
            fg=theme.TEXT_COLOR,
            font=theme.BODY_FONT,
            **kwargs
        )
    elif widget_type == "entry":
        return tk.Entry(
            parent,
            bg=theme.INPUT_BG,
            fg=theme.TEXT_COLOR,
            insertbackground=theme.TEXT_COLOR,
            relief='flat',
            bd=0,
            font=theme.BODY_FONT,
            **kwargs
        )
    elif widget_type == "frame":
        return tk.Frame(
            parent,
            bg=theme.GLASS_BG,
            relief='raised',
            bd=1,
            highlightbackground=theme.BORDER,
            highlightcolor=theme.BORDER,
            highlightthickness=1,
            **kwargs
        )
    else:
        raise ValueError(f"Unknown widget type: {widget_type}")

# TODO: Add more glassmorphic components:
# - Animated progress bars for weather loading
# - Tabbed panels for extended forecasts
# - Map integration widget
# - Voice command input widget
# - Settings panel with glassmorphic styling

# COPILOT/CLAUDE PROMPT: "Create animated weather transition effects between different weather conditions in the WeatherDisplayPanel"
# COPILOT/CLAUDE PROMPT: "Add drag-and-drop functionality to rearrange weather data panels"
# COPILOT/CLAUDE PROMPT: "Implement glassmorphic tooltips for all interactive elements"
