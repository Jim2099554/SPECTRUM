from backend.db_call_details import Base
from backend.db import engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente en transcripts.db")
