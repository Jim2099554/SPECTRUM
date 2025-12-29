# 📦 SENTINELA - Guía de Empaquetado y Deployment

**Versión:** 1.0  
**Fecha:** Diciembre 2025  
**Sistema:** Windows 10/11 (64-bit)

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Proceso de Empaquetado](#proceso-de-empaquetado)
3. [Crear Instalador Windows](#crear-instalador-windows)
4. [Testing del Instalador](#testing-del-instalador)
5. [Distribución a Clientes](#distribución-a-clientes)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Requisitos Previos

### Para Desarrollo (macOS/Linux)

- **Python 3.11+** con venv311 configurado
- **Node.js 18+** y npm
- **Git** para control de versiones

### Para Crear Instalador (Windows)

- **Inno Setup 6.2+**
  - Descargar: https://jrsoftware.org/isdl.php
  - Instalar con opciones por defecto

### Dependencias del Proyecto

```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
cd frontend
npm install
```

---

## 🚀 Proceso de Empaquetado

### Opción 1: Script Automático (Recomendado)

```bash
cd /Users/jorgeivancantumartinez/CascadeProjects/spectrum
./build_all.sh
```

Este script ejecuta automáticamente:
1. ✅ Limpieza de builds anteriores
2. ✅ Compilación del frontend React
3. ✅ Empaquetado del backend con PyInstaller
4. ✅ Generación de licencia de prueba
5. ✅ Preparación de estructura para instalador

### Opción 2: Paso a Paso Manual

#### 1. Build del Frontend

```bash
./build_frontend.sh
```

**Resultado:**
- `frontend/build/` - Archivos estáticos compilados
- `backend/client/` - Copia integrada en backend

#### 2. Build del Backend

```bash
./build_backend.sh
```

**Resultado:**
- `dist/SENTINELA_Backend/` - Ejecutable standalone
- Incluye todas las dependencias Python
- Tamaño aproximado: 150-200 MB

#### 3. Generar Licencia de Prueba

```bash
source venv311/bin/activate
python backend/scripts/generate_license.py \
  --client "Cliente de Prueba" \
  --institution "Testing" \
  --days 30 \
  --users 5 \
  --output ./test_license
```

---

## 🔨 Crear Instalador Windows

### Paso 1: Transferir Archivos a Windows

Copiar a una máquina Windows:
- `dist/SENTINELA_Backend/` (directorio completo)
- `installer.iss`
- `start_sentinela.bat`
- `LICENSE.txt`
- Documentación (*.md)
- `assets/` (si existe)

### Paso 2: Compilar con Inno Setup

1. **Abrir Inno Setup Compiler**

2. **Abrir archivo:** `installer.iss`

3. **Verificar rutas** en el script:
   ```pascal
   Source: "dist\SENTINELA_Backend\*"; DestDir: "{app}\backend";
   ```

4. **Compilar:**
   - Menu: `Build > Compile`
   - O presionar `Ctrl+F9`

5. **Resultado:**
   - `installer_output/SENTINELA_Setup_v1.0.exe`
   - Tamaño aproximado: 180-250 MB

### Paso 3: Personalización del Instalador

El instalador incluye:
- ✅ Wizard de configuración de licencia USB
- ✅ Wizard de configuración de base de datos PPL
- ✅ Creación de accesos directos
- ✅ Registro en Programas y Características
- ✅ Desinstalador automático

---

## 🧪 Testing del Instalador

### Test 1: Instalación Limpia

1. **Preparar USB de prueba:**
   ```
   test_license/sentinela.lic → Copiar a USB
   ```

2. **Ejecutar instalador:**
   ```
   SENTINELA_Setup_v1.0.exe
   ```

3. **Wizard de instalación:**
   - Aceptar licencia
   - Seleccionar directorio (default: `C:\Program Files\SENTINELA`)
   - **Licencia USB:** Seleccionar `sentinela.lic` del USB
   - **Base de datos PPL:**
     - Tipo: mysql/postgresql/mssql/sqlite
     - Host: localhost
     - Puerto: 3306 (MySQL) / 5432 (PostgreSQL)
     - Base de datos: nombre_bd
     - Usuario: usuario_bd
     - Contraseña: ********

4. **Verificar instalación:**
   - Acceso directo en escritorio
   - Acceso directo en menú inicio
   - Archivos en `C:\Program Files\SENTINELA\`

### Test 2: Primer Inicio

1. **Conectar USB con licencia**

2. **Ejecutar SENTINELA** (doble clic en acceso directo)

3. **Verificar logs:**
   ```
   ============================================================
   SENTINELA - Iniciando sistema...
   ============================================================
   ✅ Licencia USB válida
      Cliente: Cliente de Prueba
      Institución: Testing
      Expira: 2026-01-27
      Usuarios máximos: 5
   ============================================================
   ```

4. **Abrir navegador:** `http://localhost:8000`

5. **Login:**
   - Usuario: admin@sentinela.com
   - Contraseña: admin123
   - Código 2FA: (revisar logs o MailHog)

### Test 3: Funcionalidades

- ✅ Dashboard carga correctamente
- ✅ Red de vínculos visualiza datos
- ✅ Mapa geográfico centrado en México
- ✅ Palabras peligrosas detecta frases
- ✅ Transcripciones se muestran
- ✅ Búsqueda por PIN funciona

### Test 4: Desconexión de USB

1. **Con SENTINELA corriendo, desconectar USB**

2. **Verificar comportamiento:**
   - Sistema debe detectar desconexión
   - Mostrar advertencia
   - Solicitar reconexión

3. **Reconectar USB:**
   - Sistema debe reanudar operación normal

### Test 5: Desinstalación

1. **Panel de Control > Programas y Características**

2. **Desinstalar SENTINELA**

3. **Verificar limpieza:**
   - Archivos eliminados de `C:\Program Files\SENTINELA\`
   - Accesos directos eliminados
   - Registro de Windows limpio

---

## 📦 Distribución a Clientes

### Paquete de Entrega

Cada cliente debe recibir:

1. **Instalador:**
   - `SENTINELA_Setup_v1.0.exe`

2. **USB con Licencia:**
   - `sentinela.lic` (archivo encriptado)
   - Etiquetado con nombre del cliente

3. **Documentación:**
   - `MANUAL_USUARIO.pdf`
   - `GUIA_INSTALACION.pdf`
   - `LICENSE_INFO.txt` (en sobre sellado)

4. **Información de Soporte:**
   - Email: soporte@sentinela.com
   - Teléfono: +52 (XXX) XXX-XXXX
   - Horario: Lunes a Viernes, 9:00 - 18:00

### Checklist de Entrega

- [ ] Instalador probado en ambiente limpio
- [ ] Licencia USB generada y validada
- [ ] Documentación impresa y digital
- [ ] Información de base de datos del cliente
- [ ] Credenciales de administrador inicial
- [ ] Contacto de soporte técnico
- [ ] Acuerdo de nivel de servicio (SLA)

---

## 🔍 Solución de Problemas

### Error: "No se encontró licencia USB"

**Causa:** USB no conectado o archivo incorrecto

**Solución:**
1. Verificar que USB esté conectado
2. Verificar que archivo se llame `sentinela.lic`
3. Verificar que USB sea detectado por Windows

### Error: "No se puede conectar a la base de datos"

**Causa:** Configuración incorrecta o BD no accesible

**Solución:**
1. Verificar que servidor de BD esté corriendo
2. Verificar credenciales en `backend/config/database_config.json`
3. Verificar firewall no bloquee conexión
4. Probar conexión con cliente de BD (MySQL Workbench, pgAdmin, etc.)

### Error: "Puerto 8000 ya en uso"

**Causa:** Otra instancia de SENTINELA o aplicación usando el puerto

**Solución:**
1. Cerrar otras instancias de SENTINELA
2. Verificar procesos en Task Manager
3. Cambiar puerto en configuración (si es necesario)

### Error: "Licencia expirada"

**Causa:** Fecha de expiración alcanzada

**Solución:**
1. Contactar con proveedor
2. Solicitar renovación de licencia
3. Reemplazar archivo `sentinela.lic` en USB

### Frontend no carga / Pantalla en blanco

**Causa:** Archivos del frontend no copiados correctamente

**Solución:**
1. Verificar que exista `backend/client/` con archivos HTML/JS/CSS
2. Verificar logs del backend para errores
3. Limpiar caché del navegador
4. Probar en navegador diferente

---

## 📊 Estructura del Instalador

```
C:\Program Files\SENTINELA\
├── backend\
│   ├── SENTINELA_Backend.exe    # Ejecutable principal
│   ├── config\
│   │   ├── database_config.json # Configuración de BD
│   │   └── sentinela.lic        # Licencia (copiada del USB)
│   ├── data\
│   │   └── risk_phrases_corrected.json
│   ├── photos\                  # Fotos de PPL
│   ├── transcripts\             # PDFs de transcripciones
│   ├── audios\                  # Archivos de audio
│   ├── client\                  # Frontend React compilado
│   └── transcripts.db           # Base de datos SQLite local
├── start_sentinela.bat          # Script de inicio
├── README.md
├── SISTEMA_LICENCIAS.md
└── ARQUITECTURA_BASES_DE_DATOS.md
```

---

## 🔐 Seguridad y Mejores Prácticas

### Durante el Empaquetado

1. **No incluir datos sensibles** en el instalador
2. **Generar licencias únicas** por cliente
3. **Documentar versiones** de dependencias
4. **Firmar digitalmente** el instalador (opcional pero recomendado)

### Durante la Instalación

1. **Verificar licencia** antes de instalar
2. **Configurar BD** con credenciales seguras
3. **Cambiar contraseña** de admin por defecto
4. **Configurar firewall** para permitir puerto 8000

### Post-Instalación

1. **Backup regular** de base de datos
2. **Monitorear logs** del sistema
3. **Actualizar licencias** antes de expiración
4. **Mantener USB** en lugar seguro

---

## 📝 Notas de Versión

### Versión 1.0 (Diciembre 2025)

**Incluido:**
- ✅ Sistema completo de inteligencia penitenciaria
- ✅ Dashboard con métricas en tiempo real
- ✅ Red de vínculos 3D premium
- ✅ Mapa geográfico de llamadas
- ✅ Detección de palabras peligrosas (89 frases)
- ✅ Sistema de licencias USB Dongle
- ✅ Multi-base de datos (MySQL, PostgreSQL, MSSQL, SQLite)
- ✅ Autenticación con 2FA
- ✅ Análisis de transcripciones

**Requisitos del Sistema:**
- Windows 10/11 (64-bit)
- 4 GB RAM mínimo (8 GB recomendado)
- 500 MB espacio en disco
- Conexión a Internet (para 2FA y actualizaciones)
- Puerto 8000 disponible

---

## 📞 Soporte Técnico

**Para problemas durante el empaquetado:**
- Revisar logs de PyInstaller en `build/`
- Verificar que todas las dependencias estén instaladas
- Consultar documentación de PyInstaller

**Para problemas del instalador:**
- Revisar logs de Inno Setup
- Verificar permisos de administrador
- Consultar documentación de Inno Setup

**Para soporte a clientes:**
- Email: soporte@sentinela.com
- Documentación: Ver archivos *.md incluidos
- Sistema de tickets (si está configurado)

---

**Desarrollado para SENTINELA**  
**Sistema de Inteligencia Penitenciaria**  
**© 2025 - Todos los derechos reservados**
