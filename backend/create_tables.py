from backend.db_call_details import Base
from backend.api_calls_enriched import engine

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(engine)
    print("¡Listo! Tablas creadas si no existían.")
