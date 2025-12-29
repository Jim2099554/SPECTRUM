# Script para agregar un PPL de prueba con pin=666 a la base de datos
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

try:
    from backend.models.inmate import Inmate
    from backend.db import Base
except ModuleNotFoundError:
    # Imports relativos para ejecución directa de script
    from models.inmate import Inmate
    from db import Base

# Ajusta la ruta de la base de datos si es necesario
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../transcripts.db'))
engine = create_engine(f'sqlite:///{db_path}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cambia estos datos si lo deseas
def main():
    session = SessionLocal()
    try:
        # Verifica si ya existe
        existing = session.query(Inmate).filter(Inmate.pin == '666').first()
        if existing:
            print('Eliminando registro previo con pin=666...')
            session.delete(existing)
            session.commit()
        inmate = Inmate(
            pin='666',
            photo_filename='666.jpg',  # Ahora apunta a la foto real
            status='Activo',
            crime='Robo',
            upload_date=datetime.utcnow()
        )
        session.add(inmate)
        session.commit()
        print('PPL con pin=666 agregado exitosamente')
    finally:
        session.close()

if __name__ == '__main__':
    main()
