from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models.inmate import Inmate
from backend.schemas.inmate import InmateResponse
from backend.models.investigation_folder import InvestigationFolder
from backend.schemas.investigation_folder import InvestigationFolderRead

router = APIRouter(prefix="/inmates", tags=["inmates"])

@router.get("/{pin}", response_model=InmateResponse)
def get_inmate(pin: str, db: Session = Depends(get_db)):
    inmate = db.query(Inmate).filter(Inmate.pin == pin).first()
    if not inmate:
        raise HTTPException(status_code=404, detail="Inmate not found")
    # Obtener carpetas de investigación y delitos asociados
    folders = db.query(InvestigationFolder).filter(InvestigationFolder.pin == pin).all()
    folders_data = [InvestigationFolderRead.from_orm(folder) for folder in folders]
    # Convertir inmate a dict y agregar folders
    inmate_data = inmate.__dict__.copy()
    inmate_data['investigation_folders'] = folders_data
    return inmate_data
