# Copysight Launcher for Windows (PowerShell)
# This script activates the virtual environment and starts the application

$ErrorActionPreference = "Stop"

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run install.ps1 first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Start the application
try {
    python app.py
} catch {
    Write-Host "Application exited with error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
