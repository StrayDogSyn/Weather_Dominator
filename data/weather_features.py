"""
data/weather_features.py - Advanced Weather Data Features
Implements Weather History Tracker, Simple Statistics, and City Comparison features
as specified in the project requirements.
"""

import sqlite3
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import statistics
import os

from .weather_api import WeatherAPI
from ..db.sqlite_store import WeatherDatabase

class WeatherFeatures:
    """Advanced weather data analysis and tracking features"""
    
    def __init__(self, db_path: str = "weather_dominator.db"):
        """
        Initialize weather features system
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db = WeatherDatabase(db_path)
        self.weather_api = WeatherAPI()
    
    # =============================================================================
    # 1. WEATHER HISTORY TRACKER
    # =============================================================================
    
    def save_daily_weather_to_csv(self, city: str, days: int = 7) -> str:
        """
        Save daily weather data to CSV file
        
        Args:
            city: City name to export data for
            days: Number of days to include (default: 7)
            
        Returns:
            Path to the created CSV file
        """        # Get weather data for the specified days
        weather_data = self.db.get_weather_history(city=city, days=days)
        
        # Create CSV filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_history_{city.replace(' ', '_')}_{timestamp}.csv"
        filepath = os.path.join("data", "exports", filename)
        
        # Ensure exports directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write CSV file
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'date', 'city', 'country', 'temperature', 'feels_like',
                'humidity', 'pressure', 'description', 'wind_speed',
                'wind_direction', 'visibility', 'units'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in weather_data:
                writer.writerow({
                    'date': record['timestamp'],
                    'city': record['city'],
                    'country': record.get('country', ''),
                    'temperature': record.get('temperature'),
                    'feels_like': record.get('feels_like'),
                    'humidity': record.get('humidity'),
                    'pressure': record.get('pressure'),
                    'description': record.get('description', ''),
                    'wind_speed': record.get('wind_speed'),
                    'wind_direction': record.get('wind_direction'),                    'visibility': record.get('visibility'),
                    'units': record.get('units', 'imperial')
                })
        
        return filepath
    
    def display_last_7_days(self, city: str) -> List[Dict[str, Any]]:
        """
        Display weather data for the last 7 days
        
        Args:
            city: City name to get data for
            
        Returns:
            List of weather records for the last 7 days
        """
        weather_data = self.db.get_weather_history(city=city, days=7)
        
        # Group by day and get the most recent entry for each day
        daily_data = defaultdict(list)
        for record in weather_data:
            day = datetime.fromisoformat(record['timestamp']).date()
            daily_data[day].append(record)
        
        # Get the latest record for each day
        last_7_days = []
        for day in sorted(daily_data.keys(), reverse=True)[:7]:
            latest_record = max(daily_data[day], 
                              key=lambda x: datetime.fromisoformat(x['timestamp']))
            last_7_days.append(latest_record)
        
        return last_7_days
    
    def calculate_weekly_averages(self, city: str, weeks: int = 4) -> Dict[str, Any]:
        """
        Calculate weekly averages for temperature, humidity, pressure, etc.
        
        Args:
            city: City name to calculate averages for
            weeks: Number of weeks to include in calculation
            
        Returns:
            Dictionary containing weekly averages
        """
        days = weeks * 7
        weather_data = self.db.get_weather_history(city=city, days=days)
        
        if not weather_data:
            return {"error": f"No weather data found for {city}"}
        
        # Extract numeric values
        temperatures = [r['temperature'] for r in weather_data if r.get('temperature')]
        feels_like = [r['feels_like'] for r in weather_data if r.get('feels_like')]
        humidity = [r['humidity'] for r in weather_data if r.get('humidity')]
        pressure = [r['pressure'] for r in weather_data if r.get('pressure')]
        wind_speed = [r['wind_speed'] for r in weather_data if r.get('wind_speed')]
        
        # Calculate averages
        averages = {
            "city": city,
            "period": f"Last {weeks} weeks",
            "data_points": len(weather_data),
            "averages": {
                "temperature": round(statistics.mean(temperatures), 1) if temperatures else None,
                "feels_like": round(statistics.mean(feels_like), 1) if feels_like else None,
                "humidity": round(statistics.mean(humidity), 1) if humidity else None,
                "pressure": round(statistics.mean(pressure), 2) if pressure else None,
                "wind_speed": round(statistics.mean(wind_speed), 1) if wind_speed else None
            },
            "extremes": {
                "max_temperature": max(temperatures) if temperatures else None,
                "min_temperature": min(temperatures) if temperatures else None,
                "max_humidity": max(humidity) if humidity else None,
                "min_humidity": min(humidity) if humidity else None
            }
        }
        
        return averages
      # =============================================================================
    # 2. SIMPLE STATISTICS
    # =============================================================================
    
    def get_min_max_temperature_tracking(self, city: str, days: int = 30) -> Dict[str, Any]:
        """
        Track minimum and maximum temperatures over specified period
        
        Args:
            city: City name to track
            days: Number of days to analyze
            
        Returns:
            Dictionary with min/max temperature tracking data
        """
        weather_data = self.db.get_weather_history(city=city, days=days)
        
        if not weather_data:
            return {"error": f"No temperature data found for {city}"}
        
        temperatures = [r['temperature'] for r in weather_data if r.get('temperature')]
        
        if not temperatures:
            return {"error": f"No valid temperature readings for {city}"}
        
        # Find records with min and max temperatures
        min_temp = min(temperatures)
        max_temp = max(temperatures)
        
        min_record = next(r for r in weather_data if r.get('temperature') == min_temp)
        max_record = next(r for r in weather_data if r.get('temperature') == max_temp)
        
        return {
            "city": city,
            "period": f"Last {days} days",
            "total_readings": len(temperatures),
            "temperature_range": {
                "minimum": {
                    "value": min_temp,
                    "date": min_record['timestamp'],
                    "description": min_record.get('description', 'N/A')
                },
                "maximum": {
                    "value": max_temp,
                    "date": max_record['timestamp'],
                    "description": max_record.get('description', 'N/A')
                },
                "difference": round(max_temp - min_temp, 1)
            },
            "statistics": {
                "average": round(statistics.mean(temperatures), 1),
                "median": round(statistics.median(temperatures), 1),
                "std_deviation": round(statistics.stdev(temperatures), 2) if len(temperatures) > 1 else 0            }
        }
    
    def get_weather_type_counting(self, city: str, days: int = 30) -> Dict[str, Any]:
        """
        Count different weather types and conditions
        
        Args:
            city: City name to analyze
            days: Number of days to analyze
            
        Returns:
            Dictionary with weather type counts and percentages
        """
        weather_data = self.db.get_weather_history(city=city, days=days)
        
        if not weather_data:
            return {"error": f"No weather data found for {city}"}
        
        # Count weather descriptions
        weather_counts = defaultdict(int)
        total_records = len(weather_data)
        
        for record in weather_data:
            description = record.get('description', 'Unknown')
            weather_counts[description.lower()] += 1
        
        # Calculate percentages and sort by frequency
        weather_stats = []
        for weather_type, count in sorted(weather_counts.items(), 
                                        key=lambda x: x[1], reverse=True):
            percentage = round((count / total_records) * 100, 1)
            weather_stats.append({
                "type": weather_type.title(),
                "count": count,
                "percentage": percentage
            })
        
        # Categorize by major weather types
        categories = {
            "clear": ["clear sky", "few clouds"],
            "cloudy": ["scattered clouds", "broken clouds", "overcast clouds"],
            "rainy": ["light rain", "moderate rain", "heavy rain", "drizzle"],
            "stormy": ["thunderstorm", "heavy thunderstorm", "storm"],
            "snowy": ["light snow", "snow", "heavy snow", "blizzard"],
            "foggy": ["mist", "fog", "haze"]
        }
        
        category_counts = defaultdict(int)
        for record in weather_data:
            description = record.get('description', '').lower()
            categorized = False
            for category, keywords in categories.items():
                if any(keyword in description for keyword in keywords):
                    category_counts[category] += 1
                    categorized = True
                    break
            if not categorized:
                category_counts["other"] += 1
        
        category_stats = []
        for category, count in category_counts.items():
            percentage = round((count / total_records) * 100, 1)
            category_stats.append({
                "category": category.title(),
                "count": count,
                "percentage": percentage
            })
        
        return {
            "city": city,
            "period": f"Last {days} days",
            "total_records": total_records,
            "detailed_weather_types": weather_stats,
            "weather_categories": sorted(category_stats, 
                                       key=lambda x: x['count'], reverse=True)
        }
    
    def display_in_labels(self, data: Dict[str, Any]) -> List[str]:
        """
        Format weather statistics for display in UI labels
        
        Args:
            data: Statistics data dictionary
            
        Returns:
            List of formatted strings for display
        """
        labels = []
        
        if "temperature_range" in data:
            temp_data = data["temperature_range"]
            labels.extend([
                f"🌡️ Temperature Range: {temp_data['minimum']['value']}° - {temp_data['maximum']['value']}°",
                f"📊 Average: {data['statistics']['average']}°",
                f"📈 Max: {temp_data['maximum']['value']}° on {temp_data['maximum']['date'][:10]}",
                f"📉 Min: {temp_data['minimum']['value']}° on {temp_data['minimum']['date'][:10]}"
            ])
        
        if "weather_categories" in data:
            labels.append("🌤️ Weather Distribution:")
            for category in data["weather_categories"][:5]:  # Top 5 categories
                labels.append(f"  {category['category']}: {category['percentage']}% ({category['count']} days)")
        
        if "averages" in data:
            avg = data["averages"]
            labels.extend([
                f"🌡️ Avg Temperature: {avg.get('temperature', 'N/A')}°",
                f"💧 Avg Humidity: {avg.get('humidity', 'N/A')}%",
                f"🌪️ Avg Wind Speed: {avg.get('wind_speed', 'N/A')} mph",
                f"📊 Avg Pressure: {avg.get('pressure', 'N/A')} inHg"
            ])
        
        return labels
    
    # =============================================================================
    # 3. CITY COMPARISON
    # =============================================================================
    
    def compare_2_cities_side_by_side(self, city1: str, city2: str, 
                                     days: int = 7) -> Dict[str, Any]:
        """
        Compare weather data for 2 cities side-by-side
        
        Args:
            city1: First city to compare
            city2: Second city to compare
            days: Number of days to compare (default: 7)
            
        Returns:
            Dictionary with side-by-side comparison data
        """
        # Get current weather for both cities
        current1 = self.weather_api.get_current_weather(city1)
        current2 = self.weather_api.get_current_weather(city2)
        
        # Get historical averages
        avg1 = self.calculate_weekly_averages(city1, weeks=1)
        avg2 = self.calculate_weekly_averages(city2, weeks=1)
        
        # Get min/max data
        minmax1 = self.get_min_max_temperature_tracking(city1, days)
        minmax2 = self.get_min_max_temperature_tracking(city2, days)
        
        comparison = {
            "comparison_date": datetime.now().isoformat(),
            "period": f"Last {days} days",
            "cities": {
                city1: {
                    "current_weather": current1,
                    "averages": avg1.get("averages", {}),
                    "temperature_range": minmax1.get("temperature_range", {}),
                    "data_points": avg1.get("data_points", 0)
                },
                city2: {
                    "current_weather": current2,
                    "averages": avg2.get("averages", {}),
                    "temperature_range": minmax2.get("temperature_range", {}),
                    "data_points": avg2.get("data_points", 0)
                }
            },
            "comparison_metrics": self._calculate_comparison_metrics(
                city1, city2, current1, current2, avg1, avg2
            )
        }
        
        return comparison
    
    def show_temperature_differences(self, city1: str, city2: str, 
                                   days: int = 7) -> Dict[str, Any]:
        """
        Show temperature differences between two cities
        
        Args:
            city1: First city
            city2: Second city
            days: Number of days to analyze
            
        Returns:
            Dictionary with temperature difference analysis
        """
        minmax1 = self.get_min_max_temperature_tracking(city1, days)
        minmax2 = self.get_min_max_temperature_tracking(city2, days)
        
        if "error" in minmax1 or "error" in minmax2:
            return {"error": "Insufficient data for comparison"}
        
        temp1 = minmax1["statistics"]
        temp2 = minmax2["statistics"]
        
        differences = {
            "cities": [city1, city2],
            "period": f"Last {days} days",
            "temperature_comparison": {
                "average_difference": round(temp1["average"] - temp2["average"], 1),
                "max_difference": round(
                    minmax1["temperature_range"]["maximum"]["value"] - 
                    minmax2["temperature_range"]["maximum"]["value"], 1
                ),
                "min_difference": round(
                    minmax1["temperature_range"]["minimum"]["value"] - 
                    minmax2["temperature_range"]["minimum"]["value"], 1
                )
            },
            "city_details": {
                city1: {
                    "average": temp1["average"],
                    "max": minmax1["temperature_range"]["maximum"]["value"],
                    "min": minmax1["temperature_range"]["minimum"]["value"],
                    "range": minmax1["temperature_range"]["difference"]
                },
                city2: {
                    "average": temp2["average"],
                    "max": minmax2["temperature_range"]["maximum"]["value"],
                    "min": minmax2["temperature_range"]["minimum"]["value"],
                    "range": minmax2["temperature_range"]["difference"]
                }
            },
            "analysis": {
                "warmer_city": city1 if temp1["average"] > temp2["average"] else city2,
                "temperature_gap": abs(temp1["average"] - temp2["average"]),
                "more_variable_city": city1 if minmax1["temperature_range"]["difference"] > 
                                            minmax2["temperature_range"]["difference"] else city2
            }
        }
        
        return differences
    
    def simple_text_display(self, comparison_data: Dict[str, Any]) -> List[str]:
        """
        Create simple text display for city comparison
        
        Args:
            comparison_data: Comparison data from compare_2_cities_side_by_side
            
        Returns:
            List of formatted strings for simple text display
        """
        display_lines = []
        
        if "cities" in comparison_data:
            cities = list(comparison_data["cities"].keys())
            city1, city2 = cities[0], cities[1]
            
            data1 = comparison_data["cities"][city1]
            data2 = comparison_data["cities"][city2]
            
            display_lines.extend([
                f"🏙️ CITY COMPARISON: {city1.upper()} vs {city2.upper()}",
                "=" * 50,
                ""
            ])
            
            # Current weather comparison
            if "current_weather" in data1 and "current_weather" in data2:
                curr1 = data1["current_weather"]
                curr2 = data2["current_weather"]
                
                if "error" not in curr1 and "error" not in curr2:
                    display_lines.extend([
                        "🌤️ CURRENT WEATHER:",
                        f"  {city1}: {curr1.get('temperature', 'N/A')}°F - {curr1.get('description', 'N/A')}",
                        f"  {city2}: {curr2.get('temperature', 'N/A')}°F - {curr2.get('description', 'N/A')}",
                        ""
                    ])
            
            # Average comparison
            if "averages" in data1 and "averages" in data2:
                avg1 = data1["averages"]
                avg2 = data2["averages"]
                
                display_lines.extend([
                    "📊 AVERAGE CONDITIONS:",
                    f"  Temperature: {city1} {avg1.get('temperature', 'N/A')}° | {city2} {avg2.get('temperature', 'N/A')}°",
                    f"  Humidity: {city1} {avg1.get('humidity', 'N/A')}% | {city2} {avg2.get('humidity', 'N/A')}%",
                    f"  Wind Speed: {city1} {avg1.get('wind_speed', 'N/A')} mph | {city2} {avg2.get('wind_speed', 'N/A')} mph",
                    ""
                ])
            
            # Temperature range comparison
            if "temperature_range" in data1 and "temperature_range" in data2:
                range1 = data1["temperature_range"]
                range2 = data2["temperature_range"]
                
                display_lines.extend([
                    "🌡️ TEMPERATURE RANGES:",
                    f"  {city1}: {range1.get('minimum', {}).get('value', 'N/A')}° - {range1.get('maximum', {}).get('value', 'N/A')}°",
                    f"  {city2}: {range2.get('minimum', {}).get('value', 'N/A')}° - {range2.get('maximum', {}).get('value', 'N/A')}°",
                    ""
                ])
        
        # Add comparison metrics if available
        if "comparison_metrics" in comparison_data:
            metrics = comparison_data["comparison_metrics"]
            display_lines.extend([
                "🔍 COMPARISON INSIGHTS:",
                f"  Warmer City: {metrics.get('warmer_city', 'N/A')}",
                f"  Temperature Difference: {metrics.get('temperature_difference', 'N/A')}°",
                f"  More Humid: {metrics.get('more_humid_city', 'N/A')}",
                f"  Windier: {metrics.get('windier_city', 'N/A')}"
            ])
        
        return display_lines
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    def _calculate_comparison_metrics(self, city1: str, city2: str, 
                                    current1: Dict, current2: Dict,
                                    avg1: Dict, avg2: Dict) -> Dict[str, Any]:
        """Calculate comparison metrics between two cities"""
        metrics = {}
        
        # Current temperature comparison
        if ("error" not in current1 and "error" not in current2 and
            current1.get("temperature") and current2.get("temperature")):
            temp_diff = current1["temperature"] - current2["temperature"]
            metrics["temperature_difference"] = round(temp_diff, 1)
            metrics["warmer_city"] = city1 if temp_diff > 0 else city2
        
        # Average comparisons
        if ("averages" in avg1 and "averages" in avg2):
            avg1_data = avg1["averages"]
            avg2_data = avg2["averages"]
            
            # Humidity comparison
            if avg1_data.get("humidity") and avg2_data.get("humidity"):
                metrics["more_humid_city"] = (city1 if avg1_data["humidity"] > avg2_data["humidity"] 
                                            else city2)
                metrics["humidity_difference"] = round(
                    abs(avg1_data["humidity"] - avg2_data["humidity"]), 1
                )
            
            # Wind speed comparison
            if avg1_data.get("wind_speed") and avg2_data.get("wind_speed"):
                metrics["windier_city"] = (city1 if avg1_data["wind_speed"] > avg2_data["wind_speed"] 
                                         else city2)
                metrics["wind_speed_difference"] = round(
                    abs(avg1_data["wind_speed"] - avg2_data["wind_speed"]), 1                )
        
        return metrics
    
    def export_comparison_data(self, comparison_data: Dict[str, Any], 
                             filename: Optional[str] = None) -> str:
        """
        Export comparison data to JSON file
        
        Args:
            comparison_data: Comparison data to export
            filename: Optional custom filename
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"city_comparison_{timestamp}.json"
        
        filepath = os.path.join("data", "exports", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comparison_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def get_comprehensive_city_report(self, city: str, days: int = 30) -> Dict[str, Any]:
        """
        Generate a comprehensive weather report for a city
        
        Args:
            city: City name
            days: Number of days to analyze
            
        Returns:
            Comprehensive weather report
        """
        report = {
            "city": city,
            "report_date": datetime.now().isoformat(),
            "analysis_period": f"Last {days} days",
            "current_weather": self.weather_api.get_current_weather(city),
            "historical_summary": self.calculate_weekly_averages(city, weeks=days//7),
            "temperature_analysis": self.get_min_max_temperature_tracking(city, days),
            "weather_patterns": self.get_weather_type_counting(city, days),
            "recent_data": self.display_last_7_days(city)
        }
        
        return report

# Convenience functions for easy use
def track_weather_history(city: str, days: int = 7) -> str:
    """Export weather history to CSV"""
    features = WeatherFeatures()
    return features.save_daily_weather_to_csv(city, days)

def get_weather_stats(city: str, days: int = 30) -> Dict[str, Any]:
    """Get comprehensive weather statistics"""
    features = WeatherFeatures()
    return {
        "temperature_tracking": features.get_min_max_temperature_tracking(city, days),
        "weather_types": features.get_weather_type_counting(city, days),
        "weekly_averages": features.calculate_weekly_averages(city, weeks=days//7)
    }

def compare_cities(city1: str, city2: str, days: int = 7) -> Dict[str, Any]:
    """Compare two cities weather data"""
    features = WeatherFeatures()
    return features.compare_2_cities_side_by_side(city1, city2, days)

def get_city_report(city: str, days: int = 30) -> Dict[str, Any]:
    """Get comprehensive city weather report"""
    features = WeatherFeatures()
    return features.get_comprehensive_city_report(city, days)

# Example usage and testing
if __name__ == "__main__":
    # Test the Weather Features system
    features = WeatherFeatures()
    
    print("🌤️ Weather Features System Test")
    print("=" * 40)
    
    test_city = "New York"
    
    # Test 1: Weather History Tracker
    print(f"\n📊 Testing Weather History for {test_city}:")
    try:
        csv_file = features.save_daily_weather_to_csv(test_city, 7)
        print(f"✅ CSV exported to: {csv_file}")
        
        last_7_days = features.display_last_7_days(test_city)
        print(f"✅ Last 7 days data: {len(last_7_days)} records")
        
        weekly_avg = features.calculate_weekly_averages(test_city, 4)
        if "error" not in weekly_avg:
            print(f"✅ Weekly averages calculated: {weekly_avg['data_points']} data points")
        
    except Exception as e:
        print(f"❌ History tracking error: {e}")
    
    # Test 2: Simple Statistics
    print(f"\n📈 Testing Simple Statistics for {test_city}:")
    try:
        temp_tracking = features.get_min_max_temperature_tracking(test_city, 30)
        if "error" not in temp_tracking:
            print(f"✅ Temperature tracking: {temp_tracking['total_readings']} readings")
        
        weather_types = features.get_weather_type_counting(test_city, 30)
        if "error" not in weather_types:
            print(f"✅ Weather types: {len(weather_types['detailed_weather_types'])} types found")
        
    except Exception as e:
        print(f"❌ Statistics error: {e}")
    
    # Test 3: City Comparison
    print(f"\n🏙️ Testing City Comparison:")
    try:
        comparison = features.compare_2_cities_side_by_side("New York", "Los Angeles", 7)
        print(f"✅ Cities compared: {list(comparison['cities'].keys())}")
        
        temp_diff = features.show_temperature_differences("New York", "Los Angeles", 7)
        if "error" not in temp_diff:
            print(f"✅ Temperature differences calculated")
        
        display_text = features.simple_text_display(comparison)
        print(f"✅ Display text generated: {len(display_text)} lines")
        
    except Exception as e:
        print(f"❌ Comparison error: {e}")
    
    print(f"\n🌤️ Weather Features Test Complete!")
