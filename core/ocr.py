from pathlib import Path
import subprocess
import pdfplumber
from PIL import Image, ImageFilter, ImageOps
import pytesseract

# Versuche, LanguageTool für Korrekturen zu laden (optional)
try:
    import language_tool_python
    _tool = language_tool_python.LanguageTool('de-DE')
except Exception:
    _tool = None

# Tesseract-Zeichen-Whitelist (inkl. Umlaute)
_TESSERACT_WHITELIST = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'abcdefghijklmnopqrstuvwxyz'
    'ÄÖÜäöüß'
)


def correct_text(text: str) -> str:
    """
    Versucht, OCR-Fehler mittels LanguageTool zu korrigieren.
    Falls nicht vorhanden: Originaltext zurückgeben.
    """
    if not _tool:
        return text
    try:
        matches = _tool.check(text)
        return language_tool_python.utils.correct(text, matches)
    except Exception:
        return text


def ocr_pdf(input_pdf: Path, output_pdf: Path):
    """
    Führe OCR mit ocrmypdf durch (Deskew, Rotation, PDF-Ausgabe).
    Bei Fehlern Rückfall auf manuelle Seite-für-Seite-OCR.
    Tipp: Scanne mit 600 DPI, Graustufen oder 1-Bit B/W.
    """
    print(f"🔍 Running OCR on {input_pdf.name}...")
    cmd = [
        'ocrmypdf',
        '--force-ocr',
        '--deskew',
        '--rotate-pages',
        '--optimize', '1',
        '--output-type', 'pdf',  # Verhindert PDF/A-Konvertierung
        '--jobs', '4',
        str(input_pdf),
        str(output_pdf)
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ OCR completed: {output_pdf.name}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ OCRmypdf failed ({e.returncode}), falling back to manual OCR.")
        manual_page_ocr(input_pdf, output_pdf)


def manual_page_ocr(input_pdf: Path, output_pdf: Path):
    """
    Wandelt PDF-Seiten in Bilder (600 DPI) um,
    führt Tesseract-OCR mit Whitelist aus und korrigiert optional.
    Erzeugt neue PDF-Datei.
    """
    from fpdf import FPDF

    print(f"🔄 Performing manual page-by-page OCR on {input_pdf.name}...")
    text_pages = []
    with pdfplumber.open(input_pdf) as pdf:
        for page in pdf.pages:
            pil_img = page.to_image(resolution=600).original
            img = preprocess_image(pil_img)
            raw = pytesseract.image_to_string(
                img,
                lang='deu',
                config=(
                    '--oem 1 --psm 6 '
                    f'-c tessedit_char_whitelist={_TESSERACT_WHITELIST} '
                    '-c user_defined_dpi=600'
                )
            )
            corrected = correct_text(raw)
            text_pages.append(corrected)
    # Erzeuge PDF mit erkannten Texten
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for page_text in text_pages:
        pdf.add_page()
        pdf.set_xy(10, 10)
        pdf.set_font('Arial', size=12)
        for line in page_text.splitlines():
            pdf.multi_cell(0, 10, line)
    pdf.output(str(output_pdf))
    print(f"✅ Manual OCR completed: {output_pdf.name}")


def preprocess_image(img: Image.Image) -> Image.Image:
    """
    Konvertiert Bild in Graustufen, optimiert Kontrast,
    reduziert Rauschen und wandelt in 1-Bit Schwarzweiß für OCR.
    """
    img = img.convert('L')
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    threshold = 180
    bw = img.point(lambda p: 255 if p > threshold else 0)
    return bw.convert('1')


def extract_text(pdf_path: Path) -> str:
    """
    Extrahiert Text mit pdfplumber; bei schwachem Ergebnis Fallback auf Tesseract.
    Optionale Rechtschreibkorrektur.
    """
    print(f"💬 Extracting text from {pdf_path.name}...")
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and len(text.strip()) > 50:
                corrected = correct_text(text)
                texts.append(corrected)
            else:
                pil_img = page.to_image(resolution=600).original
                img = preprocess_image(pil_img)
                raw = pytesseract.image_to_string(
                    img,
                    lang='deu',
                    config=(
                        '--oem 1 --psm 6 '
                        f'-c tessedit_char_whitelist={_TESSERACT_WHITELIST} '
                        '-c user_defined_dpi=600'
                    )
                )
                texts.append(correct_text(raw))
    combined = "\n".join(texts)
    print(f"✅ Text extraction completed ({len(combined)} chars)")
    return combined
