from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models.inmate import Inmate
from pydantic import BaseModel

router = APIRouter(prefix="/fingerprint", tags=["Fingerprint"])

class FingerprintRegisterRequest(BaseModel):
    pin: str
    fingerprint_template: str  # Puede ser base64 o string generado por el SDK

class FingerprintVerifyRequest(BaseModel):
    pin: str
    fingerprint_template: str

@router.post("/register")
def register_fingerprint(data: FingerprintRegisterRequest, db: Session = Depends(get_db)):
    inmate = db.query(Inmate).filter(Inmate.pin == data.pin).first()
    if not inmate:
        raise HTTPException(status_code=404, detail="PPL no encontrado")
    inmate.fingerprint_template = data.fingerprint_template
    db.commit()
    return {"status": "registered"}

@router.post("/verify")
def verify_fingerprint(data: FingerprintVerifyRequest, db: Session = Depends(get_db)):
    inmate = db.query(Inmate).filter(Inmate.pin == data.pin).first()
    if not inmate or not inmate.fingerprint_template:
        raise HTTPException(status_code=404, detail="PPL o huella no encontrada")
    # Aquí se debería usar el SDK real para comparar la huella recibida con la almacenada
    # Por ahora, simulamos una coincidencia exacta para pruebas
    if data.fingerprint_template == inmate.fingerprint_template:
        return {"status": "verified"}
    else:
        raise HTTPException(status_code=401, detail="Huella no coincide")
