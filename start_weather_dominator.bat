@echo off
echo.
echo =====================================================
echo    COBRA WEATHER DOMINATOR - LAUNCHING...
echo =====================================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.7+
    pause
    exit /b 1
)

echo.
echo Starting Weather Dominator Application...
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application failed to start!
    echo Check the console output above for details.
    echo.
    pause
)
