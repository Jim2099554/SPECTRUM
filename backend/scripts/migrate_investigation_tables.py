"""
Script universal de migración para crear las tablas InvestigationFolder y Crime en la base de datos configurada.
Funciona con SQLite, MySQL, PostgreSQL, etc. según la cadena de conexión en backend/db.py.
"""
import sys
import os
from sqlalchemy import create_engine
from backend.models.investigation_folder import InvestigationFolder, Crime
from backend.db import Base

# Permite importar backend.* aunque ejecutes desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

# Usa la cadena de conexión definida en backend/db.py
from backend.db import engine

if __name__ == "__main__":
    print("Creando tablas InvestigationFolder y Crime...")
    Base.metadata.create_all(engine)
    print("¡Tablas creadas correctamente!")
