# Script para crear la tabla de eventos de alerta y frases de alerta si no existen
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.db import Base, engine
from backend.models.alert import AlertPhrase, AlertEvent
from backend.db_call_details import Call  # Importa también el modelo de llamadas

if __name__ == "__main__":
    print("Creando tablas de alertas si no existen...")
    Base.metadata.create_all(bind=engine)
    print("Listo. Tablas de alertas creadas o ya existentes.")
