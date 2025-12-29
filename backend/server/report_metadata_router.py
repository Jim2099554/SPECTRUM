from fastapi import APIRouter, HTTPException
from typing import List, Dict
import os
import re
from PyPDF2 import PdfReader

router = APIRouter()

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")

@router.get("/api/reports/{pin}")
def get_reports_metadata(pin: str) -> List[Dict]:
    try:
        results = []
        all_files = os.listdir(TRANSCRIPTS_DIR)
        # Buscar archivos PDF que correspondan al PIN
        files = [f for f in all_files if f.startswith(f"{pin}_") and f.endswith(".pdf")]

        for filename in files:
            path = os.path.join(TRANSCRIPTS_DIR, filename)
            # Extraer fecha y hora del nombre de archivo
            pattern = re.compile(r"{}_(\d{{4}}-\d{{2}}-\d{{2}})_T(\d{{2}}-\d{{2}}-\d{{2}})_reporte\.pdf".format(pin))
            m = pattern.match(filename)
            fecha, hora = None, None
            if m:
                fecha, hora = m.group(1), m.group(2).replace('-', ':')
            # Extraer participantes y resumen del PDF
            participantes = set()
            resumen = ""
            try:
                reader = PdfReader(path)
                text = " ".join(page.extract_text() or '' for page in reader.pages)
                # Buscar nombres simples (mayúsculas y minúsculas, heurística)
                nombres = re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+", text)
                participantes.update(nombres)
                # Buscar resumen
                mres = re.search(r"Resumen: ([^\n]+)", text)
                if mres:
                    resumen = mres.group(1)
            except Exception as e:
                resumen = f"[Error leyendo PDF: {e}]"
            results.append({
                "filename": filename,
                "fecha": fecha,
                "hora": hora,
                "participantes": list(participantes),
                "resumen": resumen
            })
        # Ordenar por fecha/hora descendente
        results.sort(key=lambda r: (r["fecha"] or "", r["hora"] or ""), reverse=True)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
