# Script para procesar PDFs de transcripciones y generar eventos de alerta en la base de datos
import sys, os, re, json
from datetime import datetime
from PyPDF2 import PdfReader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.db import SessionLocal
from backend.models.alert import AlertPhrase, AlertEvent
from backend.db_call_details import Call

PDF_DIR = os.path.join(os.path.dirname(__file__), "transcripts", "pdf")
PHRASES_PATH = os.path.join(os.path.dirname(__file__), "data/risk_phrases_corrected.json")

def load_phrases():
    with open(PHRASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_or_create_phrase(db, phrase):
    db_phrase = db.query(AlertPhrase).filter_by(phrase=phrase).first()
    if not db_phrase:
        db_phrase = AlertPhrase(phrase=phrase)
        db.add(db_phrase)
        db.commit()
        db.refresh(db_phrase)
    return db_phrase

def get_call_id_from_filename(db, filename):
    # Extrae el pin, fecha y hora del nombre de archivo: <pin>_YYYY-MM-DD_Thh-mm-ss_*.pdf
    base = os.path.basename(filename)
    match = re.match(r"(\d+)_([0-9]{4}-[0-9]{2}-[0-9]{2})_T([0-9]{2}-[0-9]{2}-[0-9]{2})_.*\\.pdf", base)
    if not match:
        return None
    pin = match.group(1)
    date = match.group(2)
    hora = match.group(3).replace("-", ":")  # Ajusta a formato HH:MM:SS si es necesario
    call = db.query(Call).filter_by(pin_emitter=pin, date=date, hora=hora).first()
    return call.id if call else None

def main():
    db = SessionLocal()
    phrases = load_phrases()
    alert_count = 0
    for fname in os.listdir(PDF_DIR):
        if not fname.endswith(".pdf"):
            continue
        fpath = os.path.join(PDF_DIR, fname)
        reader = PdfReader(fpath)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        call_id = get_call_id_from_filename(db, fname)
        text_lower = text.lower()
        for phrase in phrases:
            phrase_lower = phrase.lower()
            start = 0
            while True:
                idx = text_lower.find(phrase_lower, start)
                if idx == -1:
                    break
                snippet = text[max(0, idx-40):idx+len(phrase)+40].replace("\n", " ")
                db_phrase = get_or_create_phrase(db, phrase)
                event = AlertEvent(
                    phrase_id=db_phrase.id,
                    transcript_snippet=snippet.strip(),
                    timestamp=datetime.now(),
                    call_id=call_id
                )
                db.add(event)
                alert_count += 1
                start = idx + len(phrase)
        db.commit()
    db.close()
    print(f"Listo. Se generaron {alert_count} eventos de alerta desde PDFs de transcripciones.")

if __name__ == "__main__":
    main()
