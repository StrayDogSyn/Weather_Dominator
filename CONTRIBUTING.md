# Contributing to Weather Dominator

First off, thank you for considering contributing to Weather Dominator! It's people like you that make Weather Dominator such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if possible**
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain the expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/Weather_Dominator.git
cd Weather_Dominator
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

## Style Guidelines

### Python Style Guide

This project follows PEP 8 with some modifications:

* Maximum line length: 100 characters
* Use 4 spaces for indentation
* Use double quotes for strings
* Use type hints for function signatures

### Code Formatting

We use Black for code formatting:

```bash
black .
```

### Import Sorting

We use isort for organizing imports:

```bash
isort .
```

### Type Checking

We use mypy for static type checking:

```bash
mypy src/
```

### Linting

We use flake8 for linting:

```bash
flake8 .
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_weather_api.py
```

### Writing Tests

* Place test files in the `tests/` directory
* Name test files as `test_*.py`
* Name test functions as `test_*`
* Use descriptive names for test functions
* Include docstrings for complex test cases
* Use fixtures for common setup

Example test structure:

```python
def test_weather_api_success():
    """Test that weather API returns correct data for valid city."""
    weather_api = WeatherAPI(api_key="test_key")
    result = weather_api.get_current_weather("New York")
    
    assert "temp" in result
    assert "humidity" in result
    assert result["city"] == "New York"
```

## Documentation

### Docstring Format

We use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description of function.
    
    Longer description if needed. Can span multiple lines
    and include detailed information about the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
        
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Code Comments

* Use comments to explain "why", not "what"
* Keep comments up to date
* Write comments in complete sentences
* Capitalize the first word
* Use inline comments sparingly

## Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
* `feat`: New feature
* `fix`: Bug fix
* `docs`: Documentation only changes
* `style`: Code style changes (formatting, missing semi colons, etc)
* `refactor`: Code refactoring
* `perf`: Performance improvement
* `test`: Adding missing tests
* `chore`: Changes to build process or auxiliary tools

**Example:**

```
feat(weather-api): add caching for API responses

Implement response caching to reduce API calls and improve
performance. Cache expires after 5 minutes.

Closes #123
```

## Project Structure

```
Weather_Dominator/
├── src/                  # Core source code
│   ├── constants.py      # Application constants
│   ├── config_manager.py # Configuration management
│   ├── exceptions.py     # Custom exceptions
│   └── logger.py         # Logging configuration
├── data/                 # Data modules
├── ui/                   # User interface
├── db/                   # Database layer
├── ml/                   # Machine learning
├── utils/                # Utilities
├── tests/                # Test suite
├── docs/                 # Documentation
└── config/               # Configuration files
```

## Review Process

1. **Create a branch** for your changes
2. **Make your changes** with clear, descriptive commits
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Run the test suite** to ensure everything passes
6. **Submit a pull request** with a clear description

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages follow the format
- [ ] No merge conflicts
- [ ] Reviewed own code changes

## Questions?

Feel free to:
* Open an issue with the "question" label
* Start a discussion in GitHub Discussions
* Contact the maintainers

## Recognition

Contributors will be recognized in:
* The project README
* Release notes
* Contributors page

Thank you for contributing to Weather Dominator! 🌩️
