import sqlite3
import os
import re
from PyPDF2 import PdfReader
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
db_path = os.path.join(BASE_DIR, "transcripts.db")

def extract_names_and_aliases(text):
    """
    Extrae nombres propios y posibles alias de un texto.
    Retorna un diccionario con nombres y alias detectados.
    """
    names = set()
    aliases = set()
    
    # Patrones para nombres propios (Capitalizado)
    name_pattern = r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+\b'
    detected_names = re.findall(name_pattern, text)
    names.update(detected_names)
    
    # Patrones para alias comunes en contexto criminal
    # Formato: "el/la [alias]", "[alias]", "apodo [alias]"
    alias_patterns = [
        r'(?:el|la)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # el Z-1, la Flaca
        r'apodo\s+"?([^"]+)"?',  # apodo "El Tigre"
        r'alias\s+"?([^"]+)"?',  # alias "Z-1"
        r'"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"',  # "El Tigre"
        r'\b([A-Z]-\d+)\b',  # Z-1, M-2
        r'\b(Z-\d+|M-\d+|L-\d+)\b',  # Códigos militares
    ]
    
    for pattern in alias_patterns:
        detected_aliases = re.findall(pattern, text, re.IGNORECASE)
        aliases.update(detected_aliases)
    
    return list(names), list(aliases)

def extract_phone_from_filename(filename):
    """
    Extrae el número de teléfono del nombre del archivo PDF.
    Formato esperado: PIN_FECHA_THORA_NUMERO_reporte.pdf
    """
    # Buscar patrón de número telefónico (10 dígitos)
    match = re.search(r'_(\d{10})_', filename)
    if match:
        return match.group(1)
    return None

def process_transcripts():
    """
    Procesa todos los PDFs de transcripciones y extrae contactos con sus identidades.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Diccionario para agrupar información por número de teléfono
    contacts_data = defaultdict(lambda: {
        'names': set(),
        'aliases': set(),
        'dates': [],
        'call_count': 0
    })
    
    files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".pdf")]
    print(f"📄 Procesando {len(files)} archivos PDF...")
    
    for filename in files:
        path = os.path.join(TRANSCRIPTS_DIR, filename)
        
        # Extraer PIN, fecha y número del nombre del archivo
        match = re.match(r'(\d{3,})_(\d{4}-\d{2}-\d{2})_T(\d{2}-\d{2}-\d{2}).*\.pdf', filename)
        if not match:
            continue
            
        pin, fecha, hora = match.group(1), match.group(2), match.group(3)
        phone_number = extract_phone_from_filename(filename)
        
        if not phone_number:
            continue
        
        try:
            # Leer el PDF y extraer texto
            reader = PdfReader(path)
            text = " ".join(page.extract_text() or '' for page in reader.pages)
            
            # Extraer nombres y alias
            names, aliases = extract_names_and_aliases(text)
            
            # Agregar información al diccionario
            contacts_data[phone_number]['names'].update(names)
            contacts_data[phone_number]['aliases'].update(aliases)
            contacts_data[phone_number]['dates'].append(fecha)
            contacts_data[phone_number]['call_count'] += 1
            
        except Exception as e:
            print(f"⚠️  Error procesando {filename}: {e}")
            continue
    
    # Insertar datos en la tabla contacts
    print(f"\n💾 Guardando {len(contacts_data)} contactos en la base de datos...")
    
    for phone_number, data in contacts_data.items():
        # Determinar el nombre principal (el más común o el primero)
        primary_name = list(data['names'])[0] if data['names'] else None
        primary_alias = list(data['aliases'])[0] if data['aliases'] else None
        
        dates = sorted(data['dates'])
        first_seen = dates[0] if dates else None
        last_seen = dates[-1] if dates else None
        
        # Insertar o actualizar contacto
        cursor.execute("""
            INSERT OR REPLACE INTO contacts 
            (phone_number, identity_name, alias, first_seen, last_seen, call_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (phone_number, primary_name, primary_alias, first_seen, last_seen, data['call_count']))
        
        # Si hay múltiples nombres/alias, crear enlaces de identidad
        if len(data['names']) > 1 or len(data['aliases']) > 1:
            all_identities = list(data['names']) + list(data['aliases'])
            for identity in all_identities:
                cursor.execute("""
                    INSERT OR REPLACE INTO identity_links
                    (identity_name, linked_phones, last_updated)
                    VALUES (?, ?, ?)
                """, (identity, phone_number, last_seen))
    
    conn.commit()
    conn.close()
    
    print("✅ Contactos extraídos y guardados exitosamente")
    print(f"\n📊 Resumen:")
    print(f"   - Total de contactos únicos: {len(contacts_data)}")
    print(f"   - Contactos con nombre: {sum(1 for d in contacts_data.values() if d['names'])}")
    print(f"   - Contactos con alias: {sum(1 for d in contacts_data.values() if d['aliases'])}")

if __name__ == "__main__":
    process_transcripts()
