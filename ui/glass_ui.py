"""
ui/glass_ui.py - Glassmorphic UI components for Weather Dominator
Implement glassmorphic panels for weather display, Cobra intelligence, and alert system.
Create a widget factory for consistent glass-styled components.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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

# Import Interactive Features
try:
    from .interactive_features import InteractiveFeatures
    INTERACTIVE_AVAILABLE = True
except ImportError:
    print("⚠️ Interactive Features not available")
    INTERACTIVE_AVAILABLE = False
    InteractiveFeatures = None

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

class InteractiveFeaturesPanel(GlassPanel):
    """Glassmorphic panel for Interactive Features (Weather Journal, Favorites, Alerts)"""
    
    def __init__(self, parent, theme):
        super().__init__(parent, theme, "🎯 INTERACTIVE COMMAND CENTER")
        if INTERACTIVE_AVAILABLE and InteractiveFeatures is not None:
            self.interactive_features = InteractiveFeatures()
        else:
            self.interactive_features = None
        self.create_interactive_widgets()
    
    def create_interactive_widgets(self):
        """Create interactive features widgets"""
        # Create notebook for tabbed interface
        notebook_frame = tk.Frame(self, bg=self.theme.GLASS_BG)
        notebook_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Create custom tabbed interface
        self.create_tab_headers(notebook_frame)
        self.create_tab_content(notebook_frame)
        
        # Set default tab
        self.current_tab = 0
        self.show_tab(0)
    
    def create_tab_headers(self, parent):
        """Create tab headers"""
        self.tab_frame = tk.Frame(parent, bg=self.theme.GLASS_BG)
        self.tab_frame.pack(fill='x', pady=(0, 10))
        
        self.tab_buttons = []
        tab_configs = [
            ("📔 JOURNAL", 0, "Weather Journal & Mood Tracking"),
            ("⭐ FAVORITES", 1, "Favorite Cities & Quick Access"),
            ("🚨 ALERTS", 2, "Weather Alerts & Notifications")
        ]
        
        for text, index, tooltip in tab_configs:
            btn = tk.Button(
                self.tab_frame,
                text=text,
                font=self.theme.SMALL_FONT,
                bg=self.theme.INPUT_BG,
                fg=self.theme.TEXT_COLOR,
                activebackground=self.theme.PRIMARY_ACCENT,
                activeforeground='white',
                relief='flat',
                bd=0,
                pady=8,
                command=lambda i=index: self.show_tab(i)
            )
            btn.pack(side='left', fill='x', expand=True, padx=2)
            self.tab_buttons.append(btn)
    
    def create_tab_content(self, parent):
        """Create content for all tabs"""
        self.content_frame = tk.Frame(parent, bg=self.theme.GLASS_BG)
        self.content_frame.pack(fill='both', expand=True)
        
        # Tab 0: Weather Journal
        self.journal_frame = tk.Frame(self.content_frame, bg=self.theme.GLASS_BG)
        self.create_journal_tab()
        
        # Tab 1: Favorite Cities
        self.favorites_frame = tk.Frame(self.content_frame, bg=self.theme.GLASS_BG)
        self.create_favorites_tab()
        
        # Tab 2: Weather Alerts
        self.alerts_frame = tk.Frame(self.content_frame, bg=self.theme.GLASS_BG)
        self.create_alerts_tab()
    
    def create_journal_tab(self):
        """Create weather journal tab"""
        # Journal entry section
        entry_frame = tk.Frame(self.journal_frame, bg=self.theme.GLASS_BG)
        entry_frame.pack(fill='x', pady=(0, 10))
        
        # City input
        tk.Label(entry_frame, text="City:", font=self.theme.SMALL_FONT, 
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(anchor='w')
        self.journal_city_entry = tk.Entry(
            entry_frame, font=self.theme.SMALL_FONT, bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG, relief='flat', bd=1
        )
        self.journal_city_entry.pack(fill='x', pady=(2, 5))
        
        # Mood selection
        tk.Label(entry_frame, text="Mood:", font=self.theme.SMALL_FONT,
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(anchor='w')
        self.mood_var = tk.StringVar(value="neutral")
        mood_frame = tk.Frame(entry_frame, bg=self.theme.GLASS_BG)
        mood_frame.pack(fill='x', pady=(2, 5))
        
        moods = [("😊 Happy", "happy"), ("😐 Neutral", "neutral"), ("😢 Sad", "sad"), 
                ("⚡ Energetic", "energetic"), ("😌 Calm", "calm")]
        for i, (text, value) in enumerate(moods):
            tk.Radiobutton(
                mood_frame, text=text, variable=self.mood_var, value=value,
                font=('Arial', 8), bg=self.theme.GLASS_BG, fg=self.theme.TEXT_COLOR,
                selectcolor=self.theme.PRIMARY_ACCENT, relief='flat'
            ).pack(side='left' if i < 3 else 'left', padx=5)
        
        # Note input
        tk.Label(entry_frame, text="Weather Note:", font=self.theme.SMALL_FONT,
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(anchor='w')
        self.journal_note_text = tk.Text(
            entry_frame, height=3, font=self.theme.SMALL_FONT,
            bg=self.theme.INPUT_BG, fg=self.theme.INPUT_FG, relief='flat', bd=1
        )
        self.journal_note_text.pack(fill='x', pady=(2, 5))
        
        # Buttons
        button_frame = tk.Frame(entry_frame, bg=self.theme.GLASS_BG)
        button_frame.pack(fill='x', pady=5)
        
        tk.Button(
            button_frame, text="📝 Add Entry", font=self.theme.SMALL_FONT,
            bg=self.theme.PRIMARY_ACCENT, fg='white', relief='flat', bd=0,
            command=self.add_journal_entry
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            button_frame, text="💾 Export Journal", font=self.theme.SMALL_FONT,
            bg=self.theme.SECONDARY_ACCENT, fg='white', relief='flat', bd=0,
            command=self.export_journal
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame, text="🧠 Analyze Mood", font=self.theme.SMALL_FONT,
            bg="#6a5acd", fg='white', relief='flat', bd=0,
            command=self.analyze_mood
        ).pack(side='left', padx=5)
        
        # Recent entries display
        tk.Label(self.journal_frame, text="Recent Journal Entries:", 
                font=self.theme.LABEL_FONT, fg=self.theme.PRIMARY_ACCENT,
                bg=self.theme.GLASS_BG).pack(anchor='w', pady=(10, 5))
        
        # Scrollable text widget for entries
        self.journal_display = tk.Text(
            self.journal_frame, height=8, font=self.theme.SMALL_FONT,
            bg=self.theme.INPUT_BG, fg=self.theme.INPUT_FG, relief='flat', bd=1,
            state='disabled'
        )
        self.journal_display.pack(fill='both', expand=True, pady=(0, 5))
        
        # Load recent entries
        self.refresh_journal_display()
    
    def create_favorites_tab(self):
        """Create favorite cities tab"""
        # Add favorite section
        add_frame = tk.Frame(self.favorites_frame, bg=self.theme.GLASS_BG)
        add_frame.pack(fill='x', pady=(0, 10))
        
        # City input
        tk.Label(add_frame, text="City Name:", font=self.theme.SMALL_FONT,
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(anchor='w')
        self.fav_city_entry = tk.Entry(
            add_frame, font=self.theme.SMALL_FONT, bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG, relief='flat', bd=1
        )
        self.fav_city_entry.pack(fill='x', pady=(2, 5))
        
        # Nickname input
        tk.Label(add_frame, text="Nickname (optional):", font=self.theme.SMALL_FONT,
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(anchor='w')
        self.fav_nickname_entry = tk.Entry(
            add_frame, font=self.theme.SMALL_FONT, bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG, relief='flat', bd=1
        )
        self.fav_nickname_entry.pack(fill='x', pady=(2, 5))
        
        # Add button
        tk.Button(
            add_frame, text="⭐ Add to Favorites", font=self.theme.SMALL_FONT,
            bg=self.theme.PRIMARY_ACCENT, fg='white', relief='flat', bd=0,
            command=self.add_favorite_city
        ).pack(fill='x', pady=5)
        
        # Favorites list
        tk.Label(self.favorites_frame, text="Favorite Cities:", 
                font=self.theme.LABEL_FONT, fg=self.theme.PRIMARY_ACCENT,
                bg=self.theme.GLASS_BG).pack(anchor='w', pady=(10, 5))
        
        # Scrollable frame for favorites
        self.favorites_display = tk.Text(
            self.favorites_frame, height=10, font=self.theme.SMALL_FONT,
            bg=self.theme.INPUT_BG, fg=self.theme.INPUT_FG, relief='flat', bd=1,
            state='disabled'
        )
        self.favorites_display.pack(fill='both', expand=True)
        
        # Refresh favorites display
        self.refresh_favorites_display()
    
    def create_alerts_tab(self):
        """Create weather alerts tab"""
        # Alert setup section
        setup_frame = tk.Frame(self.alerts_frame, bg=self.theme.GLASS_BG)
        setup_frame.pack(fill='x', pady=(0, 10))
        
        # City input
        tk.Label(setup_frame, text="City to Monitor:", font=self.theme.SMALL_FONT,
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(anchor='w')
        self.alert_city_entry = tk.Entry(
            setup_frame, font=self.theme.SMALL_FONT, bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG, relief='flat', bd=1
        )
        self.alert_city_entry.pack(fill='x', pady=(2, 5))
        
        # Temperature thresholds
        temp_frame = tk.Frame(setup_frame, bg=self.theme.GLASS_BG)
        temp_frame.pack(fill='x', pady=5)
        
        tk.Label(temp_frame, text="Min Temp (°F):", font=self.theme.SMALL_FONT,
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(side='left')
        self.min_temp_entry = tk.Entry(
            temp_frame, width=8, font=self.theme.SMALL_FONT, bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG, relief='flat', bd=1
        )
        self.min_temp_entry.pack(side='left', padx=(5, 15))
        self.min_temp_entry.insert(0, "32")
        
        tk.Label(temp_frame, text="Max Temp (°F):", font=self.theme.SMALL_FONT,
                fg=self.theme.TEXT_COLOR, bg=self.theme.GLASS_BG).pack(side='left')
        self.max_temp_entry = tk.Entry(
            temp_frame, width=8, font=self.theme.SMALL_FONT, bg=self.theme.INPUT_BG,
            fg=self.theme.INPUT_FG, relief='flat', bd=1
        )
        self.max_temp_entry.pack(side='left', padx=5)
        self.max_temp_entry.insert(0, "90")
        
        # Alert buttons
        alert_button_frame = tk.Frame(setup_frame, bg=self.theme.GLASS_BG)
        alert_button_frame.pack(fill='x', pady=5)
        
        tk.Button(
            alert_button_frame, text="🚨 Set Alert", font=self.theme.SMALL_FONT,
            bg=self.theme.DANGER_COLOR, fg='white', relief='flat', bd=0,
            command=self.set_temperature_alert
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            alert_button_frame, text="🔔 Start Monitoring", font=self.theme.SMALL_FONT,
            bg="#32cd32", fg='white', relief='flat', bd=0,
            command=self.start_alert_monitoring
        ).pack(side='left', padx=5)
        
        # Active alerts display
        tk.Label(self.alerts_frame, text="Active Alerts:", 
                font=self.theme.LABEL_FONT, fg=self.theme.PRIMARY_ACCENT,
                bg=self.theme.GLASS_BG).pack(anchor='w', pady=(10, 5))
        
        self.alerts_display = tk.Text(
            self.alerts_frame, height=8, font=self.theme.SMALL_FONT,
            bg=self.theme.INPUT_BG, fg=self.theme.INPUT_FG, relief='flat', bd=1,
            state='disabled'
        )
        self.alerts_display.pack(fill='both', expand=True)
        
        # Refresh alerts display
        self.refresh_alerts_display()
    
    def show_tab(self, tab_index):
        """Show the specified tab"""
        # Update button appearances
        for i, btn in enumerate(self.tab_buttons):
            if i == tab_index:
                btn.config(bg=self.theme.PRIMARY_ACCENT, fg='white')
            else:
                btn.config(bg=self.theme.INPUT_BG, fg=self.theme.TEXT_COLOR)
        
        # Hide all frames
        for frame in [self.journal_frame, self.favorites_frame, self.alerts_frame]:
            frame.pack_forget()
        
        # Show selected frame
        if tab_index == 0:
            self.journal_frame.pack(fill='both', expand=True)
        elif tab_index == 1:
            self.favorites_frame.pack(fill='both', expand=True)
        elif tab_index == 2:
            self.alerts_frame.pack(fill='both', expand=True)
        
        self.current_tab = tab_index
    
    def add_journal_entry(self):
        """Add a new journal entry"""
        if not self.interactive_features:
            messagebox.showinfo("Demo Mode", "Interactive features not available in demo mode")
            return
        
        city = self.journal_city_entry.get().strip()
        mood = self.mood_var.get()
        note = self.journal_note_text.get("1.0", tk.END).strip()
        
        if not city or not note:
            messagebox.showwarning("Input Required", "Please enter both city and note")
            return
        
        try:
            success = self.interactive_features.add_daily_weather_note(city, note, mood)
            if success:
                messagebox.showinfo("Success", "Journal entry added successfully!")
                # Clear inputs
                self.journal_city_entry.delete(0, tk.END)
                self.journal_note_text.delete("1.0", tk.END)
                # Refresh display
                self.refresh_journal_display()
            else:
                messagebox.showerror("Error", "Failed to add journal entry")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding journal entry: {e}")
    
    def export_journal(self):
        """Export journal to text file"""
        if not self.interactive_features:
            messagebox.showinfo("Demo Mode", "Interactive features not available in demo mode")
            return
        
        try:
            filepath = self.interactive_features.save_journal_to_text_file()
            if filepath:
                messagebox.showinfo("Export Success", f"Journal exported to:\n{filepath}")
            else:
                messagebox.showerror("Export Error", "Failed to export journal")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting journal: {e}")
    
    def analyze_mood(self):
        """Analyze mood patterns"""
        if not self.interactive_features:
            messagebox.showinfo("Demo Mode", "Interactive features not available in demo mode")
            return
        
        try:
            analysis = self.interactive_features.analyze_mood_weather_correlation()
            if "error" not in analysis:
                insights = analysis.get('insights', [])
                total_entries = analysis.get('total_entries', 0)
                
                if insights:
                    insight_text = f"Analysis of {total_entries} entries:\n\n" + "\n".join(insights)
                else:
                    insight_text = f"Analyzed {total_entries} entries. No significant patterns found yet."
                
                messagebox.showinfo("Mood Analysis", insight_text)
            else:
                messagebox.showinfo("Analysis", "Not enough data for analysis yet")
        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing mood: {e}")
    
    def add_favorite_city(self):
        """Add a city to favorites"""
        if not self.interactive_features:
            messagebox.showinfo("Demo Mode", "Interactive features not available in demo mode")
            return
        
        city = self.fav_city_entry.get().strip()
        nickname = self.fav_nickname_entry.get().strip()
        
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name")
            return
        
        try:
            success = self.interactive_features.add_preferred_location(city, nickname=nickname)
            if success:
                messagebox.showinfo("Success", f"Added {city} to favorites!")
                # Clear inputs
                self.fav_city_entry.delete(0, tk.END)
                self.fav_nickname_entry.delete(0, tk.END)
                # Refresh display
                self.refresh_favorites_display()
            else:
                messagebox.showwarning("Duplicate", "City already in favorites or invalid city")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding favorite: {e}")
    
    def set_temperature_alert(self):
        """Set temperature alert for a city"""
        if not self.interactive_features:
            messagebox.showinfo("Demo Mode", "Interactive features not available in demo mode")
            return
        
        city = self.alert_city_entry.get().strip()
        
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city to monitor")
            return
        
        try:
            min_temp = float(self.min_temp_entry.get())
            max_temp = float(self.max_temp_entry.get())
            
            if min_temp >= max_temp:
                messagebox.showwarning("Invalid Range", "Min temperature must be less than max temperature")
                return
            
            success = self.interactive_features.set_temperature_threshold(city, min_temp, max_temp)
            if success:
                messagebox.showinfo("Success", f"Temperature alert set for {city}!")
                self.refresh_alerts_display()
            else:
                messagebox.showerror("Error", "Failed to set temperature alert")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid temperature values")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting alert: {e}")
    
    def start_alert_monitoring(self):
        """Start alert monitoring"""
        if not self.interactive_features:
            messagebox.showinfo("Demo Mode", "Interactive features not available in demo mode")
            return
        
        try:
            success = self.interactive_features.create_simple_notifications("popup")
            if success:
                messagebox.showinfo("Monitoring Started", "Alert monitoring is now active!")
            else:
                messagebox.showerror("Error", "Failed to start alert monitoring")
        except Exception as e:
            messagebox.showerror("Error", f"Error starting monitoring: {e}")
    
    def refresh_journal_display(self):
        """Refresh the journal entries display"""
        if not self.interactive_features:
            self.journal_display.config(state='normal')
            self.journal_display.delete("1.0", tk.END)
            self.journal_display.insert("1.0", "Demo Mode: Interactive features not available\n\nTo use the weather journal:\n1. Enter a city name\n2. Select your mood\n3. Write a weather note\n4. Click 'Add Entry'")
            self.journal_display.config(state='disabled')
            return
        
        try:
            entries = self.interactive_features.get_journal_entries(7)  # Last 7 days
            
            self.journal_display.config(state='normal')
            self.journal_display.delete("1.0", tk.END)
            
            if entries:
                for entry in entries:
                    date = entry.get('date', '')[:10]
                    city = entry.get('city', 'Unknown')
                    mood = entry.get('mood', 'Unknown')
                    note = entry.get('note', 'No note')[:50] + ("..." if len(entry.get('note', '')) > 50 else "")
                    
                    self.journal_display.insert(tk.END, f"{date} | {city} | {mood.title()}\n{note}\n\n")
            else:
                self.journal_display.insert("1.0", "No journal entries found. Add your first entry above!")
            
            self.journal_display.config(state='disabled')
        except Exception as e:
            self.journal_display.config(state='normal')
            self.journal_display.delete("1.0", tk.END)
            self.journal_display.insert("1.0", f"Error loading journal entries: {e}")
            self.journal_display.config(state='disabled')
    
    def refresh_favorites_display(self):
        """Refresh the favorites display"""
        if not self.interactive_features:
            self.favorites_display.config(state='normal')
            self.favorites_display.delete("1.0", tk.END)
            self.favorites_display.insert("1.0", "Demo Mode: Interactive features not available\n\nTo use favorite cities:\n1. Enter a city name\n2. Optionally add a nickname\n3. Click 'Add to Favorites'\n4. Use quick switching for easy access")
            self.favorites_display.config(state='disabled')
            return
        
        try:
            favorites = self.interactive_features.enable_quick_switching()
            
            self.favorites_display.config(state='normal')
            self.favorites_display.delete("1.0", tk.END)
            
            if favorites:
                for fav in favorites:
                    city = fav.get('city', 'Unknown')
                    nickname = fav.get('nickname', city)
                    temp = fav.get('current_temp', 'N/A')
                    condition = fav.get('current_condition', 'Unknown')
                    
                    self.favorites_display.insert(tk.END, f"⭐ {nickname} ({city})\n")
                    self.favorites_display.insert(tk.END, f"   {temp}°F - {condition}\n\n")
            else:
                self.favorites_display.insert("1.0", "No favorite cities added yet. Add your first favorite above!")
            
            self.favorites_display.config(state='disabled')
        except Exception as e:
            self.favorites_display.config(state='normal')
            self.favorites_display.delete("1.0", tk.END)
            self.favorites_display.insert("1.0", f"Error loading favorites: {e}")
            self.favorites_display.config(state='disabled')
    
    def refresh_alerts_display(self):
        """Refresh the alerts display"""
        if not self.interactive_features:
            self.alerts_display.config(state='normal')
            self.alerts_display.delete("1.0", tk.END)
            self.alerts_display.insert("1.0", "Demo Mode: Interactive features not available\n\nTo use weather alerts:\n1. Enter a city to monitor\n2. Set min/max temperature thresholds\n3. Click 'Set Alert'\n4. Start monitoring for notifications")
            self.alerts_display.config(state='disabled')
            return
        
        try:
            alerts = self.interactive_features.get_active_alerts()
            
            self.alerts_display.config(state='normal')
            self.alerts_display.delete("1.0", tk.END)
            
            if alerts:
                for alert in alerts:
                    city = alert.get('city', 'Unknown')
                    min_temp = alert.get('min_threshold', 'N/A')
                    max_temp = alert.get('max_threshold', 'N/A')
                    alert_type = alert.get('alert_type', 'both')
                    trigger_count = alert.get('trigger_count', 0)
                    
                    self.alerts_display.insert(tk.END, f"🚨 {city}\n")
                    self.alerts_display.insert(tk.END, f"   Thresholds: {min_temp}°F - {max_temp}°F ({alert_type})\n")
                    self.alerts_display.insert(tk.END, f"   Triggered: {trigger_count} times\n\n")
            else:
                self.alerts_display.insert("1.0", "No active alerts. Set up your first alert above!")
            
            self.alerts_display.config(state='disabled')
        except Exception as e:
            self.alerts_display.config(state='normal')
            self.alerts_display.delete("1.0", tk.END)
            self.alerts_display.insert("1.0", f"Error loading alerts: {e}")
            self.alerts_display.config(state='disabled')

class SmartFeaturesPanel(GlassPanel):
    """Glassmorphic panel for Smart Features (Predictions, Trends, Activity Suggestions)"""
    
    def __init__(self, parent, theme):
        super().__init__(parent, theme, "🧠 SMART WEATHER AI")
        
        # Import Smart Features
        try:
            from ..ml.smart_features import SmartWeatherFeatures
            self.smart_features = SmartWeatherFeatures()
        except ImportError:
            try:
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from ml.smart_features import SmartWeatherFeatures
                self.smart_features = SmartWeatherFeatures()
            except ImportError:
                self.smart_features = None
        
        # Current city for smart features
        self.current_city = "New York"
        
        self.create_smart_features_interface()
    
    def create_smart_features_interface(self):
        """Create the complete smart features interface with tabs"""
        # City input section
        input_frame = tk.Frame(self, bg=self.theme.GLASS_BG)
        input_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            input_frame,
            text="AI Analysis City:",
            font=self.theme.LABEL_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        ).pack(side='left')
        
        self.city_entry = tk.Entry(
            input_frame,
            font=self.theme.INPUT_FONT,
            bg=self.theme.INPUT_BG,
            fg=self.theme.TEXT_COLOR,
            relief='flat',
            bd=5,
            width=20
        )
        self.city_entry.pack(side='left', padx=(10, 5))
        self.city_entry.insert(0, self.current_city)
        
        # Update button
        self.update_button = tk.Button(
            input_frame,
            text="🔄 Analyze",
            font=self.theme.BUTTON_FONT,
            bg=self.theme.PRIMARY_ACCENT,
            fg='white',
            activebackground=self.theme.SECONDARY_ACCENT,
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            command=self.update_smart_analysis
        )
        self.update_button.pack(side='left', padx=5)
        
        # Create tabbed interface for smart features
        self.create_smart_tabs()
    
    def create_smart_tabs(self):
        """Create tabbed interface for smart features"""
        # Tab container
        tab_container = tk.Frame(self, bg=self.theme.GLASS_BG)
        tab_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab buttons frame
        tab_buttons_frame = tk.Frame(tab_container, bg=self.theme.GLASS_BG)
        tab_buttons_frame.pack(fill='x', pady=(0, 10))
        
        # Tab buttons
        self.smart_tab_buttons = []
        self.current_smart_tab = 0
        
        smart_tabs = [
            ("🔮 Tomorrow's Guess", 0),
            ("📈 Trend Detection", 1),
            ("🎯 Activity Suggester", 2)
        ]
        
        for text, index in smart_tabs:
            btn = tk.Button(
                tab_buttons_frame,
                text=text,
                font=self.theme.BUTTON_FONT,
                bg=self.theme.INPUT_BG,
                fg=self.theme.TEXT_COLOR,
                activebackground=self.theme.PRIMARY_ACCENT,
                activeforeground='white',
                relief='flat',
                bd=0,
                pady=8,
                command=lambda i=index: self.show_smart_tab(i)
            )
            btn.pack(side='left', fill='x', expand=True, padx=2)
            self.smart_tab_buttons.append(btn)
        
        # Content frame for tab panels
        self.smart_content_frame = tk.Frame(tab_container, bg=self.theme.GLASS_BG)
        self.smart_content_frame.pack(fill='both', expand=True)
        
        # Create tab panels
        self.create_prediction_tab()
        self.create_trends_tab()
        self.create_activity_tab()
        
        # Show default tab
        self.show_smart_tab(0)
        
        # Load initial sample data to demonstrate features
        self.load_initial_smart_data()
    
    def show_smart_tab(self, tab_index):
        """Show the specified smart features tab"""
        # Update button appearances
        for i, btn in enumerate(self.smart_tab_buttons):
            if i == tab_index:
                btn.config(bg=self.theme.PRIMARY_ACCENT, fg='white')
            else:
                btn.config(bg=self.theme.INPUT_BG, fg=self.theme.TEXT_COLOR)
        
        # Hide all tab frames
        for widget in self.smart_content_frame.winfo_children():
            widget.pack_forget()
        
        # Show selected tab
        if tab_index == 0:
            self.prediction_frame.pack(fill='both', expand=True)
        elif tab_index == 1:
            self.trends_frame.pack(fill='both', expand=True)
        elif tab_index == 2:
            self.activity_frame.pack(fill='both', expand=True)
        
        self.current_smart_tab = tab_index
    
    def create_prediction_tab(self):
        """Create Tomorrow's Guess prediction tab"""
        self.prediction_frame = tk.Frame(self.smart_content_frame, bg=self.theme.GLASS_BG)
        
        # Prediction display
        pred_display_frame = tk.Frame(self.prediction_frame, bg=self.theme.GLASS_BG)
        pred_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tomorrow's prediction section
        tomorrow_frame = tk.Frame(pred_display_frame, bg=self.theme.INPUT_BG, relief='raised', bd=1)
        tomorrow_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            tomorrow_frame,
            text="🔮 TOMORROW'S WEATHER PREDICTION",
            font=self.theme.SECTION_FONT,
            fg=self.theme.PRIMARY_ACCENT,
            bg=self.theme.INPUT_BG
        ).pack(pady=10)
        
        # Prediction content
        self.prediction_content = tk.Frame(tomorrow_frame, bg=self.theme.INPUT_BG)
        self.prediction_content.pack(fill='x', padx=20, pady=10)
        
        # Prediction text
        self.prediction_text = tk.Text(
            self.prediction_content,
            height=8,
            font=self.theme.BODY_FONT,
            bg=self.theme.CONTENT_BG,
            fg=self.theme.TEXT_COLOR,
            relief='flat',
            bd=5,
            wrap='word',
            state='disabled'
        )
        self.prediction_text.pack(fill='x', pady=5)
        
        # Accuracy tracking section
        accuracy_frame = tk.Frame(pred_display_frame, bg=self.theme.INPUT_BG, relief='raised', bd=1)
        accuracy_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            accuracy_frame,
            text="📊 PREDICTION ACCURACY TRACKING",
            font=self.theme.SECTION_FONT,
            fg=self.theme.SECONDARY_ACCENT,
            bg=self.theme.INPUT_BG
        ).pack(pady=10)
        
        self.accuracy_text = tk.Text(
            accuracy_frame,
            height=4,
            font=self.theme.BODY_FONT,
            bg=self.theme.CONTENT_BG,
            fg=self.theme.TEXT_COLOR,
            relief='flat',
            bd=5,
            wrap='word',
            state='disabled'
        )
        self.accuracy_text.pack(fill='x', padx=20, pady=10)
    
    def create_trends_tab(self):
        """Create Trend Detection tab"""
        self.trends_frame = tk.Frame(self.smart_content_frame, bg=self.theme.GLASS_BG)
        
        # Trends display
        trends_display_frame = tk.Frame(self.trends_frame, bg=self.theme.GLASS_BG)
        trends_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Temperature trends section
        temp_trends_frame = tk.Frame(trends_display_frame, bg=self.theme.INPUT_BG, relief='raised', bd=1)
        temp_trends_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            temp_trends_frame,
            text="📈 TEMPERATURE TREND ANALYSIS",
            font=self.theme.SECTION_FONT,
            fg=self.theme.PRIMARY_ACCENT,
            bg=self.theme.INPUT_BG
        ).pack(pady=10)
        
        # Trend arrows display
        self.trends_arrows_frame = tk.Frame(temp_trends_frame, bg=self.theme.INPUT_BG)
        self.trends_arrows_frame.pack(fill='x', padx=20, pady=10)
        
        # Trend summary
        self.trends_text = tk.Text(
            temp_trends_frame,
            height=6,
            font=self.theme.BODY_FONT,
            bg=self.theme.CONTENT_BG,
            fg=self.theme.TEXT_COLOR,
            relief='flat',
            bd=5,
            wrap='word',
            state='disabled'
        )
        self.trends_text.pack(fill='x', padx=20, pady=10)
        
        # Weather patterns section
        patterns_frame = tk.Frame(trends_display_frame, bg=self.theme.INPUT_BG, relief='raised', bd=1)
        patterns_frame.pack(fill='x')
        
        tk.Label(
            patterns_frame,
            text="🔍 WEATHER PATTERN IDENTIFICATION",
            font=self.theme.SECTION_FONT,
            fg=self.theme.SECONDARY_ACCENT,
            bg=self.theme.INPUT_BG
        ).pack(pady=10)
        
        self.patterns_text = tk.Text(
            patterns_frame,
            height=6,
            font=self.theme.BODY_FONT,
            bg=self.theme.CONTENT_BG,
            fg=self.theme.TEXT_COLOR,
            relief='flat',
            bd=5,
            wrap='word',
            state='disabled'
        )
        self.patterns_text.pack(fill='x', padx=20, pady=10)
    
    def create_activity_tab(self):
        """Create Activity Suggester tab"""
        self.activity_frame = tk.Frame(self.smart_content_frame, bg=self.theme.GLASS_BG)
        
        # Activity display
        activity_display_frame = tk.Frame(self.activity_frame, bg=self.theme.GLASS_BG)
        activity_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Random suggestion section
        random_frame = tk.Frame(activity_display_frame, bg=self.theme.INPUT_BG, relief='raised', bd=1)
        random_frame.pack(fill='x', pady=(0, 10))
        
        random_header = tk.Frame(random_frame, bg=self.theme.INPUT_BG)
        random_header.pack(fill='x', pady=10)
        
        tk.Label(
            random_header,
            text="🎲 RANDOM ACTIVITY SUGGESTION",
            font=self.theme.SECTION_FONT,
            fg=self.theme.PRIMARY_ACCENT,
            bg=self.theme.INPUT_BG
        ).pack(side='left', padx=20)
        
        self.random_activity_button = tk.Button(
            random_header,
            text="🔄 Get New Suggestion",
            font=self.theme.BUTTON_FONT,
            bg=self.theme.SECONDARY_ACCENT,
            fg='white',
            activebackground=self.theme.PRIMARY_ACCENT,
            relief='flat',
            bd=0,
            padx=10,
            pady=5,
            command=self.get_random_activity
        )
        self.random_activity_button.pack(side='right', padx=20)
        
        self.random_activity_text = tk.Text(
            random_frame,
            height=3,
            font=self.theme.BODY_FONT,
            bg=self.theme.CONTENT_BG,
            fg=self.theme.TEXT_COLOR,
            relief='flat',
            bd=5,
            wrap='word',
            state='disabled'
        )
        self.random_activity_text.pack(fill='x', padx=20, pady=10)
        
        # Categorized activities section
        categories_frame = tk.Frame(activity_display_frame, bg=self.theme.INPUT_BG, relief='raised', bd=1)
        categories_frame.pack(fill='both', expand=True)
        
        tk.Label(
            categories_frame,
            text="🎯 WEATHER-BASED ACTIVITY RECOMMENDATIONS",
            font=self.theme.SECTION_FONT,
            fg=self.theme.SECONDARY_ACCENT,
            bg=self.theme.INPUT_BG
        ).pack(pady=10)
        
        # Create scrollable text for all activities
        self.activities_text = tk.Text(
            categories_frame,
            height=12,
            font=self.theme.BODY_FONT,
            bg=self.theme.CONTENT_BG,
            fg=self.theme.TEXT_COLOR,
            relief='flat',
            bd=5,
            wrap='word',
            state='disabled'
        )
        self.activities_text.pack(fill='both', expand=True, padx=20, pady=10)
    
    def update_smart_analysis(self):
        """Update all smart feature analyses for the specified city"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name for AI analysis.")
            return
        
        self.current_city = city
        
        if not self.smart_features:
            messagebox.showerror("Error", "Smart Features not available. Please check module installation.")
            return
        
        try:
            # Update all tabs
            self.update_predictions()
            self.update_trends()
            self.update_activities()
            
            messagebox.showinfo("Analysis Complete", f"Smart analysis updated for {city}!")
            
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error during smart analysis: {str(e)}")
    
    def update_predictions(self):
        """Update tomorrow's weather prediction"""
        if not self.smart_features:
            return
        
        try:
            prediction = self.smart_features.predict_tomorrows_weather(self.current_city)
            accuracy = self.smart_features.track_prediction_accuracy(self.current_city)
            
            # Update prediction display
            self.prediction_text.config(state='normal')
            self.prediction_text.delete("1.0", tk.END)
            
            if "error" in prediction:
                self.prediction_text.insert("1.0", f"❌ {prediction['error']}\n\nTip: More historical data needed for accurate predictions.")
            else:
                pred_data = prediction.get('prediction', {})
                confidence = prediction.get('confidence', 0)
                
                content = f"🏙️ City: {self.current_city}\n"
                content += f"📅 Prediction Date: {prediction.get('prediction_date', 'Unknown')}\n\n"
                content += f"🌡️ Temperature: {pred_data.get('temperature', 'N/A')}°F\n"
                content += f"🤗 Feels Like: {pred_data.get('feels_like', 'N/A')}°F\n"
                content += f"💧 Humidity: {pred_data.get('humidity', 'N/A')}%\n"
                content += f"🌤️ Condition: {pred_data.get('condition', 'Unknown')}\n"
                content += f"📊 Confidence Level: {confidence}%\n\n"
                
                if confidence >= 80:
                    content += "✅ High confidence prediction"
                elif confidence >= 60:
                    content += "⚠️ Moderate confidence prediction"
                else:
                    content += "🔍 Low confidence - more data needed"
                
                self.prediction_text.insert("1.0", content)
            
            self.prediction_text.config(state='disabled')
            
            # Update accuracy display
            self.accuracy_text.config(state='normal')
            self.accuracy_text.delete("1.0", tk.END)
            
            if "error" in accuracy:
                self.accuracy_text.insert("1.0", f"📊 {accuracy['error']}")
            else:
                acc_content = f"📈 Total Predictions: {accuracy.get('total_predictions', 0)}\n"
                acc_content += f"✅ Accurate Predictions: {accuracy.get('accurate_predictions', 0)}\n"
                acc_content += f"🎯 Accuracy Rate: {accuracy.get('accuracy_percentage', 0)}%\n"
                acc_content += f"📝 Note: {accuracy.get('note', 'Temperature accuracy within 5°F')}"
                
                self.accuracy_text.insert("1.0", acc_content)
            
            self.accuracy_text.config(state='disabled')
            
        except Exception as e:
            self.prediction_text.config(state='normal')
            self.prediction_text.delete("1.0", tk.END)
            self.prediction_text.insert("1.0", f"Error loading predictions: {e}")
            self.prediction_text.config(state='disabled')
    
    def update_trends(self):
        """Update temperature trends and patterns"""
        if not self.smart_features:
            return
        
        try:
            trends = self.smart_features.detect_temperature_trends(self.current_city)
            patterns = self.smart_features.identify_weather_patterns(self.current_city)
            
            # Clear previous trend arrows
            for widget in self.trends_arrows_frame.winfo_children():
                widget.destroy()
            
            # Update trends display
            self.trends_text.config(state='normal')
            self.trends_text.delete("1.0", tk.END)
            
            if "error" in trends:
                self.trends_text.insert("1.0", f"❌ {trends['error']}\n\nTip: Need more historical data for trend analysis.")
            else:
                # Display trend arrows
                arrows = trends.get('trend_arrows', {})
                if arrows:
                    tk.Label(
                        self.trends_arrows_frame,
                        text=f"Overall: {arrows.get('overall', '➡️')}",
                        font=('Arial', 14, 'bold'),
                        fg=self.theme.PRIMARY_ACCENT,
                        bg=self.theme.INPUT_BG
                    ).pack(side='left', padx=10)
                    
                    tk.Label(
                        self.trends_arrows_frame,
                        text=f"Recent: {arrows.get('recent', '🌡️')}",
                        font=('Arial', 14, 'bold'),
                        fg=self.theme.SECONDARY_ACCENT,
                        bg=self.theme.INPUT_BG
                    ).pack(side='left', padx=10)
                    
                    tk.Label(
                        self.trends_arrows_frame,
                        text=f"Short-term: {arrows.get('short_term', '➡️')}",
                        font=('Arial', 14, 'bold'),
                        fg=self.theme.TEXT_COLOR,
                        bg=self.theme.INPUT_BG
                    ).pack(side='left', padx=10)
                
                # Display trend summary
                summary = trends.get('summary', 'No trend analysis available')
                trend_data = trends.get('trends', {})
                
                content = f"🏙️ City: {self.current_city}\n"
                content += f"📊 Analysis Period: {trends.get('analysis_period', 'Unknown')}\n"
                content += f"📈 Data Points: {trends.get('data_points', 0)}\n\n"
                content += f"📝 Summary: {summary}\n\n"
                
                if trend_data and "error" not in trend_data:
                    temp_range = trend_data.get('temperature_range', {})
                    content += f"🌡️ Temperature Range:\n"
                    content += f"   • Current: {temp_range.get('current', 'N/A')}°F\n"
                    content += f"   • Min: {temp_range.get('min', 'N/A')}°F\n"
                    content += f"   • Max: {temp_range.get('max', 'N/A')}°F\n"
                
                self.trends_text.insert("1.0", content)
            
            self.trends_text.config(state='disabled')
            
            # Update patterns display
            self.patterns_text.config(state='normal')
            self.patterns_text.delete("1.0", tk.END)
            
            if "error" in patterns:
                self.patterns_text.insert("1.0", f"❌ {patterns['error']}")
            else:
                patterns_data = patterns.get('patterns', {})
                content = f"🔍 Pattern Analysis for {self.current_city}\n\n"
                
                # Weekly patterns
                weekly = patterns_data.get('weekly_patterns', {})
                if weekly and "error" not in weekly:
                    daily_avg = weekly.get('daily_averages', {})
                    if daily_avg:
                        content += "📅 Weekly Temperature Patterns:\n"
                        for day, temp in daily_avg.items():
                            content += f"   • {day}: {temp}°F\n"
                        content += "\n"
                
                # Weather cycles
                cycles = patterns_data.get('weather_cycles', {})
                if cycles and "error" not in cycles:
                    weather_cycles = cycles.get('weather_cycles', [])
                    if weather_cycles:
                        content += "🔄 Weather Cycles Detected:\n"
                        for cycle in weather_cycles[:3]:  # Show top 3
                            content += f"   • {cycle.get('condition', 'Unknown')}: {cycle.get('duration', 0)} days\n"
                        content += "\n"
                
                # Pressure patterns
                pressure = patterns_data.get('pressure_patterns', {})
                if pressure and "error" not in pressure:
                    trend = pressure.get('pressure_trend', 'unknown')
                    content += f"🌪️ Pressure Trend: {trend.replace('_', ' ').title()}\n"
                
                self.patterns_text.insert("1.0", content)
            
            self.patterns_text.config(state='disabled')
            
        except Exception as e:
            self.trends_text.config(state='normal')
            self.trends_text.delete("1.0", tk.END)
            self.trends_text.insert("1.0", f"Error loading trends: {e}")
            self.trends_text.config(state='disabled')
    
    def update_activities(self):
        """Update activity suggestions"""
        if not self.smart_features:
            return
        
        try:
            activities = self.smart_features.suggest_weather_based_activities(self.current_city)
            
            # Update activities display
            self.activities_text.config(state='normal')
            self.activities_text.delete("1.0", tk.END)
            
            if "error" in activities:
                self.activities_text.insert("1.0", f"❌ {activities['error']}")
            else:
                current_weather = activities.get('current_weather', {})
                suggestions = activities.get('activity_suggestions', {})
                suitability = activities.get('weather_suitability', {})
                
                content = f"🏙️ Current Weather in {self.current_city}:\n"
                content += f"🌡️ {current_weather.get('temperature', 'N/A')}°F - {current_weather.get('condition', 'Unknown')}\n"
                content += f"💨 Wind: {current_weather.get('wind_speed', 'N/A')} mph\n"
                content += f"💧 Humidity: {current_weather.get('humidity', 'N/A')}%\n\n"
                
                # Weather suitability
                content += "📊 Weather Suitability:\n"
                for activity_type, rating in suitability.items():
                    emoji = {"excellent": "🟢", "good": "🟡", "fair": "🟠", "poor": "🔴"}.get(rating, "⚪")
                    content += f"   {emoji} {activity_type.replace('_', ' ').title()}: {rating.title()}\n"
                content += "\n"
                
                # Activity suggestions by category
                for category, activity_list in suggestions.items():
                    if activity_list:
                        category_emoji = {
                            "outdoor": "🌤️",
                            "indoor": "🏠",
                            "exercise": "💪",
                            "social": "👥"
                        }.get(category, "🎯")
                        
                        content += f"{category_emoji} {category.title()} Activities:\n"
                        for activity in activity_list:
                            content += f"   • {activity}\n"
                        content += "\n"
                
                self.activities_text.insert("1.0", content)
            
            self.activities_text.config(state='disabled')
            
            # Also update random suggestion
            self.get_random_activity()
            
        except Exception as e:
            self.activities_text.config(state='normal')
            self.activities_text.delete("1.0", tk.END)
            self.activities_text.insert("1.0", f"Error loading activities: {e}")
            self.activities_text.config(state='disabled')
    
    def get_random_activity(self):
        """Get a random activity suggestion"""
        if not self.smart_features:
            return
        
        try:
            random_suggestion = self.smart_features.get_random_activity_suggestion(self.current_city)
            
            self.random_activity_text.config(state='normal')
            self.random_activity_text.delete("1.0", tk.END)
            
            if "error" in random_suggestion:
                self.random_activity_text.insert("1.0", f"❌ {random_suggestion['error']}")
            else:
                weather = random_suggestion.get('weather', {})
                suggestion = random_suggestion.get('random_suggestion', 'No suggestion available')
                alternative = random_suggestion.get('alternative_suggestion', '')
                tip = random_suggestion.get('tip', '')
                
                content = f"🎲 Random Suggestion:\n{suggestion}\n\n"
                if alternative:
                    content += f"🎯 Alternative: {alternative}\n\n"
                content += f"💡 {tip}"
                
                self.random_activity_text.insert("1.0", content)
            
            self.random_activity_text.config(state='disabled')
            
        except Exception as e:
            self.random_activity_text.config(state='normal')
            self.random_activity_text.delete("1.0", tk.END)
            self.random_activity_text.insert("1.0", f"Error getting random activity: {e}")
            self.random_activity_text.config(state='disabled')
    
    def load_initial_smart_data(self):
        """Load initial sample data to demonstrate smart features"""
        try:
            # Show sample prediction data
            self.prediction_text.config(state='normal')
            self.prediction_text.delete("1.0", tk.END)
            
            sample_prediction = """🏙️ City: New York
📅 Prediction Date: Tomorrow

🌡️ Temperature: 75°F
🤗 Feels Like: 78°F
💧 Humidity: 65%
🌤️ Condition: Partly Cloudy
📊 Confidence Level: 85%

✅ High confidence prediction

🔍 Click '🔄 Analyze' to get real predictions for any city!"""
            
            self.prediction_text.insert("1.0", sample_prediction)
            self.prediction_text.config(state='disabled')
            
            # Show sample accuracy data
            self.accuracy_text.config(state='normal')
            self.accuracy_text.delete("1.0", sample_accuracy)
            
            sample_accuracy = """📈 Total Predictions: 47
✅ Accurate Predictions: 39
🎯 Accuracy Rate: 83%
📝 Note: Temperature accuracy within 5°F"""
            
            self.accuracy_text.insert("1.0", sample_accuracy)
            self.accuracy_text.config(state='disabled')
            
            # Show sample trends data
            self.trends_text.config(state='normal')
            self.trends_text.delete("1.0", tk.END)
            
            sample_trends = """🏙️ City: New York
📊 Analysis Period: Last 7 days
📈 Data Points: 48

📝 Summary: Temperature showing gradual warming trend with stable humidity levels.

🌡️ Temperature Range:
   • Current: 72°F
   • Min: 68°F
   • Max: 78°F

🔍 Click '🔄 Analyze' to see real trend analysis!"""
            
            self.trends_text.insert("1.0", sample_trends)
            self.trends_text.config(state='disabled')
            
            # Show sample patterns data
            self.patterns_text.config(state='normal')
            self.patterns_text.delete("1.0", tk.END)
            
            sample_patterns = """🔍 Pattern Analysis for New York

📅 Weekly Temperature Patterns:
   • Monday: 71°F
   • Tuesday: 73°F
   • Wednesday: 75°F
   • Thursday: 74°F
   • Friday: 72°F
   • Saturday: 76°F
   • Sunday: 70°F

🔄 Weather Cycles Detected:
   • Clear: 3 days
   • Partly Cloudy: 2 days
   • Cloudy: 2 days

🌪️ Pressure Trend: Stable"""
            
            self.patterns_text.insert("1.0", sample_patterns)
            self.patterns_text.config(state='disabled')
            
            # Show sample activities data
            self.activities_text.config(state='normal')
            self.activities_text.delete("1.0", tk.END)
            
            sample_activities = """🏙️ Current Weather in New York:
🌡️ 72°F - Partly Cloudy
💨 Wind: 8 mph
💧 Humidity: 60%

📊 Weather Suitability:
   🟢 Outdoor Activities: Excellent
   🟡 Water Sports: Good
   🟢 Exercise: Excellent
   🟢 Social Events: Excellent

🌤️ Outdoor Activities:
   • Go for a walk in Central Park
   • Have a picnic lunch
   • Play outdoor sports
   • Visit outdoor markets

🏠 Indoor Activities:
   • Visit museums
   • Go shopping
   • Watch a movie
   • Try a new restaurant

💪 Exercise Activities:
   • Go for a run
   • Cycling in the park
   • Outdoor yoga class
   • Tennis or basketball

👥 Social Activities:
   • Meet friends for coffee
   • Outdoor dining
   • Group fitness class
   • Attend outdoor events

🔍 Click '🔄 Analyze' to get personalized suggestions for any city!"""
            
            self.activities_text.insert("1.0", sample_activities)
            self.activities_text.config(state='disabled')
            
            # Show sample random activity
            self.random_activity_text.config(state='normal')
            self.random_activity_text.delete("1.0", tk.END)
            
            sample_random = """🎲 Random Suggestion:
Perfect weather for a scenic walk! Head to a nearby park or waterfront area for some fresh air and light exercise.

🎯 Alternative: Visit a local farmers market for fresh produce and local crafts.

💡 Pro tip: The weather is ideal for photography - golden hour lighting expected around sunset!"""
            
            self.random_activity_text.insert("1.0", sample_random)
            self.random_activity_text.config(state='disabled')
            
            # Add sample trend arrows
            for widget in self.trends_arrows_frame.winfo_children():
                widget.destroy()
                
            tk.Label(
                self.trends_arrows_frame,
                text="Overall: ↗️",
                font=('Arial', 14, 'bold'),
                fg=self.theme.PRIMARY_ACCENT,
                bg=self.theme.INPUT_BG
            ).pack(side='left', padx=10)
            
            tk.Label(
                self.trends_arrows_frame,
                text="Recent: 🌡️",
                font=('Arial', 14, 'bold'),
                fg=self.theme.SECONDARY_ACCENT,
                bg=self.theme.INPUT_BG
            ).pack(side='left', padx=10)
            
            tk.Label(
                self.trends_arrows_frame,
                text="Short-term: ➡️",
                font=('Arial', 14, 'bold'),
                fg=self.theme.TEXT_COLOR,
                bg=self.theme.INPUT_BG
            ).pack(side='left', padx=10)
            
        except Exception as e:
            print(f"Error loading initial smart data: {e}")
