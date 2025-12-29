"""
Script para poblar las tablas alert_phrases, calls y alert_events con registros de prueba consistentes.
"""
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Permite importar backend.* aunque ejecutes desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

from backend.db_call_details import Call
from backend.models.alert import AlertPhrase, AlertEvent

DATABASE_URL = "sqlite:///backend/database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 1. Inserta una frase de alerta
alert_phrase = AlertPhrase(phrase="palabra de alerta de prueba")
session.add(alert_phrase)
session.commit()

# 2. Inserta una llamada
call = Call(
    pin_emitter="666",
    phone_number="5545678901",
    date="2025-04-10",
    hora="09:00:00"
)
session.add(call)
session.commit()

# 3. Inserta un evento de alerta asociado a los anteriores
alert_event = AlertEvent(
    phrase_id=alert_phrase.id,
    transcript_snippet="Frase de alerta detectada en la llamada",
    timestamp=datetime.now(),
    call_id=call.id
)
session.add(alert_event)
session.commit()

print(f"Registros de prueba insertados: alert_phrase_id={alert_phrase.id}, call_id={call.id}, alert_event_id={alert_event.id}")
