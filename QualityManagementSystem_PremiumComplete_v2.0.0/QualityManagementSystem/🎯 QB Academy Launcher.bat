@echo off
title QB Academy Quality Management System v2.0 - Premium Edition
color 0A
cls

echo.
echo ████████████████████████████████████████████████████████
echo ██                                                    ██
echo ██    QB Academy Quality Management System v2.0       ██
echo ██    Premium Arabic Enhancement Edition              ██
echo ██                                                    ██
echo ████████████████████████████████████████████████████████
echo.

REM Change to the directory where the script is located
cd /d "%~dp0"

echo 🔍 System Check...
echo ✅ Location: %CD%
echo.

REM Check if Python is installed
echo 🐍 Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo 📥 Please install Python 3.7+ from: https://python.org
    echo 📌 Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo ✅ Python is ready
echo.

REM Check if the main file exists
if not exist "qb.py" (
    echo ❌ qb.py not found in current directory
    echo 📁 Current location: %CD%
    echo.
    pause
    exit /b 1
)
echo ✅ QB Academy application found
echo.

REM Quick dependency check and install
echo 📦 Checking/Installing dependencies...
pip install arabic-reshaper python-bidi Pillow reportlab >nul 2>&1
echo ✅ Dependencies ready
echo.

echo 🚀 Launching QB Academy Quality Management System...
echo 💡 Login with: admin / admin123
echo.

REM Start the application
python qb.py

REM If we get here, the app has closed
echo.
echo 👋 Thank you for using QB Academy Quality Management System!
echo.
pause
