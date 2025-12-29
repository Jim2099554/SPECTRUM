import os
from dotenv import load_dotenv

# Carga variables de entorno desde .env si existe
load_dotenv()

# Configuración centralizada
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///backend/transcripts.db")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # Obligatoria para cifrado
AUDIO_UPLOAD_DIR = os.getenv("AUDIO_UPLOAD_DIR", "./secure_audio")

# Puedes agregar aquí otras variables de entorno necesarias, por ejemplo SMTP, GCS, etc.
