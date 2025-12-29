import os
import requests

def batch_transcribe(audio_dir, pin, endpoint="http://localhost:8000/stream/fragment"):
    """
    Sube todos los archivos de audio .wav en audio_dir al endpoint de transcripción,
    usando el PIN indicado. Genera las transcripciones y reportes con la misma nomenclatura que el audio.
    """
    archivos = [f for f in os.listdir(audio_dir) if f.lower().endswith('.wav')]
    if not archivos:
        print(f"No se encontraron archivos .wav en {audio_dir}")
        return
    print(f"Se encontraron {len(archivos)} archivos .wav para transcribir con PIN {pin}.")
    for archivo in archivos:
        path_audio = os.path.join(audio_dir, archivo)
        print(f"Subiendo {archivo} ...")
        try:
            with open(path_audio, 'rb') as f:
                files = {'file': (archivo, f, 'audio/wav')}
                data = {'pin': pin}
                response = requests.post(endpoint, files=files, data=data)
            if response.status_code == 200:
                print(f"✅ Transcripción exitosa para {archivo}: {response.json()}")
            else:
                print(f"❌ Error en {archivo}: {response.status_code} {response.text}")
        except Exception as e:
            print(f"❌ Excepción en {archivo}: {e}")

if __name__ == "__main__":
    AUDIO_DIR = "/Users/jorgeivancantumartinez/CascadeProjects/spectrum/transcripts"
    PIN = "666"
    batch_transcribe(AUDIO_DIR, PIN)
