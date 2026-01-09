# SENTINELA - Sistema de Inteligencia Penitenciaria

## 🚀 Instalación Rápida

### Windows

1. **Descargue el ejecutable** correspondiente a su rol:
   - `SENTINELA_Centro.exe` - Para centros penitenciarios
   - `SENTINELA_Admin.exe` - Para administración global

2. **Ejecute el instalador** haciendo doble clic

3. **Configuración inicial automática:**
   - La primera vez que ejecute SENTINELA, se abrirá un asistente de configuración
   - Siga las instrucciones en pantalla para configurar:
     - Sistema telefónico (PBX) - Opcional
     - Bases de datos de PPL - Obligatorio
     - Bases de datos de llamadas - Opcional
     - Bases de datos de carpetas - Opcional

4. **¡Listo!** SENTINELA está configurado y listo para usar

### macOS

1. **Descargue el ejecutable** correspondiente a su rol:
   - `SENTINELA_Centro.app` - Para centros penitenciarios
   - `SENTINELA_Admin.app` - Para administración global

2. **Mueva la aplicación** a la carpeta Aplicaciones

3. **Primera ejecución:**
   - Haga clic derecho → "Abrir" (para evitar advertencia de seguridad)
   - El asistente de configuración se abrirá automáticamente

4. **Configure el sistema** siguiendo el asistente

5. **¡Listo!** SENTINELA está configurado y listo para usar

---

## 📞 Configuración de PBX (Sistema Telefónico)

SENTINELA soporta los siguientes sistemas PBX:

### ✅ Totalmente Compatible (Listo para usar)
- **Asterisk** - PBX open source más popular
- **Grandstream UCM** - UCM6200, UCM6300, etc.
- **Elastix / Issabel / FreePBX** - Distribuciones basadas en Asterisk

### 🔄 Compatible (Requiere configuración adicional)
- **3CX** - PBX empresarial
- **FreeSWITCH** - Plataforma de comunicaciones
- **Microsoft Teams** - Sistema de comunicación empresarial

### ⚠️ Requiere Desarrollo Personalizado
- **Cisco CUCM** - Cisco Unified Communications Manager
- **Avaya Aura** - Sistema empresarial
- **Huawei eSpace** - Solución de comunicaciones
- **Mitel / NEC / Panasonic** - Otros sistemas empresariales

### ❌ Sin PBX
- Puede usar SENTINELA sin PBX, cargando archivos de audio manualmente

---

## 🗄️ Configuración de Bases de Datos

### Base de Datos PPL (Obligatoria)
Contiene información de las Personas Privadas de la Libertad:
- PIN / Número de PPL
- Nombre completo
- Fotografía
- Fecha de ingreso
- Delito

**Tipos soportados:** MySQL, PostgreSQL, Microsoft SQL Server

### Base de Datos de Llamadas (Opcional)
Registros históricos de llamadas telefónicas del PBX

### Base de Datos de Carpetas (Opcional)
Expedientes e investigaciones relacionadas con PPL

---

## 🔧 Reconfiguración

Si necesita cambiar la configuración después de la instalación:

### Windows
```cmd
cd "C:\Program Files\SENTINELA"
python backend\scripts\initial_setup_wizard.py
```

### macOS
```bash
cd /Applications/SENTINELA.app/Contents/MacOS
python backend/scripts/initial_setup_wizard.py
```

O ejecute los wizards individuales:
- `python backend/scripts/pbx_setup_wizard.py` - Solo PBX
- `python backend/scripts/database_setup_wizard.py` - Solo bases de datos

---

## 📋 Requisitos del Sistema

### Mínimos
- **Sistema Operativo:** Windows 10/11 o macOS 10.15+
- **RAM:** 4 GB
- **Disco:** 2 GB de espacio libre
- **Procesador:** Intel Core i3 o equivalente

### Recomendados
- **RAM:** 8 GB o más
- **Disco:** 10 GB de espacio libre (para audios y transcripciones)
- **Procesador:** Intel Core i5 o superior
- **Red:** Conexión a Internet para transcripción en la nube

---

## 🆘 Solución de Problemas

### "No se puede conectar al PBX"
1. Verifique que el servidor PBX esté encendido y accesible
2. Compruebe las credenciales AMI en la configuración
3. Asegúrese de que el firewall permita la conexión al puerto 5038

### "No se encuentra la base de datos PPL"
1. Verifique que el servidor de base de datos esté corriendo
2. Compruebe las credenciales de conexión
3. Asegúrese de que la tabla y campos existan

### "Error al iniciar SENTINELA"
1. Ejecute como administrador (Windows) o con permisos (macOS)
2. Verifique que no haya otro proceso usando el puerto 8000
3. Revise los logs en la carpeta `logs/`

---

## 📞 Soporte Técnico

Para asistencia técnica, contacte a:
- **Email:** soporte@sentinela.com
- **Teléfono:** +52 XXX XXX XXXX
- **Documentación:** [docs.sentinela.com](https://docs.sentinela.com)

---

## 📄 Licencia

SENTINELA requiere una licencia USB válida para funcionar.
- **Duración:** 1 año desde la activación
- **Tipo:** Licencia física USB (no transferible)

---

**Versión:** 2.0  
**Fecha:** Enero 2026  
**© 2026 SENTINELA - Sistema de Inteligencia Penitenciaria**
