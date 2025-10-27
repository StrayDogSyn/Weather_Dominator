"""
Pytest configuration and shared fixtures for Weather Dominator tests
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing path to test data directory"""
    data_dir = Path(__file__).parent / "test_data"
    data_dir.mkdir(exist_ok=True)
    yield data_dir
    # Cleanup after all tests
    if data_dir.exists():
        shutil.rmtree(data_dir)


@pytest.fixture
def temp_dir():
    """Fixture providing a temporary directory for each test"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_weather_data():
    """Fixture providing sample weather data"""
    return {
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
        "sunrise": "06:30",
        "sunset": "18:45",
        "timestamp": "2025-10-26 12:00:00",
        "units": "imperial",
    }


@pytest.fixture
def sample_character_data():
    """Fixture providing sample G.I. Joe character data"""
    return {
        "name": "Cobra Commander",
        "bio": "The ruthless leader of Cobra",
        "full_bio": "Cobra Commander is the supreme leader of the terrorist organization Cobra.",
        "image_url": "https://example.com/cobra_commander.jpg",
        "wiki_url": "https://gijoe.fandom.com/wiki/Cobra_Commander",
        "page_id": 12345,
        "is_cobra": True,
    }


@pytest.fixture
def mock_config():
    """Fixture providing mock configuration data"""
    return {
        "api_keys": {"openweather": "test_weather_key", "gijoe": "test_gijoe_key"},
        "preferences": {"theme": "cobra", "units": "imperial", "auto_save": True},
        "window": {"width": 1200, "height": 800},
    }


@pytest.fixture(autouse=True)
def reset_logging():
    """Fixture to reset logging configuration between tests"""
    import logging

    # Store original state
    original_handlers = logging.root.handlers[:]
    original_level = logging.root.level

    yield

    # Restore original state
    logging.root.handlers = original_handlers
    logging.root.level = original_level


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Fixture to set mock environment variables"""

    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, value)

    return _set_env


@pytest.fixture
def capture_logs():
    """Fixture to capture log output"""
    import io
    import logging

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    yield log_stream

    root_logger.removeHandler(handler)


# Pytest hooks for custom behavior
def pytest_configure(config):
    """Pytest configuration hook"""
    # Register custom markers
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add unit marker to all tests in test_*.py files
        if "test_" in item.nodeid:
            if "unit" not in [marker.name for marker in item.iter_markers()]:
                item.add_marker(pytest.mark.unit)


def pytest_report_header(config):
    """Add custom header to pytest report"""
    return [
        "Weather Dominator Test Suite",
        f"Python: {sys.version}",
        f"Platform: {sys.platform}",
    ]


# Skip tests that require external resources
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--run-api",
        action="store_true",
        default=False,
        help="Run tests that make actual API calls",
    )
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="Run slow tests"
    )


def pytest_runtest_setup(item):
    """Setup hook for each test"""
    # Skip API tests unless --run-api flag is provided
    if "api" in [marker.name for marker in item.iter_markers()]:
        if not item.config.getoption("--run-api"):
            pytest.skip("need --run-api option to run")

    # Skip slow tests unless --run-slow flag is provided
    if "slow" in [marker.name for marker in item.iter_markers()]:
        if not item.config.getoption("--run-slow"):
            pytest.skip("need --run-slow option to run")
