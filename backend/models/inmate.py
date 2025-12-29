from sqlalchemy import Column, Integer, String, DateTime
from backend.db import Base
from datetime import datetime

class Inmate(Base):
    __tablename__ = "inmates"
    id = Column(Integer, primary_key=True, index=True)
    pin = Column(String, unique=True, index=True, nullable=False)
    photo_filename = Column(String, nullable=False)
    status = Column(String, nullable=False)
    crime = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    fingerprint_template = Column(String, nullable=True)  # Plantilla biométrica de la huella digital
