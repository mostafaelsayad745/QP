@echo off
title QB Academy Quality Management System v2.0
color 0A

echo =====================================================
echo    QB Academy Quality Management System v2.0
echo    Premium Arabic Enhancement Edition
echo =====================================================
echo.

REM Change to the directory where the script is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if required packages are installed
echo 🔍 Checking dependencies...
python -c "import arabic_reshaper, bidi" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install arabic-reshaper python-bidi Pillow reportlab
    if errorlevel 1 (
        echo ❌ Failed to install packages
        pause
        exit /b 1
    )
    echo ✅ Packages installed successfully
) else (
    echo ✅ All dependencies are ready
)

echo.
echo 🚀 Starting QB Academy Quality Management System...
echo.

REM Start the application
python qb.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Application ended with an error
    pause
)
