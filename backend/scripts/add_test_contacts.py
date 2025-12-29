import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "transcripts.db")

# Datos de prueba: contactos con identidades
test_contacts = [
    # Mismo contacto con múltiples números
    {"phone": "5545678901", "name": "Juan Pérez", "alias": "El Tigre"},
    {"phone": "5556789012", "name": "Juan Pérez", "alias": "El Tigre"},  # Mismo nombre/alias
    
    # Contacto con solo alias
    {"phone": "5523456789", "name": None, "alias": "Z-1"},
    
    # Contacto con solo nombre
    {"phone": "5534567890", "name": "Ana López", "alias": None},
    
    # Contacto sin identidad (solo número)
    {"phone": "8134779134", "name": None, "alias": None},
]

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("📝 Agregando contactos de prueba...")

for contact in test_contacts:
    cursor.execute("""
        INSERT OR REPLACE INTO contacts 
        (phone_number, identity_name, alias, first_seen, last_seen, call_count)
        VALUES (?, ?, ?, '2025-04-15', '2025-04-20', 5)
    """, (contact["phone"], contact["name"], contact["alias"]))
    
    label = contact["name"] or contact["alias"] or contact["phone"]
    print(f"  ✓ {contact['phone']} → {label}")

conn.commit()
conn.close()

print("\n✅ Contactos de prueba agregados exitosamente")
print("\n💡 Ahora la red de vínculos mostrará:")
print("   - 'Juan Pérez \"El Tigre\"' agrupando 2 números")
print("   - 'Z-1' para un número")
print("   - 'Ana López' para otro número")
print("   - El último número sin identidad mostrará solo el número")
