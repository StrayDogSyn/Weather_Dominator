"""
Smart Weather Features - Advanced AI and Machine Learning Features

This module implements smart weather features including:
1. Tomorrow's Guess - Weather prediction with confidence levels
2. Trend Detection - Temperature trends and pattern identification  
3. Activity Suggester - Weather-based activity recommendations

Author: Weather Dominator Team
Date: June 2025
"""

import os
import json
import random
import statistics
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

# Import our local modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.sqlite_store import WeatherDatabase
from data.weather_api import WeatherAPI


class SmartWeatherFeatures:
    """Smart weather analysis and prediction features"""
    
    def __init__(self, db_path: str = "weather_dominator.db"):
        """
        Initialize smart weather features system
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db = WeatherDatabase(db_path)
        self.weather_api = WeatherAPI()
        self.predictions_file = "data/exports/predictions_accuracy.json"
        self.ensure_data_directories()
    
    def ensure_data_directories(self):
        """Ensure all required data directories exist"""
        os.makedirs("data/exports", exist_ok=True)
        os.makedirs("data/user_preferences", exist_ok=True)
    
    # =============================================================================
    # 1. TOMORROW'S GUESS - Weather Prediction
    # =============================================================================
    
    def predict_tomorrows_weather(self, city: str) -> Dict[str, Any]:
        """
        Predict tomorrow's weather using basic prediction logic
        
        Args:
            city: City name to predict weather for
            
        Returns:
            Dictionary with prediction data and confidence level
        """
        # Get recent weather history for analysis
        recent_data = self.db.get_weather_history(city=city, days=7)
        
        if len(recent_data) < 3:
            return {
                "error": f"Insufficient historical data for {city}",
                "confidence": 0,
                "prediction": None
            }
        
        # Analyze recent trends
        temperatures = [r['temperature'] for r in recent_data if r.get('temperature')]
        humidity = [r['humidity'] for r in recent_data if r.get('humidity')]
        pressure = [r['pressure'] for r in recent_data if r.get('pressure')]
        descriptions = [r.get('description', '') for r in recent_data]
        
        # Basic prediction logic
        prediction = self._generate_basic_prediction(
            temperatures, humidity, pressure, descriptions
        )
        
        # Calculate confidence based on data consistency
        confidence = self._calculate_prediction_confidence(
            temperatures, humidity, pressure
        )
        
        # Store prediction for accuracy tracking
        self._store_prediction(city, prediction, confidence)
        
        return {
            "city": city,
            "prediction_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "prediction": prediction,
            "confidence": confidence,
            "method": "trend_analysis",
            "data_points": len(recent_data),
            "accuracy_note": "Prediction based on recent weather patterns"
        }
    
    def _generate_basic_prediction(self, temperatures: List[float], 
                                 humidity: List[float], 
                                 pressure: List[float],
                                 descriptions: List[str]) -> Dict[str, Any]:
        """Generate basic weather prediction from historical data"""
        
        if not temperatures:
            return {"error": "No temperature data available"}
        
        # Temperature prediction (simple trend analysis)
        if len(temperatures) >= 3:
            recent_temp_trend = temperatures[-1] - temperatures[-3]
            predicted_temp = round(temperatures[-1] + (recent_temp_trend * 0.5), 1)
        else:
            predicted_temp = round(statistics.mean(temperatures), 1)
        
        # Humidity prediction
        predicted_humidity = round(statistics.mean(humidity[-3:]), 1) if humidity else None
        
        # Pressure prediction
        predicted_pressure = round(statistics.mean(pressure[-3:]), 2) if pressure else None
        
        # Weather condition prediction (most common recent condition)
        if descriptions:
            condition_counts = defaultdict(int)
            for desc in descriptions[-3:]:  # Look at last 3 days
                condition_counts[desc.lower()] += 1
            predicted_condition = max(condition_counts.items(), key=lambda x: x[1])[0].title()
        else:
            predicted_condition = "Partly Cloudy"
        
        return {
            "temperature": predicted_temp,
            "humidity": predicted_humidity,
            "pressure": predicted_pressure,
            "condition": predicted_condition,
            "feels_like": round(predicted_temp - 2 + random.uniform(-1, 1), 1)
        }
    
    def _calculate_prediction_confidence(self, temperatures: List[float],
                                       humidity: List[float],
                                       pressure: List[float]) -> int:
        """Calculate confidence level (0-100) based on data consistency"""
        
        confidence_factors = []
        
        # Temperature consistency
        if len(temperatures) >= 3:
            temp_std = statistics.stdev(temperatures[-3:])
            temp_confidence = max(0, 100 - (temp_std * 10))  # Lower std = higher confidence
            confidence_factors.append(temp_confidence)
        
        # Data availability
        data_availability = (
            (50 if temperatures else 0) +
            (25 if humidity else 0) +
            (25 if pressure else 0)
        )
        confidence_factors.append(data_availability)
        
        # Historical data amount
        data_amount_confidence = min(100, len(temperatures) * 15)  # More data = more confidence
        confidence_factors.append(data_amount_confidence)
        
        return round(statistics.mean(confidence_factors)) if confidence_factors else 50
    
    def _store_prediction(self, city: str, prediction: Dict[str, Any], confidence: int):
        """Store prediction for later accuracy tracking"""
        
        prediction_data = {
            "city": city,
            "prediction_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "created_date": datetime.now().isoformat(),
            "prediction": prediction,
            "confidence": confidence,
            "verified": False
        }
        
        # Load existing predictions
        predictions = []
        if os.path.exists(self.predictions_file):
            try:
                with open(self.predictions_file, 'r') as f:
                    predictions = json.load(f)
            except:
                predictions = []
        
        predictions.append(prediction_data)
        
        # Save updated predictions
        with open(self.predictions_file, 'w') as f:
            json.dump(predictions, f, indent=2)
    
    def track_prediction_accuracy(self, city: str) -> Dict[str, Any]:
        """
        Track accuracy of previous predictions
        
        Args:
            city: City to check prediction accuracy for
            
        Returns:
            Dictionary with accuracy statistics
        """
        if not os.path.exists(self.predictions_file):
            return {"error": "No predictions found to track"}
        
        try:
            with open(self.predictions_file, 'r') as f:
                all_predictions = json.load(f)
        except:
            return {"error": "Could not load predictions data"}
        
        # Filter predictions for this city that can be verified
        city_predictions = [
            p for p in all_predictions 
            if p['city'].lower() == city.lower() 
            and datetime.strptime(p['prediction_date'], "%Y-%m-%d").date() <= datetime.now().date()
        ]
        
        if not city_predictions:
            return {"error": f"No verifiable predictions found for {city}"}
        
        # Calculate accuracy by comparing with actual weather
        accurate_predictions = 0
        total_predictions = len(city_predictions)
        
        for pred in city_predictions:
            pred_date = pred['prediction_date']            # Get actual weather for that date from database
            # Since get_weather_by_date doesn't exist, we'll get recent history and filter
            actual_weather = self._get_weather_for_date(city, pred_date)
            
            if actual_weather and not pred['verified']:
                # Simple accuracy check (within 5 degrees)
                pred_temp = pred['prediction'].get('temperature')
                actual_temp = actual_weather.get('temperature')
                
                if pred_temp and actual_temp and abs(pred_temp - actual_temp) <= 5:
                    accurate_predictions += 1
                
                # Mark as verified
                pred['verified'] = True
        
        # Update predictions file
        with open(self.predictions_file, 'w') as f:
            json.dump(all_predictions, f, indent=2)
        
        accuracy_percentage = round((accurate_predictions / total_predictions) * 100, 1) if total_predictions > 0 else 0
        
        return {
            "city": city,
            "total_predictions": total_predictions,
            "accurate_predictions": accurate_predictions,
            "accuracy_percentage": accuracy_percentage,
            "note": "Accuracy measured as temperature within 5°F of actual"
        }
    
    def _get_weather_for_date(self, city: str, date_str: str) -> Optional[Dict[str, Any]]:
        """
        Get weather data for a specific date
        
        Args:
            city: City name
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            Weather data dictionary or None if not found
        """
        # Get recent weather history (expand search to cover more days)
        weather_history = self.db.get_weather_history(city=city, days=60)
        
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        for record in weather_history:
            if record.get('timestamp'):
                record_date = datetime.fromisoformat(record['timestamp']).date()
                if record_date == target_date:
                    return record
        
        return None
    
    # =============================================================================
    # 2. TREND DETECTION
    # =============================================================================
    
    def detect_temperature_trends(self, city: str, days: int = 14) -> Dict[str, Any]:
        """
        Detect temperature trends and show trend arrows
        
        Args:
            city: City name to analyze trends for
            days: Number of days to analyze (default: 14)
            
        Returns:
            Dictionary with trend information and arrows
        """
        weather_data = self.db.get_weather_history(city=city, days=days)
        
        if len(weather_data) < 5:
            return {"error": f"Insufficient data for trend analysis for {city}"}
        
        # Extract temperatures with dates
        temp_data = []
        for record in weather_data:
            if record.get('temperature'):
                temp_data.append({
                    'date': datetime.fromisoformat(record['timestamp']),
                    'temperature': record['temperature']
                })
        
        # Sort by date
        temp_data.sort(key=lambda x: x['date'])
        
        # Analyze trends
        trends = self._analyze_temperature_trends(temp_data)
        
        return {
            "city": city,
            "analysis_period": f"Last {days} days",
            "data_points": len(temp_data),
            "trends": trends,
            "trend_arrows": self._generate_trend_arrows(trends),
            "summary": self._generate_trend_summary(trends)
        }
    
    def _analyze_temperature_trends(self, temp_data: List[Dict]) -> Dict[str, Any]:
        """Analyze temperature trends from historical data"""
        
        temperatures = [d['temperature'] for d in temp_data]
        dates = [d['date'] for d in temp_data]
        
        # Overall trend (simple linear regression)
        n = len(temperatures)
        if n < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        # Calculate trend direction
        x_values = list(range(n))
        mean_x = statistics.mean(x_values)
        mean_y = statistics.mean(temperatures)
        
        numerator = sum((x_values[i] - mean_x) * (temperatures[i] - mean_y) for i in range(n))
        denominator = sum((x_values[i] - mean_x) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        # Recent trend (last 5 days vs previous 5 days)
        if n >= 10:
            recent_avg = statistics.mean(temperatures[-5:])
            previous_avg = statistics.mean(temperatures[-10:-5])
            recent_change = recent_avg - previous_avg
        else:
            recent_change = 0
        
        # Short-term trend (last 3 days)
        if n >= 3:
            short_term_change = temperatures[-1] - temperatures[-3]
        else:
            short_term_change = 0
        
        return {
            "overall_slope": round(slope, 3),
            "overall_direction": "rising" if slope > 0.1 else "falling" if slope < -0.1 else "stable",
            "recent_change": round(recent_change, 1),
            "short_term_change": round(short_term_change, 1),
            "temperature_range": {
                "min": min(temperatures),
                "max": max(temperatures),
                "current": temperatures[-1]
            }
        }
    
    def _generate_trend_arrows(self, trends: Dict[str, Any]) -> Dict[str, str]:
        """Generate trend arrows based on trend analysis"""
        
        if "error" in trends:
            return {"overall": "➡️", "recent": "➡️", "short_term": "➡️"}
        
        arrows = {}
        
        # Overall trend arrow
        direction = trends.get("overall_direction", "stable")
        if direction == "rising":
            arrows["overall"] = "📈"
        elif direction == "falling":
            arrows["overall"] = "📉"
        else:
            arrows["overall"] = "➡️"
        
        # Recent trend arrow
        recent_change = trends.get("recent_change", 0)
        if recent_change > 2:
            arrows["recent"] = "🔥"  # Getting warmer
        elif recent_change < -2:
            arrows["recent"] = "🧊"  # Getting cooler
        else:
            arrows["recent"] = "🌡️"  # Stable
        
        # Short-term arrow
        short_change = trends.get("short_term_change", 0)
        if short_change > 1:
            arrows["short_term"] = "⬆️"
        elif short_change < -1:
            arrows["short_term"] = "⬇️"
        else:
            arrows["short_term"] = "➡️"
        
        return arrows
    
    def _generate_trend_summary(self, trends: Dict[str, Any]) -> str:
        """Generate human-readable trend summary"""
        
        if "error" in trends:
            return "Unable to determine trends due to insufficient data"
        
        direction = trends.get("overall_direction", "stable")
        recent_change = trends.get("recent_change", 0)
        
        if direction == "rising":
            base = "Temperatures are trending upward"
        elif direction == "falling":
            base = "Temperatures are trending downward"
        else:
            base = "Temperatures have been relatively stable"
        
        if abs(recent_change) > 3:
            if recent_change > 0:
                addition = f", with a noticeable warming of {recent_change:.1f}°F recently"
            else:
                addition = f", with a noticeable cooling of {abs(recent_change):.1f}°F recently"
        else:
            addition = " with minor recent fluctuations"
        
        return base + addition
    
    def identify_weather_patterns(self, city: str, days: int = 30) -> Dict[str, Any]:
        """
        Identify recurring weather patterns
        
        Args:
            city: City name to analyze
            days: Number of days to analyze
            
        Returns:
            Dictionary with identified patterns
        """
        weather_data = self.db.get_weather_history(city=city, days=days)
        
        if len(weather_data) < 7:
            return {"error": f"Insufficient data for pattern analysis for {city}"}
        
        patterns = {
            "weekly_patterns": self._analyze_weekly_patterns(weather_data),
            "weather_cycles": self._analyze_weather_cycles(weather_data),
            "pressure_patterns": self._analyze_pressure_patterns(weather_data)
        }
        
        return {
            "city": city,
            "analysis_period": f"Last {days} days",
            "patterns": patterns
        }
    
    def _analyze_weekly_patterns(self, weather_data: List[Dict]) -> Dict[str, Any]:
        """Analyze weekly weather patterns"""
        
        day_temps = defaultdict(list)
        
        for record in weather_data:
            if record.get('temperature'):
                date = datetime.fromisoformat(record['timestamp'])
                day_name = date.strftime('%A')
                day_temps[day_name].append(record['temperature'])
        
        day_averages = {}
        for day, temps in day_temps.items():
            if temps:
                day_averages[day] = round(statistics.mean(temps), 1)
        
        return {
            "daily_averages": day_averages,
            "warmest_day": max(day_averages.items(), key=lambda x: x[1]) if day_averages else None,
            "coolest_day": min(day_averages.items(), key=lambda x: x[1]) if day_averages else None
        }
    
    def _analyze_weather_cycles(self, weather_data: List[Dict]) -> Dict[str, Any]:
        """Analyze weather condition cycles"""
        
        conditions = [r.get('description', '').lower() for r in weather_data if r.get('description')]
        
        if len(conditions) < 3:
            return {"error": "Insufficient condition data"}
        
        # Look for consecutive weather patterns
        cycles = []
        current_cycle = [conditions[0]]
        
        for i in range(1, len(conditions)):
            if conditions[i] == conditions[i-1]:
                current_cycle.append(conditions[i])
            else:
                if len(current_cycle) > 1:
                    cycles.append({
                        "condition": current_cycle[0].title(),
                        "duration": len(current_cycle)
                    })
                current_cycle = [conditions[i]]
        
        # Add final cycle
        if len(current_cycle) > 1:
            cycles.append({
                "condition": current_cycle[0].title(),
                "duration": len(current_cycle)
            })
        
        return {
            "weather_cycles": cycles,
            "longest_cycle": max(cycles, key=lambda x: x['duration']) if cycles else None,
            "total_cycles": len(cycles)
        }
    
    def _analyze_pressure_patterns(self, weather_data: List[Dict]) -> Dict[str, Any]:
        """Analyze atmospheric pressure patterns"""
        
        pressures = [(datetime.fromisoformat(r['timestamp']), r['pressure']) 
                    for r in weather_data if r.get('pressure')]
        
        if len(pressures) < 5:
            return {"error": "Insufficient pressure data"}
        
        pressures.sort(key=lambda x: x[0])
        pressure_values = [p[1] for p in pressures]
        
        # Detect pressure trends
        rising_periods = 0
        falling_periods = 0
        
        for i in range(1, len(pressure_values)):
            if pressure_values[i] > pressure_values[i-1]:
                rising_periods += 1
            elif pressure_values[i] < pressure_values[i-1]:
                falling_periods += 1
        
        return {
            "pressure_trend": "mostly_rising" if rising_periods > falling_periods else 
                            "mostly_falling" if falling_periods > rising_periods else "variable",
            "rising_periods": rising_periods,
            "falling_periods": falling_periods,
            "pressure_range": {
                "min": round(min(pressure_values), 2),
                "max": round(max(pressure_values), 2),
                "current": round(pressure_values[-1], 2)
            }
        }
    
    # =============================================================================
    # 3. ACTIVITY SUGGESTER
    # =============================================================================
    
    def suggest_weather_based_activities(self, city: str) -> Dict[str, Any]:
        """
        Suggest activities based on current weather conditions
        
        Args:
            city: City name to get weather and suggest activities for
            
        Returns:
            Dictionary with activity suggestions
        """
        # Get current weather
        current_weather = self.weather_api.get_current_weather(city)
        
        if not current_weather or "error" in current_weather:
            return {"error": f"Could not get current weather for {city}"}
        
        # Extract weather parameters
        temperature = current_weather.get('temperature', 70)
        description = current_weather.get('description', '').lower()
        humidity = current_weather.get('humidity', 50)
        wind_speed = current_weather.get('wind_speed', 5)
        
        # Generate activity suggestions
        activities = self._generate_activity_suggestions(
            temperature, description, humidity, wind_speed
        )
        
        return {
            "city": city,
            "current_weather": {
                "temperature": temperature,
                "condition": description.title(),
                "humidity": humidity,
                "wind_speed": wind_speed
            },
            "activity_suggestions": activities,
            "weather_suitability": self._assess_weather_suitability(temperature, description)
        }
    
    def _generate_activity_suggestions(self, temperature: float, description: str, 
                                     humidity: float, wind_speed: float) -> Dict[str, List[str]]:
        """Generate activity suggestions based on weather parameters"""
        
        activities = {
            "outdoor": [],
            "indoor": [],
            "exercise": [],
            "social": []
        }
        
        # Temperature-based suggestions
        if temperature >= 80:
            activities["outdoor"].extend([
                "🏊‍♀️ Swimming or water activities",
                "🍦 Visit an ice cream shop",
                "🌳 Find shade in a park",
                "🌊 Beach or lake activities"
            ])
            activities["indoor"].extend([
                "❄️ Visit air-conditioned museums",
                "🛍️ Indoor shopping centers",
                "🎬 Movie theater"
            ])
        elif temperature >= 65:
            activities["outdoor"].extend([
                "🚶‍♀️ Walking or hiking",
                "🚴‍♀️ Cycling",
                "🏞️ Picnic in the park",
                "🎾 Outdoor sports"
            ])
        elif temperature >= 45:
            activities["outdoor"].extend([
                "🧥 Brisk walk with jacket",
                "☕ Outdoor café (with heater)",
                "🍂 Fall activities"
            ])
        else:
            activities["indoor"].extend([
                "🏠 Cozy indoor activities",
                "📚 Reading by the fireplace",
                "🍲 Cooking warm meals",
                "🎮 Indoor gaming"
            ])
        
        # Weather condition-based suggestions
        if "rain" in description or "drizzle" in description:
            activities["indoor"].extend([
                "☔ Indoor museums or galleries",
                "📖 Reading at a café",
                "🎭 Theater or cinema",
                "🍕 Try a new restaurant"
            ])
        elif "snow" in description:
            activities["outdoor"].extend([
                "⛄ Build a snowman",
                "🎿 Skiing or snowboarding",
                "❄️ Winter photography",
                "🏂 Snow activities"
            ])
        elif "clear" in description or "sunny" in description:
            activities["outdoor"].extend([
                "☀️ Outdoor photography",
                "🌻 Visit botanical gardens",
                "🏖️ Beach day",
                "🥾 Nature hiking"
            ])
        
        # Wind-based suggestions
        if wind_speed > 15:
            activities["outdoor"].extend([
                "🪁 Kite flying",
                "⛵ Sailing (if near water)",
                "🌪️ Wind photography"
            ])
            activities["indoor"].extend([
                "🏠 Stay indoors - windy conditions"
            ])
        
        # Humidity-based suggestions
        if humidity > 80:
            activities["indoor"].extend([
                "🏠 Air-conditioned spaces recommended",
                "💧 Stay hydrated indoors"
            ])
        
        # Exercise suggestions
        if temperature >= 60 and temperature <= 75 and "rain" not in description:
            activities["exercise"].extend([
                "🏃‍♀️ Perfect weather for jogging",
                "🚴‍♀️ Ideal cycling conditions",
                "⚽ Outdoor team sports",
                "🧘‍♀️ Outdoor yoga"
            ])
        else:
            activities["exercise"].extend([
                "🏋️‍♀️ Indoor gym workout",
                "🧘‍♀️ Indoor yoga or stretching",
                "🏓 Indoor sports",
                "💃 Dance or fitness classes"
            ])
        
        # Social suggestions
        if temperature >= 65 and "rain" not in description:
            activities["social"].extend([
                "🍔 Outdoor barbecue",
                "🎪 Outdoor events or festivals",
                "⚽ Group sports activities",
                "🌳 Park gatherings"
            ])
        else:
            activities["social"].extend([
                "🍕 Indoor dining with friends",
                "🎲 Board game night",
                "🎬 Group movie night",
                "☕ Cozy café meetups"
            ])
        
        return activities
    
    def _assess_weather_suitability(self, temperature: float, description: str) -> Dict[str, str]:
        """Assess suitability for different activity types"""
        
        suitability = {
            "outdoor_activities": "poor",
            "exercise": "poor",
            "social_gatherings": "fair",
            "travel": "fair"
        }
        
        # Temperature assessment
        if 65 <= temperature <= 80:
            suitability["outdoor_activities"] = "excellent"
            suitability["exercise"] = "excellent"
        elif 55 <= temperature <= 85:
            suitability["outdoor_activities"] = "good"
            suitability["exercise"] = "good"
        elif 45 <= temperature <= 90:
            suitability["outdoor_activities"] = "fair"
            suitability["exercise"] = "fair"
        
        # Weather condition adjustments
        if "rain" in description or "storm" in description:
            suitability["outdoor_activities"] = "poor"
            suitability["exercise"] = "poor"
            suitability["travel"] = "poor"
        elif "snow" in description:
            suitability["outdoor_activities"] = "fair"  # Winter activities
            suitability["exercise"] = "fair"
            suitability["travel"] = "poor"
        elif "clear" in description or "sunny" in description:
            # Boost ratings for clear weather
            if suitability["outdoor_activities"] in ["good", "fair"]:
                suitability["outdoor_activities"] = "excellent"
            if suitability["exercise"] in ["good", "fair"]:
                suitability["exercise"] = "excellent"
        
        return suitability
    
    def get_custom_activity_lists(self, weather_type: str) -> List[str]:
        """
        Get custom activity lists for specific weather types
        
        Args:
            weather_type: Type of weather ("sunny", "rainy", "snowy", "cloudy", "windy")
            
        Returns:
            List of suggested activities for the weather type
        """
        activity_lists = {
            "sunny": [
                "🌞 Beach volleyball",
                "🏖️ Sunbathing",
                "🥾 Hiking trails",
                "🚴‍♀️ Bike rides",
                "🌻 Garden work",
                "📸 Outdoor photography",
                "🏊‍♀️ Swimming",
                "⛳ Golf",
                "🎾 Tennis",
                "🛍️ Outdoor markets"
            ],
            "rainy": [
                "☔ Visit museums",
                "📚 Read books at library",
                "🎬 Watch movies",
                "🍲 Cook comfort food",
                "🎨 Indoor art projects",
                "🧩 Solve puzzles",
                "🎮 Video games",
                "☕ Café hopping",
                "🛀 Spa day at home",
                "📝 Journal writing"
            ],
            "snowy": [
                "⛄ Build snowmen",
                "🎿 Skiing/snowboarding",
                "❄️ Snow photography",
                "🏂 Snow angels",
                "🔥 Cozy fireplace time",
                "☕ Hot chocolate making",
                "🧣 Knitting/crafts",
                "🎯 Indoor target practice",
                "📖 Winter reading",
                "🍲 Hearty soup cooking"
            ],
            "cloudy": [
                "🚶‍♀️ Nature walks",
                "📸 Moody photography",
                "🏞️ Park exploration",
                "🎨 Outdoor sketching",
                "☕ Outdoor café visits",
                "🛍️ Window shopping",
                "🌿 Gardening",
                "🚴‍♀️ Leisurely bike rides",
                "🎭 Street performances",
                "🌳 Tree identification"
            ],
            "windy": [
                "🪁 Kite flying",
                "⛵ Sailing",
                "🌪️ Wind chime listening",
                "📸 Wind effect photography",
                "🏃‍♀️ Wind-assisted running",
                "🌬️ Wind power demos",
                "🏠 Indoor activities",
                "📚 Reading by windows",
                "🍵 Warm beverage making",
                "🧘‍♀️ Meditation indoors"
            ]
        }
        
        return activity_lists.get(weather_type.lower(), [
            "🌤️ Check current weather",
            "📱 Weather app exploration",
            "🌍 Weather around the world",
            "📊 Weather data analysis"
        ])
    
    def get_random_activity_suggestion(self, city: str) -> Dict[str, Any]:
        """
        Get a random activity suggestion based on current weather
        
        Args:
            city: City name to get weather and suggest activity for
            
        Returns:
            Dictionary with a random activity suggestion
        """
        # Get weather-based suggestions
        suggestions = self.suggest_weather_based_activities(city)
        
        if "error" in suggestions:
            return suggestions
        
        # Collect all activities
        all_activities = []
        for category, activities in suggestions["activity_suggestions"].items():
            all_activities.extend(activities)
        
        if not all_activities:
            return {"error": "No activities found for current weather"}
        
        # Pick a random activity
        random_activity = random.choice(all_activities)
        
        # Get weather condition for custom suggestions
        condition = suggestions["current_weather"]["condition"].lower()
        weather_type = "sunny"  # default
        
        if "rain" in condition:
            weather_type = "rainy"
        elif "snow" in condition:
            weather_type = "snowy"
        elif "cloud" in condition:
            weather_type = "cloudy"
        elif "wind" in condition:
            weather_type = "windy"
        elif "clear" in condition or "sun" in condition:
            weather_type = "sunny"
        
        custom_activities = self.get_custom_activity_lists(weather_type)
        random_custom = random.choice(custom_activities) if custom_activities else ""
        
        return {
            "city": city,
            "weather": suggestions["current_weather"],
            "random_suggestion": random_activity,
            "alternative_suggestion": random_custom,
            "weather_suitability": suggestions["weather_suitability"],
            "tip": "🎲 Refresh for a new random suggestion!"
        }


# =============================================================================
# CONVENIENCE FUNCTIONS AND EXAMPLE USAGE
# =============================================================================

def demo_smart_features():
    """Demonstrate all smart weather features"""
    
    smart = SmartWeatherFeatures()
    
    print("=== SMART WEATHER FEATURES DEMO ===\n")
    
    # Test prediction
    print("1. TOMORROW'S GUESS")
    print("-" * 30)
    prediction = smart.predict_tomorrows_weather("New York")
    print(f"Prediction: {json.dumps(prediction, indent=2)}")
    
    # Test accuracy tracking
    print("\n2. PREDICTION ACCURACY")
    print("-" * 30)
    accuracy = smart.track_prediction_accuracy("New York")
    print(f"Accuracy: {json.dumps(accuracy, indent=2)}")
    
    # Test trend detection
    print("\n3. TREND DETECTION")
    print("-" * 30)
    trends = smart.detect_temperature_trends("New York")
    print(f"Trends: {json.dumps(trends, indent=2)}")
    
    # Test pattern identification
    print("\n4. WEATHER PATTERNS")
    print("-" * 30)
    patterns = smart.identify_weather_patterns("New York")
    print(f"Patterns: {json.dumps(patterns, indent=2)}")
    
    # Test activity suggestions
    print("\n5. ACTIVITY SUGGESTER")
    print("-" * 30)
    activities = smart.suggest_weather_based_activities("New York")
    print(f"Activities: {json.dumps(activities, indent=2)}")
    
    # Test random suggestion
    print("\n6. RANDOM ACTIVITY")
    print("-" * 30)
    random_activity = smart.get_random_activity_suggestion("New York")
    print(f"Random Activity: {json.dumps(random_activity, indent=2)}")


def get_smart_features_summary():
    """Get a summary of all available smart features"""
    return {
        "Tomorrow's Guess": {
            "description": "AI-powered weather prediction with confidence levels",
            "functions": ["predict_tomorrows_weather", "track_prediction_accuracy"],
            "accuracy": "Basic trend analysis with accuracy tracking"
        },
        "Trend Detection": {
            "description": "Temperature trends and pattern identification",
            "functions": ["detect_temperature_trends", "identify_weather_patterns"],
            "features": ["Trend arrows", "Pattern cycles", "Pressure analysis"]
        },
        "Activity Suggester": {
            "description": "Weather-based activity recommendations",
            "functions": ["suggest_weather_based_activities", "get_random_activity_suggestion"],
            "categories": ["Outdoor", "Indoor", "Exercise", "Social"]
        }
    }


if __name__ == "__main__":
    demo_smart_features()
