# Instalación y Wizard de Spectrum

## Instalación paso a paso (wizard automático)

1. **Verifica que tienes Python 3.9+ y Node.js 18+ instalados.**
   - Puedes comprobarlo ejecutando `python3 --version` y `node --version`.
2. **Ejecuta el wizard de instalación:**
   ```bash
   python3 install_sentinela.py
   ```
   o en Windows:
   ```cmd
   py install_sentinela.py
   ```
3. **Sigue los pasos interactivos:**
   - El wizard te preguntará si quieres usar una base de datos externa para la información y fotos de PPL.
   - Si eliges SÍ, ten a la mano:
     - La URL de conexión de la base de datos externa (por ejemplo, `postgresql://user:pass@host:port/db`)
     - El endpoint o URL para obtener fotos de PPL (puede ser API REST o ruta de red accesible por HTTP)
   - El wizard probará la conexión a ambos servicios y te avisará si hay algún error.
   - El wizard te preguntará si deseas crear un entorno virtual de Python (recomendado).
   - Instalará automáticamente las dependencias del backend y frontend.
4. **Al finalizar, el wizard te mostrará cómo arrancar el sistema.**

---

# Preparación para Producción

Sigue estos pasos para asegurar que tu instalación de Spectrum quede lista y segura para producción:

## 1. Checklist de Cambios y Configuraciones Clave

- [ ] Cambia el valor de `API_TOKEN` en el backend por un valor seguro y único.
- [ ] Cambia el valor de `REACT_APP_API_TOKEN` en el frontend para que coincida con el backend.
- [ ] Configura correctamente la ruta de `RISK_PHRASES_PATH` en el backend.
- [ ] Configura las variables SMTP para envío de correos reales (no usar MailHog en producción).
- [ ] Usa una base de datos de producción (no SQLite local si necesitas escalabilidad o concurrencia).
- [ ] Habilita HTTPS en el servidor backend y en el despliegue frontend.
- [ ] Elimina o restringe endpoints de prueba y deshabilita el modo debug.
- [ ] Revisa los permisos de los archivos de audio y transcripciones.
- [ ] Configura variables de entorno en servidores (no hardcodees secretos en el código).
- [ ] Protege el acceso a la documentación `/docs` si es necesario.

## 2. Pasos para Backend

1. **Variables de entorno:**
   - Edita `.env` en la raíz del backend:
     ```env
     API_TOKEN=tu-token-seguro
     RISK_PHRASES_PATH=la/ruta/correcta/risk_phrases.json
     SMTP_HOST=smtp.tu-dominio.com
     SMTP_PORT=465
     SMTP_USER=usuario@tu-dominio.com
     SMTP_PASS=contraseña-segura
     ```
2. **Base de datos:**
   - Usa una base de datos robusta (PostgreSQL, MySQL, etc.) si SQLite no es suficiente.
   - Ajusta la cadena de conexión en la configuración del backend.
3. **Despliegue:**
   - Usa un servidor WSGI/ASGI robusto para producción (ej: Gunicorn, Uvicorn con supervisión, etc.).
   - Configura HTTPS (puedes usar Nginx como proxy inverso).

## 3. Pasos para Frontend (React)

1. **Variables de entorno:**
   - Crea/edita `.env` en `frontend/tailadmin-react/`:
     ```env
     REACT_APP_API_TOKEN=tu-token-seguro
     ```
   - El valor debe coincidir con el backend.
2. **Build y despliegue:**
   - Ejecuta `npm run build` para generar la versión optimizada.
   - Sube el contenido de `build/` a tu servidor web (Netlify, Vercel, Nginx, etc.).
3. **Configura CORS:**
   - Asegúrate de que el backend permita el dominio de tu frontend en producción.

## 4. Seguridad

- Nunca subas `.env` ni archivos con secretos a repositorios públicos.
- Usa HTTPS en todos los servicios.
- Cambia regularmente los tokens y contraseñas.
- Limita el acceso a endpoints sensibles.

---

# Preguntas Frecuentes (FAQ)

**¿Qué pasa si olvido cambiar el API_TOKEN?**
> Cualquiera que conozca el valor por defecto podrá acceder a los endpoints protegidos. Cámbialo siempre antes de exponer el sistema.

**¿Cómo cambio la base de datos a producción?**
> Instala y configura PostgreSQL/MySQL, ajusta la cadena de conexión en la configuración del backend y realiza migraciones si es necesario.

**¿Dónde defino el token para el frontend?**
> En el archivo `.env` dentro de la carpeta del frontend (`frontend/tailadmin-react/`).

**¿Qué hago si el frontend no puede autenticarse?**
> Verifica que ambos tokens (`API_TOKEN` y `REACT_APP_API_TOKEN`) coincidan exactamente y que el header `x-token` se esté enviando.

**¿Cómo activo HTTPS?**
> Usa un proxy inverso como Nginx o configura certificados SSL en tu servidor de backend/frontend.

**¿Puedo usar SQLite en producción?**
> Solo para pruebas o bajo baja carga. Para producción, usa una base de datos robusta.

**¿Puedo proteger la documentación de la API?**
> Sí, puedes desactivar o proteger `/docs` y `/redoc` en FastAPI usando dependencias de seguridad.

---

