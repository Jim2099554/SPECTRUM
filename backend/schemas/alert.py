from pydantic import BaseModel
from datetime import datetime

class AlertPhraseBase(BaseModel):
    phrase: str

class AlertPhraseCreate(AlertPhraseBase):
    pass

class AlertPhraseRead(AlertPhraseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AlertEventBase(BaseModel):
    phrase_id: int
    transcript_snippet: str
    call_id: str

class AlertEventCreate(AlertEventBase):
    pass

class AlertEventRead(AlertEventBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
