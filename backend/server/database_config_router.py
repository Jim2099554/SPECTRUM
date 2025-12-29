"""
Router para configuración y gestión de conexiones a bases de datos externas
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import os

router = APIRouter()

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'config/database_config.json'
)


class DatabaseConfig(BaseModel):
    required: bool
    type: str
    host: str
    port: int
    database: str
    username: str
    password: str
    tables: Dict[str, str]
    fields_mapping: Optional[Dict[str, str]] = None
    search_fields: Optional[List[str]] = None


class DatabaseConfigUpdate(BaseModel):
    databases: Dict[str, DatabaseConfig]


@router.get("/database/config")
def get_database_config():
    """Obtener configuración actual de bases de datos"""
    try:
        if not os.path.exists(CONFIG_PATH):
            return {"databases": {}}
        
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Ocultar contraseñas
        for db_name, db_config in config.get('databases', {}).items():
            if 'password' in db_config:
                db_config['password'] = '********'
        
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/database/config")
def update_database_config(config: DatabaseConfigUpdate):
    """Actualizar configuración de bases de datos"""
    try:
        # Validar que exista configuración PPL
        if 'ppl' not in config.databases:
            raise HTTPException(
                status_code=400,
                detail="La base de datos PPL es obligatoria"
            )
        
        # Guardar configuración
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config.dict(), f, indent=2, ensure_ascii=False)
        
        return {"message": "Configuración guardada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/database/test")
def test_database_connection(db_name: str, config: DatabaseConfig):
    """Probar conexión a una base de datos"""
    try:
        from backend.core.database.database_manager import DatabaseManager
        
        # Crear adaptador temporal
        manager = DatabaseManager()
        adapter = manager._create_adapter(config.dict())
        
        if not adapter:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de base de datos no soportado: {config.type}"
            )
        
        # Probar conexión
        success = adapter.test_connection()
        adapter.disconnect()
        
        if success:
            return {
                "success": True,
                "message": f"Conexión exitosa a {db_name}"
            }
        else:
            return {
                "success": False,
                "message": f"No se pudo conectar a {db_name}"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/database/status")
def get_databases_status():
    """Obtener estado de todas las conexiones"""
    try:
        from backend.core.database.database_manager import get_database_manager
        
        manager = get_database_manager()
        status = {}
        
        for db_name, adapter in manager.adapters.items():
            status[db_name] = {
                "connected": adapter.is_connected,
                "required": adapter.is_required,
                "type": adapter.config.get('type', 'unknown')
            }
        
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ppl/profile/{pin}")
def get_ppl_complete_profile(pin: str):
    """
    Obtener perfil completo de un PPL desde todas las bases de datos
    
    Este endpoint:
    1. Busca el PIN en la base de datos PPL (obligatoria)
    2. Obtiene el nombre del PPL
    3. Busca en todas las demás bases de datos usando PIN y nombre
    4. Retorna toda la información consolidada
    """
    try:
        from backend.core.database.database_manager import get_database_manager
        
        manager = get_database_manager()
        
        # Conectar si no está conectado
        if not manager.ppl_adapter or not manager.ppl_adapter.is_connected:
            manager.connect_all()
        
        # Obtener perfil completo
        profile = manager.get_complete_profile(pin)
        
        if profile['errors'] and not profile['ppl_data']:
            raise HTTPException(
                status_code=404,
                detail=f"PIN {pin} no encontrado"
            )
        
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/database/initialize")
def initialize_databases():
    """Inicializar conexiones a todas las bases de datos configuradas"""
    try:
        from backend.core.database.database_manager import get_database_manager
        
        manager = get_database_manager()
        results = manager.connect_all()
        
        # Verificar que PPL esté conectada
        if not results.get('ppl', False):
            raise HTTPException(
                status_code=500,
                detail="No se pudo conectar a la base de datos PPL (obligatoria)"
            )
        
        return {
            "message": "Bases de datos inicializadas",
            "connections": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
