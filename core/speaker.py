from TTS.api import TTS
from pathlib import Path
import os
import re
from functools import lru_cache

def clean_markdown(text: str) -> str:
    """
    Entfernt Markdown und bereinigt Anführungszeichen, damit
    keine winzigen Segmente mehr entstehen, die zum Kernel-Size-Fehler führen.
    """
    # Grundlegende Markdown-Entfernung
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^[-*]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)
    # Alle Anführungszeichen entfernen (vermeidet einzelne "'" Segmente)
    text = text.replace('"', "").replace("'", "")
    # Mehrere Leerzeilen reduzieren
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()

AUDIO_OUTPUT_DIR = Path("output/audio")
AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@lru_cache(maxsize=1)
def get_tts_engine():
    return TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False, gpu=False)

def speak_text(text: str, filename: str = "speech.wav") -> str:
    clean_text = clean_markdown(text)
    if len(clean_text) < 5:
        raise ValueError("Text zu kurz für Sprachausgabe.")
    out_path = AUDIO_OUTPUT_DIR / filename
    print(f"[DEBUG] TTS speaking full text to: {out_path}")
    print(f"[DEBUG] Cleaned text preview: {clean_text[:120]}{'...' if len(clean_text)>120 else ''}")
    # Einziger (!) tts_to_file-Aufruf – keine Splitting-Option nötig
    get_tts_engine().tts_to_file(text=clean_text, file_path=str(out_path))
    os.startfile(str(out_path))  # öffnet Default-Player
    return str(out_path)
