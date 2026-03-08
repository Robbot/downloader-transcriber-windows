# Copysight

Cross-platform desktop app for extracting structured insights from online videos. Download, transcribe, and analyze videos in one click using local Whisper transcription and AI-powered analysis.

## About

Copysight follows a simple pipeline:

1. **Download** audio from any video URL (YouTube, Vimeo, etc.)
2. **Transcribe** locally using Whisper (no cloud audio)
3. **Analyze** with AI via OpenRouter API
4. **Organize** results in a library with age-based categories

Built with PyWebView + vanilla HTML/CSS/JS — no frameworks, no bundlers.

## Original macOS Version

This is a cross-platform Windows port of the original macOS application by Marcin Majsawicki:

**[Original Copysight (macOS, Apple Silicon)](https://github.com/martinmajsawicki/downloader-transcriber)**

The Windows version adds support for Windows 10/11, Linux, and cross-platform compatibility using `faster-whisper` instead of `mlx-whisper`.

## Quick Start

### Windows

```bash
cd windows-port/
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Or use the provided scripts:
- `install.bat` — Creates virtual environment and installs dependencies
- `launch.bat` — Activates environment and starts the app

### Building the Executable

```bash
cd windows-port/
pip install pyinstaller
python build_exe.py
```

Output: `dist/Copysight.exe` (standalone, no Python required)

## Features

| Feature | Description |
|---------|-------------|
| One-Click Pipeline | Paste URL, get full analysis automatically |
| Local Transcription | Audio processing stays on your machine |
| Multi-Language | Auto-detect or force specific language |
| Multiple Models | tiny, base, small, medium, large, turbo |
| AI Analysis | Structured insights via OpenRouter (Gemini 2.0 Flash) |
| Library Management | Auto-organized by age (fresh, recent, settled, gold) |
| Offline Capable | Works after initial setup (transcription is local) |

## Requirements

- **Python 3.11 or 3.12** (3.14 is not supported — packages lack pre-built wheels)
- OpenRouter API key (for AI analysis)
- FFmpeg (for audio processing)

### Windows

- Windows 10/11
- Python 3.11 or 3.12 (download from [python.org](https://www.python.org/downloads/))
- Optional: NVIDIA GPU with CUDA for faster transcription

### Linux/macOS (Cross-platform)

- Python 3.11 or 3.12
- Optional: CUDA for GPU acceleration

## Architecture

```
windows-port/
├── app.py              # PyWebView entry point
├── downloader.py       # yt-dlp wrapper
├── transcriber.py      # faster-whisper (CUDA/CPU)
├── analyzer.py         # OpenRouter API client
├── vault.py            # API key storage
├── ui/
│   ├── index.html      # SPA with 4 screens
│   ├── app.js          # Navigation & pipeline polling
│   └── styles.css      # Complete visual theme
├── build_exe.py        # PyInstaller build script
└── requirements.txt    # Python dependencies
```

## Dependencies

```
pywebview>=5.0
yt-dlp>=2025.1.0
faster-whisper>=1.0.0
openai>=1.0.0
httpx>=0.27.0
Pillow>=10.0.0
```

## Configuration

On first run, you'll be prompted for an OpenRouter API key. This is stored in `.env` in the app directory.

Get an API key: https://openrouter.ai/keys

## Screens

1. **Input** — Paste video URL, choose language and model
2. **Processing** — Real-time pipeline status with progress
3. **Reader** — Read full transcript with AI analysis
4. **Library** — Browse all processed videos organized by age

## Brand

Copysight follows a "Minimalist Archive" aesthetic — manila paper tones, editorial typography, and precise language.

- **Colors**: Manila #F7E9C1, Red #D1344B, Blue #4A89C5, Gold #E5B742
- **Fonts**: Playfair Display, IBM Plex Sans, Georgia/Charter

## License

MIT

---

Original macOS version by [Marcin Majsawicki](https://github.com/martinmajsawicki)
Windows port by [Robbot](https://github.com/Robbot)
