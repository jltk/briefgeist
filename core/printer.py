import subprocess

def print_pdf(pdf_path: str):
    subprocess.run(["C:\\Path\\To\\SumatraPDF.exe", "-print-to-default", pdf_path])