@echo off
REM Copysight Installation Script for Windows
REM This script sets up the virtual environment and installs dependencies

cd /d "%~dp0"

echo ========================================
echo Copysight Installation for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if FFmpeg is installed
echo Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo FFmpeg not found. Downloading...
    echo.
    echo Creating ffmpeg directory in project folder...
    if not exist "ffmpeg\" mkdir ffmpeg

    echo Downloading FFmpeg (this may take a moment)...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'"

    echo Extracting FFmpeg...
    powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg' -Force"

    echo Copying ffmpeg.exe and ffprobe.exe to project directory...
    copy /Y "ffmpeg\ffmpeg-release-essentials\bin\ffmpeg.exe" . >nul 2>&1
    copy /Y "ffmpeg\ffmpeg-release-essentials\bin\ffprobe.exe" . >nul 2>&1

    echo Cleaning up...
    rmdir /s /q ffmpeg
    del ffmpeg.zip

    echo FFmpeg installed locally.
) else (
    echo FFmpeg found in PATH.
)
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install pywebview without dependencies (avoids pythonnet build)
echo.
echo Installing pywebview (without dependencies)...
pip install pywebview --no-deps

REM Install remaining dependencies
echo.
echo Installing remaining dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the application, run: launch.bat
echo.
pause
