"""
Setup configuration for Weather Dominator application.

This file allows the package to be installed via pip and sets up
entry points, dependencies, and package metadata.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, "r") as f:
        requirements = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

# Development requirements
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
    "black>=22.0.0",
    "isort>=5.10.0",
    "flake8>=4.0.0",
    "mypy>=0.950",
    "pre-commit>=2.17.0",
]

setup(
    name="weather-dominator",
    version="2.0.0",
    author="Stray Dog Syndicate",
    author_email="support@straydogsyndicate.com",
    description="Advanced Weather Control System with Glassmorphic UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StrayDogSyndicate/Weather_Dominator",
    project_urls={
        "Bug Tracker": "https://github.com/StrayDogSyndicate/Weather_Dominator/issues",
        "Documentation": "https://github.com/StrayDogSyndicate/Weather_Dominator/blob/main/README.md",
        "Source Code": "https://github.com/StrayDogSyndicate/Weather_Dominator",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Desktop Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "weather-dominator=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.sql", "*.md"],
    },
    keywords=[
        "weather",
        "api",
        "gui",
        "tkinter",
        "machine-learning",
        "glassmorphism",
        "cobra",
        "gijoe",
        "openweathermap",
    ],
    zip_safe=False,
)
