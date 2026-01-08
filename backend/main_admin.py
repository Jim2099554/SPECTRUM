from fastapi import FastAPI, Request
from backend.server.user_router import user_router
from backend.server.dangerous_words_router import dangerous_words_router
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import logging
import multiprocessing
import os

from backend.core.analysis.network_visualizer import NetworkVisualizer
from backend.core.analysis.content_analyzer import ContentAnalyzer
from backend.core.audio.cloud_transcriber import transcribe_gcs
from backend.core.licensing.license_manager import get_license_manager

# Importar routers adicionales para Admin
from backend.server.license_router import router as license_router
from backend.server.report_router import router as report_router
from backend.server.auth_router import auth_router
from backend.core.auth.verification import router as verification_router
from backend.api_calls_enriched import router as calls_router
from backend.server.alert_router import router as alert_router
from backend.server.inmate_router import router as inmate_router
from backend.server.ia_analysis_router import router as ia_analysis_router
from backend.server.fingerprint_router import router as fingerprint_router
from backend.server.database_config_router import router as database_config_router

logger = logging.getLogger(__name__)

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Methods'] = '*'
        return response

app = FastAPI(title="SENTINELA - Administrador Global")

# Evento de inicio: Verificar licencia USB (Obligatorio)
@app.on_event("startup")
async def startup_event():
    """Verificar licencia al iniciar la aplicación"""
    logger.info("=" * 60)
    logger.info("SENTINELA - ADMINISTRADOR GLOBAL - Iniciando sistema...")
    logger.info("=" * 60)
    
    # Verificar licencia USB
    license_manager = get_license_manager()
    is_valid, message, license_data = license_manager.check_license()
    
    if is_valid:
        logger.info("✅ Licencia USB válida detectada")
        logger.info(f"   Cliente: {license_data.get('client_name', 'N/A')}")
        logger.info(f"   Válida hasta: {license_data.get('expiry_date', 'N/A')[:10]}")
    else:
        logger.error(f"❌ ERROR DE LICENCIA: {message}")
        logger.error("   Conecte el USB del Administrador Global para continuar")
        # En modo Admin, podríamos ser más estrictos o permitir solo gestión de licencias
    
    logger.info("=" * 60)

# Incluir todos los routers
app.include_router(user_router)
app.include_router(dangerous_words_router)
app.include_router(auth_router, prefix="/auth")
app.include_router(verification_router, prefix="/auth")
app.include_router(calls_router)
app.include_router(alert_router)
app.include_router(inmate_router)
app.include_router(ia_analysis_router)
app.include_router(fingerprint_router)
app.include_router(report_router)
app.include_router(database_config_router)
app.include_router(license_router) # EL ADMIN SIEMPRE TIENE ACCESO A LICENCIAS

# Middleware CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar estáticos
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(BACKEND_DIR, "photos")
FRONTEND_DIR = os.path.abspath(os.path.join(BACKEND_DIR, "../frontend"))

app.mount("/photos", CustomStaticFiles(directory=PHOTOS_DIR), name="photos")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    import uvicorn
    uvicorn.run("backend.main_admin:app", host="0.0.0.0", port=8001, reload=False)
