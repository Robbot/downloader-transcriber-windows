# Copysight - Windows Quick Start

Get up and running in under 5 minutes.

## Prerequisites

1. **Windows 10 or 11** (64-bit)
2. **Python 3.10+** installed and in PATH
3. **2 GB free disk space**

## Installation (2 minutes)

### Option A: Automated Installation (Recommended)

1. Download the Windows port files
2. Double-click `install.bat`
3. Wait for installation to complete
4. Double-click `launch.bat` to start

### Option B: Manual Installation

```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

## First Run (1 minute)

1. **Settings window opens automatically**
2. **Get an API key** from [openrouter.ai](https://openrouter.ai)
3. **Paste the key** (starts with `sk-or-`)
4. **Click Done**

## Basic Usage (30 seconds)

1. **Paste a YouTube URL**
2. **Press Enter** or click the red button
3. **Wait** for processing (watch the stamps)
4. **Read your transcript and analysis**

## That's It!

Your video insights are ready in under 2 minutes.

## Need Help?

See `README_WINDOWS.md` for detailed documentation.

---

**Keyboard Shortcuts**:
- `Enter` - Start
- `Escape` - Cancel
- `←` / `→` - Navigate

**What's Happening**:
```
URL → Download MP3 → Transcribe (local) → Analyze (AI) → Done!
```

**Your Data**:
- Audio: Stays on your computer
- Transcript: Saved to `downloads/transcripts/`
- Analysis: Saved to `downloads/analyses/`
