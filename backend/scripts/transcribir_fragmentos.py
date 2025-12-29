import os
import whisper
import requests

API_URL = "http://localhost:8000/alerts"  # Ajusta si tu backend usa otro host/puerto

def obtener_frases_alerta():
    resp = requests.get(f"{API_URL}/phrases/")
    resp.raise_for_status()
    return [item["phrase"] for item in resp.json()]

def reportar_evento_alerta(phrase_id, snippet, call_id):
    payload = {
        "phrase_id": phrase_id,
        "transcript_snippet": snippet,
        "call_id": call_id
    }
    resp = requests.post(f"{API_URL}/events/", json=payload)
    resp.raise_for_status()
    return resp.json()

def transcribir_fragmentos(folder, model_name="medium", language="Spanish", call_id=None):
    model = whisper.load_model(model_name)
    # Obtener frases de alerta dinámicamente
    frases_alerta = obtener_frases_alerta()
    print("Frases de alerta cargadas:", frases_alerta)
    # Mapear frase a ID para reportar eventos
    frases_data = requests.get(f"{API_URL}/phrases/").json()
    frase_to_id = {item["phrase"]: item["id"] for item in frases_data}
    results = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".wav"):
            audio_path = os.path.join(folder, filename)
            print(f"Transcribiendo {audio_path}...")
            result = model.transcribe(audio_path, language=language)
            texto = result["text"]
            results.append((filename, texto))
            with open(os.path.join(folder, filename.replace('.wav', '.txt')), "w") as f:
                f.write(texto)
            # Detectar y reportar alertas
            for frase in frases_alerta:
                if frase.lower() in texto.lower():
                    print(f"¡Alerta detectada! Frase: {frase} en {filename}")
                    phrase_id = frase_to_id.get(frase)
                    if phrase_id:
                        reportar_evento_alerta(phrase_id, texto, call_id or folder)
    # Guarda toda la transcripción junta en un solo archivo
    with open(os.path.join(folder, "transcripcion_total.txt"), "w") as f:
        for fname, texto in results:
            f.write(f"{texto.strip()} ")  # Junta todos los textos, separados por espacio
    print("¡Transcripción completa! Archivo: transcripcion_total.txt")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python transcribir_fragmentos.py <carpeta_de_fragmentos> [call_id]")
        sys.exit(1)
    folder = sys.argv[1]
    call_id = sys.argv[2] if len(sys.argv) > 2 else None
    transcribir_fragmentos(folder, call_id=call_id)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python transcribir_fragmentos.py <carpeta_de_fragmentos>")
        sys.exit(1)
    folder = sys.argv[1]
    transcribir_fragmentos(folder)
