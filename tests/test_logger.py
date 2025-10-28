"""
Tests for src.logger module
"""
import logging
import os

import pytest

from src.logger import get_logger, log_function_call, setup_logging


class TestGetLogger:
    """Test get_logger function"""
    
    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a Logger instance"""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_with_name(self):
        """Test that logger has correct name"""
        logger = get_logger("test_module")
        assert "test_module" in logger.name
    
    def test_get_logger_multiple_calls(self):
        """Test that multiple calls work correctly"""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        assert isinstance(logger1, logging.Logger)
        assert isinstance(logger2, logging.Logger)


class TestSetupLogging:
    """Test setup_logging function"""
    
    def test_setup_logging_exists(self):
        """Test that setup_logging function exists"""
        assert callable(setup_logging)
    
    def test_setup_logging_runs(self):
        """Test that setup_logging runs without error"""
        try:
            setup_logging()
            assert True
        except Exception as e:
            pytest.fail(f"setup_logging raised {e}")


class TestLogFunctionCall:
    """Test log_function_call decorator"""
    
    def test_decorator_exists(self):
        """Test that log_function_call decorator exists"""
        assert callable(log_function_call)
    
    def test_decorator_on_function(self):
        """Test decorator on a simple function"""
        @log_function_call
        def test_function(x, y):
            return x + y
        
        result = test_function(2, 3)
        assert result == 5
    
    def test_decorator_preserves_return_value(self):
        """Test that decorator returns function result"""
        @log_function_call
        def compute(a, b):
            return a * b
        
        result = compute(4, 5)
        assert result == 20


class TestLoggerBasicOperations:
    """Test basic logger operations"""
    
    def test_logger_info(self):
        """Test logger info method"""
        logger = get_logger("test_info")
        try:
            logger.info("Test message")
            assert True
        except Exception as e:
            pytest.fail(f"Logger.info raised {e}")
    
    def test_logger_warning(self):
        """Test logger warning method"""
        logger = get_logger("test_warning")
        try:
            logger.warning("Test warning")
            assert True
        except Exception as e:
            pytest.fail(f"Logger.warning raised {e}")
    
    def test_logger_error(self):
        """Test logger error method"""
        logger = get_logger("test_error")
        try:
            logger.error("Test error")
            assert True
        except Exception as e:
            pytest.fail(f"Logger.error raised {e}")
    
    def test_logger_debug(self):
        """Test logger debug method"""
        logger = get_logger("test_debug")
        try:
            logger.debug("Test debug")
            assert True
        except Exception as e:
            pytest.fail(f"Logger.debug raised {e}")
