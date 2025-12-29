from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from backend.db import Base
from datetime import datetime

class InvestigationFolder(Base):
    __tablename__ = "investigation_folders"
    id = Column(Integer, primary_key=True, index=True)
    pin = Column(String, index=True)  # Relaciona con Inmate.pin
    folder_number = Column(String, nullable=False)
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    penitentiary_center = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    folder_type = Column(String, nullable=True)  # administrativa, penal, etc.
    description = Column(Text, nullable=True)
    place = Column(String, nullable=True)
    incident_datetime = Column(DateTime, nullable=True)
    participants = Column(JSON, nullable=True)
    evidences = Column(JSON, nullable=True)
    interviews = Column(JSON, nullable=True)
    actions = Column(JSON, nullable=True)
    analysis = Column(Text, nullable=True)
    conclusions = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    resolution_type = Column(String, nullable=True)
    notifications = Column(JSON, nullable=True)
    extra_documents = Column(JSON, nullable=True)
    crimes = relationship("Crime", back_populates="folder")

class Crime(Base):
    __tablename__ = "crimes"
    id = Column(Integer, primary_key=True, index=True)
    folder_id = Column(Integer, ForeignKey("investigation_folders.id"))
    crime_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    folder = relationship("InvestigationFolder", back_populates="crimes")
