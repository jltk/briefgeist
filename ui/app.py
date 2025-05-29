from nicegui import app, ui
from core.llm import ask_local_llm
from core.speaker import speak_text
from io import TextIOWrapper
import asyncio
from pathlib import Path

# 1) Native-Fenster konfigurieren
app.native.window_args["width"] = 800
app.native.window_args["height"] = 800

# 2) Audio-Ordner sicherstellen
Path("output/audio").mkdir(parents=True, exist_ok=True)

# 3) UI-Elemente anlegen
text = ui.textarea("📄 Brieftext").classes("w-full h-64")
reply = ui.textarea("✉️ Antwortvorschlag").classes("w-full h-48")
status = ui.label("Bereit").classes("text-sm text-gray-500")
read_button = ui.button("🔊 Vorlesen", on_click=lambda: speak_text(reply.value or ""))
read_button.disable()

# 4) Spinner initial versteckt, mittig positioniert
spinner = ui.spinner().style(
    "display:none; position:absolute; top:50%; left:50%; transform:translate(-50%, -50%);"
)

# 5) Upload → Einlesen → Analyse → UI-Update → Spinner verstecken
async def process_file(file):
    # Einlesen
    content = TextIOWrapper(file.content, encoding="utf-8").read()
    text.set_value(content)
    status.set_text("Analysiere…")
    read_button.disable()

    # Spinner einblenden
    spinner.style("display:block")
    spinner.update()

    # Analyse im Hintergrund
    try:
        result = await asyncio.to_thread(ask_local_llm, content)
        reply.set_value(result)
        status.set_text("Antwort erhalten.")
        read_button.enable()
    except Exception as e:
        status.set_text(f"Fehler: {e}")

    # Spinner wieder verstecken
    spinner.style("display:none")
    spinner.update()

# 6) Upload-Trigger
ui.upload(
    label="📎 TXT hochladen (oder hierher ziehen)",
    multiple=False,
    on_upload=process_file
)

# 7) Server starten im Native-Fenster
ui.run(native=True, reconnect_timeout=0)
