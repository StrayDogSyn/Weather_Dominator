import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

class WeatherAPI:
    """OpenWeatherMap API integration for fetching weather data"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Weather API client
        
        Args:
            api_key: OpenWeatherMap API key. If None, will try config.json then environment variables
        """
        # Priority order: provided key > config.json > environment variable
        if api_key:
            self.api_key = api_key
        else:
            # Try config.json first
            self.api_key = None
            try:
                if os.path.exists('config.json'):
                    with open('config.json', 'r') as f:
                        config = json.load(f)
                        self.api_key = config.get('api_keys', {}).get('openweather')
            except Exception:
                pass
            
            # Fallback to environment variable
            if not self.api_key:
                self.api_key = os.getenv('OPENWEATHER_API_KEY')
        
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.icon_url = "http://openweathermap.org/img/w"
        
        if not self.api_key:
            print("⚠️ Warning: No OpenWeatherMap API key found.")
            print("   Add your API key to config.json or set OPENWEATHER_API_KEY environment variable")
    
    def get_current_weather(self, city: str, units: str = "imperial") -> Dict[str, Any]:
        """
        Fetch current weather for a given city
        
        Args:
            city: City name (e.g., "New York" or "London,UK")
            units: Temperature units ("imperial" for Fahrenheit, "metric" for Celsius)
            
        Returns:
            Dictionary containing weather data or error information
        """
        if not self.api_key:
            return {"error": "API key not configured"}
            
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse and structure the response
            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
                "icon_url": f"{self.icon_url}/{data['weather'][0]['icon']}.png",
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", 0),
                "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
                "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "units": units
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except KeyError as e:
            return {"error": f"Data parsing error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_weather_forecast(self, city: str, days: int = 5, units: str = "imperial") -> Dict[str, Any]:
        """
        Fetch weather forecast for a given city
        
        Args:
            city: City name
            days: Number of days for forecast (max 5 for free API)
            units: Temperature units
            
        Returns:
            Dictionary containing forecast data or error information
        """
        if not self.api_key:
            return {"error": "API key not configured"}
            
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units,
                "cnt": days * 8  # 8 forecasts per day (every 3 hours)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse forecast data
            forecasts = []
            for item in data["list"]:
                forecast = {
                    "datetime": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M"),
                    "date": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d"),
                    "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                    "temp": round(item["main"]["temp"]),
                    "temp_min": round(item["main"]["temp_min"]),
                    "temp_max": round(item["main"]["temp_max"]),
                    "humidity": item["main"]["humidity"],
                    "description": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"],
                    "icon_url": f"{self.icon_url}/{item['weather'][0]['icon']}.png",
                    "wind_speed": item["wind"]["speed"],
                    "pop": item.get("pop", 0) * 100  # Probability of precipitation
                }
                forecasts.append(forecast)
            
            forecast_data = {
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecasts": forecasts,
                "units": units
            }
            
            return forecast_data
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except KeyError as e:
            return {"error": f"Data parsing error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_weather_alerts(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch weather alerts for given coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing alert data or error information
        """
        if not self.api_key:
            return {"error": "API key not configured"}
            
        try:
            url = f"{self.base_url}/onecall"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "exclude": "minutely,hourly,daily"  # Only get alerts
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            alerts = data.get("alerts", [])
            
            # Parse alerts
            alert_data = []
            for alert in alerts:
                alert_info = {
                    "sender": alert.get("sender_name", "Unknown"),
                    "event": alert.get("event", "Weather Alert"),
                    "start": datetime.fromtimestamp(alert["start"]).strftime("%Y-%m-%d %H:%M"),
                    "end": datetime.fromtimestamp(alert["end"]).strftime("%Y-%m-%d %H:%M"),
                    "description": alert.get("description", "No description available"),
                    "tags": alert.get("tags", [])
                }
                alert_data.append(alert_info)
            
            return {"alerts": alert_data}
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except KeyError as e:
            return {"error": f"Data parsing error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_coordinates(self, city: str) -> Optional[Dict[str, float]]:
        """
        Get coordinates for a city name
        
        Args:
            city: City name
            
        Returns:
            Dictionary with lat/lon or None if not found
        """
        if not self.api_key:
            return None
            
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": city,
                "limit": 1,
                "appid": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"]
                }
            return None
            
        except Exception:
            return None
    
    def check_severe_weather(self, weather_data: Dict[str, Any]) -> List[str]:
        """
        Check for severe weather conditions that should trigger Cobra alerts
        
        Args:
            weather_data: Weather data from get_current_weather()
            
        Returns:
            List of severe weather conditions detected
        """
        if "error" in weather_data:
            return []
        
        severe_conditions = []
        description = weather_data.get("description", "").lower()
        wind_speed = weather_data.get("wind_speed", 0)
        
        # Check for severe weather keywords
        severe_keywords = [
            "storm", "thunderstorm", "hail", "tornado", "hurricane", 
            "blizzard", "extreme", "severe", "warning", "advisory"
        ]
        
        for keyword in severe_keywords:
            if keyword in description:
                severe_conditions.append(keyword.title())
        
        # Check wind speed (for imperial units - mph)
        if weather_data.get("units") == "imperial" and wind_speed > 25:
            severe_conditions.append("High Winds")
        elif weather_data.get("units") == "metric" and wind_speed > 11:  # m/s to mph conversion
            severe_conditions.append("High Winds")
        
        return severe_conditions

# Convenience functions for easy use
def get_weather(city: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to get current weather"""
    weather_api = WeatherAPI(api_key)
    return weather_api.get_current_weather(city)

def get_forecast(city: str, days: int = 5, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to get weather forecast"""
    weather_api = WeatherAPI(api_key)
    return weather_api.get_weather_forecast(city, days)

def check_alerts(city: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to check weather alerts"""
    weather_api = WeatherAPI(api_key)
    coords = weather_api.get_coordinates(city)
    if coords:
        return weather_api.get_weather_alerts(coords["lat"], coords["lon"])
    return {"error": "Could not get coordinates for city"}

# Example usage and testing
if __name__ == "__main__":
    # Test the weather API (requires API key)
    weather_api = WeatherAPI()
    
    # Test cities
    test_cities = ["New York", "London", "Tokyo"]
    
    for city in test_cities:
        print(f"\n🌤️ Testing weather for {city}:")
        weather = weather_api.get_current_weather(city)
        
        if "error" in weather:
            print(f"❌ Error: {weather['error']}")
        else:
            print(f"✅ Temperature: {weather['temp']}°F")
            print(f"✅ Description: {weather['description']}")
            print(f"✅ Humidity: {weather['humidity']}%")
            print(f"✅ Wind: {weather['wind_speed']} mph")
            
            # Check for severe weather
            severe = weather_api.check_severe_weather(weather)
            if severe:
                print(f"⚠️ Severe conditions: {', '.join(severe)}")
