# Script para migrar todos los .txt de transcripts a PDF
import os
from fpdf import FPDF

TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "transcripts")
PDF_DIR = os.path.join(TRANSCRIPTS_DIR, "pdf")
os.makedirs(PDF_DIR, exist_ok=True)

def txt_to_pdf(txt_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            pdf.multi_cell(0, 10, line.strip())
    pdf.output(pdf_path)

for fname in os.listdir(TRANSCRIPTS_DIR):
    if fname.endswith(".txt"):
        txt_path = os.path.join(TRANSCRIPTS_DIR, fname)
        pdf_name = fname.rsplit(".", 1)[0] + ".pdf"
        pdf_path = os.path.join(PDF_DIR, pdf_name)
        txt_to_pdf(txt_path, pdf_path)
        print(f"Convertido: {fname} -> {pdf_name}")

print("Migración a PDF completada. Los archivos están en:", PDF_DIR)
