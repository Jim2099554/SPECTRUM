import sqlite3
import os

# Cambia la ruta si tu transcripts.db está en otra carpeta
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../transcripts.db'))

# Columnas a agregar (si no existen)
columns = [
    ("date", "TEXT"),
    ("duration", "INTEGER"),
    ("audio_path", "TEXT"),
    ("transcription", "TEXT"),
    ("alerts", "TEXT")
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Verifica columnas existentes
cur.execute('PRAGMA table_info(calls);')
existing_cols = {row[1] for row in cur.fetchall()}

for col, coltype in columns:
    if col not in existing_cols:
        print(f"Agregando columna {col}...")
        cur.execute(f'ALTER TABLE calls ADD COLUMN {col} {coltype};')
    else:
        print(f"La columna {col} ya existe.")

conn.commit()
conn.close()
print("\n¡Estructura de la tabla 'calls' actualizada correctamente!")
