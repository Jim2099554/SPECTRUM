# SENTINELA

Sistema de Inteligencia Penitenciaria - Análisis y Monitoreo de Comunicaciones

**Versión:** 1.0  
**Fecha:** Diciembre 2025

---

## 🛠️ Stack Tecnológico
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, PyPDF2, Google Cloud Speech
- **Frontend:** React 18+, TypeScript, TailwindCSS, Recharts, ForceGraph3D
- **Base de Datos:** MySQL, PostgreSQL, MSSQL, SQLite (multi-database support)
- **Seguridad:** Sistema de licencias USB Dongle, Autenticación 2FA, JWT
- **Infraestructura:** PyInstaller, Inno Setup, Docker (desarrollo)

---

## 🚀 Instalación Rápida

### Empaquetado y Distribución Standalone

- El backend incluye soporte para multiprocesamiento congelado (freeze_support) en main.py, necesario para compatibilidad con PyInstaller y Windows.
- Para empaquetar el backend como ejecutable standalone:
  1. Instala PyInstaller en tu entorno virtual:
     ```bash
     pip install pyinstaller
     ```
  2. Empaqueta el backend:
     ```bash
     pyinstaller --onefile --add-data "frontend:frontend" backend/main.py
     ```
     - Esto generará un ejecutable en la carpeta `dist/` que sirve tanto la API como el frontend React (asegúrate de tener la carpeta `frontend` con el build de React junto a main.py).
  3. Al ejecutar el binario generado, FastAPI servirá la app web y la API desde el mismo ejecutable.

- Si ejecutas el backend manualmente, usa SIEMPRE desde la raíz del proyecto:
  ```bash
  source venv311/bin/activate
  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
  ```
  Esto asegura que los imports absolutos funcionen y la app sirva correctamente los archivos estáticos del frontend.

- El backend ahora monta la carpeta `frontend` como ruta raíz `/`, lo que permite servir el build de React directamente desde FastAPI. Cualquier ruta no encontrada por la API servirá el `index.html` de React (SPA support).

- Troubleshooting: Si ves errores de importación (ModuleNotFoundError: No module named 'backend'), asegúrate de ejecutar desde la raíz del proyecto y no desde la carpeta backend.

### Requisitos de sistema
- Python >= 3.11
- Node.js >= 18.x y npm >= 9.x
- Docker (para pruebas locales de MailHog)
- Ollama (https://ollama.com/download) instalado y corriendo para chat IA
- Git, VSCode (recomendados)

### Backend (FastAPI)
1. Crea y activa entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Unix/macOS
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copia y edita variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env según tu configuración
   ```
4. Ejecuta el servidor:
   ```bash
   uvicorn server.microservicio_fastapi:app --reload --port 8000
   ```

---

## 🤖 Integración con Ollama AI (Chat IA)

Para que el backend pueda responder preguntas usando IA, necesitas instalar Ollama y descargar el modelo correcto:

1. **Instala Ollama**
   - Descarga e instala desde: https://ollama.com/download
2. **Descarga el modelo llama3.2**
   ```sh
   ollama pull llama3.2
   ```
3. **Inicia Ollama** (si no está corriendo ya)
   ```sh
   ollama serve
   ```
   Ollama debe estar escuchando en `http://localhost:11434`.
4. **Verifica modelos instalados**
   ```sh
   ollama list
   ```
   Debes ver `llama3.2` en la lista.
5. **Inicia el backend normalmente** (como se indica arriba).

> ⚠️ **Importante:** Si Ollama no está corriendo o el modelo no está descargado, el chat IA no funcionará y verás errores como `model 'llama3' not found` o `connection refused` en la terminal.

---

### Frontend (React)
1. Ve a la carpeta del frontend:
   ```bash
   cd frontend/tailadmin-react
   npm install
   npm start
   ```
2. Accede a [http://localhost:3000](http://localhost:3000)

---

## 📦 Herramientas y software necesarios
- **Ollama:** Para chat IA, descargar y ejecutar modelos (ver [Ollama](https://ollama.com/download))
- **MailHog:** SMTP local para pruebas de email, ejecuta:
  ```sh
  docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
  ```
  - Web UI: [http://localhost:8025](http://localhost:8025)
- **Docker:** Para MailHog y otros servicios locales
- **VSCode:** Recomendado para desarrollo

---

## 🪟 Instalación rápida en Windows

1. Abre PowerShell como administrador en la carpeta del proyecto.
2. Ejecuta:
   ```powershell
   ./install_sentinela.ps1
   ```
   El script creará carpetas necesarias y configurará variables de entorno.
3. Si falta algún requisito, sigue las instrucciones que aparecen en pantalla para instalar Python y los módulos requeridos.
4. Para iniciar el conector PBX:
   ```powershell
   python backend/pbx_connector.py
   ```

---

## ☎️ Integración y configuración de Asterisk AMI y grabación

### 1. Configurar AMI en Asterisk
Edita `/etc/asterisk/manager.conf`:
```ini
[general]
enabled = yes
bindaddr = 0.0.0.0

[sentinela]
secret = password_seguro
read = all
write = all
```
Reinicia Asterisk:
```sh
sudo systemctl restart asterisk
# o
sudo asterisk -rx "core reload"
```

### 2. Habilitar módulo de grabación
Edita `/etc/asterisk/modules.conf` y asegúrate de tener:
```ini
load => res_monitor.so
```

### 3. Verificación automática del módulo de grabación
Ejecuta el siguiente script para verificar que `res_monitor.so` está cargado:
```sh
bash scripts/check_asterisk_monitor_module.sh
```

El script mostrará un mensaje ✅ si el módulo está cargado, o ❌ si no lo está.

---

## 📝 Notas y Troubleshooting
- Si usas Mac M1/M2/M3, revisa compatibilidad de audio y ML (puede requerir instalar dependencias nativas extra)
- Si usas Ollama, asegúrate de tener modelos descargados y corriendo
- Para problemas con dependencias, elimina y recrea el entorno virtual
- El endpoint `/generate_report/` espera `{ transcription_text, call_id }` y devuelve un PDF
- Para agregar nuevas features, revisa los archivos `src/api/index.js` y `src/components/TranscriptionChat.jsx`

---

## 📚 Estructura del Proyecto
- `/server`: Backend FastAPI, lógica de reportes, IA, PDF
- `/frontend/tailadmin-react`: Frontend React (dashboard, chat, reportes)
- `/requirements.txt`: Dependencias backend
- `/README.md`: Esta guía

---

## 👥 Contribución y soporte
- Usa ramas para nuevas features y PRs para revisión
- Documenta tus endpoints y cambios en este README
- Para dudas técnicas, consulta los comentarios en el código y este README

---

¡Listo para analizar y reportar llamadas con IA! 🎙️🤖

## Project Structure

```
spectrum/
├── api/            # FastAPI routes and endpoints
├── core/           # Core business logic
│   ├── audio/      # Audio processing and transcription
│   ├── speakers/   # Speaker recognition
│   ├── analysis/   # Content analysis
│   └── alerts/     # Real-time alert system
├── models/         # Database models and schemas
├── services/       # External service integrations
├── utils/          # Utility functions
└── web/           # Web interface
```

## Security Note

This tool handles sensitive audio data. Ensure proper security measures are in place and comply with relevant privacy regulations.

---

## Cambiar el API_TOKEN para producción

El sistema utiliza un token de autenticación (`API_TOKEN`) tanto en el backend como en el frontend para proteger los endpoints sensibles.

### Backend
- El token se configura en el archivo `.env` en la raíz del proyecto backend:
  
  ```env
  API_TOKEN=tu-token-seguro
  ```
- Cambia este valor por una cadena segura antes de desplegar en producción.

### Frontend (React)
- El frontend utiliza el token para autenticar las peticiones vía el header `x-token`.
- Para producción, crea o edita un archivo `.env` en la raíz del proyecto React (`frontend/tailadmin-react/`):
  
  ```env
  REACT_APP_API_TOKEN=tu-token-seguro
  ```
- Reinicia el servidor de React después de modificar este archivo.
- Si no defines la variable, se usará el valor por defecto `testtoken` (solo recomendado para desarrollo).

**IMPORTANTE:**
- El valor de `REACT_APP_API_TOKEN` en el frontend debe coincidir exactamente con el valor de `API_TOKEN` en el backend.
- Mantén este token en secreto y nunca lo publiques en repositorios públicos.

---

