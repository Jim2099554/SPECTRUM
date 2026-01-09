# 📦 Distribución de SENTINELA - Instrucciones para el Usuario Final

## ¿Qué incluye este paquete?

Este ejecutable de SENTINELA incluye **TODO lo necesario** para funcionar:
- ✅ Sistema completo de análisis de llamadas
- ✅ Soporte para múltiples sistemas PBX (Asterisk, Grandstream, etc.)
- ✅ Wizards de configuración interactivos
- ✅ Integración con bases de datos externas
- ✅ Sistema de licencias USB
- ✅ Todas las dependencias incluidas

## 🚀 Instalación en 3 Pasos

### 1️⃣ Descargar e Instalar
- **Windows:** Ejecute `SENTINELA_Centro.exe` o `SENTINELA_Admin.exe`
- **macOS:** Abra `SENTINELA_Centro.app` o `SENTINELA_Admin.app`

### 2️⃣ Primera Ejecución
Al iniciar por primera vez, verá un asistente de configuración que le preguntará:

#### A) Sistema Telefónico (PBX)
- ¿Qué marca de PBX usa? (Asterisk, Grandstream, Cisco, etc.)
- Credenciales de conexión
- Configuración de grabación

#### B) Base de Datos de PPL (Obligatorio)
- Tipo de base de datos (MySQL, PostgreSQL, SQL Server)
- Servidor y credenciales
- Mapeo de campos

#### C) Bases de Datos Opcionales
- Base de datos de llamadas
- Base de datos de carpetas/investigaciones

### 3️⃣ ¡Listo!
SENTINELA quedará configurado y listo para usar.

## 📞 Sistemas PBX Soportados

| PBX | Estado | Configuración |
|-----|--------|---------------|
| Asterisk | ✅ Listo | Automática |
| Grandstream UCM | ✅ Listo | Automática |
| Elastix/Issabel | ✅ Listo | Automática |
| FreeSWITCH | 🔄 Próximamente | Manual |
| 3CX | 🔄 Próximamente | Manual |
| Cisco CUCM | ⚠️ Requiere desarrollo | Contactar soporte |
| Avaya Aura | ⚠️ Requiere desarrollo | Contactar soporte |
| Huawei eSpace | ⚠️ Requiere desarrollo | Contactar soporte |
| Sin PBX | ✅ Soportado | Modo manual |

## 🔧 Reconfiguración

Si necesita cambiar la configuración después:

### Opción 1: Desde la interfaz
1. Abra SENTINELA
2. Vaya a Configuración → Sistema
3. Seleccione "Reconfigurar"

### Opción 2: Desde línea de comandos
```bash
# Windows
cd "C:\Program Files\SENTINELA"
python backend\scripts\initial_setup_wizard.py

# macOS
cd /Applications/SENTINELA.app/Contents/MacOS
python backend/scripts/initial_setup_wizard.py
```

## 📋 Información Requerida

Antes de instalar, tenga a mano:

### Para PBX (si aplica)
- Dirección IP del servidor PBX
- Puerto AMI (generalmente 5038)
- Usuario y contraseña AMI

### Para Base de Datos PPL
- Tipo de base de datos
- Servidor y puerto
- Nombre de la base de datos
- Usuario y contraseña
- Nombre de la tabla de PPL
- Nombres de los campos (PIN, Nombre, Foto, etc.)

## 🆘 Problemas Comunes

### "No puedo conectarme al PBX"
- Verifique que el servidor PBX esté encendido
- Compruebe que el firewall permita conexiones al puerto 5038
- Verifique las credenciales AMI

### "No encuentro la base de datos"
- Verifique que el servidor de BD esté corriendo
- Compruebe las credenciales
- Asegúrese de que la tabla exista

### "El wizard no aparece"
- Ejecute manualmente: `python backend/scripts/initial_setup_wizard.py`
- O contacte a soporte técnico

## 📞 Soporte

**Email:** soporte@sentinela.com  
**Teléfono:** +52 XXX XXX XXXX  
**Horario:** Lunes a Viernes, 9:00 - 18:00

---

**Versión:** 2.0  
**Fecha:** Enero 2026  
**© SENTINELA - Sistema de Inteligencia Penitenciaria**
