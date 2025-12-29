from backend.db import Transcript, SessionLocal, Base, engine

# Demo transcripts to insert
TRANSCRIPTS = [
    "Llamada entre internos sobre fuga.",
    "Se menciona la palabra clave: 'túnel'.",
    "Conversación sobre actividades cotidianas.",
    "Discusión sobre medidas de seguridad en el penal."
]

def insert_demo_transcripts():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for text in TRANSCRIPTS:
            transcript = Transcript(transcript=text)
            db.add(transcript)
        db.commit()
        print(f"Inserted {len(TRANSCRIPTS)} demo transcripts.")
    finally:
        db.close()
if __name__ == "__main__":
    insert_demo_transcripts()
