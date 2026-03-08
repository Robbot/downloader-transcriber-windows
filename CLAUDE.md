# Copysight — Claude Code Instructions

## What this is

A cross-platform desktop app (PyWebView + vanilla HTML/CSS/JS) that extracts structured insights from online videos. Runs locally with Whisper transcription and AI-powered analysis via OpenRouter.

**Two versions:**
- `src/` — Original macOS version (Apple Silicon, mlx-whisper)
- `windows-port/` — Windows port (cross-platform, faster-whisper)

No frameworks, no bundlers, no npm.

---

## Project Structure

```
downloader-transcriber-windows/
├── src/                    # macOS version (mlx-whisper, Apple Silicon)
│   ├── app.py              # PyWebView entry point
│   ├── transcriber.py      # mlx-whisper (Metal/GPU)
│   ├── ui/                 # Frontend (HTML/CSS/JS)
│   └── CLAUDE.md           # macOS-specific instructions
│
├── windows-port/           # Windows/cross-platform version
│   ├── app.py              # PyWebView entry point
│   ├── transcriber.py      # faster-whisper (CUDA/CPU)
│   ├── ui/                 # Frontend (HTML/CSS/JS)
│   ├── build_exe.py        # PyInstaller build script
│   ├── install.bat/ps1     # Installation scripts
│   └── launch.bat/ps1      # Launch scripts
│
└── CLAUDE.md               # This file
```

---

## How to Run

### macOS (Apple Silicon only)
```bash
cd src/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
venv/bin/python app.py
```

### Windows / Linux / Cross-platform
```bash
cd windows-port/
python -m venv venv
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

### Build Windows Executable
```bash
cd windows-port/
pip install pyinstaller
python build_exe.py
# Output: dist/Copysight.exe
```

---

## Architecture

**Python backend** (PyWebView bridge):
- `app.py` — Entry point, `Api` class exposed to JS via `window.pywebview.api.*`
- `downloader.py` — yt-dlp wrapper, returns `{mp3, meta}` dict
- `transcriber.py` — Whisper transcription (mlx-whisper on macOS, faster-whisper on Windows)
- `analyzer.py` — OpenRouter API (Gemini 2.0 Flash) via OpenAI SDK
- `vault.py` — API key storage in `.env`

**Frontend** (vanilla, no frameworks):
- `ui/index.html` — SPA with 4 screens + settings overlay
- `ui/app.js` — Navigation, pipeline polling, typewriter, reader, library
- `ui/styles.css` — Complete visual theme

**Bridge pattern**: JS calls Python via `window.pywebview.api.method_name()` returning a Promise. Pipeline runs in background thread; JS polls every 500ms.

---

## Key Differences Between Versions

| Component | macOS (`src/`) | Windows (`windows-port/`) |
|-----------|----------------|---------------------------|
| **Transcription** | `mlx-whisper` | `faster-whisper` |
| **GPU Acceleration** | Metal/Apple Neural Engine | CUDA (NVIDIA) or CPU |
| **Path handling** | Homebrew (`/opt/homebrew/bin`) | Windows program paths |
| **Launcher** | `.app` bundle | `.bat`/`.ps1` scripts or `.exe` |
| **Build tool** | `build_app.sh` | `build_exe.py` (PyInstaller) |

---

## Key Conventions

### Python
- All public `Api` methods return dicts (JSON-serializable for the bridge)
- Shared state protected by `threading.Lock` — always use `self._lock`
- File paths: `DOWNLOADS_DIR`, `TRANSCRIPTS_DIR`, `ANALYSES_DIR` constants
- Versioned filenames: `Name_suffix_YYYYMMDD_HHmm.txt`

### JavaScript
- Vanilla JS only — no frameworks, no modules, no build step
- `var` not `const`/`let` (legacy consistency — don't mix styles)
- All pywebview calls must have `.catch()` handler
- DOM refs declared at top of app.js as `const`

### CSS
- CSS variables in `:root` — use them, don't hardcode colors
- Fonts via `<link>` in HTML `<head>` (not `@import` in CSS)
- `user-select: none` on body, `user-select: text` on `.reader-content`

---

## Brand Guidelines

**Read `brand/guidelines.md` before visual changes.** Key rules:

- **Aesthetic**: "Minimalist Archive" — manila paper, editorial typography, subtle textures
- **Colors**: `--base` #F7E9C1, `--red` #D1344B, `--blue` #4A89C5, `--gold` #E5B742, `--ink` #2B2B2B
- **Fonts**: Playfair Display (brand), IBM Plex Sans/Condensed (UI), Georgia/Charter (reading), IBM Plex Mono (metadata)
- **Tone**: Precise, calm, empowering. No emoji, no exclamation marks
- **Analysis format**: 3 editorial paragraphs, 9 insights with **bold titles** inline

---

## What NOT to Do

- Don't add frameworks (React, Vue, etc.) — intentionally vanilla
- Don't change brand colors/fonts without checking `brand/guidelines.md`
- Don't add security hardening — this is a local desktop app
- Don't use `@import` in CSS for fonts — use `<link>` in HTML
- Don't use `let`/`const` for variables in app.js (except DOM refs)
- Don't add npm, webpack, or build toolchains

---

## Dependencies

### macOS (`src/requirements.txt`)
```
pywebview>=5.0
yt-dlp>=2025.1.0
mlx-whisper>=0.1.0
openai>=1.0.0
python-dotenv
Pillow>=10.0.0
```

### Windows (`windows-port/requirements.txt`)
```
pywebview>=5.0
yt-dlp>=2025.1.0
faster-whisper>=1.0.0
openai>=1.0.0
httpx>=0.27.0
Pillow>=10.0.0
```

---

## File Output Format

Analysis files saved with source URL header:
```
<!-- source: https://youtube.com/watch?v=... -->
## Praktyczne tipy
...
```

---

## Testing Without PyWebView

Open `ui/index.html` via HTTP server. The JS has fallback (`if (!window.pywebview)`) for testing UI. Reader can be tested by calling `populateReader(text, meta)` from browser console.
