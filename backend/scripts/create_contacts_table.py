import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "transcripts.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tabla de contactos con identidades
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number VARCHAR NOT NULL,
    identity_name VARCHAR,
    alias VARCHAR,
    first_seen DATE,
    last_seen DATE,
    call_count INTEGER DEFAULT 0,
    UNIQUE(phone_number, identity_name)
)
""")

# Crear tabla de relaciones entre identidades (para detectar cuando una persona usa múltiples números)
cursor.execute("""
CREATE TABLE IF NOT EXISTS identity_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_name VARCHAR NOT NULL,
    linked_phones TEXT,
    confidence_score REAL DEFAULT 1.0,
    last_updated DATE
)
""")

conn.commit()
conn.close()

print("✅ Tablas de contactos e identidades creadas exitosamente")
