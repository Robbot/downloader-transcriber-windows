"""
PyInstaller build script for creating a standalone Windows executable.

This script packages Copysight into a single .exe file for easy distribution.

Requirements:
    pip install pyinstaller

Usage:
    python build_exe.py
"""

import os
import sys
import subprocess

# PyInstaller configuration
APP_NAME = "Copysight"
ICON_PATH = "assets/icon.ico" if os.path.exists("assets/icon.ico") else None
SCRIPT_FILE = "app.py"
SPEC_FILE = f"{APP_NAME}.spec"

# PyInstaller command arguments
PYINSTALLER_ARGS = [
    "pyinstaller",
    "--onefile",  # Create a single executable
    "--windowed",  # Hide console window (use --console for debugging)
    "--name", APP_NAME,
    "--add-data", "ui;ui",  # Include UI files
    "--add-data", "assets;assets",  # Include assets
    "--hidden-import", "webview",
    "--hidden-import", "yt_dlp",
    "--hidden-import", "faster_whisper",
    "--hidden-import", "openai",
    "--hidden-import", "httpx",
    "--collect-all", "faster_whisper",  # Include all faster-whisper dependencies
    SCRIPT_FILE,
]


def build():
    """Build the executable using PyInstaller."""
    print("=" * 50)
    print("Building Copysight Windows executable")
    print("=" * 50)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("ERROR: PyInstaller is not installed")
        print("Install it with: pip install pyinstaller")
        return False

    # Add icon if available
    if ICON_PATH:
        PYINSTALLER_ARGS.extend(["--icon", ICON_PATH])
        print(f"Using icon: {ICON_PATH}")
    else:
        print("No icon found, using default")

    print()
    print("Running PyInstaller...")
    print("Command:", " ".join(PYINSTALLER_ARGS))
    print()

    # Run PyInstaller
    try:
        result = subprocess.run(PYINSTALLER_ARGS, check=True)
        print()
        print("=" * 50)
        print("Build completed successfully!")
        print("=" * 50)
        print()
        print(f"Executable location: dist/{APP_NAME}.exe")
        print()
        return True
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 50)
        print("Build failed!")
        print("=" * 50)
        print()
        print(f"Error: {e}")
        return False


def clean():
    """Clean build artifacts."""
    import shutil
    dirs_to_remove = ["build", "dist"]
    files_to_remove = [SPEC_FILE]

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed: {dir_name}")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Removed: {file_name}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
    else:
        success = build()
        sys.exit(0 if success else 1)
