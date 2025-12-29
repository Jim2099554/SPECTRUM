# Script para procesar transcripciones y generar eventos de alerta en la base de datos
import sys, os, re, json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.db import SessionLocal
from backend.models.alert import AlertPhrase, AlertEvent
from backend.db_call_details import Call

TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "transcripts")
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
    # Extrae el pin del nombre de archivo: <pin>_YYYY-MM-DD_Thh-mm-ss.txt
    base = os.path.basename(filename)
    match = re.match(r"(\d+)_\d{4}-\d{2}-\d{2}_Ttranscripcion.txt", base)
    if not match:
        return None
    pin = match.group(1)
    # Busca la llamada más reciente con ese pin
    call = db.query(Call).filter_by(pin_emitter=pin).order_by(Call.timestamp.desc()).first()
    return call.id if call else None

def main():
    db = SessionLocal()
    phrases = load_phrases()
    alert_count = 0
    for fname in os.listdir(TRANSCRIPTS_DIR):
        if not fname.endswith(".txt"):
            continue
        fpath = os.path.join(TRANSCRIPTS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        call_id = get_call_id_from_filename(db, fname)
        for line in lines:
            for phrase in phrases:
                if phrase.lower() in line.lower():
                    db_phrase = get_or_create_phrase(db, phrase)
                    event = AlertEvent(
                        phrase_id=db_phrase.id,
                        transcript_snippet=line.strip(),
                        timestamp=datetime.now(),
                        call_id=call_id
                    )
                    db.add(event)
                    alert_count += 1
        db.commit()
    db.close()
    print(f"Listo. Se generaron {alert_count} eventos de alerta desde transcripciones.")

if __name__ == "__main__":
    main()
