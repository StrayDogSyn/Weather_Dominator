"""
Weather Dominator - COBRA Weather Application
A modern Glassmorphism Tkinter app with transparent background and styled frame container
Integrates weather data, G.I. Joe character data, and machine learning predictions
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from theme_config import GlassmorphicTheme, CobraTheme

# Import our custom modules
try:
    from ui.glass_ui import WeatherDisplayPanel, CobraIntelPanel, InteractiveFeaturesPanel, SmartFeaturesPanel, SmartAIPanel
    from data.weather_api import WeatherAPI
    from data.gijoe_api import GIJoeAPI
    from db.sqlite_store import WeatherDatabase
    from ml.predictor import WeatherPredictor
    from utils.helpers import TemperatureConverter, DataFormatter, ImageCache, ConfigManager
    UI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some modules not available: {e}")
    UI_AVAILABLE = False
    WeatherDisplayPanel = None
    CobraIntelPanel = None
    InteractiveFeaturesPanel = None
    SmartFeaturesPanel = None
    SmartAIPanel = None
    WeatherAPI = None
    GIJoeAPI = None
    WeatherDatabase = None
    WeatherPredictor = None
    TemperatureConverter = None
    DataFormatter = None
    ImageCache = None
    ConfigManager = None

class GlassmorphicWindow:
    def __init__(self, theme=None):
        self.theme = theme or GlassmorphicTheme()
        self.root = tk.Tk()
        
        # Initialize components if available
        if UI_AVAILABLE:
            try:
                self.weather_api = WeatherAPI() if WeatherAPI is not None else None
                self.gijoe_api = GIJoeAPI() if GIJoeAPI is not None else None
                self.database = WeatherDatabase() if WeatherDatabase is not None else None
                self.predictor = WeatherPredictor() if WeatherPredictor is not None else None
                self.alert_system = None  # Will be initialized after root window
                self.config = ConfigManager() if ConfigManager is not None else None
            except Exception as e:
                print(f"⚠️ Error initializing components: {e}")
                self.weather_api = None
                self.gijoe_api = None
                self.database = None
                self.predictor = None
                self.alert_system = None
                self.config = None
        else:
            self.weather_api = None
            self.gijoe_api = None
            self.database = None
            self.predictor = None
            self.alert_system = None
            self.config = None
            
        self.setup_window()
        self.create_glassmorphic_frame()
        
        # Initialize alert system after window is created
        self.alert_system = None  # Simple alert system can be added later if needed
        
    def setup_window(self):
        """Configure the main window with transparent background"""
        self.root.title("COBRA Weather Dominator")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.theme.WINDOW_BG)
        
        # Center the window on screen
        self.center_window()
        
        # Make window semi-transparent (Windows specific)
        if sys.platform.startswith('win'):
            self.root.wm_attributes('-alpha', self.theme.WINDOW_ALPHA)
            # Remove window decorations for modern look
            self.root.overrideredirect(False)
            
        # Set minimum size
        self.root.minsize(900, 600)
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_glassmorphic_frame(self):
        """Create the main glassmorphic container frame with two main sections"""
        # Main container with padding
        self.main_container = tk.Frame(
            self.root,
            bg=self.theme.CONTAINER_BG,
            relief='flat',
            bd=0
        )
        self.main_container.pack(fill='both', expand=True, 
                               padx=self.theme.PADDING_LARGE, 
                               pady=self.theme.PADDING_LARGE)
        
        # Glassmorphic frame with rounded appearance simulation
        self.glass_frame = tk.Frame(
            self.main_container,
            bg=self.theme.GLASS_BG,
            relief='raised',
            bd=self.theme.BORDER_WIDTH,
            highlightbackground=self.theme.BORDER,
            highlightcolor=self.theme.BORDER,
            highlightthickness=self.theme.BORDER_WIDTH
        )
        self.glass_frame.pack(fill='both', expand=True, 
                            padx=self.theme.PADDING_MEDIUM, 
                            pady=self.theme.PADDING_MEDIUM)
        
        # Add close button at top-right
        self.add_close_button()
        
        # Inner content frame
        self.content_frame = tk.Frame(
            self.glass_frame,
            bg=self.theme.CONTENT_BG,
            relief='flat',
            bd=0
        )
        self.content_frame.pack(fill='both', expand=True, 
                              padx=self.theme.PADDING_LARGE, 
                              pady=(5, self.theme.PADDING_LARGE))
        
        # Add glassmorphic effect simulation with multiple frames
        self.add_glassmorphic_effects()
        
        # Add title
        self.add_title()
        
        # Create two main sections: Weather Data Display and Cobra Intelligence Panel
        self.create_main_sections()
        
    def add_close_button(self):
        """Add a custom close button positioned at top-right of glass frame"""
        close_frame = tk.Frame(self.glass_frame, bg=self.theme.GLASS_BG)
        close_frame.pack(side='top', fill='x', pady=(5, 0))
        
        close_button = tk.Button(
            close_frame,
            text="✕",
            font=('Arial', 14, 'bold'),
            fg=self.theme.DANGER_COLOR,
            bg=self.theme.GLASS_BG,
            activebackground=self.theme.DANGER_COLOR,
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=8,
            pady=4,
            command=self.root.quit
        )
        close_button.pack(side='right', padx=(0, 10))
        
        # Add hover effects
        def on_enter(e):
            close_button.config(bg=self.theme.DANGER_COLOR, fg='white')
        
        def on_leave(e):
            close_button.config(bg=self.theme.GLASS_BG, fg=self.theme.DANGER_COLOR)
            
        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)
        
    def add_glassmorphic_effects(self):
        """Add visual effects to simulate glassmorphism"""
        # Top highlight for glass effect
        highlight_frame = tk.Frame(
            self.content_frame,
            bg=self.theme.HIGHLIGHT,
            height=self.theme.GLASS_HIGHLIGHT_HEIGHT
        )
        highlight_frame.pack(side='top', fill='x', padx=1, pady=1)
        
        # Subtle gradient effect using multiple frames
        for i, color in enumerate(self.theme.GRADIENT_COLORS):
            gradient_frame = tk.Frame(
                self.content_frame,
                bg=color,
                height=self.theme.GRADIENT_FRAME_HEIGHT
            )
            gradient_frame.pack(side='top', fill='x')
            
    def add_title(self):
        """Add the main title to the glassmorphic window"""
        title_frame = tk.Frame(self.content_frame, bg=self.theme.CONTENT_BG)
        title_frame.pack(fill='x', pady=(20, 30))
        
        # Main title
        title_label = tk.Label(
            title_frame,
            text="COBRA WEATHER DOMINATOR",
            font=self.theme.TITLE_FONT,
            fg=self.theme.TITLE_COLOR,
            bg=self.theme.CONTENT_BG
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="Advanced Weather Control System",
            font=self.theme.SUBTITLE_FONT,
            fg=self.theme.SUBTITLE_COLOR,
            bg=self.theme.CONTENT_BG
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Separator line
        separator = tk.Frame(
            title_frame,
            bg=self.theme.HIGHLIGHT,
            height=self.theme.SEPARATOR_HEIGHT
        )
        separator.pack(fill='x', pady=(15, 0), padx=50)
        
    def create_main_sections(self):
        """Create the main sections with tabbed interface for all features"""
        # Create main sections container
        sections_frame = tk.Frame(self.content_frame, bg=self.theme.CONTENT_BG)
        sections_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        if UI_AVAILABLE and WeatherDisplayPanel is not None and CobraIntelPanel is not None and InteractiveFeaturesPanel is not None and SmartFeaturesPanel is not None:
            try:
                # Create tabbed interface
                self.create_tab_interface(sections_frame)
                
            except Exception as e:
                print(f"⚠️ Error creating UI panels: {e}")
                self.create_fallback_sections(sections_frame)
        else:
            self.create_fallback_sections(sections_frame)
    
    def create_tab_interface(self, parent):
        """Create tabbed interface with all three panels"""
        # Create tab headers
        tab_header_frame = tk.Frame(parent, bg=self.theme.CONTENT_BG)
        tab_header_frame.pack(fill='x', pady=(0, 10))
        
        # Tab buttons
        self.tab_buttons = []
        self.current_tab = 0
        
        tab_configs = [
            ("⛈️ WEATHER INTEL", 0, "Weather Data & Forecasting"),
            ("🐍 COBRA INTEL", 1, "Character Intelligence Database"),
            ("🎯 INTERACTIVE", 2, "Journal, Favorites & Alerts"),
            ("🧠 SMART AI", 3, "Predictions, Trends & Activities")
        ]
        
        for text, index, tooltip in tab_configs:
            btn = tk.Button(
                tab_header_frame,
                text=text,
                font=self.theme.BUTTON_FONT,
                bg=self.theme.INPUT_BG,
                fg=self.theme.TEXT_COLOR,
                activebackground=self.theme.PRIMARY_ACCENT,
                activeforeground='white',
                relief='flat',
                bd=0,
                pady=12,
                command=lambda i=index: self.show_main_tab(i)
            )
            btn.pack(side='left', fill='x', expand=True, padx=5)
            self.tab_buttons.append(btn)
        
        # Create content frame for panels
        self.panels_container = tk.Frame(parent, bg=self.theme.CONTENT_BG)
        self.panels_container.pack(fill='both', expand=True)
        
        # Create all panels
        if WeatherDisplayPanel is not None:
            self.weather_panel = WeatherDisplayPanel(self.panels_container, self.theme)
        if CobraIntelPanel is not None:
            self.cobra_panel = CobraIntelPanel(self.panels_container, self.theme)
        if InteractiveFeaturesPanel is not None:
            self.interactive_panel = InteractiveFeaturesPanel(self.panels_container, self.theme)
        if SmartAIPanel is not None:
            self.smart_panel = SmartAIPanel(self.panels_container, self.theme)
        
        # Connect button events
        if hasattr(self, 'weather_panel'):
            self.weather_panel.fetch_button.config(command=self.fetch_weather_data)
        if hasattr(self, 'cobra_panel'):
            self.cobra_panel.search_button.config(command=self.search_character_data)
        
        # Show default tab
        self.show_main_tab(0)
        
        # Load sample data on startup
        self.load_sample_data()
    
    def show_main_tab(self, tab_index):
        """Show the specified main tab"""
        # Update button appearances
        for i, btn in enumerate(self.tab_buttons):
            if i == tab_index:
                btn.config(bg=self.theme.PRIMARY_ACCENT, fg='white')
            else:
                btn.config(bg=self.theme.INPUT_BG, fg=self.theme.TEXT_COLOR)
        
        # Hide all panels
        if hasattr(self, 'weather_panel'):
            self.weather_panel.pack_forget()
        if hasattr(self, 'cobra_panel'):
            self.cobra_panel.pack_forget()
        if hasattr(self, 'interactive_panel'):
            self.interactive_panel.pack_forget()
        if hasattr(self, 'smart_panel'):
            self.smart_panel.pack_forget()
        
        # Show selected panel
        if tab_index == 0 and hasattr(self, 'weather_panel'):
            self.weather_panel.pack(fill='both', expand=True, padx=5, pady=5)
        elif tab_index == 1 and hasattr(self, 'cobra_panel'):
            self.cobra_panel.pack(fill='both', expand=True, padx=5, pady=5)
        elif tab_index == 2 and hasattr(self, 'interactive_panel'):
            self.interactive_panel.pack(fill='both', expand=True, padx=5, pady=5)
        elif tab_index == 3 and hasattr(self, 'smart_panel'):
            self.smart_panel.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.current_tab = tab_index
    
    def load_sample_data(self):
        """Load sample data to demonstrate the interface"""
        try:
            # Sample weather data
            sample_weather = {
                "city": "COBRA Command",
                "country": "Unknown",
                "temp": 72,
                "feels_like": 75,
                "humidity": 65,
                "pressure": 1013,
                "description": "Clear Skies - Perfect for Operations",
                "icon": "01d",
                "wind_speed": 5.2,
                "visibility": 10.0,
                "sunrise": "06:30",
                "sunset": "19:45",
                "timestamp": "Operational Status: ACTIVE"
            }
            
            # Sample character data
            sample_character = {
                "name": "Cobra Commander",
                "biography": "The ruthless leader of the terrorist organization COBRA. Known for his distinctive helmet and desire for world domination.",
                "affiliation": "COBRA",
                "speciality": "Terrorist Leader",
                "team": "COBRA Command"
            }
            
            # Update displays with sample data
            if hasattr(self, 'weather_panel'):
                self.weather_panel.update_weather_data(sample_weather)
            if hasattr(self, 'cobra_panel'):
                self.cobra_panel.update_character_data(sample_character)
            
        except Exception as e:
            print(f"⚠️ Error loading sample data: {e}")
    
    def create_fallback_sections(self, parent):
        """Create fallback sections when UI components are not available"""
        # Simple weather section
        weather_frame = tk.Frame(parent, bg=self.theme.GLASS_BG, relief='raised', bd=1)
        weather_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(
            weather_frame,
            text="⛈️ WEATHER INTELLIGENCE",
            font=self.theme.TITLE_FONT,
            fg=self.theme.PRIMARY_ACCENT,
            bg=self.theme.GLASS_BG
        ).pack(pady=20)
        
        tk.Label(
            weather_frame,
            text="Weather API integration ready for activation",
            font=self.theme.BODY_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        ).pack(pady=10)
        
        # Simple cobra section
        cobra_frame = tk.Frame(parent, bg=self.theme.GLASS_BG, relief='raised', bd=1)
        cobra_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(
            cobra_frame,
            text="🐍 COBRA INTELLIGENCE",
            font=self.theme.TITLE_FONT,
            fg="#dc143c",
            bg=self.theme.GLASS_BG
        ).pack(pady=20)
        
        tk.Label(
            cobra_frame,
            text="Character database ready for interrogation",
            font=self.theme.BODY_FONT,
            fg=self.theme.TEXT_COLOR,
            bg=self.theme.GLASS_BG
        ).pack(pady=10)
    
    def fetch_weather_data(self):
        """Fetch weather data from API"""
        if not hasattr(self, 'weather_panel'):
            return
            
        if not self.weather_api:
            # Demo mode - show sample data with real city input
            city = self.weather_panel.city_entry.get().strip() or "Demo City"
            
            sample_weather = {
                "city": city,
                "country": "Demo",
                "temp": 68,
                "feels_like": 72,
                "humidity": 58,
                "pressure": 1015,
                "description": "Partly Cloudy - Tactical Advantage",
                "icon": "02d",
                "wind_speed": 8.3,
                "visibility": 15.2,
                "sunrise": "06:45",
                "sunset": "19:20",
                "timestamp": f"LIVE DATA - {city.upper()}"
            }
            
            self.weather_panel.update_weather_data(sample_weather)
            print(f"📊 Demo weather data displayed for {city}")
            return
            
        city = self.weather_panel.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name.")
            return
            
        try:
            # Show loading
            self.weather_panel.temp_label.config(text="Loading weather data...")
            self.root.update()
            
            # Fetch weather data
            weather_data = self.weather_api.get_current_weather(city)
            
            # Update display
            self.weather_panel.update_weather_data(weather_data)
            
            # Log to database
            if self.database and "error" not in weather_data:
                self.database.log_weather_data(weather_data)
                self.database.log_user_search("weather", city, 1)
            
            # Check for severe weather and trigger alert
            if self.alert_system and self.weather_api:
                severe_conditions = self.weather_api.check_severe_weather(weather_data)
                if severe_conditions:
                    self.alert_system.trigger_alert(f"SEVERE WEATHER: {', '.join(severe_conditions)}")
            
        except Exception as e:
            error_msg = f"Error fetching weather data: {str(e)}"
            self.weather_panel.update_weather_data({"error": error_msg})
            print(f"❌ {error_msg}")
    
    def search_character_data(self):
        """Search for character data from G.I. Joe API"""
        if not hasattr(self, 'cobra_panel'):
            return
            
        if not self.gijoe_api:
            # Demo mode - show sample data with real character input
            character_name = self.cobra_panel.character_entry.get().strip() or "Demo Agent"
            
            # Sample character database
            character_db = {
                "cobra commander": {
                    "name": "Cobra Commander",
                    "biography": "The ruthless leader of COBRA. Master of disguise and manipulation, seeks world domination through technological superiority.",
                    "affiliation": "COBRA",
                    "speciality": "Terrorist Leader"
                },
                "destro": {
                    "name": "Destro",
                    "biography": "Arms dealer and weapons manufacturer. Wears a chrome-plated mask and leads the Military Armaments Research Syndicate (M.A.R.S.).",
                    "affiliation": "COBRA",
                    "speciality": "Weapons Supplier"
                },
                "duke": {
                    "name": "Duke",
                    "biography": "First Sergeant and field commander of G.I. Joe. Natural leader with exceptional tactical skills and unwavering loyalty.",
                    "affiliation": "G.I. Joe",
                    "speciality": "First Sergeant"
                },
                "snake eyes": {
                    "name": "Snake Eyes",
                    "biography": "Silent ninja commando and sword master. Wears black combat suit and never speaks. One of G.I. Joe's most effective operatives.",
                    "affiliation": "G.I. Joe",
                    "speciality": "Commando"
                }
            }
            
            char_data = character_db.get(character_name.lower(), {
                "name": character_name,
                "biography": f"Intelligence file for {character_name} is currently classified. Recommend further investigation.",
                "affiliation": "Unknown",
                "speciality": "Under Investigation"
            })
            
            self.cobra_panel.update_character_data(char_data)
            print(f"🔍 Demo character data displayed for {character_name}")
            return
            
        character_name = self.cobra_panel.character_entry.get().strip()
        if not character_name:
            messagebox.showwarning("Input Required", "Please enter a character name.")
            return
            
        try:
            # Show loading
            self.cobra_panel.char_name_label.config(text="Searching Cobra database...")
            self.root.update()
            
            # Search character data
            char_data = self.gijoe_api.get_character_data(character_name)
            
            # Update display
            self.cobra_panel.update_character_data(char_data)
            
            # Log to database
            if self.database and "error" not in char_data:
                self.database.log_character_lookup(character_name, char_data)
                self.database.log_user_search("character", character_name, 1)
            
        except Exception as e:
            error_msg = f"Error searching character: {str(e)}"
            self.cobra_panel.update_character_data({"error": error_msg})
            print(f"❌ {error_msg}")
    
    def run(self):
        """Start the application main loop"""
        print("Starting COBRA Weather Dominator...")
        print("Glassmorphic window initialized successfully!")
        self.root.mainloop()

def main():
    """Main function to run the application"""
    try:
        # You can switch themes here
        # app = GlassmorphicWindow(CobraTheme())  # For COBRA red theme
        app = GlassmorphicWindow()  # Default blue theme
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
