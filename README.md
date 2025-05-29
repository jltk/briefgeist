# Brifegeist

[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![python: 3.9+](https://img.shields.io/badge/python-3.9%2B-important.svg)](https://www.python.org/)  

**Brifegeist** ist eine modulare Python-Suite zur automatisierten Verarbeitung, Analyse und Beantwortung deutscher Schriftstücke.  
Sie kombiniert:

1. **Watcher-Service** (Watchdog) zum Echtzeit-Monitoring eingehender Scans  
2. **OCR-Modul** (Tesseract) zur Textextraktion aus PDF-Scans  
3. **Analyse-Engine** (lokales LLM via Ollama “gemma:7b”)  

## 📦 Installation

```bash
git clone https://github.com/DeinUser/Brifegeist.git
cd Brifegeist
python -m venv venv
source venv/bin/activate  # bzw. venv\Scripts\activate on Windows
pip install -r requirements.txt


**Briefgeist** is a privacy-first, local desktop assistant for automating the reading, analysis, and response of scanned physical letters.

- 🖨️ Scan letters (via NAPS2)
- 🧠 Analyze content with a local LLM (Gemma 7B via Ollama)
- 🗣 Text-to-speech playback (Coqui TTS)
- 📄 Suggest replies or fill forms
- 🖥️ Simple GUI (NiceGUI)
- 💻 100% offline, no cloud or telemetry

---

## ✅ Features

| Feature            | Status |
|--------------------|--------|
| OCR (ocrmypdf)     | ✅     |
| Text extraction    | ✅     |
| Local LLM (Ollama) | ✅     |
| TTS voice output   | ✅     |
| GUI (NiceGUI)      | ✅     |
| Multi-page scan    | ✅     |

---

## 🛠 Setup (Windows 10+)

### 1. Install System Dependencies

- [Python 3.11](https://www.python.org/downloads/release/python-3119/)
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)  
  → Select: "Desktop development with C++"
- [Tesseract OCR (UB Mannheim)](https://github.com/UB-Mannheim/tesseract/wiki)
- [SumatraPDF](https://www.sumatrapdfreader.org/download-free-pdf-viewer.html)
- [NAPS2 (scanner frontend)](https://www.naps2.com)
- [Ollama (LLM runtime)](https://ollama.com)

### 2. Clone This Repo

```bash
git clone https://github.com/yourname/briefgeist.git
cd briefgeist
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start Ollama

```bash
ollama run gemma:7b
```

---

## 🚀 Usage

### 1. Scan

Use NAPS2 to scan a letter as PDF into the `input/` folder.

### 2. Process with Watcher

```bash
python watcher/watcher.py
```

This will:

* OCR the scanned PDF
* Extract text
* Save `.txt` in `output/`
* Archive the original in `processed/`

### 3. Open GUI

```bash
python ui/app.py
```

* Upload the `.txt`
* Click "Analyze"
* Click "Read Aloud"

---

## 🧪 Testing

| Test Step            | Expected Result                     |
| -------------------- | ----------------------------------- |
| Drop PDF in `input/` | Processed + `.txt` created          |
| Run GUI              | Interface appears with input fields |
| Analyze              | LLM provides meaningful summary     |
| Read Aloud           | Voice plays locally                 |
| Print PDF (optional) | Sent to default printer             |

---

## 🗂 Project Structure

```
briefgeist/
├── core/
├── ui/
├── watcher/
├── input/         ← Drop PDFs here
├── output/        ← Get your results here
├── processed/     ← Archived input
```

---

## 🔐 Security & Privacy

Briefgeist runs fully offline. No cloud calls. No telemetry. No account required.

---

## 📦 Next Milestones

* [ ] Improve UI/UX
* [ ] Form field detection (insurance, invoices, etc.)
* [ ] Auto-response generation as PDF
* [ ] One-click print & archive
* [ ] Portable GUI build (PyInstaller)

---

## 💬 License

GPLv3