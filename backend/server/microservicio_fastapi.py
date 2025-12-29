from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.server.report_router import router as report_router
from backend.server.report_metadata_router import router as report_metadata_router
from backend.server.auth_router import auth_router
import traceback
from fastapi.responses import PlainTextResponse
import whisper
from datetime import datetime
import os
import json
import re
import requests
from PyPDF2 import PdfReader
import sqlite3
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montar la carpeta de audios como archivos estáticos
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audios')
os.makedirs(AUDIO_DIR, exist_ok=True)
app.mount('/audios', StaticFiles(directory=AUDIO_DIR), name='audios')

PHOTOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'photos')
os.makedirs(PHOTOS_DIR, exist_ok=True)
print('PHOTOS_DIR ABSOLUTE PATH:', PHOTOS_DIR)
print('Archivos en PHOTOS_DIR:', os.listdir(PHOTOS_DIR))
app.mount('/photos', StaticFiles(directory=PHOTOS_DIR), name='photos')

# Configuración de CORS antes de los routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"Exception occurred:\n{tb}")
    return PlainTextResponse(str(tb), status_code=500)
app.include_router(report_router)
app.include_router(report_metadata_router)
app.include_router(auth_router, prefix="/auth")
from backend.core.auth.verification import router as verification_router
app.include_router(verification_router, prefix="/auth")

from backend.server.inmate_router import router as inmate_router
app.include_router(inmate_router)

from backend.server.alert_router import router as alert_router
app.include_router(alert_router)


# =============================
# TODO: ELIMINAR ENDPOINTS DEMO EN PRODUCCIÓN
# Estos endpoints solo son útiles para pruebas del frontend local.
# =============================
from fastapi.responses import JSONResponse
from fastapi import Query

@app.get("/api/transcribe-demo.json")
async def transcribe_demo():
    # TODO: Eliminar este endpoint en producción
    return JSONResponse(content={
        "transcriptions": [
            {"id": 1, "text": "Ejemplo de transcripción 1"},
            {"id": 2, "text": "Ejemplo de transcripción 2"}
        ]
    })

@app.get("/api/new_terms-demo.json")
async def new_terms_demo():
    # TODO: Eliminar este endpoint en producción
    return JSONResponse(content={
        "terms": [
            "fuga", "escape", "contrabando"
        ]
    })

# =============================
# Endpoint: /pins (demo temporal para frontend)
# =============================
@app.get("/pins")
async def get_pins(q: str = Query(None)):
    """
    Devuelve una lista de pines de ejemplo. Si se pasa el parámetro 'q', filtra los pines cuyo nombre o descripción contenga 'q'.
    """
    fake_pins = [
        {"id": 1, "name": "Pin 123", "desc": "Llamada entre Juan y María"},
        {"id": 2, "name": "Pin 456", "desc": "Llamada entre Pedro y Ana"},
        {"id": 3, "name": "Pin 789", "desc": "Llamada entre Luis y Sofía"},
    ]
    if q:
        filtered = [pin for pin in fake_pins if q in pin["name"] or q in pin["desc"]]
        return JSONResponse(content=filtered)
    return JSONResponse(content=fake_pins)

# Endpoint: /llamadas-por-dia
@app.get("/llamadas-por-dia")
async def llamadas_por_dia(pin: str = Query(...)):
    """
    Devuelve el número de llamadas por día para un PIN específico.
    Formato de respuesta: [{"date": "2025-04-01", "count": 2}, ...]
    """
    conn = sqlite3.connect("transcripts.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, COUNT(*) as count
        FROM calls
        WHERE pin_emitter = ?
        GROUP BY date
        ORDER BY date
    """, (pin,))
    rows = cursor.fetchall()
    conn.close()
    # Siempre devolver un array de objetos
    result = [{"fecha": row[0], "llamadas": row[1]} for row in rows]
    return JSONResponse(content=result)


# Endpoint: /api/ollama/query
@app.post("/api/ollama/query")
async def ollama_query(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    transcripts_dir = "transcripts"
    pdfs = [f for f in os.listdir(transcripts_dir) if f.endswith('_reporte.pdf')]
    filtros = []
    context = ""

    # Detectar criterios
    pin_match = re.search(r'\b\d{3,}\b', prompt)
    mes_match = re.search(r'(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|\b0[1-9]|1[0-2]\b)', prompt, re.IGNORECASE)
    anio_match = re.search(r'\b20\d{2}\b', prompt)
    dia_match = re.search(r'\b([12][0-9]|3[01]|0[1-9])\b', prompt)
    tel_match = re.search(r'\+?\d{10,}', prompt)
    nombre_match = re.search(r'(Juan|María|Pedro|Pérez|López|Doña Mari|El Chino|El Ingeniero|El Primo|La Tía|La Güera)', prompt, re.IGNORECASE)

    # Filtrar por PIN (más flexible: cualquier archivo que contenga el PIN y termine en _reporte.pdf)
    if pin_match:
        pin = pin_match.group(0)
        pdfs = [f for f in pdfs if pin in f and f.endswith('_reporte.pdf')]
        filtros.append(f"PIN {pin}")
    # Filtrar por año
    if anio_match:
        anio = anio_match.group(0)
        pdfs = [f for f in pdfs if f"_{anio}-" in f]
        filtros.append(f"año {anio}")
    # Filtrar por mes (número o nombre)
    if mes_match:
        mes = mes_match.group(0)
        meses = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06", "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"}
        mes_num = meses.get(mes.lower(), mes.zfill(2)) if not mes.isdigit() else mes.zfill(2)
        pdfs = [f for f in pdfs if re.search(rf"_\d{{4}}-{mes_num}-\d{{2}}_", f)]
        filtros.append(f"mes {mes}")
    # Filtrar por día
    if dia_match:
        dia = dia_match.group(0).zfill(2)
        pdfs = [f for f in pdfs if re.search(rf"_\d{{4}}-\d{{2}}-{dia}_", f)]
        filtros.append(f"día {dia}")
    # Filtrar por número telefónico
    if tel_match:
        tel = tel_match.group(0)
        # Buscar PDFs que contengan el teléfono en el texto
        pdfs_tel = []
        for f in pdfs:
            try:
                reader = PdfReader(os.path.join(transcripts_dir, f))
                texto = " ".join([p.extract_text() or "" for p in reader.pages])
                if tel in texto:
                    pdfs_tel.append(f)
            except Exception:
                continue
        pdfs = pdfs_tel
        filtros.append(f"teléfono {tel}")
    # Filtrar por nombre
    if nombre_match:
        nombre = nombre_match.group(0)
        pdfs_nombre = []
        for f in pdfs:
            try:
                reader = PdfReader(os.path.join(transcripts_dir, f))
                texto = " ".join([p.extract_text() or "" for p in reader.pages])
                if nombre.lower() in texto.lower():
                    pdfs_nombre.append(f)
            except Exception:
                continue
        pdfs = pdfs_nombre
        filtros.append(f"nombre {nombre}")

    # Extraer contexto
    if pdfs:
        for f in sorted(pdfs):
            try:
                reader = PdfReader(os.path.join(transcripts_dir, f))
                context += f"\n--- CONTENIDO DE {f} ---\n"
                for page in reader.pages:
                    context += page.extract_text() + "\n"
            except Exception as e:
                context += f"[Error leyendo PDF {f}: {e}]\n"
    else:
        context = f"[No se encontró reporte PDF para los criterios: {', '.join(filtros) if filtros else 'ninguno'}]"

    # Instrucciones explícitas para el modelo
    instrucciones = (
        "Eres un asistente experto en análisis de llamadas y reportes policiales. "
        "Puedes responder preguntas sobre nombres, personas, parentescos, relaciones, fechas, lugares, cantidades, objetos, "
        "palabras clave relacionadas con delitos y hacer resúmenes o identificar temas principales. "
        "Si la pregunta no se relaciona con el contenido del reporte, responde educadamente que no hay información."
    )
    ejemplos = (
        "Ejemplo 1:\n"
        "Pregunta: ¿Qué personas participaron en la llamada con PIN 1234?\n"
        "Respuesta: En la llamada con PIN 1234 participaron Juan Pérez y María López.\n\n"
        "Ejemplo 2:\n"
        "Pregunta: ¿Cuánto dinero se mencionó en la llamada con PIN 555?\n"
        "Respuesta: Se mencionó una cantidad de $10,000 pesos.\n\n"
        "Ejemplo 3:\n"
        "Pregunta: ¿Qué lugares aparecen en la llamada del 10 de abril?\n"
        "Respuesta: Se mencionaron los lugares 'La Central' y 'Oficina principal'.\n\n"
        "Ejemplo 4:\n"
        "Pregunta: ¿Qué parentesco hay entre los participantes de la llamada con PIN 789?\n"
        "Respuesta: María López es madre de Juan Pérez.\n\n"
        "Ejemplo 5:\n"
        "Pregunta: ¿Se mencionó alguna palabra relacionada con delitos en la llamada con PIN 999?\n"
        "Respuesta: Sí, se mencionaron las palabras 'droga' y 'peligro'.\n\n"
        "Ejemplo 6:\n"
        "Pregunta: Hazme un resumen de la llamada del 10 de abril.\n"
        "Respuesta: La llamada trató sobre la coordinación de una entrega y la participación de varios involucrados.\n\n"
    )
    contexto_extra = f"Contexto extraído de los reportes filtrados ({', '.join(filtros) if filtros else 'todos'}):\n" + context
    full_prompt = f"{instrucciones}\n\n{ejemplos}\n{contexto_extra}\nPregunta: {prompt}"
    try:
        print("Prompt enviado a Ollama:\n", full_prompt)
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": full_prompt, "stream": False}
        )
        print("Respuesta cruda de Ollama:", response.text)
        answer = response.json().get("response", "No se pudo obtener respuesta.")
    except Exception as e:
        print("Error consultando Ollama:", e)
        answer = f"Error consultando Ollama: {e}"
    return {"response": answer}

# Cargar modelo Whisper
model = whisper.load_model("base")  # Puedes usar "tiny" para que sea más rápido

# Cargar frases peligrosas
with open("config/frases_peligrosas.json", "r", encoding="utf-8") as f:
    FRASES_PELIGROSAS = json.load(f)

# Carpeta donde guardar transcripciones
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

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
            result = model.transcribe(filepath, fp16=False)
        except Exception as e:
            msg = f"Error al transcribir el fragmento: {e}"
            print(f"❌ {msg}")
            return {"error": msg}
        texto = result.get("text", "")

        # Analizar si hay frases de riesgo
        alertas = []
        for frase in FRASES_PELIGROSAS:
            if frase.lower() in texto.lower():
                alertas.append(frase)

        # Guardar texto en documento separado
        transcripcion_file = f"{TRANSCRIPTS_DIR}/{pin}_{fecha}_Ttranscripcion.txt"
        with open(transcripcion_file, "a", encoding="utf-8") as f:
            f.write(f"[{hora}] {texto.strip()}\n")

        print(f"✅ Fragmento recibido y transcrito para PIN {pin}")
        if alertas:
            print(f"🚨 ALERTA detectada en fragmento: {alertas}")

        return {"text": texto, "alertas": alertas}
    except Exception as e:
        msg = f"Error inesperado en el endpoint: {e}"
        print(f"❌ {msg}")
        return {"error": msg}
