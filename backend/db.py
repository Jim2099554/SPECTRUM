from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import DATABASE_URL
print(f"[DEBUG] Usando base de datos: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(Text, nullable=False)

# Dependency for FastAPI endpoints

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Run this once to initialize the DB
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
