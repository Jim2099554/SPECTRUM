import os
import sys
import sqlite3
import re
import requests  # Para notificar al WebSocket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
import time
from sqlalchemy.exc import OperationalError

# Permitir importar backend.db_call_details desde el root del proyecto
from backend.db_call_details import Base, CallDetails

# Configuración
TRANSCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../transcripts'))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../transcripts.db'))

# Regex mejorado para extraer PIN, fecha y opcionalmente hora del nombre de archivo
FILENAME_REGEX = re.compile(r'^(?P<pin>\d+)_(?P<date>\d{4}-\d{2}-\d{2})(?:_T(?P<hora>\d{2}-\d{2}-\d{2}))?.*')

def main():
    # Crear la tabla antes de cualquier consulta
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pin_emitter TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            date TEXT NOT NULL,
            hora TEXT
        )
    ''')
    conn.commit()

    archivos = os.listdir(TRANSCRIPTS_DIR)
    llamadas_unicas = set()
    # Preparar SQLAlchemy para call_details (usar ruta absoluta)
    engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)

    for nombre in archivos:
        match = FILENAME_REGEX.match(nombre)
        if match:
            pin = match.group('pin')
            date = match.group('date')
            hora = match.group('hora') if match.group('hora') else None
            # Extraer número de teléfono del nombre o archivo (simulado aquí)
            phone_number = ""
            phone_match = re.search(r'(\d{10,})', nombre)
            if phone_match:
                phone_number = phone_match.group(1)
            else:
                phone_number = "0000000000"

            # Verificar si ya existe la llamada
            cursor.execute('''
                SELECT id FROM calls WHERE pin_emitter = ? AND phone_number = ? AND date = ? AND (hora IS ? OR hora = ?)
            ''', (pin, phone_number, date, hora if hora else None, hora))
            call_row = cursor.fetchone()
            if not call_row:
                cursor.execute('''
                    INSERT INTO calls (pin_emitter, phone_number, date, hora) VALUES (?, ?, ?, ?)
                ''', (pin, phone_number, date, hora))
                call_id = cursor.lastrowid
                # Notificar al WebSocket que hay una nueva llamada
                try:
                    requests.post("http://localhost:8001/notify_new_call", timeout=1)
                except Exception as e:
                    print(f"[WARN] No se pudo notificar al WebSocket: {e}")
            else:
                call_id = call_row[0]

            # --- Enriquecer y poblar call_details ---
            # Leer transcripción si existe
            transcript_path = os.path.join(TRANSCRIPTS_DIR, nombre)
            transcript_text = ""
            if os.path.isfile(transcript_path):
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    transcript_text = f.read()

            # Simular duración y participantes
            duration = "00:02:30"  # Simulado, puedes extraerlo si tienes el dato
            participants = [
                {"role": "emisor", "nombre": f"PIN {pin}", "numero": pin},
                {"role": "receptor", "nombre": "Desconocido", "numero": phone_number}
            ]

            # Detectar tema y riesgo
            topic = None
            risk_level = 0
            risk_factors = []
            # Palabras clave de riesgo (puedes cargar desde JSON)
            palabras_riesgo = ["fraude", "transferencia", "depósito", "hazle como si fuera oficial", "cuenta", "dinero"]
            for palabra in palabras_riesgo:
                if palabra in transcript_text.lower():
                    risk_factors.append(palabra)
            if risk_factors:
                risk_level = 80  # Simulado: alto si hay match
                topic = "fraude financiero"
            else:
                risk_level = 10  # Bajo
                topic = "conversación general"

            # Insertar en call_details solo si no existe
            session = Session()
            try:
                exists = session.query(CallDetails).filter_by(call_id=call_id).first()
                if not exists:
                    call_details = CallDetails(
                        call_id=call_id,
                        duration=duration,
                        participants=participants,
                        transcript=transcript_text,
                        topic=topic,
                        risk_level=risk_level,
                        risk_factors=risk_factors,
                        created_at=datetime.utcnow()
                    )
                    # Intentar commit con reintentos si la base está bloqueada
                    for intento in range(5):
                        try:
                            session.add(call_details)
                            session.commit()
                            print(f"[INFO] Insertado detalle para call_id={call_id}")
                            break
                        except OperationalError as e:
                            if 'database is locked' in str(e):
                                print(f"[WARN] DB locked, reintentando ({intento+1}/5)...")
                                time.sleep(0.2)
                                session.rollback()
                            else:
                                raise
                    # Pequeño retardo para evitar lock
                    time.sleep(0.1)
            except Exception as e:
                print(f"[ERROR] Falló la inserción de detalles para call_id={call_id}: {e}")
            finally:
                session.close()
    conn.commit()
    print(f"Sincronizados {len(llamadas_unicas)} llamadas únicas desde archivos de /transcripts a tabla calls.")
    conn.close()

if __name__ == "__main__":
    main()
