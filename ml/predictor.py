"""
ml/predictor.py - Machine learning module for weather predictions
Use scikit-learn to create a regression model predicting temperature trends or severe weather likelihood.
Include functions for training, saving/loading model, and generating predictions.
"""

try:
    import numpy as np
    NUMPY_AVAILABLE = True
    ndarray = np.ndarray
except ImportError:
    print("⚠️ numpy not available. Using basic math functions instead.")
    NUMPY_AVAILABLE = False
    # Create a simple numpy-like interface for basic operations
    class SimpleNumpy:
        @staticmethod
        def sqrt(x):
            return x ** 0.5
        @staticmethod
        def array(x):
            return list(x) if isinstance(x, (list, tuple)) else [x]
        @staticmethod
        def unique(x):
            return list(set(x))
        @staticmethod
        def mean(x):
            return sum(x) / len(x) if len(x) > 0 else 0
    np = SimpleNumpy()
    ndarray = list  # Use list as ndarray fallback for type annotations
import pickle
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import os

# Try to import sklearn, but provide fallbacks if not available
try:
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    print("⚠️ scikit-learn not available. ML features will use simple fallback methods.")
    SKLEARN_AVAILABLE = False
    # Set classes to None when imports fail
    RandomForestRegressor = None
    RandomForestClassifier = None
    train_test_split = None
    mean_squared_error = None
    accuracy_score = None
    classification_report = None
    StandardScaler = None

class WeatherPredictor:
    """Machine learning predictor for weather forecasting and severe weather detection"""
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize the weather predictor
        
        Args:
            model_dir: Directory to store trained models
        """
        self.model_dir = model_dir
        self.temperature_model = None
        self.severe_weather_model = None
        self.scaler = None
        
        # Create models directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        
        # Model file paths
        self.temp_model_path = os.path.join(model_dir, "temperature_model.pkl")
        self.severe_model_path = os.path.join(model_dir, "severe_weather_model.pkl")
        self.scaler_path = os.path.join(model_dir, "scaler.pkl")
        
        # Feature names for consistency
        self.feature_names = [
            "humidity", "pressure", "wind_speed", "visibility",
            "hour", "month", "season", "temp_lag1", "temp_lag2"
        ]
        
        # Load existing models if available
        self.load_models()
    
    def prepare_features(self, weather_data_list: List[Dict[str, Any]]) -> Tuple[Any, Any]:
        """
        Prepare features from weather data for training
        
        Args:
            weather_data_list: List of weather data dictionaries
            
        Returns:
            Tuple of (features, targets) arrays
        """
        features = []
        targets = []
        
        # Sort by timestamp to ensure proper lag features
        sorted_data = sorted(weather_data_list, key=lambda x: x.get("timestamp", ""))
        
        for i, data in enumerate(sorted_data):
            if "error" in data or not data.get("temp"):
                continue
            
            # Extract features
            feature_row = [
                data.get("humidity", 50),
                data.get("pressure", 1013.25),
                data.get("wind_speed", 0),
                data.get("visibility", 10),
                self._extract_hour(data.get("timestamp")),
                self._extract_month(data.get("timestamp")),
                self._extract_season(data.get("timestamp")),
                # Lag features (previous temperatures)
                sorted_data[i-1].get("temp", data.get("temp")) if i > 0 else data.get("temp"),
                sorted_data[i-2].get("temp", data.get("temp")) if i > 1 else data.get("temp")
            ]
            
            features.append(feature_row)
            targets.append(data.get("temp"))
        
        return np.array(features), np.array(targets)
    
    def prepare_severe_weather_features(self, weather_data_list: List[Dict[str, Any]]) -> Tuple[Any, Any]:
        """
        Prepare features for severe weather classification
        
        Args:
            weather_data_list: List of weather data dictionaries
            
        Returns:
            Tuple of (features, severe_weather_labels) arrays
        """
        features = []
        labels = []
        
        for data in weather_data_list:
            if "error" in data:
                continue
            
            # Extract features (same as temperature prediction)
            feature_row = [
                data.get("humidity", 50),
                data.get("pressure", 1013.25),
                data.get("wind_speed", 0),
                data.get("visibility", 10),
                self._extract_hour(data.get("timestamp")),
                self._extract_month(data.get("timestamp")),
                self._extract_season(data.get("timestamp")),
                data.get("temp", 70),
                data.get("feels_like", 70)
            ]
            
            # Determine if severe weather (simplified criteria)
            is_severe = self._is_severe_weather(data)
            
            features.append(feature_row)
            labels.append(1 if is_severe else 0)
        
        return np.array(features), np.array(labels)
    
    def train_temperature_model(self, weather_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train temperature prediction model
        
        Args:
            weather_data_list: List of historical weather data
              Returns:
            Training results and metrics
        """
        if not SKLEARN_AVAILABLE or train_test_split is None or StandardScaler is None or RandomForestRegressor is None or mean_squared_error is None:
            return self._train_simple_temperature_model(weather_data_list)
        
        try:
            # Prepare data
            X, y = self.prepare_features(weather_data_list)
            
            if len(X) < 10:
                return {"error": "Not enough data for training (minimum 10 records required)"}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.temperature_model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.temperature_model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_pred = self.temperature_model.predict(X_train_scaled)
            test_pred = self.temperature_model.predict(X_test_scaled)
            
            train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
            
            # Feature importance
            feature_importance = dict(zip(self.feature_names, self.temperature_model.feature_importances_))
            
            # Save model
            self.save_models()
            
            return {
                "model_type": "RandomForestRegressor",
                "train_rmse": train_rmse,
                "test_rmse": test_rmse,
                "train_samples": len(X_train),
                "test_samples": len(X_test),
                "feature_importance": feature_importance,
                "model_saved": True
            }
            
        except Exception as e:
            return {"error": f"Training error: {str(e)}"}
    
    def train_severe_weather_model(self, weather_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train severe weather classification model
        
        Args:
            weather_data_list: List of historical weather data
              Returns:
            Training results and metrics
        """
        if not SKLEARN_AVAILABLE or train_test_split is None or StandardScaler is None or RandomForestClassifier is None or accuracy_score is None:
            return self._train_simple_severe_model(weather_data_list)
        
        try:
            # Prepare data
            X, y = self.prepare_severe_weather_features(weather_data_list)
            
            if len(X) < 10:
                return {"error": "Not enough data for training (minimum 10 records required)"}
            
            # Check if we have both classes
            if len(np.unique(y)) < 2:
                return {"error": "Need both severe and non-severe weather examples for training"}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            
            # Scale features (use existing scaler or create new one)
            if self.scaler is None:
                self.scaler = StandardScaler()
                X_train_scaled = self.scaler.fit_transform(X_train)
            else:
                X_train_scaled = self.scaler.transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.severe_weather_model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.severe_weather_model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_pred = self.severe_weather_model.predict(X_train_scaled)
            test_pred = self.severe_weather_model.predict(X_test_scaled)
            
            train_accuracy = accuracy_score(y_train, train_pred)
            test_accuracy = accuracy_score(y_test, test_pred)
            
            # Save model
            self.save_models()
            
            return {
                "model_type": "RandomForestClassifier",
                "train_accuracy": train_accuracy,
                "test_accuracy": test_accuracy,
                "train_samples": len(X_train),
                "test_samples": len(X_test),
                "model_saved": True
            }
            
        except Exception as e:
            return {"error": f"Training error: {str(e)}"}
    
    def predict_temperature(self, weather_data: Dict[str, Any], hours_ahead: int = 24) -> Dict[str, Any]:
        """
        Predict future temperature
        
        Args:
            weather_data: Current weather data
            hours_ahead: Hours into the future to predict
              Returns:
            Prediction results
        """
        if not SKLEARN_AVAILABLE or self.temperature_model is None or self.scaler is None:
            return self._predict_simple_temperature(weather_data, hours_ahead)
        
        try:
            # Prepare features
            features = [
                weather_data.get("humidity", 50),
                weather_data.get("pressure", 1013.25),
                weather_data.get("wind_speed", 0),
                weather_data.get("visibility", 10),
                (datetime.now() + timedelta(hours=hours_ahead)).hour,
                (datetime.now() + timedelta(hours=hours_ahead)).month,
                self._extract_season(datetime.now().strftime("%Y-%m-%d")),
                weather_data.get("temp", 70),
                weather_data.get("temp", 70)  # Use current temp as lag
            ]
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Predict
            prediction = self.temperature_model.predict(features_scaled)[0]
            
            # Calculate confidence (simplified - based on model variance)
            confidence = min(0.95, max(0.5, 1.0 - abs(prediction - weather_data.get("temp", 70)) / 50))
            
            return {
                "predicted_temperature": round(prediction, 1),
                "current_temperature": weather_data.get("temp"),
                "hours_ahead": hours_ahead,
                "confidence": round(confidence, 2),
                "prediction_time": (datetime.now() + timedelta(hours=hours_ahead)).strftime("%Y-%m-%d %H:%M"),
                "model_version": "RandomForest_v1.0"
            }
            
        except Exception as e:
            return {"error": f"Prediction error: {str(e)}"}
    
    def predict_severe_weather(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict severe weather probability
        
        Args:
            weather_data: Current weather data
              Returns:
            Severe weather prediction results
        """
        if not SKLEARN_AVAILABLE or self.severe_weather_model is None or self.scaler is None:
            return self._predict_simple_severe(weather_data)
        
        try:
            # Prepare features
            features = [
                weather_data.get("humidity", 50),
                weather_data.get("pressure", 1013.25),
                weather_data.get("wind_speed", 0),
                weather_data.get("visibility", 10),
                datetime.now().hour,
                datetime.now().month,
                self._extract_season(datetime.now().strftime("%Y-%m-%d")),
                weather_data.get("temp", 70),
                weather_data.get("feels_like", 70)
            ]
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Predict probability
            probabilities = self.severe_weather_model.predict_proba(features_scaled)[0]
            severe_probability = probabilities[1] if len(probabilities) > 1 else 0.0
            
            # Predict class
            prediction = self.severe_weather_model.predict(features_scaled)[0]
            
            return {
                "severe_weather_probability": round(severe_probability, 2),
                "is_severe_predicted": bool(prediction),
                "confidence": round(max(probabilities), 2),
                "risk_level": self._get_risk_level(severe_probability),
                "model_version": "RandomForest_v1.0"
            }
            
        except Exception as e:
            return {"error": f"Prediction error: {str(e)}"}
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            if self.temperature_model is not None:
                with open(self.temp_model_path, 'wb') as f:
                    pickle.dump(self.temperature_model, f)
            
            if self.severe_weather_model is not None:
                with open(self.severe_model_path, 'wb') as f:
                    pickle.dump(self.severe_weather_model, f)
            
            if self.scaler is not None:
                with open(self.scaler_path, 'wb') as f:
                    pickle.dump(self.scaler, f)
            
            print("✅ Models saved successfully")
            
        except Exception as e:
            print(f"❌ Error saving models: {e}")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            if os.path.exists(self.temp_model_path):
                with open(self.temp_model_path, 'rb') as f:
                    self.temperature_model = pickle.load(f)
                print("✅ Temperature model loaded")
            
            if os.path.exists(self.severe_model_path):
                with open(self.severe_model_path, 'rb') as f:
                    self.severe_weather_model = pickle.load(f)
                print("✅ Severe weather model loaded")
            
            if os.path.exists(self.scaler_path):
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("✅ Scaler loaded")
            
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")
    
    # Simple fallback methods when sklearn is not available
    def _train_simple_temperature_model(self, weather_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simple temperature prediction using moving averages"""
        temps = [data.get("temp") for data in weather_data_list if "error" not in data and data.get("temp")]
        
        if len(temps) < 3:
            return {"error": "Not enough temperature data"}
        
        # Simple model: store recent average and trend
        self.simple_temp_model = {
            "recent_avg": np.mean(temps[-10:]),  # Last 10 readings
            "overall_avg": np.mean(temps),
            "trend": np.mean(temps[-5:]) - np.mean(temps[-10:-5]) if len(temps) >= 10 else 0
        }
        
        return {
            "model_type": "SimpleMovingAverage",
            "samples_used": len(temps),
            "recent_avg": self.simple_temp_model["recent_avg"],
            "trend": self.simple_temp_model["trend"]
        }
    
    def _train_simple_severe_model(self, weather_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simple severe weather detection using thresholds"""
        severe_count = sum(1 for data in weather_data_list if self._is_severe_weather(data))
        total_count = len(weather_data_list)
        
        self.simple_severe_model = {
            "severe_rate": severe_count / total_count if total_count > 0 else 0,
            "wind_threshold": 25,  # mph
            "pressure_threshold": 1000  # hPa
        }
        
        return {
            "model_type": "SimpleThreshold",
            "samples_used": total_count,
            "severe_rate": self.simple_severe_model["severe_rate"]
        }
    
    def _predict_simple_temperature(self, weather_data: Dict[str, Any], hours_ahead: int) -> Dict[str, Any]:
        """Simple temperature prediction"""
        if not hasattr(self, 'simple_temp_model'):
            current_temp = weather_data.get("temp", 70)
            return {
                "predicted_temperature": current_temp,
                "current_temperature": current_temp,
                "hours_ahead": hours_ahead,
                "confidence": 0.5,
                "model_version": "Simple_v1.0",
                "note": "No trained model available, using current temperature"
            }
        
        # Simple prediction: current trend + seasonal adjustment
        base_temp = self.simple_temp_model["recent_avg"]
        trend_adjustment = self.simple_temp_model["trend"] * (hours_ahead / 24)
        
        # Simple seasonal adjustment
        hour = (datetime.now() + timedelta(hours=hours_ahead)).hour
        seasonal_adj = -5 if 0 <= hour <= 6 else (5 if 12 <= hour <= 16 else 0)
        
        predicted = base_temp + trend_adjustment + seasonal_adj
        
        return {
            "predicted_temperature": round(predicted, 1),
            "current_temperature": weather_data.get("temp"),
            "hours_ahead": hours_ahead,
            "confidence": 0.7,
            "model_version": "Simple_v1.0"
        }
    
    def _predict_simple_severe(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simple severe weather prediction"""
        if not hasattr(self, 'simple_severe_model'):
            return {
                "severe_weather_probability": 0.1,
                "is_severe_predicted": False,
                "confidence": 0.5,
                "risk_level": "Low",
                "model_version": "Simple_v1.0"
            }
        
        # Check simple thresholds
        is_severe = False
        probability = self.simple_severe_model["severe_rate"]
        
        wind_speed = weather_data.get("wind_speed", 0)
        pressure = weather_data.get("pressure", 1013)
        
        if wind_speed > self.simple_severe_model["wind_threshold"]:
            is_severe = True
            probability = min(0.9, probability + 0.3)
        
        if pressure < self.simple_severe_model["pressure_threshold"]:
            is_severe = True
            probability = min(0.9, probability + 0.2)
        
        return {
            "severe_weather_probability": round(probability, 2),
            "is_severe_predicted": is_severe,
            "confidence": 0.7,
            "risk_level": self._get_risk_level(probability),
            "model_version": "Simple_v1.0"
        }
    
    # Helper methods
    def _extract_hour(self, timestamp_str: Optional[str]) -> int:
        """Extract hour from timestamp string"""
        if not timestamp_str:
            return datetime.now().hour
        try:
            return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").hour
        except:
            return datetime.now().hour
    
    def _extract_month(self, timestamp_str: Optional[str]) -> int:
        """Extract month from timestamp string"""
        if not timestamp_str:
            return datetime.now().month
        try:
            return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").month
        except:
            return datetime.now().month
    
    def _extract_season(self, timestamp_str: Optional[str]) -> int:
        """Extract season from timestamp string (0=winter, 1=spring, 2=summer, 3=fall)"""
        month = self._extract_month(timestamp_str)
        if month in [12, 1, 2]:
            return 0  # Winter
        elif month in [3, 4, 5]:
            return 1  # Spring
        elif month in [6, 7, 8]:
            return 2  # Summer
        else:
            return 3  # Fall
    
    def _is_severe_weather(self, weather_data: Dict[str, Any]) -> bool:
        """Determine if weather conditions are severe"""
        if "error" in weather_data:
            return False
        
        description = weather_data.get("description", "").lower()
        wind_speed = weather_data.get("wind_speed", 0)
        
        severe_keywords = ["storm", "severe", "tornado", "hurricane", "hail"]
        has_severe_keyword = any(keyword in description for keyword in severe_keywords)
        has_high_wind = wind_speed > 25  # mph
        
        return has_severe_keyword or has_high_wind
    
    def _get_risk_level(self, probability: float) -> str:
        """Convert probability to risk level"""
        if probability >= 0.7:
            return "High"
        elif probability >= 0.4:
            return "Medium"
        elif probability >= 0.2:
            return "Low"
        else:
            return "Minimal"

# Convenience functions
def create_predictor(model_dir: str = "models") -> WeatherPredictor:
    """Create a weather predictor instance"""
    return WeatherPredictor(model_dir)

def train_models(weather_data_list: List[Dict[str, Any]], model_dir: str = "models") -> Dict[str, Any]:
    """Train both temperature and severe weather models"""
    predictor = WeatherPredictor(model_dir)
    
    temp_results = predictor.train_temperature_model(weather_data_list)
    severe_results = predictor.train_severe_weather_model(weather_data_list)
    
    return {
        "temperature_model": temp_results,
        "severe_weather_model": severe_results
    }

# Example usage and testing
if __name__ == "__main__":
    print("🤖 Testing Weather Predictor...")
    
    # Create sample weather data for testing
    sample_data = [
        {"temp": 72, "humidity": 65, "pressure": 1013, "wind_speed": 5, "description": "Clear", "timestamp": "2024-01-01 12:00:00"},
        {"temp": 75, "humidity": 70, "pressure": 1010, "wind_speed": 8, "description": "Cloudy", "timestamp": "2024-01-01 13:00:00"},
        {"temp": 68, "humidity": 80, "pressure": 1005, "wind_speed": 15, "description": "Rain", "timestamp": "2024-01-01 14:00:00"},
        {"temp": 60, "humidity": 90, "pressure": 995, "wind_speed": 30, "description": "Thunderstorm", "timestamp": "2024-01-01 15:00:00"},
        {"temp": 65, "humidity": 75, "pressure": 1008, "wind_speed": 12, "description": "Partly Cloudy", "timestamp": "2024-01-01 16:00:00"},
    ]
    
    predictor = WeatherPredictor("test_models")
    
    # Test training
    print("\n📚 Training models...")
    temp_results = predictor.train_temperature_model(sample_data)
    print(f"Temperature model: {temp_results}")
    
    severe_results = predictor.train_severe_weather_model(sample_data)
    print(f"Severe weather model: {severe_results}")
    
    # Test predictions
    print("\n🔮 Testing predictions...")
    current_weather = {"temp": 70, "humidity": 60, "pressure": 1012, "wind_speed": 10}
    
    temp_pred = predictor.predict_temperature(current_weather, 24)
    print(f"Temperature prediction: {temp_pred}")
    
    severe_pred = predictor.predict_severe_weather(current_weather)
    print(f"Severe weather prediction: {severe_pred}")
    
    print("🤖 Weather predictor test completed!")
