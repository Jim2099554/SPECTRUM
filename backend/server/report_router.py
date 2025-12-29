from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.app.services.topic_reporter import extract_main_topic, summarize_text
from fpdf import FPDF
import os

router = APIRouter()

@router.get("/network")
def get_network(pin: str = Query(...)):
    """
    Devuelve la red de vínculos de un PIN: nodos (contactos) y enlaces (llamadas).
    Agrupa contactos por identidad (nombre/alias) cuando está disponible.
    """
    import sqlite3
    from collections import defaultdict
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "transcripts.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todos los contactos únicos y contar llamadas
        cursor.execute("""
            SELECT phone_number, COUNT(*) as call_count
            FROM calls
            WHERE pin_emitter = ?
            GROUP BY phone_number
            ORDER BY call_count DESC
        """, (pin,))
        
        contacts = cursor.fetchall()
        
        # Intentar obtener identidades de la tabla contacts
        cursor.execute("""
            SELECT phone_number, identity_name, alias
            FROM contacts
        """)
        
        identities_map = {}
        for phone, name, alias in cursor.fetchall():
            identities_map[phone] = {
                "name": name,
                "alias": alias
            }
        
        conn.close()
        
        # Agrupar contactos por identidad
        # Si múltiples números tienen el mismo nombre/alias, se agrupan en un solo nodo
        identity_groups = defaultdict(lambda: {
            "phones": [],
            "call_count": 0,
            "identity": None,
            "alias": None
        })
        
        for phone_number, call_count in contacts:
            # Buscar identidad del contacto
            identity_info = identities_map.get(phone_number, {})
            identity_name = identity_info.get("name")
            identity_alias = identity_info.get("alias")
            
            # Clave de agrupación: usar nombre/alias si existe, sino el número
            group_key = identity_name or identity_alias or phone_number
            
            identity_groups[group_key]["phones"].append(phone_number)
            identity_groups[group_key]["call_count"] += call_count
            identity_groups[group_key]["identity"] = identity_name
            identity_groups[group_key]["alias"] = identity_alias
        
        # Construir nodos y enlaces
        nodes = [{"id": pin, "label": f"PIN {pin}", "color": "red", "type": "pin"}]
        links = []
        
        for group_key, group_data in identity_groups.items():
            # Determinar etiqueta del nodo
            if group_data["identity"]:
                label = group_data["identity"]
                if group_data["alias"]:
                    label += f' "{group_data["alias"]}"'
            elif group_data["alias"]:
                label = group_data["alias"]
            else:
                # Solo número de teléfono
                label = group_key
            
            # Si hay múltiples números, agregar info
            if len(group_data["phones"]) > 1:
                label += f" ({len(group_data['phones'])} números)"
            
            # ID del nodo: usar el primer número del grupo
            node_id = group_data["phones"][0]
            
            nodes.append({
                "id": node_id,
                "label": label,
                "color": "blue",
                "type": "contact",
                "phones": group_data["phones"],  # Todos los números asociados
                "identity": group_data["identity"],
                "alias": group_data["alias"]
            })
            
            links.append({
                "source": pin,
                "target": node_id,
                "value": group_data["call_count"]
            })
        
        return {"nodes": nodes, "links": links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/llamadas")
def get_llamadas(pin: str = Query(...), contact: str = Query(...)):
    """
    Devuelve el resumen de llamadas entre un PIN y un contacto (número telefónico o identificador).
    Busca en transcripts.db y archivos PDF asociados.
    """
    import sqlite3
    import re
    from PyPDF2 import PdfReader
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
    results = []
    try:
        # 1. Buscar llamadas en transcripts.db
        db_path = os.path.join(BASE_DIR, "transcripts.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, pin_emitter, phone_number, date, duration
            FROM calls
            WHERE pin_emitter = ? AND phone_number = ?
            ORDER BY date DESC
        """, (pin, contact))
        llamadas = cursor.fetchall()
        conn.close()
        for llamada in llamadas:
            call_id, pin_emitter, phone_number, fecha, duracion = llamada
            # Buscar PDF y audio asociados (por convención de nombre)
            pdf_pattern = re.compile(rf"{pin}_({fecha})_T.*{contact}.*_reporte\\.pdf")
            pdf_file = None
            resumen = ""
            audio_url = None
            for fname in os.listdir(TRANSCRIPTS_DIR):
                if pdf_pattern.match(fname):
                    pdf_file = fname
                    break
            if pdf_file:
                pdf_path = os.path.join(TRANSCRIPTS_DIR, pdf_file)
                try:
                    reader = PdfReader(pdf_path)
                    text = " ".join(page.extract_text() or '' for page in reader.pages)
                    mres = re.search(r"Resumen: ([^\n]+)", text)
                    if mres:
                        resumen = mres.group(1)
                except Exception as e:
                    resumen = f"[Error leyendo PDF: {e}]"
                # Audio asociado
                audio_basename = pdf_file.replace('_reporte.pdf', '.wav')
                audio_path = os.path.join(os.path.dirname(__file__), '..', 'audios', audio_basename)
                audio_url = f'/audios/{audio_basename}' if os.path.exists(audio_path) else None
            results.append({
                "call_id": call_id,
                "pin": pin_emitter,
                "contact": phone_number,
                "fecha": fecha,
                "duracion": duracion,
                "resumen": resumen,
                "pdf": f"/transcripts/{pdf_file}" if pdf_file else None,
                "audio": audio_url
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pins")
def get_pins(q: str = None):
    """
    Devuelve todos los PINs únicos extraídos de los archivos PDF en transcripts/.
    Si se pasa el query param 'q', filtra los PINs que contienen ese substring.
    """
    try:
        files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".pdf")]
        pins = set()
        for filename in files:
            m = re.match(r"(\d{3,})_", filename)
            if m:
                pins.add(m.group(1))
        pins_list = sorted(pins)
        if q:
            pins_list = [p for p in pins_list if q in p]
        return {"pins": pins_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import re
from PyPDF2 import PdfReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")

@router.get("/transcriptions")
def get_all_transcriptions():
    """
    Devuelve todos los reportes PDF con metadatos: filename, fecha, hora, participantes, resumen.
    """
    try:
        results = []
        files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".pdf")]
        for filename in files:
            path = os.path.join(TRANSCRIPTS_DIR, filename)
            m = re.match(r"(\d{3,})_(\d{4}-\d{2}-\d{2})_T(\d{2}-\d{2}-\d{2})_reporte\.pdf", filename)
            pin, fecha, hora = None, None, None
            if m:
                pin, fecha, hora = m.group(1), m.group(2), m.group(3).replace('-', ':')
            participantes = set()
            resumen = ""
            try:
                reader = PdfReader(path)
                text = " ".join(page.extract_text() or '' for page in reader.pages)
                nombres = re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+", text)
                participantes.update(nombres)
                mres = re.search(r"Resumen: ([^\n]+)", text)
                if mres:
                    resumen = mres.group(1)
            except Exception as e:
                resumen = f"[Error leyendo PDF: {e}]"
            # Buscar archivo de audio correspondiente
            audio_basename = filename.replace('_reporte.pdf', '.wav') if filename else None
            audio_path = os.path.join(os.path.dirname(__file__), 'audios', audio_basename) if audio_basename else None
            audio_url = f'/audios/{audio_basename}' if audio_basename and os.path.exists(audio_path) else None
            results.append({
                "filename": filename,
                "pin": pin,
                "fecha": fecha,
                "hora": hora,
                "participantes": list(participantes),
                "resumen": resumen,
                "audio_url": audio_url
            })
        results.sort(key=lambda r: (r["fecha"] or "", r["hora"] or ""), reverse=True)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transcriptions/{pin}")
def get_transcriptions_by_pin(pin: str):
    """
    Devuelve los reportes PDF filtrados por el PIN especificado.
    """
    try:
        results = []
        files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.startswith(f"{pin}_") and f.endswith(".pdf")]
        for filename in files:
            path = os.path.join(TRANSCRIPTS_DIR, filename)
            m = re.match(rf"{pin}_(\d{{4}}-\d{{2}}-\d{{2}})_T(\d{{2}}-\d{{2}}-\d{{2}})_reporte\.pdf", filename)
            fecha, hora = None, None
            if m:
                fecha, hora = m.group(1), m.group(2).replace('-', ':')
            participantes = set()
            resumen = ""
            try:
                reader = PdfReader(path)
                text = " ".join(page.extract_text() or '' for page in reader.pages)
                nombres = re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+", text)
                participantes.update(nombres)
                mres = re.search(r"Resumen: ([^\n]+)", text)
                if mres:
                    resumen = mres.group(1)
            except Exception as e:
                resumen = f"[Error leyendo PDF: {e}]"
                        # Buscar archivo de audio correspondiente
            audio_basename = filename.replace('_reporte.pdf', '.wav') if filename else None
            audio_path = os.path.join(os.path.dirname(__file__), 'audios', audio_basename) if audio_basename else None
            audio_url = f'/audios/{audio_basename}' if audio_basename and os.path.exists(audio_path) else None
            results.append({
                "filename": filename,
                "pin": pin,
                "fecha": fecha,
                "hora": hora,
                "participantes": list(participantes),
                "resumen": resumen,
                "audio_url": audio_url
            })
        results.sort(key=lambda r: (r["fecha"] or "", r["hora"] or ""), reverse=True)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts")
def get_alerts():
    """
    Busca palabras clave de riesgo en los resúmenes y devuelve alertas con fecha, participantes y fragmento relevante.
    """
    palabras_riesgo = [
        # Narco y estructuras criminales
        "sicario", "halcones", "punteros", "postas", "posta", "estaca", "estacas", "gente del cerro", "gente del monte", "gente de la sierra",
        "comandante", "jefe de plaza", "compa", "escolta", "coyote", "pollero", "cuacito", "cuasillo", "cuas", "sancudo", "dronero", "plaza", "gente", "la gente",
        # Producción y tráfico
        "cocinero", "químico", "troquero", "cargador", "jalador", "pasta blues", "oxis", "m&m's", "cuerno de chivo", "cuerno", "r", "r-15", "lanzapapas",
        "boludo", "minimi", "chaparrita", "super güera", "5.7", "matapolicías",
        # Blindaje y vehículos
        "empecherado", "troca", "trocona", "perrona", "monstruo", "bestia", "burrito", "mula",
        # Comunicación y logística
        "pitufo", "perico", "piloto", "paloma", "ave", "volador", "capitán",
        # Religiosos/sectarios
        "la flaca", "la santa muerte", "la santa", "la niña blanca", "sanjudas tadeo", "sanjuditas", "judas", "san benito", "santo niño de atocha", "malverde",
        # Conflicto y violencia
        "contras", "topón", "caliente", "jale", "levantón", "madrina", "la línea", "sapo", "culebra", "chapulín", "brincaplazas", "cuatro letras", "encostalado", "mochar", "chapo", "aparatos", "clave", "plebada", "lavada", "alterado", "enfierrado", "cocodrilo", "huachos", "chota", "tira", "placa", "azules", "puercos", "firme", "pagar renta", "cooperación", "pago", "mensualidad", "charola", "vacuna", "dar piso", "bajar", "tronar", "plebe", "hacer una limpia", "pollitos de colores",
        # Originales del sistema
        "fierro", "paquete", "jefe", "guardia", "cargamento", "mercancía", "luz verde", "seña", "dinero", "mover", "camioneta", "transferencia", "reparto", "piedra", "cristal", "droga", "golpe", "candado", "puerta trasera"
    ]
    try:
        alerts = []
        files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".pdf")]
        for filename in files:
            path = os.path.join(TRANSCRIPTS_DIR, filename)
            fecha, participantes, resumen = None, [], ""
            m = re.match(r"(\d{3,})_(\d{4}-\d{2}-\d{2})_T(\d{2}-\d{2}-\d{2})_reporte\.pdf", filename)
            if m:
                fecha = m.group(2)
            try:
                reader = PdfReader(path)
                text = " ".join(page.extract_text() or '' for page in reader.pages)
                nombres = re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+", text)
                participantes = list(set(nombres))
                mres = re.search(r"Resumen: ([^\n]+)", text)
                if mres:
                    resumen = mres.group(1)
                for palabra in palabras_riesgo:
                    if palabra in resumen.lower():
                        alerts.append({
                            "fecha": fecha,
                            "participantes": participantes,
                            "alerta": palabra,
                            "fragmento": resumen
                        })
                        break
            except Exception:
                continue
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ReportRequest(BaseModel):
    transcription_text: str
    call_id: str

@router.post("/generate_report/")
async def generate_report(request: ReportRequest):
    try:
        topic = extract_main_topic(request.transcription_text)
        summary = summarize_text(request.transcription_text)
        
        # Obtener fecha y hora actual para el nombre del archivo
        from datetime import datetime
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("T%H-%M-%S")
        transcripts_dir = "transcripts"
        import os
        os.makedirs(transcripts_dir, exist_ok=True)
        pdf_filename = f"{request.call_id}_{fecha}_{hora}_reporte.pdf"
        pdf_path = os.path.join(transcripts_dir, pdf_filename)

        # Crear PDF Reporte
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Reporte de Llamada: {request.call_id}", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(0, 10, txt=f"Fecha: {fecha}  Hora: {hora}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Tema principal: {topic}")
        pdf.ln(5)
        # --- NUEVO: Resaltar palabras clave en el resumen ---
        # Obtener palabras clave de alerta (puedes adaptar esto según tu flujo)
        from backend.core.analysis.content_analyzer import ContentAnalyzer
        analyzer = ContentAnalyzer()
        # Extrae palabras clave usando los patrones definidos
        palabras_clave = set()
        for category, patterns in analyzer.risk_patterns.items():
            for pattern in patterns:
                import re
                for match in re.findall(pattern, summary):
                    palabras_clave.add(match)
        # Resalta palabras clave en el resumen
        resumen = summary
        resumen_words = resumen.split()
        for word in resumen_words:
            clean_word = word.strip('.,;:!?()[]"')
            if any(clean_word.lower() == k.lower() for k in palabras_clave):
                # Fondo amarillo
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(255, 255, 0)
                pdf.cell(pdf.get_string_width(word + ' '), 10, word + ' ', ln=0, fill=True)
                pdf.set_fill_color(255, 255, 255)
            else:
                pdf.set_text_color(0, 0, 0)
                pdf.cell(pdf.get_string_width(word + ' '), 10, word + ' ', ln=0, fill=False)
        pdf.ln(10)
        # --- FIN NUEVO ---
        pdf.output(pdf_path)

        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
