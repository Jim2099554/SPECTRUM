# 🔐 SENTINELA - Sistema de Licencias USB Dongle

## 📋 Descripción General

SENTINELA utiliza un sistema de licencias basado en **USB Dongle** para proteger el software y controlar el acceso. El sistema verifica la presencia de un archivo de licencia encriptado en una memoria USB antes de permitir el uso completo del sistema.

---

## 🎯 Características del Sistema

### ✅ Seguridad
- **Encriptación XOR** con clave secreta
- **Firma digital** SHA-256 para validación
- **Hardware ID** opcional para vincular a equipo específico
- **Verificación continua** de presencia del USB

### ✅ Flexibilidad
- **Licencias temporales** con fecha de expiración configurable
- **Múltiples usuarios** simultáneos configurables
- **Módulos habilitados** personalizables por cliente
- **Renovación remota** mediante nuevo archivo de licencia

### ✅ Control
- **Monitoreo en tiempo real** de conexión USB
- **Revocación de licencias** mediante flag en el archivo
- **Registro de uso** y auditoría
- **Modo limitado** si no hay licencia válida

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────┐
│   SENTINELA (Aplicación)            │
│                                     │
│   ┌─────────────────────────────┐  │
│   │  License Manager            │  │
│   │  - Verificación continua    │  │
│   │  - Monitoreo USB            │  │
│   │  - Validación de firma      │  │
│   └──────────┬──────────────────┘  │
│              │                      │
└──────────────┼──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │  USB Dongle  │
        │              │
        │ sentinela.lic│  ← Archivo encriptado
        └──────────────┘
```

---

## 📁 Componentes del Sistema

### 1. **License Manager** (`license_manager.py`)
Gestor principal del sistema de licencias.

**Funciones principales:**
- `check_license()` - Verificar licencia al inicio
- `monitor_usb()` - Monitorear conexión USB
- `validate_license()` - Validar datos de licencia
- `get_license_info()` - Obtener información de licencia

### 2. **License Generator** (`generate_license.py`)
Generador de archivos de licencia para distribuir.

**Modos de uso:**
- **Interactivo**: Sin argumentos, guía paso a paso
- **CLI**: Con argumentos para automatización

### 3. **License Router** (`license_router.py`)
API REST para gestión de licencias.

**Endpoints:**
- `GET /license/status` - Estado de licencia
- `GET /license/info` - Información detallada
- `POST /license/verify` - Forzar verificación
- `GET /license/monitor` - Monitorear USB

---

## 🔧 Uso del Generador de Licencias

### Modo Interactivo (Recomendado)

```bash
cd /Users/jorgeivancantumartinez/CascadeProjects/spectrum
source venv311/bin/activate
python backend/scripts/generate_license.py
```

El sistema solicitará:
1. Nombre del cliente
2. Institución/Organización
3. Días de validez (default: 365)
4. Usuarios máximos (default: 5)
5. ¿Vincular a equipo específico? (s/n)
6. Directorio de salida

### Modo CLI (Automatizado)

```bash
python backend/scripts/generate_license.py \
  --client "Secretaría de Seguridad Pública" \
  --institution "Gobierno del Estado" \
  --days 365 \
  --users 10 \
  --output ./licenses/cliente1
```

### Con Hardware ID (Vincular a equipo)

```bash
python backend/scripts/generate_license.py \
  --client "Centro Penitenciario Norte" \
  --institution "SSP Estatal" \
  --days 730 \
  --users 5 \
  --hardware-id "abc123def456..." \
  --output ./licenses/centro_norte
```

---

## 📦 Archivos Generados

Cada licencia genera 2 archivos:

### 1. `sentinela.lic` (Archivo de Licencia)
- Archivo encriptado con datos de licencia
- **Este es el archivo que va en el USB**
- No debe ser modificado

### 2. `LICENSE_INFO.txt` (Información de Referencia)
- Información legible para el administrador
- Incluye clave de licencia, fechas, módulos
- Instrucciones de uso
- **Guardar para registros internos**

---

## 🎫 Estructura de una Licencia

```json
{
  "license_key": "SENT-A1B2-C3D4-E5F6-G7H8",
  "client_name": "Secretaría de Seguridad Pública",
  "institution": "Gobierno del Estado",
  "issue_date": "2025-12-28T10:00:00",
  "expiry_date": "2026-12-28T10:00:00",
  "max_users": 10,
  "modules": [
    "dashboard",
    "analytics",
    "network",
    "alerts",
    "reports"
  ],
  "version": "1.0",
  "revoked": false,
  "hardware_id": "opcional",
  "signature": "sha256_hash..."
}
```

---

## 🚀 Proceso de Distribución

### Para el Proveedor (Tú)

1. **Generar licencia** usando el script
   ```bash
   python backend/scripts/generate_license.py
   ```

2. **Copiar `sentinela.lic` a USB**
   - Usar USB de calidad
   - Etiquetar el USB con nombre del cliente
   - Incluir `LICENSE_INFO.txt` en sobre sellado

3. **Entregar al cliente**
   - USB con licencia
   - Documentación de instalación
   - Información de soporte técnico

4. **Guardar registros**
   - `LICENSE_INFO.txt` en base de datos
   - Fecha de emisión y expiración
   - Cliente y número de serie

### Para el Cliente

1. **Recibir USB** con licencia

2. **Conectar USB** al equipo donde está instalado SENTINELA

3. **Iniciar SENTINELA**
   - El sistema detecta automáticamente la licencia
   - Muestra información de licencia en logs
   - Habilita todas las funciones

4. **Mantener USB conectado** durante el uso

5. **Renovación**
   - Al vencer, solicitar nueva licencia
   - Reemplazar archivo `sentinela.lic` en el mismo USB

---

## ⚙️ Validaciones del Sistema

### Al Iniciar SENTINELA

1. ✅ **Buscar USB** con archivo `sentinela.lic`
2. ✅ **Leer y desencriptar** archivo de licencia
3. ✅ **Verificar firma digital** (integridad)
4. ✅ **Verificar fecha de expiración**
5. ✅ **Verificar Hardware ID** (si aplica)
6. ✅ **Verificar que no esté revocada**

### Durante el Uso

- **Monitoreo continuo** cada X minutos
- **Verificar que USB siga conectado**
- **Si se desconecta**: Pausar sistema y solicitar reconexión

---

## 🔒 Seguridad del Sistema

### Encriptación
- **Algoritmo**: XOR con clave secreta
- **Clave**: `SENTINELA_2025_SECURE_KEY`
- **Formato**: Hexadecimal

### Firma Digital
- **Algoritmo**: SHA-256
- **Datos firmados**: license_key + client_name + expiry_date
- **Verificación**: Al cargar licencia

### Hardware ID (Opcional)
- **Componentes**: CPU ID + MAC Address
- **Hash**: SHA-256 (32 caracteres)
- **Uso**: Vincular licencia a equipo específico

---

## 🛠️ Mantenimiento y Soporte

### Renovar Licencia

```bash
# Generar nueva licencia con mismos datos
python backend/scripts/generate_license.py \
  --client "Cliente Existente" \
  --institution "Misma Institución" \
  --days 365 \
  --users 10 \
  --output ./licenses/renovacion
```

### Revocar Licencia

Editar manualmente el archivo JSON antes de encriptar:
```json
{
  ...
  "revoked": true
}
```

### Aumentar Usuarios

Generar nueva licencia con `--users` mayor:
```bash
--users 20  # Aumentar de 10 a 20
```

### Cambiar Módulos

```bash
--modules dashboard analytics network alerts reports custom_module
```

---

## 📊 Monitoreo y Logs

### Logs de Inicio

```
============================================================
SENTINELA - Iniciando sistema...
============================================================
✅ Licencia USB válida
   Cliente: Secretaría de Seguridad Pública
   Institución: Gobierno del Estado
   Expira: 2026-12-28
   Usuarios máximos: 10
============================================================
```

### Logs de Error

```
⚠️  No se encontró USB con licencia válida
   El sistema funcionará en modo limitado
   Por favor conecte el USB de licencia para acceso completo
```

---

## 🆘 Solución de Problemas

### "No se encontró USB con licencia válida"
- ✅ Verificar que el USB esté conectado
- ✅ Verificar que el archivo se llame `sentinela.lic`
- ✅ Verificar que el USB sea detectado por el sistema operativo

### "Licencia expirada"
- ✅ Contactar con proveedor para renovación
- ✅ Solicitar nueva licencia con fecha actualizada

### "Licencia no válida para este equipo"
- ✅ La licencia está vinculada a otro equipo
- ✅ Solicitar licencia sin Hardware ID o para este equipo específico

### "Firma de licencia inválida"
- ✅ El archivo fue modificado o está corrupto
- ✅ Solicitar nuevo archivo de licencia

---

## 💡 Mejores Prácticas

### Para el Proveedor

1. **Mantener registro** de todas las licencias emitidas
2. **Backup** de archivos `LICENSE_INFO.txt`
3. **Etiquetar USBs** claramente con cliente y fecha
4. **Usar USBs de calidad** para evitar fallos
5. **Documentar** fechas de renovación

### Para el Cliente

1. **Backup del USB** en lugar seguro
2. **No modificar** el archivo `sentinela.lic`
3. **Mantener USB conectado** durante uso
4. **Renovar antes** de la fecha de expiración
5. **Contactar soporte** ante cualquier problema

---

## 📞 Soporte Técnico

**Email**: soporte@sentinela.com  
**Teléfono**: +52 (XXX) XXX-XXXX  
**Horario**: Lunes a Viernes, 9:00 - 18:00

---

## 📝 Notas de Versión

**Versión 1.0** (Diciembre 2025)
- ✅ Sistema de licencias USB Dongle implementado
- ✅ Encriptación y firma digital
- ✅ Generador de licencias interactivo y CLI
- ✅ Monitoreo continuo de USB
- ✅ API REST para gestión de licencias
- ✅ Integración con inicio de aplicación

---

**Desarrollado para SENTINELA**  
**Sistema de Inteligencia Penitenciaria**  
**© 2025 - Todos los derechos reservados**
