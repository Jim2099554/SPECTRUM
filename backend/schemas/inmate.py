from pydantic import BaseModel
from datetime import datetime

class InmateBase(BaseModel):
    id: int
    pin: str
    photo_filename: str
    status: str
    crime: str
    upload_date: datetime
    fingerprint_template: str | None = None  # Plantilla biométrica opcional

class InmateResponse(InmateBase):
    class Config:
        orm_mode = True
