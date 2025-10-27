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

### Code Quality Tools

We use multiple tools to maintain code quality. All tools are configured to run automatically via pre-commit hooks.

#### Black - Code Formatter

Black formats Python code to a consistent style:

```bash
# Check what would be formatted
black src/ tests/ *.py --check

# Apply formatting
black src/ tests/ *.py
```

Configuration:
- Line length: 100 characters
- Target Python version: 3.13

#### isort - Import Sorter

isort organizes imports in a consistent, readable format:

```bash
# Check import organization
isort src/ tests/ *.py --check --diff

# Apply import sorting
isort src/ tests/ *.py
```

Configuration:
- Profile: black (compatible with Black formatter)
- Line length: 100 characters

#### flake8 - Code Linter

flake8 checks code for style issues and potential bugs:

```bash
# Run flake8 on source code
flake8 src/ --max-line-length=100 --extend-ignore=E203,W503,W293
```

Configuration:
- Max line length: 100
- Ignored rules: E203 (whitespace before ':'), W503 (line break before binary operator), W293 (blank line contains whitespace)
- Excludes: `.git`, `__pycache__`, `build`, `dist`, `.eggs`, `*.egg`

#### mypy - Static Type Checker

mypy validates type hints for type safety:

```bash
# Run type checking on src/
mypy src/ --ignore-missing-imports --no-strict-optional
```

Configuration:
- Ignores missing imports from external libraries
- No strict optional checking
- Only checks `src/` directory

### Running All Quality Checks

Run all quality tools at once:

```bash
# Format code
black src/ tests/ *.py

# Sort imports
isort src/ tests/ *.py

# Check code quality
flake8 src/ --max-line-length=100 --extend-ignore=E203,W503,W293

# Type check
mypy src/ --ignore-missing-imports --no-strict-optional
```

Or use pre-commit to run all checks:

```bash
# Run on staged files
pre-commit run

# Run on all files
pre-commit run --all-files
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

```text
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

```text
feat(weather-api): add caching for API responses

Implement response caching to reduce API calls and improve
performance. Cache expires after 5 minutes.

Closes #123
```

## Project Structure

```text
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

* [ ] Code follows the project's style guidelines
* [ ] Tests pass locally
* [ ] New tests added for new functionality
* [ ] Documentation updated
* [ ] Commit messages follow the format
* [ ] No merge conflicts
* [ ] Reviewed own code changes

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
