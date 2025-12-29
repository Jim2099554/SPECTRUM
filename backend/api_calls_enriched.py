from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db_call_details import Base, CallDetails, Call
import os

import os
from backend.config import DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

router = APIRouter()

from fastapi import Request

@router.get("/llamadas-por-dia")
def llamadas_por_dia(pin: Optional[str] = Query(None)):
    session = Session()
    from sqlalchemy import func
    q = session.query(Call.date, func.count(Call.id))
    if pin:
        q = q.filter(Call.pin_emitter == pin)
    q = q.group_by(Call.date).order_by(Call.date)
    results = [
        {"fecha": row[0], "llamadas": row[1]} for row in q.all()
    ]
    session.close()
    return results

# --- NUEVO ENDPOINT PARA LLAMADAS POR PIN ---

@router.get("/llamadas")
def get_llamadas_by_pin(pin: str):
    session = Session()
    # Buscar llamadas por PIN
    q = session.query(Call, CallDetails).join(CallDetails, Call.id == CallDetails.call_id)
    q = q.filter(Call.pin_emitter == pin)
    q = q.order_by(Call.date.desc())
    results = []
    for call, details in q.all():
        # Construir nombre base para archivos
        base_name = f"{call.pin_emitter}_{call.date}"
        if call.hora:
            base_name += f"_{call.hora}"
        # Buscar archivos en /client/
        audio_path = f"/client/{base_name}.wav"
        pdf_path = f"/client/{base_name}.pdf"
        # Si no existen, poner None
        audio_url = audio_path if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), f"../{audio_path}"))) else None
        pdf_url = pdf_path if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), f"../{pdf_path}"))) else None
        # Resumen: usar los primeros 200 caracteres de la transcripción como ejemplo
        resumen = (details.transcript[:200] + "...") if details.transcript else None
        results.append({
            "id": call.id,
            "fecha": call.date,
            "hora": call.hora,
            "duracion": details.duration,
            "telefono": call.phone_number,
            "resumen": resumen,
            "pdf_url": pdf_url,
            "audio_url": audio_url
        })
    session.close()
    return JSONResponse(content={"llamadas": results})

@router.get("/api/calls/enriched")
def get_enriched_calls(
    pin_emitter: Optional[str] = Query(None),
    phone_number: Optional[str] = Query(None),
    min_risk: Optional[int] = Query(None),
    max_risk: Optional[int] = Query(None),
    limit: int = Query(50, gt=0, le=200),
):
    session = Session()
    q = session.query(Call, CallDetails).join(CallDetails, Call.id == CallDetails.call_id)
    if pin_emitter:
        q = q.filter(Call.pin_emitter == pin_emitter)
    if phone_number:
        q = q.filter(Call.phone_number == phone_number)
    if min_risk is not None:
        q = q.filter(CallDetails.risk_level >= min_risk)
    if max_risk is not None:
        q = q.filter(CallDetails.risk_level <= max_risk)
    q = q.order_by(CallDetails.created_at.desc()).limit(limit)

    results = []
    for call, details in q.all():
        results.append({
            "id": call.id,
            "pin_emitter": call.pin_emitter,
            "phone_number": call.phone_number,
            "date": call.date,
            "hora": call.hora,
            "duration": details.duration,
            "participants": details.participants,
            "transcript": details.transcript,
            "topic": details.topic,
            "risk_level": details.risk_level,
            "risk_factors": details.risk_factors,
            "created_at": details.created_at,
        })
    session.close()
    return {"calls": results}
