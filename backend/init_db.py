"""
Script de inicialización para crear todas las tablas necesarias en la base de datos SQLite
usando los modelos declarados en backend/models y backend/db_call_details.py.

Asegúrate de que la cadena de conexión sea la misma que usa tu backend.
"""
import sys
import os
from sqlalchemy import create_engine

# Permite importar backend.* aunque ejecutes desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

from backend.models.alert import Base as AlertBase
from backend.db_call_details import Base as CallBase
from backend.models.inmate import Inmate
from backend.db import Base

from backend.config import DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear todas las tablas de los modelos importados
Base.metadata.create_all(engine)

print("Tablas creadas correctamente en backend/transcripts.db")
