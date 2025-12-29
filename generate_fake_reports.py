import os
from fpdf import FPDF
from datetime import datetime, timedelta
import random

# Carpeta donde se guardarán los PDFs
TRANSCRIPTS_DIR = os.path.join("server", "transcripts")
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

# Personas y números de teléfono simulados
contacts = [
    {"name": "Juan Pérez", "phone": "+5215551234567"},
    {"name": "La Güera", "phone": "+5215559876543"},
    {"name": "El Chino", "phone": "+5215552468101"},
    {"name": "Doña Mari", "phone": "+5215551357913"},
    {"name": "El Ingeniero", "phone": "+5215551122334"},
    {"name": "El Primo", "phone": "+5215552233445"},
    {"name": "La Tía", "phone": "+5215553344556"},
]

# Frases coloquiales ambiguas sobre delitos
phrases = [
    "Ya está todo listo para el encargo, nomás hay que esperar la seña.",
    "No digas nada por teléfono, ya sabes cómo está la cosa.",
    "El paquete va a llegar por la noche, tú estate al tiro.",
    "Dile a la Güera que tenga la feria lista.",
    "No te preocupes, el jefe ya dio luz verde.",
    "Vamos a mover la mercancía cuando se vayan los guardias.",
    "El Ingeniero dice que la puerta trasera está abierta.",
    "La moto ya está en el cargamento, sólo falta la señal.",
    "No te vayas a rajar, esto es entre nosotros.",
    "Si preguntan, tú no sabes nada, ¿ok?",
    "El Chino consiguió el fierro, pero hay que ser discretos.",
    "El Primo va a pasar por la mercancía en la noche.",
    "La Tía va a guardar las cosas en su casa.",
    "No te preocupes, nadie se va a enterar.",
    "Ya tenemos la dirección, sólo falta el aviso.",
    "Que no se le olvide a Doña Mari apagar las cámaras.",
    "El dinero se reparte después, primero lo importante.",
    "Si ves algo raro, me marcas de volada.",
    "La Güera dice que todo está bajo control.",
    "No uses nombres, sólo apodos en los mensajes.",
]

# Generar fechas y horas aleatorias en abril
base_date = datetime(2025, 4, 1, 8, 0, 0)
dates = set()
while len(dates) < 30:
    d = base_date + timedelta(days=random.randint(0, 27), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    dates.add(d)
dates = sorted(list(dates))

for i, dt in enumerate(dates):
    # Selecciona 1-3 participantes por conversación
    n_participants = random.randint(2, 4)
    participants = random.sample(contacts, n_participants)
    main_contact = participants[0]
    other_contacts = participants[1:]

    fecha = dt.strftime('%Y-%m-%d')
    hora = dt.strftime('T%H-%M-%S')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt=f'Reporte de Llamada: 666', ln=True, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, txt=f'Fecha: {fecha}  Hora: {hora}', ln=True)
    pdf.ln(5)
    # Participantes y teléfonos
    participantes_str = ', '.join([f"{p['name']} ({p['phone']})" for p in participants])
    pdf.cell(0, 10, txt=f'Participantes: {participantes_str}', ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f'Tema principal: Conversación de riesgo, lenguaje coloquial y referencias ambiguas a delitos.')
    pdf.ln(5)
    # Generar conversación simulada
    conversation = []
    word_count = 0
    while word_count < 1000:
        speaker = random.choice(participants)
        phrase = random.choice(phrases)
        line = f"{speaker['name']} ({speaker['phone']}): {phrase}"
        conversation.append(line)
        word_count += len(phrase.split()) + len(speaker['name'].split())
    texto = '\n'.join(conversation)
    pdf.multi_cell(0, 10, f'Resumen: {texto}')
    pdf.ln(10)
    aclaratoria = (
        "NOTA TÉCNICA: De acuerdo con los registros del sistema SENTINELA, todas las llamadas asociadas al PIN 666 "
        "fueron realizadas desde la cuenta personal e intransferible del interno. "
        "Por la operativa del sistema, se asume que la voz predominante en estas grabaciones corresponde al titular del PIN, "
        "salvo evidencia de suplantación. No se empleó biometría de voz para esta conclusión."
    )
    pdf.set_font('Arial', 'I', 10)
    pdf.multi_cell(0, 8, aclaratoria)
    fname = os.path.join(TRANSCRIPTS_DIR, f'666_{fecha}_{hora}_reporte.pdf')
    pdf.output(fname)
print("¡30 reportes PDF generados correctamente!")
