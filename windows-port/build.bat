@echo off
REM Copysight Windows Build Script
REM This script builds a standalone Windows executable using PyInstaller

cd /d "%~dp0"

echo ========================================
echo Copysight Windows Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Clean previous build
if exist "build\" (
    echo Cleaning previous build...
    rmdir /s /q build
)
if exist "dist\" (
    echo Cleaning previous distribution...
    rmdir /s /q dist
)
if exist "Copysight.spec" (
    del Copysight.spec
)

echo.
echo Building Copysight.exe...
echo.

REM Build the executable
pyinstaller --onefile --windowed --name Copysight ^
    --add-data "ui;ui" ^
    --add-data "assets;assets" ^
    --hidden-import webview ^
    --hidden-import yt_dlp ^
    --hidden-import faster_whisper ^
    --hidden-import openai ^
    --hidden-import httpx ^
    --hidden-import faster_whisper.utils ^
    --hidden-import faster_whisper.vad ^
    --collect-all faster_whisper ^
    app.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    echo.
    echo Check the error messages above for details.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\Copysight.exe
echo.

REM Show file size
for %%A in ("dist\Copysight.exe") do (
    set size=%%~zA
    set /a sizeMB=!size! / 1048576
)
echo File size: !sizeMB! MB
echo.

REM Test if executable exists
if exist "dist\Copysight.exe" (
    echo [OK] Executable created successfully
    echo.
    echo To run the application:
    echo   dist\Copysight.exe
    echo.
    echo To test the executable now, press Y.
    choice /c YN /m "Do you want to test the executable now"
    if errorlevel 2 (
        echo.
        echo Skipping test. You can run it manually later.
    ) else (
        echo.
        echo Launching Copysight...
        start "" "dist\Copysight.exe"
    )
) else (
    echo [ERROR] Executable was not created!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Summary
echo ========================================
echo.
echo Source: windows-port\
echo Output: dist\Copysight.exe
echo.
echo To distribute:
echo   1. Copy Copysight.exe to target machine
echo   2. No Python installation required
echo   3. Whisper models download on first run
echo.
echo For distribution options, see BUILD_WINDOWS.md
echo.
pause
