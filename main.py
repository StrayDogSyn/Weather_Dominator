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
    from ui.glass_ui import WeatherDisplayPanel, CobraIntelPanel, CobraAlertSystem, create_glass_widget
    from data.weather_api import WeatherAPI
    from data.gijoe_api import GIJoeAPI
    from db.sqlite_store import WeatherDatabase
    from ml.predictor import WeatherPredictor
    from utils.helpers import TemperatureConverter, DataFormatter, ImageCache, ConfigManager
    UI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some modules not available: {e}")
    UI_AVAILABLE = False
    # Set classes to None when imports fail
    WeatherDisplayPanel = None
    CobraIntelPanel = None
    CobraAlertSystem = None
    create_glass_widget = None
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
        self.root = tk.Tk()        # Initialize components if available
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
        self.add_close_button()        # Initialize alert system after window is created
        if UI_AVAILABLE and CobraAlertSystem is not None:
            self.alert_system = CobraAlertSystem(self.root)
        
    def setup_window(self):
        """Configure the main window with transparent background"""
        self.root.title("COBRA Weather Dominator")
        self.root.geometry("800x600")
        self.root.configure(bg=self.theme.WINDOW_BG)
        
        # Center the window on screen
        self.center_window()
        
        # Make window semi-transparent (Windows specific)
        if sys.platform.startswith('win'):
            self.root.wm_attributes('-alpha', self.theme.WINDOW_ALPHA)
            # Remove window decorations for modern look
            self.root.overrideredirect(False)
            
        # Set minimum size
        self.root.minsize(600, 400)
        
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
        
        # Inner content frame
        self.content_frame = tk.Frame(
            self.glass_frame,
            bg=self.theme.CONTENT_BG,
            relief='flat',
            bd=0
        )
        self.content_frame.pack(fill='both', expand=True, 
                              padx=self.theme.PADDING_LARGE, 
                              pady=self.theme.PADDING_LARGE)
        
        # Add glassmorphic effect simulation with multiple frames
        self.add_glassmorphic_effects()
        
        # Add title
        self.add_title()
        
        # Create two main sections: Weather Data Display and Cobra Intelligence Panel
        self.create_main_sections()
        
    def add_glassmorphic_effects(self):
        """Add visual effects to simulate glassmorphism"""
        # Top highlight for glass effect
        highlight_frame = tk.Frame(
            self.glass_frame,
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
        title_frame.pack(fill='x', pady=(20, 40))
        
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
        separator.pack(fill='x', pady=(20, 0), padx=50)
        
    def add_close_button(self):
        """Add a custom close button for borderless window"""
        close_frame = tk.Frame(self.content_frame, bg=self.theme.CONTENT_BG)
        close_frame.pack(side='bottom', fill='x', pady=(0, 10))
        
        close_button = tk.Button(
            close_frame,
            text="✕",
            font=('Arial', 12, 'bold'),
            fg=self.theme.DANGER_COLOR,
            bg=self.theme.BUTTON_BG,
            activebackground=self.theme.DANGER_COLOR,
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=10,
            pady=5,
            command=self.root.quit
        )
        close_button.pack(side='right')
        
        # Add hover effects
        def on_enter(e):
            close_button.config(bg=self.theme.DANGER_COLOR, fg='white')
        
        def on_leave(e):
            close_button.config(bg=self.theme.BUTTON_BG, fg=self.theme.DANGER_COLOR)
            
        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)
        
    def create_main_sections(self):
        """Create the two main sections: Weather Data Display and Cobra Intelligence Panel"""
        # Create main sections container
        sections_frame = tk.Frame(self.content_frame, bg=self.theme.CONTENT_BG)
        sections_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        if UI_AVAILABLE and WeatherDisplayPanel is not None and CobraIntelPanel is not None:
            try:
                # Weather Data Display Panel (left side)
                self.weather_panel = WeatherDisplayPanel(sections_frame, self.theme)
                self.weather_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
                
                # Cobra Intelligence Panel (right side)
                self.cobra_panel = CobraIntelPanel(sections_frame, self.theme)
                self.cobra_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
                
                # Connect button events
                self.weather_panel.fetch_button.config(command=self.fetch_weather_data)
                self.cobra_panel.search_button.config(command=self.search_character_data)
                
            except Exception as e:
                print(f"⚠️ Error creating UI panels: {e}")
                self.create_fallback_sections(sections_frame)
        else:
            self.create_fallback_sections(sections_frame)
    
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
        if not self.weather_api:
            messagebox.showwarning("API Not Available", "Weather API is not configured.")
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
        if not self.gijoe_api:
            messagebox.showwarning("API Not Available", "G.I. Joe API is not configured.")
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
