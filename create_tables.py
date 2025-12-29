import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from db_call_details import Base
from api_calls_enriched import engine

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(engine)
    print("¡Listo! Tablas creadas si no existían.")
