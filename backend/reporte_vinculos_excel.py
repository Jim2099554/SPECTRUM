import sqlite3
import pandas as pd
from collections import Counter, defaultdict
import networkx as nx
import matplotlib.pyplot as plt

DB_PATH = "transcripts.db"
EXCEL_PATH = "reporte_vinculos.xlsx"
GRAFICO_PATH = "reporte_vinculos_grafo.png"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Obtener todos los PINs únicos
cursor.execute("SELECT DISTINCT pin_emitter FROM calls")
pins = [row[0] for row in cursor.fetchall()]

reporte = []
G = nx.Graph()

for pin in pins:
    # 1. Contactos frecuentes y fechas
    cursor.execute("SELECT phone_number, date FROM calls WHERE pin_emitter = ?", (pin,))
    llamadas = cursor.fetchall()
    contactos = [row[0] for row in llamadas]
    fechas_por_contacto = defaultdict(list)
    for phone, fecha in llamadas:
        fechas_por_contacto[phone].append(fecha)
    contactos_frecuentes = Counter(contactos).most_common()

    # 2. Otros PINs que llaman a los mismos números
    contactos_set = set(contactos)
    pin_vinculos = defaultdict(set)
    for phone in contactos_set:
        cursor.execute("SELECT DISTINCT pin_emitter FROM calls WHERE phone_number = ? AND pin_emitter != ?", (phone, pin))
        for row in cursor.fetchall():
            pin_vinculos[phone].add(row[0])

    # 3. Armar el reporte por contacto
    for phone, count in contactos_frecuentes:
        otros_pins = ', '.join(sorted(pin_vinculos[phone])) if pin_vinculos[phone] else ''
        fechas = ', '.join(sorted(set(fechas_por_contacto[phone])))
        reporte.append({
            'PIN': pin,
            'Contacto': phone,
            'Veces_llamado': count,
            'Fechas': fechas,
            'PINs_vinculados': otros_pins
        })
        # Grafo: nodo PIN - nodo contacto
        G.add_edge(f"PIN {pin}", phone)
        # Grafo: vinculación entre PINs por contacto compartido
        for otro_pin in pin_vinculos[phone]:
            G.add_edge(f"PIN {pin}", f"PIN {otro_pin}", color='red')

conn.close()

# Exportar a Excel
pd.DataFrame(reporte).to_excel(EXCEL_PATH, index=False)
print(f"Reporte de vínculos exportado a {EXCEL_PATH}")

# Visualización del grafo
plt.figure(figsize=(10,7))
edge_colors = [G[u][v].get('color', 'gray') for u,v in G.edges()]
pos = nx.spring_layout(G, k=0.5, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors, font_size=8)
plt.title("Red de vínculos entre PINs y contactos")
plt.tight_layout()
plt.savefig(GRAFICO_PATH)
print(f"Gráfico de red guardado en {GRAFICO_PATH}")
