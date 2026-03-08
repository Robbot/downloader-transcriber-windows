"""
Windows-compatible transcription module using faster-whisper.

Replaces mlx-whisper (macOS/Apple Silicon only) with faster-whisper
which works on Windows, Linux, and macOS with CPU or CUDA GPU acceleration.
"""

import sys
import os
import subprocess


# Model name mapping: UI key → faster-whisper model identifier
# faster-whisper uses OpenAI's standard model names
_WHISPER_MODELS = {
    "tiny": "tiny",
    "base": "base",
    "small": "small",
    "medium": "medium",
    "large": "large-v3",
    "turbo": "large-v3",  # Use large-v3 as fallback for turbo
}


def _detect_device():
    """Detect the best available device for transcription.

    Returns:
        tuple: (device, compute_type) where device is "cuda" or "cpu"
               and compute_type is "float16" for CUDA or "int8" for CPU
    """
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda", "float16"
    except ImportError:
        pass
    return "cpu", "int8"


def _get_audio_duration(audio_path):
    """Get audio duration in seconds using ffprobe. Returns None on failure."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', audio_path],
            capture_output=True, text=True, timeout=10,
        )
        return float(result.stdout.strip())
    except Exception:
        return None


def _format_duration(seconds):
    """Format seconds as M:SS or H:MM:SS."""
    seconds = int(seconds)
    if seconds >= 3600:
        h, rest = divmod(seconds, 3600)
        m, s = divmod(rest, 60)
        return f"{h}:{m:02d}:{s:02d}"
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def transcribe_audio(audio_path, language=None, model_size="turbo", initial_prompt=None,
                     log_fn=print, phase_fn=None):
    """
    Transcribe an audio file using faster-whisper (Windows/Linux/macOS compatible).

    Supports CPU and CUDA (NVIDIA GPU) acceleration. Models are downloaded
    on first use and cached locally.

    :param audio_path: Path to the audio file (e.g. .mp3).
    :param language: Expected language (e.g. 'pl', 'en'). If None, Whisper auto-detects.
    :param model_size: Model key ('tiny', 'base', 'small', 'medium', 'large', 'turbo').
    :param initial_prompt: Context hint to reduce hallucinations.
    :param log_fn: Logging callback (default: print).
    :param phase_fn: Optional callback(phase_str) for live UI updates.
    """
    from faster_whisper import WhisperModel

    def phase(msg):
        if phase_fn:
            phase_fn(msg)
        log_fn(msg)

    if not os.path.exists(audio_path):
        log_fn(f"Audio file not found: {audio_path}")
        return None

    # Detect device and compute type
    device, compute_type = _detect_device()

    # Resolve model name
    model_name = _WHISPER_MODELS.get(model_size, _WHISPER_MODELS["turbo"])
    model_label = model_size if model_size in _WHISPER_MODELS else "turbo"

    # Audio duration for progress display
    duration = _get_audio_duration(audio_path)
    duration_str = _format_duration(duration) if duration else None

    if duration_str:
        phase(f"Transcribing {duration_str} ({model_label})")
    else:
        file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        phase(f"Transcribing {file_size_mb:.0f} MB ({model_label})")

    # Language settings
    if language and language.lower() not in ['auto', 'none', '']:
        language_code = language.lower()
        log_fn(f"Language forced: {language}")
    else:
        language_code = None
        log_fn("Auto-detecting language")

    log_fn(f"Engine: faster-whisper · {model_name} · {device.upper()} ({compute_type})")

    try:
        # Load model (cached automatically by faster-whisper)
        model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
            download_root=os.path.expanduser("~/.cache/whisper"),
        )

        # Transcribe
        segments, info = model.transcribe(
            audio_path,
            language=language_code,
            initial_prompt=initial_prompt,
            beam_size=5,
            vad_filter=True,
            word_timestamps=False,
        )

        # Combine all segments into full text
        text_parts = []
        for segment in segments:
            text_parts.append(segment.text)

        full_text = "".join(text_parts).strip()
        detected_language = info.language if hasattr(info, 'language') else '?'
        phase(f"Done — {detected_language}")
        return full_text

    except Exception as e:
        log_fn(f"Transcription error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <audio_file> [language] [model] [prompt]")
        sys.exit(1)

    audio_file = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "auto"
    mod_size = sys.argv[3] if len(sys.argv) > 3 else "turbo"
    prompt = sys.argv[4] if len(sys.argv) > 4 else None

    text = transcribe_audio(audio_file, language=lang, model_size=mod_size, initial_prompt=prompt)

    if text:
        print("\n--- TRANSCRIPTION RESULT ---")
        print(text.strip()[:500] + "...\n(rest saved to txt file)")
        print("----------------------------")

        result_path = os.path.splitext(audio_file)[0] + ".txt"
        with open(result_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved: {result_path}")
