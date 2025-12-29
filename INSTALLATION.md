# Spectrum/SENTINELA - Guía de Instalación y Configuración (ESPAÑOL)

---

## Requisitos de software

- **Python 3.11+** (recomendado instalar con [pyenv](https://github.com/pyenv/pyenv) o gestor similar)
- **Node.js 18+** y **npm** o **yarn**
- **Git**
- **(Opcional, recomendado en Mac)**: [Homebrew](https://brew.sh/) para instalar MailHog
- **(Opcional)**: [DB Browser for SQLite](https://sqlitebrowser.org/) para inspeccionar la base de datos visualmente

---

## 1. Clona el repositorio
```bash
git clone <URL-del-repositorio>
cd spectrum
```

---

## 2. Configuración del backend (FastAPI)

### a) Crea y activa el entorno virtual
```bash
python3 -m venv venv311
source venv311/bin/activate
```

### b) Instala dependencias
```bash
pip install -r requirements.txt
```

### c) Configura variables de entorno
```bash
cp backend/.env.example backend/.env
```
Edita el archivo `backend/.env` y completa:
```env
DATABASE_URL=sqlite:///backend/transcripts.db
JWT_SECRET=pon_un_secreto_seguro
ENCRYPTION_KEY=pon_aqui_una_clave_segura
AUDIO_UPLOAD_DIR=./secure_audio
# (Opcional para correo)
SMTP_HOST=localhost
SMTP_PORT=1025
```
- **DATABASE_URL**: Cadena de conexión a la base de datos (por defecto SQLite, para producción puedes usar PostgreSQL/MySQL).
- **JWT_SECRET**: Clave secreta para autenticación. ¡Cámbiala para producción!
- **ENCRYPTION_KEY**: Clave para cifrado de datos. Usa un valor seguro y aleatorio.
- **AUDIO_UPLOAD_DIR**: Carpeta donde se almacenan los audios subidos.
- **SMTP_HOST/PORT**: Configuración para pruebas de correo (MailHog).

### d) Inicializa la base de datos (solo la primera vez o tras cambios de modelo)
```bash
python backend/init_db.py
```

### e) (Opcional) Configura MailHog para pruebas de correo
- Instala MailHog:
  ```bash
  brew install mailhog
  mailhog
  ```
- Accede a http://localhost:8025 para ver los correos enviados.

### f) Arranca el backend
```bash
source venv311/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
- El backend estará disponible en: http://localhost:8000

---

## 2.bis Configuración de credenciales AMI (Asterisk PBX)

Para conectar el sistema con la central telefónica Asterisk de cada centro penitenciario, debes definir las credenciales reales del AMI (Asterisk Manager Interface) en el archivo `backend/.env`.

Agrega las siguientes variables al archivo `.env` del backend:

```env
# Credenciales AMI para Asterisk PBX
AMI_HOST=192.168.1.100    # Dirección IP o hostname del servidor Asterisk
AMI_PORT=5038             # Puerto del AMI (por defecto 5038)
AMI_USER=sentinela        # Usuario configurado en manager.conf
AMI_PASSWORD=clave_segura # Contraseña del usuario AMI
```

**Recomendaciones:**
- Solicita al administrador de cada centro penitenciario los datos correctos.
- El usuario y contraseña deben coincidir con los definidos en el archivo `manager.conf` del Asterisk.
- No compartas estas credenciales fuera del área técnica.
- Usa una contraseña fuerte y cámbiala periódicamente.
- Si el PBX está en otra red, asegúrate de que el firewall permita la conexión al puerto AMI.

**Ejemplo de sección en `.env` para un centro:**
```env
AMI_HOST=10.10.10.5
AMI_PORT=5038
AMI_USER=monitor_centro
AMI_PASSWORD=claveUltraSegura2025
```

---

## 3. Configuración del frontend (Vite + React)

### a) Ve a la carpeta frontend
```bash
cd frontend
```

### b) Copia y edita el archivo de entorno
```bash
cp .env.example .env
```
Edita `.env` si necesitas cambiar la URL del backend:
```env
VITE_BACKEND_URL=http://localhost:8000
```

### c) Instala dependencias
```bash
npm install
# o
# yarn install
```

### d) Arranca el frontend
```bash
npm run dev
# o
# yarn dev
```
- El frontend estará disponible en: http://localhost:17167

---

## 4. Buenas prácticas y recomendaciones de seguridad

- **Arranca siempre el backend antes que el frontend** para evitar errores de CORS.
- El proxy de Vite está configurado para evitar problemas de CORS en desarrollo.
- Si cambias el puerto o URL del backend, actualiza la variable en `.env` del frontend.
- Para producción, **restringe los orígenes permitidos en el middleware CORS** del backend.
- **Nunca subas archivos `.env` ni claves sensibles a repositorios públicos.**
- Haz respaldos regulares de la base de datos.
- Usa HTTPS y restringe CORS en producción.
- Cambia todas las contraseñas y claves por defecto antes de poner en producción.
- Realiza migraciones y respaldos periódicos de la base de datos.
- Si usas autenticación, elimina el usuario admin temporal tras el primer acceso y crea un administrador propio.

---

## 4. Set Up Google Cloud Credentials (If Using GCS Features)
Some features require access to Google Cloud Storage. Set up your credentials as follows:
- Create a service account in Google Cloud Console.
- Download the JSON key file.
- Set the environment variable:
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
  ```

## 5. Run Tests (Optional, for Verification)
To verify your installation and code integrity, run the test suite:
```bash
pytest --maxfail=10 --disable-warnings -q
```

## 6. Run the Application
Start the main application (adjust the entry point as needed):
```bash
python main.py
```

---

**Notes:**
- Ensure you are using a compatible Python version (preferably Python 3.8+).
- If you add new dependencies, update `requirements.txt` accordingly.
- For any issues, check your virtual environment, dependency versions, and credentials.

---

For further details, refer to the project README or contact the maintainer.
