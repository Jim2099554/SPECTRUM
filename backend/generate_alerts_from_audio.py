# Script: Transcribe .wav files with Whisper and generate alert events
import os
import re
import json
import sys
from datetime import datetime
import whisper
from fpdf import FPDF
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.db import SessionLocal
from backend.models.alert import AlertPhrase, AlertEvent
from backend.db_call_details import Call

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "transcripts")
PHRASES_PATH = os.path.join(os.path.dirname(__file__), "data/risk_phrases_corrected.json")
TRANSCRIPT_PDF_DIR = os.path.join(AUDIO_DIR, "pdf_from_audio")
os.makedirs(TRANSCRIPT_PDF_DIR, exist_ok=True)

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
    # <pin>_YYYY-MM-DD_Txx-xx-xx_*.wav
    base = os.path.basename(filename)
    match = re.match(r"(\d+)_([0-9]{4}-[0-9]{2}-[0-9]{2})_T([0-9]{2}-[0-9]{2}-[0-9]{2})_.*\\.wav", base)
    if not match:
        return None
    pin = match.group(1)
    date = match.group(2)
    hora = match.group(3).replace("-", ":")
    call = db.query(Call).filter_by(pin_emitter=pin, date=date, hora=hora).first()
    return call.id if call else None

def save_transcript_pdf(transcript, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in transcript.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(pdf_path)

def main():
    db = SessionLocal()
    phrases = load_phrases()
    model = whisper.load_model("base")
    alert_count = 0
    for fname in os.listdir(AUDIO_DIR):
        if not fname.endswith(".wav"):
            continue
        fpath = os.path.join(AUDIO_DIR, fname)
        print(f"Transcribiendo {fname}...")
        result = model.transcribe(fpath, fp16=False)
        transcript = result["text"]
        print(f"Transcripción: {transcript}")
        pdf_name = fname.rsplit(".", 1)[0] + ".pdf"
        pdf_path = os.path.join(TRANSCRIPT_PDF_DIR, pdf_name)
        save_transcript_pdf(transcript, pdf_path)
        call_id = get_call_id_from_filename(db, fname)
        text_lower = transcript.lower()
        for phrase in phrases:
            phrase_lower = phrase.lower()
            start = 0
            while True:
                idx = text_lower.find(phrase_lower, start)
                if idx == -1:
                    break
                snippet = transcript[max(0, idx-40):idx+len(phrase)+40].replace("\n", " ")
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
    print(f"Listo. Se generaron {alert_count} eventos de alerta desde audios transcritos.")

if __name__ == "__main__":
    main()
