import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import requests
import time
import os

SAMPLERATE = 16000  # Hz
DURATION = 5        # segundos
from datetime import datetime

PIN = input("Introduce el PIN del PPL (interno): ")
PHONE_NUMBER = input("Introduce el número de teléfono al que se enlazará la llamada: ")
# Captura la fecha y hora exacta de inicio
inicio_llamada = datetime.now().strftime("%Y%m%d_%H%M%S")

MAX_SILENT_FRAGMENTS = 6  # 6 fragmentos = 30 segundos de silencio
silent_count = 0
fragmentos = []  # Lista para acumular los fragmentos de audio
silencios = []   # Lista de índices de fragmentos silenciosos consecutivos al final
fragmentos_respuestas = []  # Guarda las respuestas del backend para la transcripción y alertas

while True:
    print("🎙️ Grabando 5 segundos...")
    audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    fragmentos.append(audio.copy())  # Guarda el fragmento en la lista
    scipy.io.wavfile.write("fragmento_temp.wav", SAMPLERATE, audio)

    try:
        with open("fragmento_temp.wav", "rb") as f:
            files = {"file": ("fragmento.wav", f, "audio/wav")}
            data = {"pin": PIN}
            response = requests.post("http://localhost:8000/stream/fragment", files=files, data=data, timeout=10)
        respuesta = response.json()
        fragmentos_respuestas.append(respuesta)  # Guarda la respuesta para la transcripción/alertas
        print("📤 Enviado fragmento, respuesta:", respuesta)
        # Si el texto está vacío o casi vacío, cuenta como silencio
        if not respuesta.get("text", "").strip():
            silent_count += 1
            silencios.append(len(fragmentos)-1)  # Guarda el índice de este fragmento silencioso
            print(f"🔇 Fragmento silencioso ({silent_count}/{MAX_SILENT_FRAGMENTS})")
        else:
            silent_count = 0
            silencios = []  # Reinicia la lista si hay un fragmento con voz
        if silent_count >= MAX_SILENT_FRAGMENTS:
            print("🛑 Demasiados fragmentos silenciosos. Terminando grabación.")
            break
    except Exception as e:
        print(f"❌ Error al enviar fragmento: {e}")
        break  # termina si no hay backend o hay error de red

    time.sleep(1)

# Al terminar, elimina 5 de los 6 últimos fragmentos silenciosos (si existen)
if len(silencios) >= MAX_SILENT_FRAGMENTS:
    # Conserva solo el último fragmento silencioso
    for idx in silencios[:-1]:
        fragmentos[idx] = None  # Marca para eliminar
    fragmentos = [frag for frag in fragmentos if frag is not None]

# Une todos los fragmentos restantes en un solo array
if fragmentos:
    audio_completo = np.concatenate(fragmentos, axis=0)
    nombre_archivo = f"{PIN}_{inicio_llamada}.wav"
    scipy.io.wavfile.write(nombre_archivo, SAMPLERATE, audio_completo)
    print(f"💾 Archivo final guardado como {nombre_archivo}")

    # --- NUEVO: Guardar registro en la base de datos ---
    import sqlite3
    import os

    # Construir la ruta relativa para guardar en la base
    audio_dir = "../audios"  # Ajusta si tu carpeta de audios es diferente
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    audio_destino = os.path.join(audio_dir, nombre_archivo)
    os.replace(nombre_archivo, audio_destino)  # Mueve el archivo al directorio de audios
    ruta_audio_rel = os.path.relpath(audio_destino, start=os.path.dirname(__file__))

    # Concatenar la transcripción y las alertas
    transcripcion = " ".join([frag.get("text", "") for frag in getattr(globals(), 'fragmentos_respuestas', []) if frag.get("text", "")])
    alertas = []
    for frag in getattr(globals(), 'fragmentos_respuestas', []):
        alertas.extend(frag.get("alertas", []))
    alertas_str = ", ".join(alertas)

    # Calcular duración total
    duracion_total = int(len(audio_completo) / SAMPLERATE)

    # Insertar en la base de datos
    db_path = os.path.join(os.path.dirname(__file__), '../transcripts.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO calls (pin_emitter, phone_number, date, duration, audio_path, transcription, alerts)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        PIN,
        PHONE_NUMBER,
        inicio_llamada,
        duracion_total,
        ruta_audio_rel,
        transcripcion,
        alertas_str
    ))
    conn.commit()
    conn.close()
    print(f"🗃️ Registro insertado en la base de datos: {db_path}")
    # --- FIN NUEVO ---
else:
    print("⚠️ No se grabó audio útil para guardar.")

# Limpieza: elimina el archivo temporal
if os.path.exists("fragmento_temp.wav"):
    os.remove("fragmento_temp.wav")

print("✅ Grabación finalizada automáticamente.")
