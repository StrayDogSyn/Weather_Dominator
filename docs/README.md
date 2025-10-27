# 🌩️ COBRA Weather Dominator

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**A sophisticated Python application combining real-time weather intelligence, character database, and machine learning predictions in a sleek glassmorphic interface inspired by G.I. Joe's COBRA organization.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Architecture](#-architecture)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## ✨ Features

### 🌍 Weather Intelligence System
- **Real-time Weather Data**: Current conditions for any city worldwide via OpenWeatherMap API
- **Comprehensive Metrics**: Temperature, humidity, wind speed, pressure, visibility
- **Dynamic Weather Icons**: Visual condition indicators with icon support
- **Tactical Forecasting**: Sunrise/sunset times and operational status tracking
- **Severe Weather Alerts**: Automatic detection and notification of hazardous conditions
- **Demo Mode**: Full functionality without API keys using realistic sample data

### 🐍 COBRA Intelligence Database
- **Character Lookup**: Comprehensive G.I. Joe and COBRA operative profiles
- **Detailed Profiles**: Biography, affiliation, specialties, and operational data
- **Wiki Integration**: Direct links to Fandom wiki pages
- **Security Clearance Levels**: COBRA EYES ONLY, CLASSIFIED, RESTRICTED classifications
- **Relationship Mapping**: Character allies, vehicles, and base assignments
- **Image Gallery Support**: Multiple character images and profile photos

### 🎨 Modern Glassmorphic Interface
- **Sleek Design**: Professional glass-effect panels with transparency
- **Dual Themes**: Blue default theme and authentic COBRA red theme
- **Responsive Layout**: Optimized 1200x800 display with fluid scaling
- **Interactive Elements**: Smooth hover effects and dynamic updates
- **Professional Typography**: Carefully selected fonts and hierarchical sizing
- **Micro-interactions**: Polished button states and transition effects

### 🧠 Machine Learning & Analytics
- **Weather Predictions**: ML-powered forecasting based on historical data
- **Pattern Recognition**: Trend analysis for temperature and conditions
- **Confidence Scoring**: Prediction reliability metrics
- **Model Versioning**: Track and compare different model versions
- **Data Visualization**: Graphical representations of predictions

### 📊 Data Management
- **SQLite Database**: Efficient local data storage and caching
- **Search History**: Track user queries and popular searches
- **Data Export**: Export weather data and reports
- **Automatic Cleanup**: Configurable data retention policies
- **Backup System**: Automated backup of critical data files

---

## 📸 Screenshots

<div align="center">

### Main Interface
*Coming Soon - Modern glassmorphic weather and intelligence dashboard*

### Weather Intelligence Panel
*Coming Soon - Real-time weather data with tactical overlay*

### COBRA Intelligence Panel
*Coming Soon - Character database with security clearance levels*

</div>

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **tkinter** (usually included with Python)

### Method 1: Standard Installation

```bash
# Clone the repository
git clone https://github.com/StrayDogSyndicate/Weather_Dominator.git
cd Weather_Dominator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Method 2: Development Installation

```bash
# Clone the repository
git clone https://github.com/StrayDogSyndicate/Weather_Dominator.git
cd Weather_Dominator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run the application
python main.py
```

### Method 3: Quick Launch (Windows)

Simply double-click `start_weather_dominator.bat` for instant launch!

---

## ⚡ Quick Start

### Running Without Configuration

The application works perfectly out-of-the-box in **Demo Mode**:

```bash
python main.py
```

### Running with Live Weather Data

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Add your API key to `config/config.json`:

```json
{
  "api_keys": {
    "openweather": "your_api_key_here"
  }
}
```

3. Launch the application:

```bash
python main.py
```

---

## ⚙️ Configuration

### Configuration File Structure

Create or edit `config/config.json`:

```json
{
  "api_keys": {
    "openweather": "your_openweather_api_key",
    "fandom": "your_fandom_api_key"
  },
  "preferences": {
    "temperature_unit": "F",
    "wind_unit": "mph",
    "pressure_unit": "hPa",
    "theme": "default"
  },
  "cache": {
    "max_age_days": 7,
    "max_size_mb": 50
  },
  "database": {
    "path": "weather_dominator.db",
    "cleanup_days": 30
  }
}
```

### Environment Variables

Alternatively, set environment variables:

```bash
# Windows PowerShell
$env:OPENWEATHER_API_KEY="your_api_key_here"
$env:TEMP_UNIT="F"
$env:APP_THEME="cobra"

# Linux/macOS
export OPENWEATHER_API_KEY="your_api_key_here"
export TEMP_UNIT="F"
export APP_THEME="cobra"
```

### Theme Selection

Switch between themes in `main.py`:

```python
# Blue glassmorphic theme (default)
app = GlassmorphicWindow()

# COBRA red military theme
app = GlassmorphicWindow(CobraTheme())
```

---

## 📖 Usage Guide

### Weather Intelligence

1. **Enter Target Location**: Type any city name (e.g., "New York", "London", "Tokyo")
2. **Acquire Data**: Click "🌍 ACQUIRE WEATHER DATA" or press Enter
3. **View Results**: Real-time conditions, forecast, and tactical information

**Demo Cities to Try:**
- New York, London, Tokyo, Paris (realistic demo data)
- "COBRA Command" (special demo location)

### Character Intelligence

1. **Enter Target Subject**: Type a character name
2. **Interrogate Database**: Click "🔍 INTERROGATE DATABASE"
3. **Review Intel**: Character profile, affiliation, and security status

**Pre-loaded Characters:**
- **COBRA**: Cobra Commander, Destro, Baroness, Storm Shadow, Zartan
- **G.I. Joe**: Duke, Snake Eyes, Scarlett, Roadblock
- **Custom**: Any name generates an investigation profile

### Interactive Features

- **Favorites**: Save frequently checked cities
- **Alerts**: Set up weather condition notifications
- **Journal**: Keep notes on weather patterns
- **Export**: Save data in multiple formats

### Smart AI Features

- **Predictions**: ML-powered weather forecasts
- **Trends**: Historical pattern analysis
- **Activities**: Weather-appropriate suggestions
- **Confidence Metrics**: Prediction reliability scores

---

## 🏗️ Architecture

### Project Structure

```
Weather_Dominator/
├── src/                      # Source code package
│   ├── constants.py          # Application constants
│   ├── config_manager.py     # Configuration management
│   ├── exceptions.py         # Custom exceptions
│   └── logger.py             # Logging configuration
├── data/                     # Data modules
│   ├── weather_api.py        # OpenWeatherMap integration
│   ├── gijoe_api.py          # Character database API
│   ├── weather_features.py   # Weather feature processing
│   └── favorite_cities.json  # User favorites
├── ui/                       # User interface modules
│   ├── glass_ui.py           # Main UI panels
│   ├── interactive_features.py
│   └── visual_features.py
├── db/                       # Database layer
│   └── sqlite_store.py       # SQLite operations
├── ml/                       # Machine learning
│   ├── predictor.py          # Weather prediction models
│   └── smart_features.py     # AI features
├── utils/                    # Utility functions
│   └── helpers.py            # Helper functions
├── config/                   # Configuration files
│   └── config.json           # Application configuration
├── schemas/                  # Database schemas
│   ├── gijoe_database_schema.sql
│   └── gijoe_database_schema_mssql.sql
├── tests/                    # Test suite
├── docs/                     # Documentation
├── main.py                   # Application entry point
├── theme_config.py           # Theme definitions
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── README.md                 # This file
└── LICENSE                   # MIT License
```

### Design Patterns

- **Separation of Concerns**: Modular architecture with clear responsibilities
- **Dependency Injection**: Flexible component coupling
- **Factory Pattern**: Theme and configuration creation
- **Singleton Pattern**: Configuration and database managers
- **Observer Pattern**: Event handling for UI updates
- **Strategy Pattern**: Interchangeable API implementations

### Key Components

- **ConfigManager**: Centralized configuration with environment variable support
- **WeatherAPI**: OpenWeatherMap API wrapper with error handling
- **GIJoeAPI**: Fandom wiki integration for character data
- **WeatherDatabase**: SQLite data persistence layer
- **WeatherPredictor**: ML model for weather predictions
- **GlassmorphicWindow**: Main UI controller

---

## 📚 API Documentation

### Weather API

```python
from data.weather_api import WeatherAPI

# Initialize API
weather_api = WeatherAPI(api_key="your_key")

# Get current weather
weather = weather_api.get_current_weather("New York")

# Get forecast
forecast = weather_api.get_weather_forecast("London", days=5)

# Check for alerts
coords = weather_api.get_coordinates("Tokyo")
alerts = weather_api.get_weather_alerts(coords["lat"], coords["lon"])
```

### Character API

```python
from data.gijoe_api import GIJoeAPI

# Initialize API
gijoe_api = GIJoeAPI()

# Get character data
character = gijoe_api.get_character_data("Cobra Commander")

# Get full intelligence package
intel = gijoe_api.get_cobra_intel_package("Destro")

# Get vehicle information
vehicle = gijoe_api.get_cobra_vehicle_data("HISS Tank")
```

### Database API

```python
from db.sqlite_store import WeatherDatabase

# Initialize database
db = WeatherDatabase()

# Log weather data
db.log_weather_data(weather_dict)

# Get search statistics
stats = db.get_search_stats(search_type="weather")

# Clean up old data
db.clear_old_data(days=30)
```

---

## 💻 Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/StrayDogSyndicate/Weather_Dominator.git
cd Weather_Dominator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Code Style

This project follows:
- **PEP 8** style guide
- **Black** code formatter
- **isort** import sorting
- **flake8** linting
- **mypy** type checking

Format code:
```bash
black .
isort .
flake8 .
mypy .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_weather_api.py

# Run with verbose output
pytest -v
```

---

## 🧪 Testing

### Test Coverage

- Unit tests for all API modules
- Integration tests for database operations
- UI component tests
- Mock API responses for offline testing

### Test Structure

```
tests/
├── __init__.py
├── test_weather_api.py
├── test_gijoe_api.py
├── test_database.py
├── test_config.py
├── test_ml_predictor.py
└── fixtures/
    ├── sample_weather.json
    └── sample_character.json
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow the existing code style
- Write tests for new features
- Update documentation as needed
- Add entries to CHANGELOG.md
- Ensure all tests pass before submitting

### Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenWeatherMap** for weather data API
- **G.I. Joe Fandom Wiki** for character information
- **Python Community** for excellent libraries and tools
- **Tkinter** for cross-platform GUI framework
- **SQLite** for embedded database engine

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/StrayDogSyndicate/Weather_Dominator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/StrayDogSyndicate/Weather_Dominator/discussions)
- **Email**: support@straydogsyndicate.com

---

## 🗺️ Roadmap

### Version 2.1.0 (Planned)
- [ ] REST API endpoint for external integrations
- [ ] Docker container support
- [ ] Web-based interface option
- [ ] Mobile app companion

### Version 2.2.0 (Future)
- [ ] Multi-language support
- [ ] Advanced ML models with TensorFlow
- [ ] Real-time weather radar integration
- [ ] Social features and sharing

---

## 📊 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/StrayDogSyndicate/Weather_Dominator)
![GitHub last commit](https://img.shields.io/github/last-commit/StrayDogSyndicate/Weather_Dominator)
![GitHub issues](https://img.shields.io/github/issues/StrayDogSyndicate/Weather_Dominator)
![GitHub pull requests](https://img.shields.io/github/issues-pr/StrayDogSyndicate/Weather_Dominator)
![GitHub stars](https://img.shields.io/github/stars/StrayDogSyndicate/Weather_Dominator?style=social)

---

<div align="center">

**⚡ Built with Python • Powered by COBRA • Ready for Deployment ⚡**

*"Weather is the ultimate weapon - and COBRA controls the skies!"*

Made with ❤️ by [Stray Dog Syndicate](https://github.com/StrayDogSyndicate)

</div>
