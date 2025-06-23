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
    from PIL import Image, ImageTk
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
            fg=self.theme.TEXT_COLOR,
            insertbackground=self.theme.TEXT_COLOR,
            relief='flat',
            bd=0
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
        
        # Update temperature
        temp = data.get('temperature', '--')
        self.temp_label.config(text=f"{temp}°F", fg=self.theme.TEXT_COLOR)
        
        # Update description
        desc = data.get('description', 'Unknown conditions')
        self.desc_label.config(text=desc.title())
        
        # Update additional info
        humidity = data.get('humidity', '--')
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        
        wind_speed = data.get('wind_speed', '--')
        self.wind_label.config(text=f"Wind: {wind_speed} mph")
        
        pressure = data.get('pressure', '--')
        self.pressure_label.config(text=f"Pressure: {pressure} hPa")
        
        # Update weather icon based on condition
        condition = data.get('condition', '').lower()
        if 'rain' in condition:
            self.icon_label.config(text="🌧️")
        elif 'storm' in condition:
            self.icon_label.config(text="⛈️")
        elif 'snow' in condition:
            self.icon_label.config(text="❄️")
        elif 'cloud' in condition:
            self.icon_label.config(text="☁️")
        elif 'clear' in condition:
            self.icon_label.config(text="☀️")
        else:
            self.icon_label.config(text="🌤️")

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
            fg=self.theme.TEXT_COLOR,
            insertbackground=self.theme.TEXT_COLOR,
            relief='flat',
            bd=0
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
        
        bio = data.get('bio', 'No intelligence available.')
        self.char_bio_label.config(text=bio)
        
        affiliation = data.get('affiliation', 'Unknown')
        self.char_affiliation_label.config(text=f"Affiliation: {affiliation}")
        
        # Update character image/icon
        if 'cobra' in name.lower() or 'cobra' in affiliation.lower():
            self.char_image_label.config(text="🐍")
        elif 'joe' in affiliation.lower():
            self.char_image_label.config(text="🪖")
        else:
            self.char_image_label.config(text="👤")

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
