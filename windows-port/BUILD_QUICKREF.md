# Quick Build Guide - Windows Executable

## TL;DR - Build in 3 Steps

### 1. Install PyInstaller
```cmd
pip install pyinstaller
```

### 2. Run Build Script
```cmd
build.bat
```

### 3. Find the Executable
```
dist\Copysight.exe
```

---

## Manual Build (Alternative)

```cmd
pyinstaller --onefile --windowed --name Copysight --add-data "ui;ui" --add-data "assets;assets" --hidden-import webview --hidden-import yt_dlp --hidden-import faster_whisper --hidden-import openai --hidden-import httpx --collect-all faster_whisper app.py
```

---

## Expected Results

- **File size**: 140-200 MB
- **Location**: `dist/Copysight.exe`
- **Type**: Windows executable
- **Requirements**: Windows 10/11 (64-bit)

---

## Distribution

Simply copy `Copysight.exe` to any Windows machine. No Python installation required.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PyInstaller not found | `pip install pyinstaller` |
| Build fails | Check error messages, ensure all dependencies installed |
| Antivirus alert | False positive, add exclusion |
| Missing modules | Add `--hidden-import module_name` |

---

## Full Documentation

See `BUILD_WINDOWS.md` for detailed build instructions.
