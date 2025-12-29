from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class CrimeBase(BaseModel):
    crime_name: str
    description: Optional[str] = None

class CrimeRead(CrimeBase):
    id: int
    class Config:
        orm_mode = True

class InvestigationFolderBase(BaseModel):
    folder_number: str
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    penitentiary_center: Optional[str] = None
    unit: Optional[str] = None
    folder_type: Optional[str] = None
    description: Optional[str] = None
    place: Optional[str] = None
    incident_datetime: Optional[datetime] = None
    participants: Optional[Any] = None
    evidences: Optional[Any] = None
    interviews: Optional[Any] = None
    actions: Optional[Any] = None
    analysis: Optional[str] = None
    conclusions: Optional[str] = None
    recommendations: Optional[str] = None
    resolution_type: Optional[str] = None
    notifications: Optional[Any] = None
    extra_documents: Optional[Any] = None

class InvestigationFolderRead(InvestigationFolderBase):
    id: int
    pin: str
    crimes: List[CrimeRead] = []
    class Config:
        orm_mode = True
