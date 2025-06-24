"""
ui/interactive_features.py - Interactive Features for Weather Dominator
Implements Weather Journal, Favorite Cities, and Weather Alerts
as specified in the project requirements.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import threading
import time

# Handle relative imports for both direct execution and module imports
try:
    from ..data.weather_features import WeatherFeatures
    from ..data.weather_api import WeatherAPI
    from ..db.sqlite_store import WeatherDatabase
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data.weather_features import WeatherFeatures
    from data.weather_api import WeatherAPI
    from db.sqlite_store import WeatherDatabase

class InteractiveFeatures:
    """Interactive features for weather application"""
    
    def __init__(self, db_path: str = "weather_dominator.db"):
        """
        Initialize interactive features system
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db = WeatherDatabase(db_path)
        self.weather_api = WeatherAPI()
        self.weather_features = WeatherFeatures(db_path)
        
        # File paths
        self.journal_file = "data/weather_journal.json"
        self.favorites_file = "data/favorite_cities.json"
        self.alerts_file = "data/weather_alerts.json"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Initialize data structures
        self._init_data_files()
        
        # Alert monitoring
        self.alert_thread = None
        self.monitoring_alerts = False
    
    def _init_data_files(self):
        """Initialize data files if they don't exist"""
        default_data = {
            self.journal_file: [],
            self.favorites_file: [],
            self.alerts_file: []
        }
        
        for file_path, default_content in default_data.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_content, f, indent=2)
    
    # =============================================================================
    # 1. WEATHER JOURNAL
    # =============================================================================
    
    def add_daily_weather_note(self, city: str, note: str, mood: str = "neutral") -> bool:
        """
        Add daily weather notes
        
        Args:
            city: City name
            note: Weather note/observation
            mood: User's mood (happy, sad, neutral, energetic, calm)
            
        Returns:
            Success status
        """
        try:
            # Get current weather for context
            current_weather = self.weather_api.get_current_weather(city)
            
            journal_entry = {
                "id": f"{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "date": datetime.now().isoformat(),
                "city": city,
                "note": note,
                "mood": mood,
                "weather_data": current_weather,
                "tags": self._extract_tags(note)
            }
            
            # Load existing entries
            with open(self.journal_file, 'r') as f:
                entries = json.load(f)
            
            # Add new entry
            entries.append(journal_entry)
            
            # Save updated entries
            with open(self.journal_file, 'w') as f:
                json.dump(entries, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error adding journal entry: {e}")
            return False
    
    def track_mood_with_weather(self, mood: str, weather_condition: str, 
                               temperature: float, notes: str = "") -> bool:
        """
        Track mood correlations with weather
        
        Args:
            mood: User's mood
            weather_condition: Current weather condition
            temperature: Current temperature
            notes: Additional notes
            
        Returns:
            Success status
        """
        mood_entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "weather_condition": weather_condition,
            "temperature": temperature,
            "notes": notes,
            "mood_score": self._mood_to_score(mood)
        }
        
        try:
            # Load existing entries
            with open(self.journal_file, 'r') as f:
                entries = json.load(f)
            
            # Add mood tracking to latest entry or create new one
            if entries and entries[-1].get('date', '')[:10] == datetime.now().strftime('%Y-%m-%d'):
                entries[-1]['mood_tracking'] = mood_entry
            else:
                # Create new entry for mood tracking
                new_entry = {
                    "id": f"mood_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "date": datetime.now().isoformat(),
                    "type": "mood_tracking",
                    "mood_tracking": mood_entry
                }
                entries.append(new_entry)
            
            # Save updated entries
            with open(self.journal_file, 'w') as f:
                json.dump(entries, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error tracking mood: {e}")
            return False
    
    def save_journal_to_text_file(self, filename: Optional[str] = None) -> str:
        """
        Save journal entries to a text file
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weather_journal_{timestamp}.txt"
        
        filepath = os.path.join("data", "exports", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            with open(self.journal_file, 'r') as f:
                entries = json.load(f)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("WEATHER JOURNAL\n")
                f.write("=" * 50 + "\n\n")
                
                for entry in entries:
                    f.write(f"Date: {entry.get('date', 'Unknown')[:10]}\n")
                    f.write(f"City: {entry.get('city', 'Unknown')}\n")
                    f.write(f"Mood: {entry.get('mood', 'Unknown')}\n")
                    
                    weather_data = entry.get('weather_data', {})
                    if weather_data and 'error' not in weather_data:
                        f.write(f"Weather: {weather_data.get('temperature', 'N/A')}°F - {weather_data.get('description', 'N/A')}\n")
                    
                    f.write(f"Note: {entry.get('note', 'No note')}\n")
                    
                    if entry.get('tags'):
                        f.write(f"Tags: {', '.join(entry['tags'])}\n")
                    
                    f.write("-" * 30 + "\n\n")
            
            return filepath
            
        except Exception as e:
            print(f"Error saving journal to text file: {e}")
            return ""
    
    def get_journal_entries(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get journal entries for specified period
        
        Args:
            days: Number of days to retrieve
            
        Returns:
            List of journal entries
        """
        try:
            with open(self.journal_file, 'r') as f:
                entries = json.load(f)
            
            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_entries = []
            
            for entry in entries:
                entry_date = datetime.fromisoformat(entry.get('date', ''))
                if entry_date >= cutoff_date:
                    filtered_entries.append(entry)
            
            return sorted(filtered_entries, key=lambda x: x.get('date', ''), reverse=True)
            
        except Exception as e:
            print(f"Error getting journal entries: {e}")
            return []
    
    def analyze_mood_weather_correlation(self) -> Dict[str, Any]:
        """
        Analyze correlation between mood and weather
        
        Returns:
            Analysis results
        """
        try:
            entries = self.get_journal_entries(90)  # Last 3 months
            
            mood_weather_data = []
            mood_counts = {}
            weather_mood_counts = {}
            
            for entry in entries:
                mood = entry.get('mood')
                weather_data = entry.get('weather_data', {})
                
                if mood and weather_data and 'error' not in weather_data:
                    temp = weather_data.get('temperature')
                    description = weather_data.get('description', '').lower()
                    
                    mood_weather_data.append({
                        'mood': mood,
                        'temperature': temp,
                        'description': description,
                        'date': entry.get('date', '')
                    })
                    
                    # Count moods
                    mood_counts[mood] = mood_counts.get(mood, 0) + 1
                    
                    # Count weather-mood combinations
                    weather_key = self._categorize_weather(description)
                    if weather_key not in weather_mood_counts:
                        weather_mood_counts[weather_key] = {}
                    weather_mood_counts[weather_key][mood] = weather_mood_counts[weather_key].get(mood, 0) + 1
            
            # Calculate correlations
            correlations = {}
            for weather_type, moods in weather_mood_counts.items():
                total_entries = sum(moods.values())
                correlations[weather_type] = {
                    mood: round((count / total_entries) * 100, 1)
                    for mood, count in moods.items()
                }
            
            return {
                "total_entries": len(mood_weather_data),
                "analysis_period": "Last 90 days",
                "mood_distribution": mood_counts,
                "weather_mood_correlations": correlations,
                "insights": self._generate_mood_insights(correlations)
            }
            
        except Exception as e:
            print(f"Error analyzing mood-weather correlation: {e}")
            return {"error": str(e)}
    
    # =============================================================================
    # 2. FAVORITE CITIES
    # =============================================================================
    
    def add_preferred_location(self, city: str, country: str = "", 
                             nickname: str = "") -> bool:
        """
        Add city to favorites with preferred settings
        
        Args:
            city: City name
            country: Country name
            nickname: Optional nickname for the city
            
        Returns:
            Success status
        """
        try:
            # Validate city by getting weather data
            weather_data = self.weather_api.get_current_weather(city)
            if "error" in weather_data:
                return False
            
            favorite = {
                "id": f"{city.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
                "city": city,
                "country": country or weather_data.get('country', ''),
                "nickname": nickname,
                "added_date": datetime.now().isoformat(),
                "last_checked": datetime.now().isoformat(),
                "check_frequency": "daily",  # daily, hourly, manual
                "alert_enabled": True,
                "temperature_unit": "fahrenheit",
                "notes": ""
            }
            
            # Load existing favorites
            with open(self.favorites_file, 'r') as f:
                favorites = json.load(f)
            
            # Check if city already exists
            for fav in favorites:
                if fav['city'].lower() == city.lower():
                    return False  # Already exists
            
            # Add new favorite
            favorites.append(favorite)
            
            # Save updated favorites
            with open(self.favorites_file, 'w') as f:
                json.dump(favorites, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error adding favorite city: {e}")
            return False
    
    def enable_quick_switching(self) -> List[Dict[str, Any]]:
        """
        Get favorites list for quick switching
        
        Returns:
            List of favorite cities with quick access data
        """
        try:
            with open(self.favorites_file, 'r') as f:
                favorites = json.load(f)
            
            quick_access = []
            for fav in favorites:
                # Get current weather for each favorite
                weather_data = self.weather_api.get_current_weather(fav['city'])
                
                quick_item = {
                    "city": fav['city'],
                    "nickname": fav.get('nickname', fav['city']),
                    "current_temp": weather_data.get('temperature', 'N/A') if 'error' not in weather_data else 'N/A',
                    "current_condition": weather_data.get('description', 'Unknown') if 'error' not in weather_data else 'Unknown',
                    "last_checked": fav.get('last_checked', ''),
                    "alert_enabled": fav.get('alert_enabled', False)
                }
                quick_access.append(quick_item)
            
            return quick_access
            
        except Exception as e:
            print(f"Error getting quick access list: {e}")
            return []
    
    def setup_persistent_storage(self, backup_interval: int = 24) -> bool:
        """
        Setup persistent storage with backup
        
        Args:
            backup_interval: Backup interval in hours
            
        Returns:
            Success status
        """
        try:
            # Create backup directory
            backup_dir = "data/backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Create backup of current data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_files = {
                "journal": self.journal_file,
                "favorites": self.favorites_file,
                "alerts": self.alerts_file
            }
            
            for name, file_path in backup_files.items():
                if os.path.exists(file_path):
                    backup_path = os.path.join(backup_dir, f"{name}_backup_{timestamp}.json")
                    with open(file_path, 'r') as src, open(backup_path, 'w') as dst:
                        dst.write(src.read())
            
            # Schedule regular backups (simplified - in a real app, use a proper scheduler)
            self._schedule_backups(backup_interval)
            
            return True
            
        except Exception as e:
            print(f"Error setting up persistent storage: {e}")
            return False
    
    def remove_favorite_city(self, city: str) -> bool:
        """Remove city from favorites"""
        try:
            with open(self.favorites_file, 'r') as f:
                favorites = json.load(f)
            
            # Remove the city
            favorites = [fav for fav in favorites if fav['city'].lower() != city.lower()]
            
            # Save updated favorites
            with open(self.favorites_file, 'w') as f:
                json.dump(favorites, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error removing favorite city: {e}")
            return False
    
    # =============================================================================
    # 3. WEATHER ALERTS
    # =============================================================================
    
    def set_temperature_threshold(self, city: str, min_temp: float, 
                                max_temp: float, alert_type: str = "both") -> bool:
        """
        Set temperature threshold alerts
        
        Args:
            city: City name to monitor
            min_temp: Minimum temperature threshold
            max_temp: Maximum temperature threshold
            alert_type: "min", "max", or "both"
            
        Returns:
            Success status
        """
        try:
            alert = {
                "id": f"temp_{city.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
                "type": "temperature",
                "city": city,
                "min_threshold": min_temp,
                "max_threshold": max_temp,
                "alert_type": alert_type,
                "enabled": True,
                "created_date": datetime.now().isoformat(),
                "last_triggered": None,
                "trigger_count": 0
            }
            
            # Load existing alerts
            with open(self.alerts_file, 'r') as f:
                alerts = json.load(f)
            
            # Remove existing temperature alert for this city
            alerts = [a for a in alerts if not (a.get('type') == 'temperature' and a.get('city', '').lower() == city.lower())]
            
            # Add new alert
            alerts.append(alert)
            
            # Save updated alerts
            with open(self.alerts_file, 'w') as f:
                json.dump(alerts, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error setting temperature threshold: {e}")
            return False
    
    def create_simple_notifications(self, notification_type: str = "popup") -> bool:
        """
        Create simple notification system
        
        Args:
            notification_type: "popup", "console", or "file"
            
        Returns:
            Success status
        """
        try:
            # Start alert monitoring if not already running
            if not self.monitoring_alerts:
                self.start_alert_monitoring(notification_type)
            
            return True
            
        except Exception as e:
            print(f"Error creating notifications: {e}")
            return False
    
    def configure_user_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Configure user alert settings
        
        Args:
            settings: User settings dictionary
            
        Returns:
            Success status
        """
        try:
            settings_file = "data/user_settings.json"
            
            # Default settings
            default_settings = {
                "notification_method": "popup",
                "check_interval": 30,  # minutes
                "quiet_hours_start": "22:00",
                "quiet_hours_end": "07:00",
                "temperature_unit": "fahrenheit",
                "enable_sound": True,
                "alert_history_days": 30
            }
            
            # Merge with provided settings
            final_settings = {**default_settings, **settings}
            
            # Save settings
            with open(settings_file, 'w') as f:
                json.dump(final_settings, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error configuring user settings: {e}")
            return False
    
    def start_alert_monitoring(self, notification_type: str = "popup"):
        """Start background alert monitoring"""
        if self.monitoring_alerts:
            return
        
        self.monitoring_alerts = True
        self.alert_thread = threading.Thread(
            target=self._monitor_alerts, 
            args=(notification_type,),
            daemon=True
        )
        self.alert_thread.start()
    
    def stop_alert_monitoring(self):
        """Stop background alert monitoring"""
        self.monitoring_alerts = False
        if self.alert_thread:
            self.alert_thread.join(timeout=5)
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get list of active alerts"""
        try:
            with open(self.alerts_file, 'r') as f:
                alerts = json.load(f)
            
            return [alert for alert in alerts if alert.get('enabled', False)]
            
        except Exception as e:
            print(f"Error getting active alerts: {e}")
            return []
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _extract_tags(self, note: str) -> List[str]:
        """Extract hashtags and keywords from note"""
        import re
        
        # Extract hashtags
        hashtags = re.findall(r'#\w+', note.lower())
        
        # Extract weather-related keywords
        weather_keywords = [
            'sunny', 'cloudy', 'rainy', 'snowy', 'windy', 'foggy',
            'hot', 'cold', 'warm', 'cool', 'humid', 'dry'
        ]
        
        found_keywords = [word for word in weather_keywords if word in note.lower()]
        
        return list(set(hashtags + found_keywords))
    
    def _mood_to_score(self, mood: str) -> int:
        """Convert mood to numerical score"""
        mood_scores = {
            "very_happy": 5,
            "happy": 4,
            "neutral": 3,
            "sad": 2,
            "very_sad": 1,
            "energetic": 4,
            "calm": 3,
            "anxious": 2,
            "excited": 4,
            "tired": 2
        }
        return mood_scores.get(mood.lower(), 3)
    
    def _categorize_weather(self, description: str) -> str:
        """Categorize weather description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['clear', 'sunny']):
            return 'sunny'
        elif any(word in description_lower for word in ['rain', 'drizzle', 'shower']):
            return 'rainy'
        elif any(word in description_lower for word in ['snow', 'blizzard']):
            return 'snowy'
        elif any(word in description_lower for word in ['cloud', 'overcast']):
            return 'cloudy'
        elif any(word in description_lower for word in ['storm', 'thunder']):
            return 'stormy'
        else:
            return 'other'
    
    def _generate_mood_insights(self, correlations: Dict[str, Dict[str, float]]) -> List[str]:
        """Generate insights from mood-weather correlations"""
        insights = []
        
        for weather_type, moods in correlations.items():
            if moods:
                # Find most common mood for this weather type
                top_mood = max(moods.items(), key=lambda x: x[1])
                if top_mood[1] > 40:  # If more than 40% of the time
                    insights.append(f"You tend to feel {top_mood[0]} during {weather_type} weather ({top_mood[1]}% of the time)")
        
        return insights
    
    def _schedule_backups(self, interval_hours: int):
        """Schedule regular backups (simplified implementation)"""
        # In a real application, you would use a proper task scheduler
        # This is a simplified version for demonstration
        pass
    
    def _monitor_alerts(self, notification_type: str):
        """Background alert monitoring loop"""
        while self.monitoring_alerts:
            try:
                alerts = self.get_active_alerts()
                
                for alert in alerts:
                    if alert['type'] == 'temperature':
                        self._check_temperature_alert(alert, notification_type)
                
                # Check every 5 minutes
                time.sleep(300)
                
            except Exception as e:
                print(f"Error in alert monitoring: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _check_temperature_alert(self, alert: Dict[str, Any], notification_type: str):
        """Check if temperature alert should be triggered"""
        try:
            city = alert['city']
            weather_data = self.weather_api.get_current_weather(city)
            
            if "error" in weather_data:
                return
            
            current_temp = weather_data.get('temperature')
            if current_temp is None:
                return
            
            should_alert = False
            message = ""
            
            alert_type = alert.get('alert_type', 'both')
            min_threshold = alert.get('min_threshold')
            max_threshold = alert.get('max_threshold')
            
            if alert_type in ['min', 'both'] and current_temp <= min_threshold:
                should_alert = True
                message = f"🌡️ Cold Alert: {city} is {current_temp}°F (below {min_threshold}°F threshold)"
            
            elif alert_type in ['max', 'both'] and current_temp >= max_threshold:
                should_alert = True
                message = f"🌡️ Heat Alert: {city} is {current_temp}°F (above {max_threshold}°F threshold)"
            
            if should_alert:
                self._send_notification(message, notification_type)
                
                # Update alert record
                alert['last_triggered'] = datetime.now().isoformat()
                alert['trigger_count'] = alert.get('trigger_count', 0) + 1
                
                # Save updated alert
                with open(self.alerts_file, 'r') as f:
                    alerts = json.load(f)
                
                for i, a in enumerate(alerts):
                    if a['id'] == alert['id']:
                        alerts[i] = alert
                        break
                
                with open(self.alerts_file, 'w') as f:
                    json.dump(alerts, f, indent=2)
        
        except Exception as e:
            print(f"Error checking temperature alert: {e}")
    
    def _send_notification(self, message: str, notification_type: str):
        """Send notification based on type"""
        try:
            if notification_type == "popup":
                # For GUI applications, this would show a popup
                print(f"ALERT: {message}")
            elif notification_type == "console":
                print(f"WEATHER ALERT: {message}")
            elif notification_type == "file":
                alert_log = "data/alert_log.txt"
                with open(alert_log, 'a') as f:
                    f.write(f"{datetime.now().isoformat()}: {message}\n")
        
        except Exception as e:
            print(f"Error sending notification: {e}")

# Convenience functions for easy use
def add_weather_note(city: str, note: str, mood: str = "neutral") -> bool:
    """Add weather journal note"""
    interactive = InteractiveFeatures()
    return interactive.add_daily_weather_note(city, note, mood)

def add_favorite_city(city: str, nickname: str = "") -> bool:
    """Add city to favorites"""
    interactive = InteractiveFeatures()
    return interactive.add_preferred_location(city, nickname=nickname)

def set_temp_alert(city: str, min_temp: float, max_temp: float) -> bool:
    """Set temperature alert for city"""
    interactive = InteractiveFeatures()
    return interactive.set_temperature_threshold(city, min_temp, max_temp)

def get_favorite_cities() -> List[Dict[str, Any]]:
    """Get list of favorite cities"""
    interactive = InteractiveFeatures()
    return interactive.enable_quick_switching()

def analyze_mood_patterns() -> Dict[str, Any]:
    """Analyze mood and weather patterns"""
    interactive = InteractiveFeatures()
    return interactive.analyze_mood_weather_correlation()

# Example usage and testing
if __name__ == "__main__":
    # Test Interactive Features
    interactive = InteractiveFeatures()
    
    print("🎯 Interactive Features Test")
    print("=" * 35)
    
    # Test 1: Weather Journal
    print(f"\n📔 Testing Weather Journal:")
    success = interactive.add_daily_weather_note(
        "New York", 
        "Beautiful sunny day, perfect for a walk in the park! #sunny #happy",
        "happy"
    )
    print(f"✅ Journal entry added: {success}")
    
    # Add a few more entries for testing
    interactive.track_mood_with_weather("energetic", "clear sky", 75.0, "Feeling great today!")
    
    # Export journal
    journal_file = interactive.save_journal_to_text_file()
    print(f"✅ Journal exported to: {journal_file}")
    
    # Test 2: Favorite Cities
    print(f"\n⭐ Testing Favorite Cities:")
    success = interactive.add_preferred_location("Los Angeles", "USA", "LA")
    print(f"✅ Favorite city added: {success}")
    
    success = interactive.add_preferred_location("London", "UK", "London Town")
    print(f"✅ Favorite city added: {success}")
    
    favorites = interactive.enable_quick_switching()
    print(f"✅ Quick access list: {len(favorites)} cities")
    
    # Test 3: Weather Alerts
    print(f"\n🚨 Testing Weather Alerts:")
    success = interactive.set_temperature_threshold("New York", 32.0, 90.0)
    print(f"✅ Temperature alert set: {success}")
    
    success = interactive.create_simple_notifications("console")
    print(f"✅ Notification system started: {success}")
    
    # Test user settings
    settings = {
        "notification_method": "console",
        "check_interval": 15,
        "temperature_unit": "fahrenheit"
    }
    success = interactive.configure_user_settings(settings)
    print(f"✅ User settings configured: {success}")
    
    # Test 4: Mood Analysis
    print(f"\n🧠 Testing Mood Analysis:")
    analysis = interactive.analyze_mood_weather_correlation()
    if "error" not in analysis:
        print(f"✅ Mood analysis completed: {analysis['total_entries']} entries analyzed")
        if analysis.get('insights'):
            print(f"✅ Insights generated: {len(analysis['insights'])} insights")
    else:
        print(f"⚠️ Mood analysis: {analysis.get('error', 'No data available yet')}")
    
    # Test 5: Persistent Storage
    print(f"\n💾 Testing Persistent Storage:")
    success = interactive.setup_persistent_storage(24)
    print(f"✅ Persistent storage setup: {success}")
    
    print(f"\n🎯 Interactive Features Test Complete!")
    
    # Cleanup: Stop alert monitoring
    interactive.stop_alert_monitoring()
