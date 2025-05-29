from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.ocr import ocr_pdf, extract_text
from pathlib import Path
import shutil, time

IN, OUT, DONE = Path("input"), Path("output"), Path("processed")
for p in (IN, OUT, DONE):
    p.mkdir(exist_ok=True)

class Handler(FileSystemEventHandler):
    def process(self, path: Path):
        if path.suffix.lower() == ".pdf":
            ocr_path = OUT / path.name
            ocr_pdf(path, ocr_path)
            text = extract_text(ocr_path)
            (OUT / f"{path.stem}.txt").write_text(text, encoding="utf-8")
            shutil.move(path, DONE / path.name)

    def on_created(self, event):
        # manuell sicherstellen, dass die Datei nicht gerade noch geschrieben wird
        time.sleep(0.1)
        self.process(Path(event.src_path))

    def on_moved(self, event):
        # manche Tools verschieben fertige Dateien ins Watch-Verzeichnis
        self.process(Path(event.dest_path))

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), str(IN), recursive=False)
    observer.start()
    print("📱 Watching input/ for new scans…")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
