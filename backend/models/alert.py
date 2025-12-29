from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db import Base

class AlertPhrase(Base):
    __tablename__ = "alert_phrases"
    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AlertEvent(Base):
    __tablename__ = "alert_events"
    id = Column(Integer, primary_key=True, index=True)
    phrase_id = Column(Integer, ForeignKey("alert_phrases.id"))
    phrase = relationship("AlertPhrase")
    transcript_snippet = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    call_id = Column(String)  # o Integer si tienes modelo de llamada
