import sqlite3

# Connect to the SQLite database (will create if it doesn't exist)
conn = sqlite3.connect("transcripts.db")
cursor = conn.cursor()

# Create the 'calls' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pin_emitter TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

# Insert some demo call records
from datetime import datetime, timedelta
import random

# Generar fechas demo
base_date = datetime(2025, 4, 1)
fechas = [(base_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6)]

sample_calls = [
    ("1001", "5551234", fechas[0]),
    ("1002", "5555678", fechas[1]),
    ("1001", "5555678", fechas[2]),
    ("1003", "5551234", fechas[3]),
    ("1002", "5551234", fechas[4]),
    ("1001", "5551234", fechas[5]),  # Duplicate to test link count
]

cursor.executemany(
    "INSERT INTO calls (pin_emitter, phone_number, date) VALUES (?, ?, ?)",
    sample_calls
)

conn.commit()
print(f"Created 'calls' table and inserted {len(sample_calls)} demo records.")
conn.close()
