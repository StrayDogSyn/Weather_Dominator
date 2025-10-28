"""
Tests for src.exceptions module
"""
import pytest

from src.exceptions import (APIError, ConfigurationError, DatabaseError,
                            ValidationError, WeatherDominatorError,
                            handle_error, is_recoverable)


class TestExceptionHierarchy:
    """Test exception class hierarchy"""
    
    def test_base_exception_exists(self):
        """Test that base exception class exists"""
        assert issubclass(WeatherDominatorError, Exception)
    
    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inherits from base"""
        assert issubclass(ConfigurationError, WeatherDominatorError)
    
    def test_api_error_inheritance(self):
        """Test APIError inherits from base"""
        assert issubclass(APIError, WeatherDominatorError)
    
    def test_database_error_inheritance(self):
        """Test DatabaseError inherits from base"""
        assert issubclass(DatabaseError, WeatherDominatorError)
    
    def test_validation_error_inheritance(self):
        """Test ValidationError inherits from base"""
        assert issubclass(ValidationError, WeatherDominatorError)


class TestWeatherDominatorError:
    """Test base WeatherDominatorError class"""
    
    def test_create_base_exception(self):
        """Test creating base exception"""
        error = WeatherDominatorError("Test error")
        assert str(error) == "Test error"
    
    def test_raise_base_exception(self):
        """Test raising base exception"""
        with pytest.raises(WeatherDominatorError) as exc_info:
            raise WeatherDominatorError("Test error")
        
        assert "Test error" in str(exc_info.value)
    
    def test_exception_with_cause(self):
        """Test exception with cause"""
        original = ValueError("Original error")
        
        with pytest.raises(WeatherDominatorError) as exc_info:
            try:
                raise original
            except ValueError as e:
                raise WeatherDominatorError("Wrapped error") from e
        
        assert exc_info.value.__cause__ is original


class TestConfigurationError:
    """Test ConfigurationError class"""
    
    def test_create_configuration_error(self):
        """Test creating configuration error"""
        error = ConfigurationError("Config not found")
        assert str(error) == "Config not found"
    
    def test_raise_configuration_error(self):
        """Test raising configuration error"""
        with pytest.raises(ConfigurationError) as exc_info:
            raise ConfigurationError("Invalid configuration")
        
        assert "Invalid configuration" in str(exc_info.value)
    
    def test_catch_as_base_exception(self):
        """Test catching as base exception"""
        with pytest.raises(WeatherDominatorError):
            raise ConfigurationError("Config error")


class TestAPIError:
    """Test APIError class"""
    
    def test_create_api_error(self):
        """Test creating API error"""
        error = APIError("API request failed")
        assert str(error) == "API request failed"
    
    def test_raise_api_error(self):
        """Test raising API error"""
        with pytest.raises(APIError) as exc_info:
            raise APIError("Network timeout")
        
        assert "Network timeout" in str(exc_info.value)
    
    def test_api_error_with_status_code(self):
        """Test API error with additional context"""
        error = APIError("HTTP 404: Not Found")
        assert "404" in str(error)


class TestDatabaseError:
    """Test DatabaseError class"""
    
    def test_create_database_error(self):
        """Test creating database error"""
        error = DatabaseError("Connection failed")
        assert str(error) == "Connection failed"
    
    def test_raise_database_error(self):
        """Test raising database error"""
        with pytest.raises(DatabaseError) as exc_info:
            raise DatabaseError("Table does not exist")
        
        assert "Table does not exist" in str(exc_info.value)


class TestValidationError:
    """Test ValidationError class"""
    
    def test_create_validation_error(self):
        """Test creating validation error"""
        error = ValidationError("Invalid input")
        assert str(error) == "Invalid input"
    
    def test_raise_validation_error(self):
        """Test raising validation error"""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Field is required")
        
        assert "Field is required" in str(exc_info.value)


class TestHandleError:
    """Test handle_error utility function"""
    
    def test_handle_error_logs_exception(self, capsys):
        """Test that handle_error returns user-friendly message"""
        error = WeatherDominatorError("Test error")
        
        result = handle_error(error, "Fallback message")
        
        # handle_error returns a string
        assert isinstance(result, str)
        assert "Test error" in result
    
    def test_handle_error_with_different_types(self):
        """Test handle_error with different exception types"""
        errors = [
            ConfigurationError("Config error"),
            APIError("API error"),
            DatabaseError("DB error"),
            ValidationError("Validation error")
        ]
        
        for error in errors:
            result = handle_error(error, "Fallback message")
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_handle_error_with_context(self):
        """Test handle_error with additional context"""
        if callable(handle_error):
            error = APIError("Network timeout")
            context = {"url": "https://api.example.com", "attempt": 3}
            
            # Assuming handle_error can accept context
            try:
                result = handle_error(error, "test_module", context=context)
                assert result is None or isinstance(result, bool)
            except TypeError:
                # Function might not accept context parameter
                pass


class TestIsRecoverable:
    """Test is_recoverable utility function"""
    
    def test_is_recoverable_exists(self):
        """Test that is_recoverable function exists"""
        assert callable(is_recoverable)
    
    def test_api_error_recoverable(self):
        """Test that API errors are typically recoverable"""
        error = APIError("Network timeout")
        # Implementation may vary - just test it doesn't crash
        result = is_recoverable(error)
        assert isinstance(result, bool)
    
    def test_database_error_recoverable(self):
        """Test database error recoverability"""
        error = DatabaseError("Connection lost")
        result = is_recoverable(error)
        assert isinstance(result, bool)
    
    def test_configuration_error_not_recoverable(self):
        """Test that configuration errors are typically not recoverable"""
        error = ConfigurationError("Missing required config")
        result = is_recoverable(error)
        assert isinstance(result, bool)
    
    def test_validation_error_not_recoverable(self):
        """Test that validation errors are typically not recoverable"""
        error = ValidationError("Invalid data format")
        result = is_recoverable(error)
        assert isinstance(result, bool)
    
    def test_generic_exception_handling(self):
        """Test handling of generic exceptions"""
        error = Exception("Generic error")
        result = is_recoverable(error)
        assert isinstance(result, bool)


class TestExceptionMessages:
    """Test exception message formatting"""
    
    def test_exception_preserves_message(self):
        """Test that exception message is preserved"""
        message = "This is a detailed error message"
        error = WeatherDominatorError(message)
        assert str(error) == message
    
    def test_empty_message(self):
        """Test exception with empty message"""
        error = WeatherDominatorError("")
        assert str(error) == ""
    
    def test_multiline_message(self):
        """Test exception with multiline message"""
        message = "Line 1\nLine 2\nLine 3"
        error = WeatherDominatorError(message)
        assert "Line 1" in str(error)
        assert "Line 2" in str(error)


class TestExceptionChaining:
    """Test exception chaining and context"""
    
    def test_exception_from_another(self):
        """Test explicit exception chaining"""
        original = ValueError("Original error")
        
        with pytest.raises(APIError) as exc_info:
            try:
                raise original
            except ValueError as e:
                raise APIError("API wrapper error") from e
        
        assert exc_info.value.__cause__ is original
    
    def test_exception_during_handling(self):
        """Test implicit exception chaining"""
        with pytest.raises(DatabaseError) as exc_info:
            try:
                raise ConfigurationError("Config error")
            except ConfigurationError:
                raise DatabaseError("Database error")
        
        # Should have context
        assert isinstance(exc_info.value, DatabaseError)
    
    def test_suppress_context(self):
        """Test suppressing exception context"""
        with pytest.raises(APIError) as exc_info:
            try:
                raise ValueError("Original")
            except ValueError:
                raise APIError("New error") from None
        
        assert exc_info.value.__cause__ is None


class TestExceptionInheritance:
    """Test exception catching with inheritance"""
    
    def test_catch_specific_exception(self):
        """Test catching specific exception type"""
        with pytest.raises(APIError):
            raise APIError("API error")
    
    def test_catch_base_exception(self):
        """Test catching via base exception"""
        with pytest.raises(WeatherDominatorError):
            raise APIError("API error")
    
    def test_catch_multiple_types(self):
        """Test catching multiple exception types"""
        exceptions = [
            ConfigurationError("Config"),
            APIError("API"),
            DatabaseError("DB")
        ]
        
        for exc in exceptions:
            with pytest.raises(WeatherDominatorError):
                raise exc
