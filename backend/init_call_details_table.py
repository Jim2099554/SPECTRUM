from sqlalchemy import create_engine
from db_call_details import Base

# Ajusta el path si tu DB está en otra ubicación
DATABASE_URL = "sqlite:///../transcripts.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabla call_details creada o ya existente.")
