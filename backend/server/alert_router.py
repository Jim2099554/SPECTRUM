from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models.alert import AlertPhrase, AlertEvent
from backend.schemas.alert import (
    AlertPhraseCreate, AlertPhraseRead,
    AlertEventCreate, AlertEventRead
)

router = APIRouter(prefix="/alerts", tags=["alerts"])

# CRUD para frases de alerta
@router.post("/phrases/", response_model=AlertPhraseRead)
def create_alert_phrase(phrase: AlertPhraseCreate, db: Session = Depends(get_db)):
    db_phrase = AlertPhrase(phrase=phrase.phrase)
    db.add(db_phrase)
    db.commit()
    db.refresh(db_phrase)
    return db_phrase

@router.get("/phrases/", response_model=list[AlertPhraseRead])
def list_alert_phrases(db: Session = Depends(get_db)):
    return db.query(AlertPhrase).all()

@router.delete("/phrases/{phrase_id}", response_model=dict)
def delete_alert_phrase(phrase_id: int, db: Session = Depends(get_db)):
    phrase = db.query(AlertPhrase).get(phrase_id)
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    db.delete(phrase)
    db.commit()
    return {"ok": True}

# CRUD para eventos de alerta
@router.post("/events/", response_model=AlertEventRead)
def create_alert_event(event: AlertEventCreate, db: Session = Depends(get_db)):
    db_event = AlertEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

from fastapi import Query

@router.get("/events/", response_model=list[AlertEventRead])
def list_alert_events(pin: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(AlertEvent)
    if pin:
        # Suponiendo que AlertEvent tiene un campo call_id y Call tiene pin_emitter
        from backend.db_call_details import Call
        query = query.join(Call, AlertEvent.call_id == Call.id).filter(Call.pin_emitter == pin)
    return query.order_by(AlertEvent.timestamp.desc()).all()
