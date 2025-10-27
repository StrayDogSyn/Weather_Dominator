"""
db/sqlite_store.py - SQLite database management
Create a database schema for weather logs, user searches, and ML predictions.
Write functions to insert, update, retrieve, and clear records.
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import os

from src.logger import get_logger
from src.exceptions import DatabaseError
from src.constants import DEFAULT_DB_PATH

# Initialize logger for this module
logger = get_logger(__name__)

class WeatherDatabase:
    """SQLite database for storing weather data, searches, and predictions"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database connection
        
        Args:
            db_path: Path to the SQLite database file. If None, uses default from constants
            
        Raises:
            DatabaseError: If database initialization fails
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        logger.info(f"Initializing WeatherDatabase at: {self.db_path}")
        self.init_database()
    
    def init_database(self):
        """
        Initialize database tables if they don't exist
        
        Raises:
            DatabaseError: If table creation fails
        """
        logger.debug("Initializing database tables")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Weather logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS weather_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        country TEXT,
                        temperature REAL,
                        feels_like REAL,
                        humidity INTEGER,
                        pressure REAL,
                        description TEXT,
                        wind_speed REAL,
                        wind_direction REAL,
                        visibility REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        units TEXT DEFAULT 'imperial',
                        raw_data TEXT  -- JSON string of full API response
                    )
                """)
                
                # User searches table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_searches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        search_type TEXT NOT NULL,  -- 'weather' or 'character'
                        search_query TEXT NOT NULL,
                        results_found INTEGER DEFAULT 0,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT,
                        session_id TEXT
                    )
                """)
                
                # ML predictions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ml_predictions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        prediction_type TEXT NOT NULL,  -- 'temperature', 'humidity', 'severe_weather'
                        predicted_value REAL,
                        confidence_score REAL,
                        model_version TEXT,
                        features_used TEXT,  -- JSON string of features
                        actual_value REAL,  -- Filled in later for model evaluation
                        prediction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        target_date DATETIME  -- Date the prediction is for
                    )
                """)
                
                # Character lookups table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS character_lookups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        character_name TEXT NOT NULL,
                        found_name TEXT,
                        bio TEXT,
                        is_cobra BOOLEAN DEFAULT 0,
                        wiki_url TEXT,
                        image_url TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        cached_data TEXT  -- JSON string of full character data
                    )
                """)
                
                # System logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS system_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        log_level TEXT NOT NULL,  -- 'INFO', 'WARNING', 'ERROR'
                        module TEXT,
                        message TEXT NOT NULL,
                        error_details TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_logs(city)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_weather_timestamp ON weather_logs(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_searches_type ON user_searches(search_type)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_city ON ml_predictions(city)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_character_name ON character_lookups(character_name)")
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise DatabaseError(f"Failed to initialize database: {str(e)}")
    
    def log_weather_data(self, weather_data: Dict[str, Any]) -> Optional[int]:
        """
        Log weather data to the database
        
        Args:
            weather_data: Weather data dictionary from API
            
        Returns:
            Row ID of inserted record or None if error
            
        Raises:
            DatabaseError: If insert operation fails
        """
        if "error" in weather_data:
            logger.warning("Cannot log weather data: error in data")
            return None
        
        logger.debug(f"Logging weather data for city: {weather_data.get('city')}")
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO weather_logs (
                        city, country, temperature, feels_like, humidity, 
                        pressure, description, wind_speed, wind_direction, 
                        visibility, units, raw_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    weather_data.get("city"),
                    weather_data.get("country"),
                    weather_data.get("temp"),
                    weather_data.get("feels_like"),
                    weather_data.get("humidity"),
                    weather_data.get("pressure"),
                    weather_data.get("description"),
                    weather_data.get("wind_speed"),
                    weather_data.get("wind_direction"),
                    weather_data.get("visibility"),
                    weather_data.get("units", "imperial"),
                    json.dumps(weather_data)
                ))
                
                conn.commit()
                row_id = cursor.lastrowid
                logger.info(f"Weather data logged successfully, ID: {row_id}")
                return row_id
                
        except sqlite3.Error as e:
            logger.error(f"Database error logging weather data: {e}")
            raise DatabaseError(f"Failed to log weather data: {str(e)}")
    
    def log_user_search(self, search_type: str, search_query: str, results_found: int = 0, 
                       ip_address: Optional[str] = None, session_id: Optional[str] = None) -> Optional[int]:
        """
        Log user search activity
        
        Args:
            search_type: Type of search ('weather' or 'character')
            search_query: What the user searched for
            results_found: Number of results returned
            ip_address: User's IP address (optional)
            session_id: Session identifier (optional)
            
        Returns:
            Row ID of inserted record or None if error
            
        Raises:
            DatabaseError: If insert operation fails
        """
        logger.debug(f"Logging user search: type={search_type}, query={search_query}")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO user_searches (
                        search_type, search_query, results_found, ip_address, session_id
                    ) VALUES (?, ?, ?, ?, ?)
                """, (search_type, search_query, results_found, ip_address, session_id))
                
                conn.commit()
                row_id = cursor.lastrowid
                logger.info(f"User search logged successfully, ID: {row_id}")
                return row_id
                
        except sqlite3.Error as e:
            logger.error(f"Database error logging user search: {e}")
            raise DatabaseError(f"Failed to log user search: {str(e)}")
    
    def log_ml_prediction(self, city: str, prediction_type: str, predicted_value: float,
                         confidence_score: float, model_version: str, features_used: Dict[str, Any],
                         target_date: Optional[datetime] = None) -> Optional[int]:
        """
        Log ML prediction to database
        
        Args:
            city: City the prediction is for
            prediction_type: Type of prediction
            predicted_value: The predicted value
            confidence_score: Model confidence (0.0 to 1.0)
            model_version: Version of the model used
            features_used: Dictionary of features used for prediction
            target_date: Date the prediction is for (default: now)
            
        Returns:
            Row ID of inserted record or None if error
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                target_date = target_date or datetime.now()
                
                cursor.execute("""
                    INSERT INTO ml_predictions (
                        city, prediction_type, predicted_value, confidence_score,
                        model_version, features_used, target_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    city, prediction_type, predicted_value, confidence_score,
                    model_version, json.dumps(features_used), target_date
                ))
                
                return cursor.lastrowid
                
        except sqlite3.Error as e:
            self.log_system_error("log_ml_prediction", str(e))
            return None
    
    def log_character_lookup(self, character_name: str, character_data: Dict[str, Any]) -> Optional[int]:
        """
        Log character lookup to database
        
        Args:
            character_name: Original search term
            character_data: Character data from API
            
        Returns:
            Row ID of inserted record or None if error
        """
        if "error" in character_data:
            return None
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO character_lookups (
                        character_name, found_name, bio, is_cobra, 
                        wiki_url, image_url, cached_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    character_name,
                    character_data.get("name"),
                    character_data.get("bio"),
                    character_data.get("is_cobra", False),
                    character_data.get("wiki_url"),
                    character_data.get("image_url"),
                    json.dumps(character_data)
                ))
                
                return cursor.lastrowid
                
        except sqlite3.Error as e:
            self.log_system_error("log_character_lookup", str(e))
            return None
    
    def log_system_error(self, module: str, error_message: str, log_level: str = "ERROR"):
        """
        Log system errors and messages
        
        Args:
            module: Module or function where error occurred
            error_message: Error message
            log_level: Severity level
        """
        logger.debug(f"Logging system error from {module}: {error_message}")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO system_logs (log_level, module, message)
                    VALUES (?, ?, ?)
                """, (log_level, module, error_message))
                
                conn.commit()
                
        except sqlite3.Error as e:
            # Can't log database errors to database, log to application logger instead
            logger.error(f"Database logging error in {module}: {error_message}, DB Error: {e}")
    
    def get_weather_history(self, city: Optional[str] = None, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get weather history for a city or all cities
        
        Args:
            city: City name (None for all cities)
            days: Number of days to look back
            
        Returns:
            List of weather records
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if city:
                    cursor.execute("""
                        SELECT * FROM weather_logs 
                        WHERE city = ? AND timestamp >= datetime('now', '-{} days')
                        ORDER BY timestamp DESC
                    """.format(days), (city,))
                else:
                    cursor.execute("""
                        SELECT * FROM weather_logs 
                        WHERE timestamp >= datetime('now', '-{} days')
                        ORDER BY timestamp DESC
                    """.format(days))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            self.log_system_error("get_weather_history", str(e))
            return []
    
    def get_search_stats(self, search_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get search statistics
        
        Args:
            search_type: Type of search to filter by (None for all)
            
        Returns:
            Dictionary with search statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total searches
                if search_type:
                    cursor.execute("SELECT COUNT(*) FROM user_searches WHERE search_type = ?", (search_type,))
                else:
                    cursor.execute("SELECT COUNT(*) FROM user_searches")
                total_searches = cursor.fetchone()[0]
                
                # Most popular searches
                if search_type:
                    cursor.execute("""
                        SELECT search_query, COUNT(*) as count 
                        FROM user_searches 
                        WHERE search_type = ?
                        GROUP BY search_query 
                        ORDER BY count DESC 
                        LIMIT 10
                    """, (search_type,))
                else:
                    cursor.execute("""
                        SELECT search_query, COUNT(*) as count 
                        FROM user_searches 
                        GROUP BY search_query 
                        ORDER BY count DESC 
                        LIMIT 10
                    """)
                popular_searches = cursor.fetchall()
                
                return {
                    "total_searches": total_searches,
                    "popular_searches": popular_searches,
                    "search_type": search_type or "all"
                }
                
        except sqlite3.Error as e:
            self.log_system_error("get_search_stats", str(e))
            return {"total_searches": 0, "popular_searches": [], "search_type": search_type or "all"}
    
    def clear_old_data(self, days: int = 30):
        """
        Clear data older than specified days
        
        Args:
            days: Number of days to keep (delete older)
            
        Raises:
            DatabaseError: If cleanup operation fails
        """
        logger.info(f"Clearing data older than {days} days")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clear old weather logs
                cursor.execute("""
                    DELETE FROM weather_logs 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(days))
                weather_deleted = cursor.rowcount
                
                # Clear old search logs
                cursor.execute("""
                    DELETE FROM user_searches 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(days))
                searches_deleted = cursor.rowcount
                
                # Clear old character lookups
                cursor.execute("""
                    DELETE FROM character_lookups 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(days))
                characters_deleted = cursor.rowcount
                
                # Clear old system logs
                cursor.execute("""
                    DELETE FROM system_logs 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(days))
                logs_deleted = cursor.rowcount
                
                conn.commit()
                
                logger.info(f"Cleaned up old data:")
                logger.info(f"  Weather logs: {weather_deleted} deleted")
                logger.info(f"  Search logs: {searches_deleted} deleted")
                logger.info(f"  Character lookups: {characters_deleted} deleted")
                logger.info(f"  System logs: {logs_deleted} deleted")
                
        except sqlite3.Error as e:
            logger.error(f"Database error during cleanup: {e}")
            raise DatabaseError(f"Failed to clear old data: {str(e)}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get overall database statistics
        
        Returns:
            Dictionary with database statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Count records in each table
                tables = ["weather_logs", "user_searches", "ml_predictions", 
                         "character_lookups", "system_logs"]
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    stats[f"{table}_count"] = cursor.fetchone()[0]
                
                # Database file size
                if os.path.exists(self.db_path):
                    stats["db_size_mb"] = round(os.path.getsize(self.db_path) / 1024 / 1024, 2)
                else:
                    stats["db_size_mb"] = 0
                
                return stats
                
        except sqlite3.Error as e:
            self.log_system_error("get_database_stats", str(e))
            return {}

# Convenience functions
def get_db_instance(db_path: str = "weather_dominator.db") -> WeatherDatabase:
    """Get a database instance"""
    return WeatherDatabase(db_path)

def log_weather(weather_data: Dict[str, Any], db_path: str = "weather_dominator.db") -> Optional[int]:
    """Convenience function to log weather data"""
    db = WeatherDatabase(db_path)
    return db.log_weather_data(weather_data)

def log_search(search_type: str, query: str, results: int = 0, db_path: str = "weather_dominator.db") -> Optional[int]:
    """Convenience function to log user search"""
    db = WeatherDatabase(db_path)
    return db.log_user_search(search_type, query, results)

# Example usage and testing
if __name__ == "__main__":
    # Test the database
    logger.info("Testing Weather Dominator Database")
    
    db = WeatherDatabase("test_weather.db")
    
    # Test weather logging
    sample_weather = {
        "city": "New York",
        "country": "US",
        "temp": 72,
        "feels_like": 75,
        "humidity": 65,
        "pressure": 1013.25,
        "description": "Clear Sky",
        "wind_speed": 5.5,
        "wind_direction": 180,
        "visibility": 10.0,
        "units": "imperial"
    }
    
    try:
        weather_id = db.log_weather_data(sample_weather)
        logger.info(f"Weather logged with ID: {weather_id}")
    except DatabaseError as e:
        logger.error(f"Error logging weather: {e}")
    
    # Test search logging
    try:
        search_id = db.log_user_search("weather", "New York", 1)
        logger.info(f"Search logged with ID: {search_id}")
    except DatabaseError as e:
        logger.error(f"Error logging search: {e}")
    
    # Test character logging
    sample_character = {
        "name": "Cobra Commander",
        "bio": "Leader of Cobra",
        "is_cobra": True,
        "wiki_url": "https://gijoe.fandom.com/wiki/Cobra_Commander"
    }
    
    try:
        char_id = db.log_character_lookup("Cobra Commander", sample_character)
        logger.info(f"Character logged with ID: {char_id}")
    except DatabaseError as e:
        logger.error(f"Error logging character: {e}")
    
    # Get statistics
    stats = db.get_database_stats()
    logger.info(f"Database stats: {stats}")
    
    logger.info("Database test completed!")
