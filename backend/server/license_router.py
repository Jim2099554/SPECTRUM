"""
Router de API para gestión de licencias USB
"""

from fastapi import APIRouter, HTTPException
from backend.core.licensing.license_manager import get_license_manager

router = APIRouter()


@router.get("/license/status")
def get_license_status():
    """
    Obtener estado actual de la licencia
    """
    manager = get_license_manager()
    
    # Verificar licencia
    is_valid, message, license_data = manager.check_license()
    
    if not is_valid:
        return {
            "valid": False,
            "message": message,
            "requires_usb": True
        }
    
    return {
        "valid": True,
        "message": "Licencia válida",
        "license_info": manager.get_license_info()
    }


@router.get("/license/info")
def get_license_info():
    """
    Obtener información detallada de la licencia actual
    """
    manager = get_license_manager()
    
    if not manager.is_valid:
        raise HTTPException(
            status_code=403,
            detail="No hay licencia válida. Por favor conecte el USB de licencia."
        )
    
    return manager.get_license_info()


@router.post("/license/verify")
def verify_license():
    """
    Forzar verificación de licencia
    """
    manager = get_license_manager()
    is_valid, message, license_data = manager.check_license()
    
    if not is_valid:
        raise HTTPException(status_code=403, detail=message)
    
    return {
        "valid": True,
        "message": message,
        "license_info": manager.get_license_info()
    }


@router.get("/license/monitor")
def monitor_usb():
    """
    Verificar que el USB de licencia siga conectado
    """
    manager = get_license_manager()
    
    if not manager.is_valid:
        return {
            "connected": False,
            "message": "No hay licencia cargada"
        }
    
    is_connected = manager.monitor_usb()
    
    if not is_connected:
        manager.is_valid = False
        return {
            "connected": False,
            "message": "USB de licencia desconectado. Por favor reconecte el USB."
        }
    
    return {
        "connected": True,
        "message": "USB de licencia conectado"
    }
