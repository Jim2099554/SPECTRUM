import os
import wave
import pyaudio
import time
from datetime import datetime
import argparse
import subprocess

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAGMENT_DURATION = 10  # segundos

def grabar_fragmentos(pin, duracion_total):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    folder = f"audio_fragments/{pin}_{timestamp}"
    os.makedirs(folder, exist_ok=True)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print(f"Grabando llamada de {pin}...")
    total_chunks = int(RATE / CHUNK * FRAGMENT_DURATION)
    num_fragments = int(duracion_total / FRAGMENT_DURATION)

    for i in range(num_fragments):
        frames = []
        for _ in range(total_chunks):
            data = stream.read(CHUNK)
            frames.append(data)
        filename = f"{folder}/fragment_{i:03d}.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        print(f"Fragmento {i+1} guardado: {filename}")

    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(f"Grabación terminada para {pin}")
    return folder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pin', required=True, help="PIN del PPL")
    parser.add_argument('--duracion', type=int, default=60, help="Duración total en segundos")
    args = parser.parse_args()

    carpeta = grabar_fragmentos(args.pin, args.duracion)

    # Ejecuta la transcripción automática
    print("Iniciando transcripción automática...")
    subprocess.run([
        "python",
        "backend/scripts/transcribir_fragmentos.py",
        carpeta
    ])
