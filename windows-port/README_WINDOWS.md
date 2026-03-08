# Copysight - Windows Port

A Windows-compatible version of Copysight - a desktop app for downloading YouTube audio, local Whisper transcription, and AI-powered text analysis via OpenRouter.

## Overview

This is a **Windows port** of the original macOS-only application. It replaces the Apple-specific `mlx-whisper` with `faster-whisper`, which works on Windows, Linux, and macOS.

### What Changed from macOS Version

| Component | macOS Version | Windows Version |
|-----------|---------------|-----------------|
| **Transcription Engine** | `mlx-whisper` (Apple Silicon only) | `faster-whisper` (cross-platform) |
| **GPU Acceleration** | Metal/Apple Neural Engine | CUDA (NVIDIA) or CPU |
| **File Explorer** | Finder | Windows Explorer |
| **Launcher** | .app bundle | .bat/.ps1 scripts or .exe |
| **FFmpeg Detection** | Homebrew paths | Windows program paths |

## Features

- **One-click pipeline**: Paste URL → Download → Transcribe → Analyze
- **Local transcription**: No cloud processing of your audio
- **Multi-language support**: Auto-detect or force specific language
- **Multiple models**: tiny, base, small, medium, large, turbo
- **AI analysis**: Powered by OpenRouter API (Gemini 2.0 Flash)
- **Library management**: Organize transcripts by age (fresh, recent, settled, gold)
- **Cross-platform**: Works on Windows 10/11, also compatible with Linux and macOS

## Requirements

### Minimum Requirements

- **Windows 10 or 11** (64-bit)
- **Python 3.10 or higher**
- **4 GB RAM** (8 GB recommended)
- **2 GB free disk space** (for Whisper models)

### Optional Requirements

- **NVIDIA GPU** with CUDA support (for faster transcription)
- **FFmpeg** (for audio processing)

### What Works Without GPU

The app works fine on CPU-only systems. Transcription will be slower but still functional:

- **With NVIDIA GPU**: ~2-5x faster than CPU
- **CPU-only**: Still usable, just slower on long videos

## Installation

### Method 1: Quick Install (Recommended)

1. **Download** the Windows port files
2. **Run** `install.bat` (double-click)
3. **Wait** for installation to complete
4. **Launch** with `launch.bat`

### Method 2: Manual Installation

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org)
   - During installation, check **"Add Python to PATH"**
   - Verify: `python --version`

2. **Install FFmpeg** (optional but recommended):
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract to `C:\FFmpeg`
   - Add `C:\FFmpeg\bin` to your PATH
   - Verify: `ffmpeg -version`

3. **Clone or download** this repository

4. **Open Command Prompt** in the project directory

5. **Create virtual environment**:
   ```cmd
   python -m venv venv
   ```

6. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate
   ```

7. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

8. **Run the application**:
   ```cmd
   python app.py
   ```

### Method 3: Standalone Executable

For a portable .exe without Python installation:

1. **Install PyInstaller**:
   ```cmd
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```cmd
   python build_exe.py
   ```

3. **Find the .exe** in the `dist/` folder

## Usage

### First Launch

1. **Launch** the application (`launch.bat` or `Copysight.exe`)
2. **Settings will open** automatically
3. **Enter your OpenRouter API key** (get one at [openrouter.ai](https://openrouter.ai))
   - Key format: `sk-or-...`
4. **Click Done** to save

### Transcribing a Video

1. **Paste a video URL** (YouTube, Vimeo, etc.)
2. **Click the red button** or press Enter
3. **Wait** for the pipeline to complete:
   - Download audio
   - Transcribe locally
   - Analyze with AI
4. **Read the results** in the Reader view

### Settings Explained

| Setting | Description |
|---------|-------------|
| **API Key** | Your OpenRouter API key (required for AI analysis) |
| **Language** | Force specific language (e.g., 'en', 'pl') or 'auto' |
| **Model** | Whisper model size (tiny/base/small/medium/large/turbo) |
| **Context** | Initial prompt to improve transcription accuracy |
| **Analysis Prompt** | Custom prompt for AI analysis (in Polish by default) |

### Library Organization

Transcripts and analyses are automatically organized by age:

| Tab | Age | Description |
|-----|-----|-------------|
| **Fresh** | 0-7 days | Recent items |
| **Recent** | 8-30 days | Last month |
| **Settled** | 1-6 months | Older items |
| **Gold** | 6+ months | Archive |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Enter** | Start pipeline (when URL is focused) |
| **Escape** | Cancel operation / close settings |
| **←** | Navigate back (Reader → Library → Input) |
| **→** | Navigate forward (Library → Reader) |

## Troubleshooting

### Common Issues

#### "Python is not recognized"

**Problem**: Python is not installed or not in PATH

**Solution**:
1. Install Python from [python.org](https://www.python.org)
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt

#### "FFmpeg not found"

**Problem**: FFmpeg is not installed or not in PATH

**Solution**:
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\FFmpeg`
3. Add `C:\FFmpeg\bin` to System PATH:
   - Press Win+R, type `sysdm.cpl`
   - Go to Advanced → Environment Variables
   - Edit Path and add `C:\FFmpeg\bin`
4. Restart Command Prompt

#### "Transcription failed"

**Problem**: Various causes (model download, GPU issues, etc.)

**Solutions**:
1. **First run**: Whisper model downloads (~1.5 GB) - wait for completion
2. **GPU error**: Try again - sometimes CUDA crashes are transient
3. **CPU fallback**: The app will use CPU if GPU fails
4. **Check disk space**: Ensure 2+ GB free for models

#### "API error (transcript saved)"

**Problem**: OpenRouter API issue (wrong key, rate limit, etc.)

**Solutions**:
1. Verify API key starts with `sk-or-`
2. Check API key validity at [openrouter.ai](https://openrouter.ai)
3. Your transcript is saved - just the analysis failed

#### "Virtual environment not found"

**Problem**: You haven't run the installation script

**Solution**: Run `install.bat` first

### Advanced Troubleshooting

#### Enable Debug Mode

Edit `launch.bat` and change:
```cmd
python app.py
```
To:
```cmd
python app.py --debug
```

#### Check Logs

The app outputs errors to the console. Keep the terminal window open to see error messages.

#### GPU Detection Issues

If you have an NVIDIA GPU but transcription uses CPU:

1. **Check CUDA installation**:
   ```cmd
   nvidia-smi
   ```

2. **Verify PyTorch CUDA support**:
   ```cmd
   python -c "import torch; print(torch.cuda.is_available())"
   ```

3. **Reinstall with CUDA support**:
   ```cmd
   pip uninstall torch torchvision
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

## File Structure

```
copysight-windows/
├── app.py              # Main application entry point
├── transcriber.py      # Transcription module (faster-whisper)
├── downloader.py       # Video downloader (yt-dlp)
├── analyzer.py         # AI analysis (OpenRouter)
├── vault.py            # API key storage
├── requirements.txt    # Python dependencies
├── install.bat         # Installation script
├── install.ps1         # PowerShell installation script
├── launch.bat          # Launch script
├── launch.ps1          # PowerShell launch script
├── build_exe.py        # PyInstaller build script
├── ui/                 # Web UI (HTML/CSS/JS)
├── assets/             # Icons and images
├── brand/              # Brand guidelines
└── downloads/          # Output folder (created at runtime)
    ├── transcripts/    # Raw transcriptions
    └── analyses/       # AI analyses
```

## Performance Tips

### For Faster Transcription

1. **Use NVIDIA GPU**: 3-5x faster than CPU
2. **Choose smaller model**: 'tiny' is fastest, 'turbo' is most accurate
3. **Shorter videos**: Processing time scales with video length
4. **SSD storage**: Faster model loading

### Model Comparison

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| **tiny** | ~40 MB | Fastest | Lower | Quick drafts |
| **base** | ~75 MB | Fast | Good | General use |
| **small** | ~250 MB | Medium | Better | Quality vs speed |
| **medium** | ~770 MB | Slow | Very Good | Important content |
| **large/turbo** | ~1.5 GB | Slowest | Best | Final transcripts |

## Security & Privacy

- **Local processing**: Audio transcription happens on your machine
- **No cloud audio**: Your audio files never leave your computer
- **API key storage**: Stored locally in `.env` file
- **OpenRouter**: Only sends text transcripts, not audio

## License

This is a Windows port of the original Copysight application by Marcin Majsawicki.
Original project: https://github.com/martinmajsawicki/downloader-transcriber

## Support

For issues specific to this Windows port, please check:
1. This README's troubleshooting section
2. The original project's documentation
3. OpenRouter API documentation

## Credits

- **Original app**: Marcin Majsawicki
- **Windows port**: Cross-platform conversion using faster-whisper
- **Dependencies**:
  - [pywebview](https://pywebview.flowrl.com/) - Native webview wrapper
  - [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video downloader
  - [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - Transcription engine
  - [OpenRouter](https://openrouter.ai/) - AI API gateway
