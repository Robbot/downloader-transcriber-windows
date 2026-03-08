@echo off
REM Copysight Launcher for Windows
REM This script activates the virtual environment and starts the application

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the application
python app.py

REM If the application crashes, keep the window open to see errors
if errorlevel 1 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)
