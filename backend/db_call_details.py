from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from backend.db import Base
from sqlalchemy.types import JSON
from datetime import datetime

# Modelo mínimo solo para migración
class Call(Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True)
    pin_emitter = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    date = Column(String, nullable=False)
    hora = Column(String, nullable=True)

class CallDetails(Base):
    __tablename__ = "call_details"
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=False, unique=True)
    duration = Column(String, nullable=True)
    participants = Column(JSON, nullable=True)  # [{"role": "emisor", "nombre": "", "numero": ""}, ...]
    transcript = Column(Text, nullable=True)
    topic = Column(String, nullable=True)
    risk_level = Column(Integer, nullable=True)
    risk_factors = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
