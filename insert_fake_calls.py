import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from db_call_details import Base, Call, CallDetails
from api_calls_enriched import engine
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

pins = ["1234", "5678"]
telefonos = ["5551112222", "5553334444"]
fechas = [
    (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)
]

transcripciones = [
    "Llamada entre internos sobre fuga.",
    "Se menciona la palabra clave: 'túnel'.",
    "Conversación sobre actividades cotidianas.",
    "Discusión sobre medidas de seguridad en el penal."
]

def insert_fake_calls():
    Base.metadata.create_all(bind=engine)
    session = Session()
    try:
        for fecha in fechas:
            for _ in range(random.randint(1, 3)):
                pin = random.choice(pins)
                telefono = random.choice(telefonos)
                hora = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
                call = Call(
                    pin_emitter=pin,
                    phone_number=telefono,
                    date=fecha,
                    hora=hora
                )
                session.add(call)
                session.flush()  # Para obtener el id
                detalles = CallDetails(
                    call_id=call.id,
                    duration=str(random.randint(1, 60)),
                    participants=None,
                    transcript=random.choice(transcripciones),
                    topic=None,
                    risk_level=random.randint(0, 100),
                    risk_factors=None
                )
                session.add(detalles)
        session.commit()
        print("¡Llamadas de prueba insertadas!")
    finally:
        session.close()

if __name__ == "__main__":
    insert_fake_calls()
