from fastapi import FastAPI, Request
from backend.server.user_router import user_router
from backend.server.dangerous_words_router import dangerous_words_router
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
from backend.core.analysis.network_visualizer import NetworkVisualizer
from backend.core.analysis.content_analyzer import ContentAnalyzer
from backend.core.audio.cloud_transcriber import transcribe_gcs
from backend.core.licensing.license_manager import get_license_manager
import logging

logger = logging.getLogger(__name__)

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Methods'] = '*'
        return response

import multiprocessing

app = FastAPI()

# Evento de inicio: Verificar licencia USB
@app.on_event("startup")
async def startup_event():
    """Verificar licencia al iniciar la aplicación"""
    logger.info("=" * 60)
    logger.info("SENTINELA - Iniciando sistema...")
    logger.info("=" * 60)
    
    # Verificar licencia USB
    license_manager = get_license_manager()
    is_valid, message, license_data = license_manager.check_license()
    
    if is_valid:
        logger.info("✅ Licencia USB válida")
        logger.info(f"   Cliente: {license_data.get('client_name', 'N/A')}")
        logger.info(f"   Institución: {license_data.get('institution', 'N/A')}")
        logger.info(f"   Expira: {license_data.get('expiry_date', 'N/A')[:10]}")
        logger.info(f"   Usuarios máximos: {license_data.get('max_users', 'N/A')}")
    else:
        logger.warning("⚠️  " + message)
        logger.warning("   El sistema funcionará en modo limitado")
        logger.warning("   Por favor conecte el USB de licencia para acceso completo")
    
    logger.info("=" * 60)

# Rutas de gestión de usuarios
app.include_router(user_router)

# Rutas de gestión de palabras peligrosas
app.include_router(dangerous_words_router)

# Middleware CORS para desarrollo
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O restringe a ["http://localhost:5173", "http://127.0.0.1:5173", "http://127.0.0.1:62013"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from backend.server.auth_router import auth_router
from backend.core.auth.verification import router as verification_router
app.include_router(auth_router, prefix="/auth")
app.include_router(verification_router, prefix="/auth")

# Incluir el router de llamadas por día y enriquecidas
from backend.api_calls_enriched import router as calls_router
app.include_router(calls_router)

# Incluir el router de alertas
from backend.server.alert_router import router as alert_router
app.include_router(alert_router)

# Incluir el router de inmates
from backend.server.inmate_router import router as inmate_router
app.include_router(inmate_router)

# Incluir el router de análisis IA
from backend.server.ia_analysis_router import router as ia_analysis_router
app.include_router(ia_analysis_router)

# Incluir el router de huella digital
from backend.server.fingerprint_router import router as fingerprint_router
app.include_router(fingerprint_router)

# Incluir el router de reportes (transcripciones, llamadas, red de vínculos)
from backend.server.report_router import router as report_router
app.include_router(report_router)

# Incluir el router de configuración de bases de datos
from backend.server.database_config_router import router as database_config_router
app.include_router(database_config_router)

# Incluir el router de licencias USB
from backend.server.license_router import router as license_router
app.include_router(license_router)

# Montar la carpeta /client como ruta estática
import os
CLIENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "client"))
app.mount("/client", StaticFiles(directory=CLIENT_DIR), name="client")

# Montar la carpeta /photos como ruta estática para servir imágenes por PIN
PHOTOS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "photos"))
app.mount("/photos", CustomStaticFiles(directory=PHOTOS_DIR), name="photos")

# Montar archivos especiales como recursos estáticos
SPECIAL_FILES_DIR = os.path.abspath(os.path.dirname(__file__))
app.mount("/special", StaticFiles(directory=SPECIAL_FILES_DIR), name="special")

# Montar la carpeta 'frontend' como raíz para servir el frontend de React
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

# --- Endpoint provisional para servir fotos de PPL por PIN ---
from fastapi import Query, HTTPException

@app.get("/photo")
async def get_photo(pin: str = Query(...)):
    """
    Endpoint provisional para servir la foto de un PPL por su PIN desde el folder local 'photos'.
    En producción, este endpoint deberá consultar la base de datos externa para obtener el path/nombre de archivo.
    """
    import os
    from pathlib import Path
    photos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "photos"))
    # Buscar jpg o png
    import sys
    for ext in ["jpg", "png"]:
        photo_path = Path(photos_dir) / f"{pin}.{ext}"
        print(f"[PHOTO ENDPOINT] photos_dir: {photos_dir}", file=sys.stderr)
        print(f"[PHOTO ENDPOINT] Buscando: {photo_path}", file=sys.stderr)
        if photo_path.exists():
            print(f"[PHOTO ENDPOINT] ENCONTRADO: {photo_path}", file=sys.stderr)
            return FileResponse(str(photo_path), media_type=f"image/{ext}")
        else:
            print(f"[PHOTO ENDPOINT] NO ENCONTRADO: {photo_path}", file=sys.stderr)
    raise HTTPException(status_code=404, detail=f"Foto para PIN {pin} no encontrada.")

# --- Cargar modelo Whisper y frases peligrosas para fragmentos ---
import whisper
import json
from datetime import datetime
from fastapi import UploadFile, Form

WHISPER_MODEL = whisper.load_model("base")
# --- Cargar frases peligrosas desde risk_phrases_corrected.json si existe, si no usa el default ---
import os

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/risk_phrases_corrected.json"))
DEFAULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/frases_peligrosas.json"))
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        FRASES_PELIGROSAS = json.load(f)
else:
    with open(DEFAULT_PATH, "r", encoding="utf-8") as f:
        FRASES_PELIGROSAS = json.load(f)

TRANSCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../transcripts"))
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
print(f"[DEBUG] Ruta absoluta de TRANSCRIPTS_DIR: {TRANSCRIPTS_DIR}")

@app.post("/stream/fragment")
async def recibir_fragmento(file: UploadFile, pin: str = Form(...)):
    try:
        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("T%H-%M-%S")
        filename = f"{pin}_{fecha}_{hora}.wav"
        filepath = os.path.join(TRANSCRIPTS_DIR, filename)

        contents = await file.read()
        if not contents or len(contents) < 1000:
            msg = "El archivo de audio recibido está vacío o es muy pequeño."
            print(f"❌ {msg}")
            return {"error": msg}
        with open(filepath, "wb") as f:
            f.write(contents)

        # Transcribir fragmento
        try:
            result = WHISPER_MODEL.transcribe(filepath, fp16=False)
        except Exception as e:
            msg = f"Error al transcribir el fragmento: {e}"
            print(f"❌ {msg}")
            return {"error": msg}
        texto = result["text"].strip()
        idioma_detectado = result.get("language", "es")
        alertas = []
        for frase in FRASES_PELIGROSAS:
            if frase.lower() in texto.lower():
                alertas.append(frase)

        # Guardar texto e idioma en documento separado
        transcripcion_file = f"{TRANSCRIPTS_DIR}/{pin}_{fecha}_Ttranscripcion.txt"
        with open(transcripcion_file, "a", encoding="utf-8") as f:
            f.write(f"[{hora}] ({idioma_detectado}) {texto.strip()}\n")

        print(f"✅ Fragmento recibido y transcrito para PIN {pin} (idioma: {idioma_detectado})")
        if alertas:
            print(f"🚨 ALERTA detectada en fragmento: {alertas}")

        return {"text": texto, "language": idioma_detectado, "alertas": alertas}
    except Exception as e:
        msg = f"Error inesperado en el endpoint: {e}"
        print(f"❌ {msg}")
        return {"error": msg}



# Initialize analyzers
network_viz = NetworkVisualizer()
content_analyzer = ContentAnalyzer()

class Conversation(BaseModel):
    speaker1: str
    speaker2: str
    content: str

@app.post("/analyze_call")
async def analyze_call(conv: Conversation):
    # Analyze content for risks
    analysis = content_analyzer.analyze_conversation(conv.content)
    
    # Add interaction to network with risk level as weight
    risk_weight = analysis['risk_level'] / 100.0  # Normalize to 0-1
    network_viz.add_interaction(
        conv.speaker1, 
        conv.speaker2, 
        "call", 
        risk_weight,
        {
            "risk_level": analysis['risk_level'],
            "risk_factors": analysis['risk_factors'],
            "sentiment": analysis['sentiment']
        }
    )
    
    return JSONResponse({
        "analysis": analysis,
        "network_metrics": network_viz.get_network_metrics()
    })

@app.get("/", response_class=HTMLResponse)
async def root():
    # Get visualization data
    viz_data = network_viz.generate_visualization()
    
    # Create HTML with embedded Plotly and form
    html_content = f"""
    <html>
        <head>
            <title>Call Analysis Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ display: flex; gap: 20px; }}
                .form-container {{ flex: 1; }}
                .viz-container {{ flex: 2; }}
                .result-container {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>Call Analysis Dashboard</h1>
            <div class="container">
                <div class="form-container">
                    <h2>Analyze Call</h2>
                    <form id="callForm" onsubmit="analyzeCall(event)">
                        <p>
                            <label for="speaker1">Speaker 1:</label><br>
                            <input type="text" id="speaker1" required>
                        </p>
                        <p>
                            <label for="speaker2">Speaker 2:</label><br>
                            <input type="text" id="speaker2" required>
                        </p>
                        <p>
                            <label for="content">Conversation:</label><br>
                            <textarea id="content" rows="5" required></textarea>
                        </p>
                        <button type="submit">Analyze</button>
                    </form>
                    <div id="result" class="result-container"></div>
                </div>
                <div class="viz-container">
                    <h2>Network Visualization</h2>
                    <div id="graph"></div>
                </div>
            </div>
            
            <script>
                // Initial visualization
                var vizData = {json.dumps(viz_data)};
                Plotly.newPlot('graph', vizData.data, vizData.layout);
                
                async function analyzeCall(event) {{
                    event.preventDefault();
                    
                    const response = await fetch('/analyze_call', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            speaker1: document.getElementById('speaker1').value,
                            speaker2: document.getElementById('speaker2').value,
                            content: document.getElementById('content').value
                        }})
                    }});
                    
                    const data = await response.json();
                    
                    // Update result display
                    const result = document.getElementById('result');
                    result.innerHTML = `
                        <h3>Analysis Results:</h3>
                        <p>Risk Level: <strong>${data.analysis.risk_level}%</strong></p>
                        <p>Risk Factors: ${data.analysis.risk_factors.join(', ')}</p>
                        <p>Sentiment: ${data.analysis.sentiment.label} 
                           (${Math.round(data.analysis.sentiment.score * 100)}%)</p>
                    `;
                    
                    // Refresh visualization
                    location.reload();
                }}
            </script>
        </body>
    </html>
    """
    return html_content

@app.post("/api/transcribe")
async def transcribe_endpoint(request: Request):
    data = await request.json()
    gcs_uri = data.get("gcs_uri")
    alert_keywords = data.get("alert_keywords", [])
    audio_base_url = data.get("audio_base_url", None)
    # Add more parameters as needed

    segments = transcribe_gcs(
        gcs_uri=gcs_uri,
        alert_keywords=alert_keywords,
        audio_base_url=audio_base_url
    )
    if segments is None:
        return JSONResponse({"error": "Transcription failed"}, status_code=500)
    return JSONResponse({"segments": segments})

if __name__ == "__main__":
    multiprocessing.freeze_support()
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
