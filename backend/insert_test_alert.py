"""
Script para insertar un registro de prueba en las tablas 'calls' y 'alert_events'.
"""
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Permite importar backend.* aunque ejecutes desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

from backend.db_call_details import Call
from backend.models.alert import AlertEvent

DATABASE_URL = "sqlite:///backend/database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Insertar una llamada de prueba
call = Call(
    pin_emitter="666",
    phone_number="5545678901",
    date="2025-04-10",
    hora="09:00:00"
)
session.add(call)
session.commit()

# Insertar un evento de alerta de prueba
alert_event = AlertEvent(
    phrase_id=1,  # Debes asegurarte de que exista una frase con id=1, o ajusta este valor
    transcript_snippet="Frase de alerta detectada en la llamada",
    timestamp=datetime.now(),
    call_id=call.id
)
session.add(alert_event)
session.commit()

print(f"Registro de prueba insertado: call_id={call.id}, alert_event_id={alert_event.id}")
