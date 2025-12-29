"""
Script para importar carpetas de investigación y delitos desde un archivo Excel a la base de datos definida en backend/db.py.
Funciona con cualquier motor SQL soportado por SQLAlchemy.
"""
import sys
import os
import pandas as pd
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from backend.db import SessionLocal
from backend.models.investigation_folder import InvestigationFolder, Crime

EXCEL_FILE = "investigations_example.xlsx"

if __name__ == "__main__":
    df = pd.read_excel(EXCEL_FILE)
    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            folder = InvestigationFolder(
                pin=row['pin'],
                folder_number=row['folder_number'],
                opened_at=row.get('opened_at'),
                closed_at=row.get('closed_at'),
                penitentiary_center=row.get('penitentiary_center'),
                unit=row.get('unit'),
                folder_type=row.get('folder_type'),
                description=row.get('description'),
                place=row.get('place'),
                incident_datetime=row.get('incident_datetime'),
                participants=row.get('participants'),
                evidences=row.get('evidences'),
                interviews=row.get('interviews'),
                actions=row.get('actions'),
                analysis=row.get('analysis'),
                conclusions=row.get('conclusions'),
                recommendations=row.get('recommendations'),
                resolution_type=row.get('resolution_type'),
                notifications=row.get('notifications'),
                extra_documents=row.get('extra_documents'),
            )
            session.add(folder)
            session.flush()  # Para obtener el id del folder
            # Delitos: espera una columna 'crimes' como lista de diccionarios
            crimes = row.get('crimes', [])
            if crimes and isinstance(crimes, list):
                for crime in crimes:
                    c = Crime(
                        folder_id=folder.id,
                        crime_name=crime.get('crime_name', ''),
                        description=crime.get('description', '')
                    )
                    session.add(c)
        session.commit()
        print("¡Importación completada!")
    except Exception as e:
        print(f"Error durante la importación: {e}")
        session.rollback()
    finally:
        session.close()
