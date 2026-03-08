# Building the Windows Executable

This guide explains how to create a standalone Windows executable (.exe) for Copysight.

## Prerequisites

1. **Windows 10 or 11** (64-bit)
2. **Python 3.10+** installed
3. **Copysight Windows port** installed and working
4. **PyInstaller** installed: `pip install pyinstaller`

## Quick Build (5 minutes)

### Step 1: Install Dependencies

```cmd
# Install PyInstaller
pip install pyinstaller

# Verify installation
pyinstaller --version
```

### Step 2: Build the Executable

```cmd
# Navigate to the Windows port directory
cd path\to\windows-port

# Build the executable
pyinstaller --onefile --windowed --name Copysight --add-data "ui;ui" --add-data "assets;assets" --hidden-import webview --hidden-import yt_dlp --hidden-import faster_whisper --hidden-import openai --hidden-import httpx --collect-all faster_whisper app.py
```

### Step 3: Find the Executable

After building, the executable will be in:
```
dist\Copysight.exe
```

### Step 4: Test the Executable

```cmd
# Run the executable
dist\Copysight.exe
```

## Build Options

### Option 1: Single File (Recommended)

Creates a single .exe file (140-200 MB):

```cmd
pyinstaller --onefile --windowed --name Copysight ^
    --add-data "ui;ui" ^
    --add-data "assets;assets" ^
    --hidden-import webview ^
    --hidden-import yt_dlp ^
    --hidden-import faster_whisper ^
    --hidden-import openai ^
    --hidden-import httpx ^
    --collect-all faster_whisper ^
    app.py
```

**Pros**:
- Single file to distribute
- Easy to share

**Cons**:
- Slower startup (extracts to temp)
- Larger file size

### Option 2: Directory (Faster Startup)

Creates a folder with the executable and dependencies:

```cmd
pyinstaller --onedir --windowed --name Copysight ^
    --add-data "ui;ui" ^
    --add-data "assets;assets" ^
    --hidden-import webview ^
    --hidden-import yt_dlp ^
    --hidden-import faster_whisper ^
    --hidden-import openai ^
    --hidden-import httpx ^
    --collect-all faster_whisper ^
    app.py
```

**Pros**:
- Faster startup
- Smaller executable

**Cons**:
- Multiple files to distribute
- Must keep folder structure intact

### Option 3: With Console (Debug Mode)

For debugging or development, show the console:

```cmd
pyinstaller --onefile --console --name Copysight_Debug ^
    --add-data "ui;ui" ^
    --add-data "assets;assets" ^
    --hidden-import webview ^
    --hidden-import yt_dlp ^
    --hidden-import faster_whisper ^
    --hidden-import openai ^
    --hidden-import httpx ^
    --collect-all faster_whisper ^
    app.py
```

## Build Script

For convenience, use the provided build script:

### Batch File (build.bat)

```batch
@echo off
echo Building Copysight Windows executable...

pyinstaller --onefile --windowed --name Copysight ^
    --add-data "ui;ui" ^
    --add-data "assets;assets" ^
    --hidden-import webview ^
    --hidden-import yt_dlp ^
    --hidden-import faster_whisper ^
    --hidden-import openai ^
    --hidden-import httpx ^
    --collect-all faster_whisper ^
    app.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable: dist\Copysight.exe
echo.
pause
```

### Python Script (build_exe.py)

The provided `build_exe.py` script can also be used:

```cmd
python build_exe.py
```

To clean build artifacts:

```cmd
python build_exe.py clean
```

## Advanced Options

### Add Icon

If you have an icon file:

```cmd
pyinstaller --onefile --windowed --icon=assets/icon.ico ...
```

### Add Version Info

Create a `version.txt` file:

```text
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Copysight'),
        StringStruct(u'FileDescription', u'Video insight extractor'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'Copysight'),
        StringStruct(u'LegalCopyright', u'2024'),
        StringStruct(u'OriginalFilename', u'Copysight.exe'),
        StringStruct(u'ProductName', u'Copysight'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Then use:

```cmd
pyinstaller --onefile --windowed --version-file=version.txt ...
```

### Exclude Unnecessary Modules

To reduce file size:

```cmd
pyinstaller --onefile --windowed ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module pandas ^
    ...
```

## Distribution

### For Personal Use

Simply copy the `dist\Copysight.exe` file to any Windows machine.

### For Distribution

1. **Create a distribution folder**:
   ```
   Copysight/
   ├── Copysight.exe
   ├── README.txt
   └── QUICKSTART.txt
   ```

2. **Create a ZIP archive**:
   ```cmd
   powershell Compress-Archive -Path Copysight -DestinationPath Copysight-v1.0.zip
   ```

3. **Optional: Create installer**:
   - Use [NSIS](https://nsis.sourceforge.io/)
   - Use [Inno Setup](https://jrsoftware.org/isinfo.php)
   - Use [WiX Toolset](https://wixtoolset.org/)

## Troubleshooting

### "Module not found" Error

Add the missing module to hidden imports:

```cmd
--hidden-import module_name
```

### "DLL not found" Error

Ensure all dependencies are included:

```cmd
--collect-all package_name
```

### Antivirus False Positive

Some antivirus software may flag PyInstaller executables as false positives. To resolve:

1. **Code sign the executable** (requires certificate)
2. **Submit to VirusTotal** for analysis
3. **Add exclusion** in antivirus software

### Large File Size

The executable includes:
- Python interpreter
- All dependencies
- faster-whisper models (downloaded on first run)
- UI files and assets

Typical size: 140-200 MB

To reduce size:
- Use `--onedir` instead of `--onefile`
- Exclude unnecessary modules
- Use UPX compression (experimental)

## Performance Tips

### Optimized Build

For best performance:

```cmd
pyinstaller --onefile --windowed ^
    --optimize=2 ^
    --strip ^
    ...
```

### UPX Compression

To compress the executable (may cause antivirus false positives):

```cmd
pyinstaller --onefile --windowed ^
    --upx-dir=C:\path\to\upx ^
    ...
```

## Verification

After building, verify:

1. **File size**: Should be 140-200 MB
2. **Launch**: Double-click to open
3. **First run**: Should download Whisper models
4. **Transcription**: Should work on CPU or GPU
5. **Analysis**: Should work with API key

## Build Artifacts

After building, you'll have:

```
windows-port/
├── build/           # Build files (can be deleted)
│   └── Copysight/
├── dist/            # Final executable
│   └── Copysight.exe
└── Copysight.spec   # PyInstaller spec file
```

To clean build artifacts:

```cmd
rmdir /s /q build dist
del Copysight.spec
```

Or use the build script:

```cmd
python build_exe.py clean
```

## Summary

Building a Windows executable is straightforward with PyInstaller:

1. Install PyInstaller: `pip install pyinstaller`
2. Run build command
3. Find executable in `dist/` folder
4. Test and distribute

The resulting .exe file is portable and can be run on any Windows 10/11 system without Python installation.

## Next Steps

After building:

1. **Test** the executable thoroughly
2. **Create documentation** for end users
3. **Package** for distribution (ZIP or installer)
4. **Distribute** to users

For support or issues, refer to the main README_WINDOWS.md file.
