import requests # type: ignore
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

from src.logger import get_logger
from src.config_manager import get_config_manager
from src.exceptions import APIError, ConfigurationError
from src.constants import (
    OPENWEATHER_BASE_URL,
    OPENWEATHER_ICON_URL,
    OPENWEATHER_GEO_URL,
    APIConfig,
)

# Initialize logger for this module
logger = get_logger(__name__)

class WeatherAPI:
    """OpenWeatherMap API integration for fetching weather data"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Weather API client
        
        Args:
            api_key: OpenWeatherMap API key. If None, will try ConfigManager then environment variables
            
        Raises:
            ConfigurationError: If API key cannot be found
        """
        logger.debug("Initializing WeatherAPI client")
        
        # Priority order: provided key > ConfigManager > environment variable
        if api_key:
            self.api_key = api_key
            logger.debug("Using provided API key")
        else:
            # Try ConfigManager first
            try:
                config_manager = get_config_manager()
                self.api_key = config_manager.get('api_keys.openweather')
                logger.debug("Retrieved API key from ConfigManager")
            except Exception as e:
                logger.debug(f"ConfigManager lookup failed: {e}")
                self.api_key = None
            
            # Fallback to environment variable
            if not self.api_key:
                self.api_key = os.getenv('OPENWEATHER_API_KEY')
                if self.api_key:
                    logger.debug("Retrieved API key from environment variable")
        
        self.base_url = OPENWEATHER_BASE_URL
        self.icon_url = OPENWEATHER_ICON_URL
        
        if not self.api_key:
            logger.warning("No OpenWeatherMap API key configured")
            logger.info("Add your API key to config.json or set OPENWEATHER_API_KEY environment variable")
    
    def get_current_weather(self, city: str, units: str = "imperial") -> Dict[str, Any]:
        """
        Fetch current weather for a given city
        
        Args:
            city: City name (e.g., "New York" or "London,UK")
            units: Temperature units ("imperial" for Fahrenheit, "metric" for Celsius)
            
        Returns:
            Dictionary containing weather data or error information
            
        Raises:
            APIError: If API request fails or returns invalid data
        """
        logger.info(f"Fetching current weather for: {city} (units: {units})")
        
        if not self.api_key:
            logger.error("API key not configured")
            raise ConfigurationError("OpenWeatherMap API key not configured")
            
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            logger.debug(f"Making API request to {url}")
            response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Received weather data for {city}")
            
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
            
            logger.info(f"Successfully fetched weather for {city}: {weather_data['temp']}° {weather_data['description']}")
            return weather_data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for city: {city}")
            raise APIError(f"Request timeout while fetching weather for {city}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {city}: {e}")
            raise APIError(f"HTTP error: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error for {city}: {e}")
            raise APIError(f"Network error: {str(e)}")
        except KeyError as e:
            logger.error(f"Data parsing error for {city}: missing key {e}")
            raise APIError(f"Invalid response data: missing {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error fetching weather for {city}")
            raise APIError(f"Unexpected error: {str(e)}")
    
    def get_weather_forecast(self, city: str, days: int = 5, units: str = "imperial") -> Dict[str, Any]:
        """
        Fetch weather forecast for a given city
        
        Args:
            city: City name
            days: Number of days for forecast (max 5 for free API)
            units: Temperature units
            
        Returns:
            Dictionary containing forecast data or error information
            
        Raises:
            APIError: If API request fails or returns invalid data
        """
        logger.info(f"Fetching {days}-day forecast for: {city}")
        
        if not self.api_key:
            logger.error("API key not configured")
            raise ConfigurationError("OpenWeatherMap API key not configured")
            
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units,
                "cnt": days * 8  # 8 forecasts per day (every 3 hours)
            }
            
            logger.debug(f"Making forecast API request to {url}")
            response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Received forecast data for {city}")
            
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
            
            logger.info(f"Successfully fetched {len(forecasts)} forecast entries for {city}")
            return forecast_data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for forecast: {city}")
            raise APIError(f"Request timeout while fetching forecast for {city}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for forecast {city}: {e}")
            raise APIError(f"HTTP error: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error for forecast {city}: {e}")
            raise APIError(f"Network error: {str(e)}")
        except KeyError as e:
            logger.error(f"Forecast data parsing error for {city}: missing key {e}")
            raise APIError(f"Invalid forecast data: missing {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error fetching forecast for {city}")
            raise APIError(f"Unexpected error: {str(e)}")
    
    def get_weather_alerts(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch weather alerts for given coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing alert data or error information
            
        Raises:
            APIError: If API request fails or returns invalid data
        """
        logger.info(f"Fetching weather alerts for coordinates: ({lat}, {lon})")
        
        if not self.api_key:
            logger.error("API key not configured")
            raise ConfigurationError("OpenWeatherMap API key not configured")
            
        try:
            url = f"{self.base_url}/onecall"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "exclude": "minutely,hourly,daily"  # Only get alerts
            }
            
            logger.debug(f"Making alerts API request to {url}")
            response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            alerts = data.get("alerts", [])
            logger.debug(f"Received {len(alerts)} weather alerts")
            
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
            
            logger.info(f"Successfully fetched {len(alert_data)} weather alerts")
            return {"alerts": alert_data}
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for alerts at ({lat}, {lon})")
            raise APIError(f"Request timeout while fetching alerts")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for alerts: {e}")
            raise APIError(f"HTTP error: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error for alerts: {e}")
            raise APIError(f"Network error: {str(e)}")
        except KeyError as e:
            logger.error(f"Alert data parsing error: missing key {e}")
            raise APIError(f"Invalid alert data: missing {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error fetching alerts")
            raise APIError(f"Unexpected error: {str(e)}")
    
    def get_coordinates(self, city: str) -> Optional[Dict[str, float]]:
        """
        Get coordinates for a city name
        
        Args:
            city: City name
            
        Returns:
            Dictionary with lat/lon or None if not found
        """
        logger.info(f"Fetching coordinates for: {city}")
        
        if not self.api_key:
            logger.error("API key not configured")
            return None
            
        try:
            url = OPENWEATHER_GEO_URL
            params = {
                "q": city,
                "limit": 1,
                "appid": self.api_key
            }
            
            logger.debug(f"Making geocoding API request to {url}")
            response = requests.get(url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            if data:
                coords = {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"]
                }
                logger.info(f"Found coordinates for {city}: {coords}")
                return coords
            
            logger.warning(f"No coordinates found for city: {city}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching coordinates for {city}: {e}")
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
            logger.debug("Cannot check severe weather: error in weather data")
            return []
        
        severe_conditions = []
        description = weather_data.get("description", "").lower()
        wind_speed = weather_data.get("wind_speed", 0)
        
        logger.debug(f"Checking severe weather conditions: {description}, wind: {wind_speed}")
        
        # Check for severe weather keywords
        severe_keywords = [
            "storm", "thunderstorm", "hail", "tornado", "hurricane", 
            "blizzard", "extreme", "severe", "warning", "advisory"
        ]
        
        for keyword in severe_keywords:
            if keyword in description:
                severe_conditions.append(keyword.title())
                logger.info(f"Severe weather detected: {keyword.title()}")
        
        # Check wind speed (for imperial units - mph)
        if weather_data.get("units") == "imperial" and wind_speed > 25:
            severe_conditions.append("High Winds")
            logger.info(f"High winds detected: {wind_speed} mph")
        elif weather_data.get("units") == "metric" and wind_speed > 11:  # m/s to mph conversion
            severe_conditions.append("High Winds")
            logger.info(f"High winds detected: {wind_speed} m/s")
        
        if severe_conditions:
            logger.warning(f"Total severe conditions detected: {len(severe_conditions)}")
        
        return severe_conditions

# Convenience functions for easy use
def get_weather(city: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to get current weather"""
    logger.debug(f"Convenience function: get_weather for {city}")
    weather_api = WeatherAPI(api_key)
    return weather_api.get_current_weather(city)

def get_forecast(city: str, days: int = 5, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to get weather forecast"""
    logger.debug(f"Convenience function: get_forecast for {city}, {days} days")
    weather_api = WeatherAPI(api_key)
    return weather_api.get_weather_forecast(city, days)

def check_alerts(city: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to check weather alerts"""
    logger.debug(f"Convenience function: check_alerts for {city}")
    weather_api = WeatherAPI(api_key)
    coords = weather_api.get_coordinates(city)
    if coords:
        return weather_api.get_weather_alerts(coords["lat"], coords["lon"])
    logger.warning(f"Could not get coordinates for city: {city}")
    return {"error": "Could not get coordinates for city"}

# Example usage and testing
if __name__ == "__main__":
    # Test the weather API (requires API key)
    logger.info("Starting WeatherAPI test")
    weather_api = WeatherAPI()
    
    # Test cities
    test_cities = ["New York", "London", "Tokyo"]
    
    for city in test_cities:
        logger.info(f"Testing weather for {city}")
        
        try:
            weather = weather_api.get_current_weather(city)
            logger.info(f"Temperature: {weather['temp']}°F")
            logger.info(f"Description: {weather['description']}")
            logger.info(f"Humidity: {weather['humidity']}%")
            logger.info(f"Wind: {weather['wind_speed']} mph")
            
            # Check for severe weather
            severe = weather_api.check_severe_weather(weather)
            if severe:
                logger.warning(f"Severe conditions: {', '.join(severe)}")
                
        except (APIError, ConfigurationError) as e:
            logger.error(f"Error fetching weather for {city}: {e}")
    
    logger.info("WeatherAPI test completed")
