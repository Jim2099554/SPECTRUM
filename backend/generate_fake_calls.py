import os
from datetime import datetime, timedelta
import random

TRANSCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../transcripts'))
PIN = '666'
FECHA_BASE = datetime(2025, 4, 10)
NOMBRES = [
    ("Pedro Hernández", "5512345678"),
    ("Juan Pérez", "5523456789"),
    ("Laura", "5534567890"),
    ("Ana López", "5545678901"),
    ("Mario", "5556789012"),
]
DELICTOS = [
    "fraude bancario", "extorsión telefónica", "robo de identidad", "transferencia ilícita", "amenaza de secuestro",
    "hackeo de cuenta", "phishing", "venta de datos", "chantaje", "estafa piramidal"
]
RESUMENES = [
    "El interlocutor intentó obtener datos bancarios con engaños.",
    "Se solicitó una transferencia urgente a una cuenta desconocida.",
    "Amenaza directa para obtener dinero mediante extorsión.",
    "Simulación de llamada oficial para fraude.",
    "Intento de obtener contraseñas mediante manipulación."
]

os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

for i in range(20):
    fecha = FECHA_BASE + timedelta(days=i // 2)
    hora = (datetime(2025, 1, 1, 9, 0) + timedelta(minutes=30*i)).time()
    nombre_emisor, tel_emisor = NOMBRES[0]  # PIN 666
    nombre_receptor, tel_receptor = random.choice(NOMBRES[1:])
    delito = random.choice(DELICTOS)
    resumen = random.choice(RESUMENES)
    texto = f"[Resumen]: {resumen}\n[Delito]: {delito}\nParticipantes: Emisor: {nombre_emisor} ({tel_emisor}), Receptor: {nombre_receptor} ({tel_receptor})\nLa llamada contiene frases asociadas a riesgo: '{delito}', 'transferencia', 'cuenta', 'dinero'.\nDuración: 00:02:{random.randint(10,59):02d}\nTranscripción simulada de una llamada real con contenido de riesgo."
    nombre_archivo = f"{PIN}_{fecha.strftime('%Y-%m-%d')}_T{hora.strftime('%H-%M-%S')}_{tel_receptor}.txt"
    with open(os.path.join(TRANSCRIPTS_DIR, nombre_archivo), 'w', encoding='utf-8') as f:
        f.write(texto)
print(f"Generados 20 archivos de llamadas ficticias en {TRANSCRIPTS_DIR}")
