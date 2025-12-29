# 🏗️ Arquitectura de Integración de Bases de Datos - SENTINELA

## 📋 Resumen Ejecutivo

SENTINELA utiliza una arquitectura modular de integración de bases de datos que permite conectarse a múltiples fuentes de datos externas usando el **PIN del PPL como clave maestra**.

---

## 🎯 Concepto Central: PIN como Clave Maestra

### Flujo de Búsqueda

```
1. Usuario ingresa PIN (ej: 666)
   ↓
2. SENTINELA busca en Base de Datos PPL (OBLIGATORIA)
   ↓
3. Obtiene: Nombre, Foto, Fecha Ingreso, Delito, etc.
   ↓
4. Usa PIN + Nombre para buscar en bases secundarias:
   ├─ PBX → Llamadas telefónicas
   ├─ Carpetas → Expedientes e investigaciones
   ├─ Visitas → Registro de visitantes
   └─ Otras → Bases de datos personalizadas
   ↓
5. Consolida toda la información en un perfil único
```

---

## 🗄️ Bases de Datos Soportadas

### Base de Datos PPL (OBLIGATORIA) ⭐

**Propósito:** Información principal del PPL

**Campos requeridos:**
- `pin` / `numero_ppl` - Identificador único
- `nombre_completo` - Nombre del PPL
- `foto` - Ruta de la fotografía (opcional)
- `fecha_ingreso` - Fecha de ingreso (opcional)
- `delito` - Delito principal (opcional)

**Tipos soportados:** MySQL, PostgreSQL, SQL Server

---

### Base de Datos PBX (OPCIONAL)

**Propósito:** Registros de llamadas telefónicas

**Campos de búsqueda:**
- `pin` - PIN del PPL
- `caller_id` - ID del llamante
- `extension` - Extensión telefónica
- `phone_number` - Número marcado

**Tipos soportados:** MySQL, PostgreSQL, SQL Server

---

### Base de Datos Carpetas/Investigaciones (OPCIONAL)

**Propósito:** Expedientes e investigaciones

**Campos de búsqueda:**
- `pin` - PIN del PPL
- `numero_expediente` - Número de carpeta
- `nombre_investigado` - Nombre en la investigación

**Tipos soportados:** MySQL, PostgreSQL, SQL Server

---

## 🔧 Componentes del Sistema

### 1. Database Manager (`database_manager.py`)

**Responsabilidades:**
- Gestionar conexiones a múltiples bases de datos
- Crear adaptadores según el tipo de BD
- Coordinar búsquedas en todas las fuentes
- Consolidar información

**Métodos principales:**
```python
# Conectar a todas las bases de datos
manager.connect_all()

# Obtener perfil completo de un PPL
profile = manager.get_complete_profile(pin="666")

# Resultado incluye:
# - ppl_data: Información del PPL
# - pbx_data: Llamadas telefónicas
# - carpetas_data: Expedientes
# - other_data: Otras fuentes
# - errors: Lista de errores
```

---

### 2. Database Adapters

**Adaptadores disponibles:**
- `MySQLAdapter` - Para bases de datos MySQL/MariaDB
- `PostgreSQLAdapter` - Para PostgreSQL
- `MSSQLAdapter` - Para Microsoft SQL Server

**Cada adaptador implementa:**
```python
- connect() → Establecer conexión
- disconnect() → Cerrar conexión
- test_connection() → Probar si funciona
- search_by_pin(pin) → Buscar por PIN
- search_by_name(name) → Buscar por nombre
```

---

### 3. API Endpoints (`database_config_router.py`)

#### GET `/database/config`
Obtener configuración actual de bases de datos

#### POST `/database/config`
Actualizar configuración de bases de datos

#### POST `/database/test`
Probar conexión a una base de datos específica

#### GET `/database/status`
Ver estado de todas las conexiones

#### GET `/ppl/profile/{pin}`
**Endpoint principal:** Obtener perfil completo de un PPL

**Ejemplo de respuesta:**
```json
{
  "pin": "666",
  "ppl_data": {
    "numero_ppl": "666",
    "nombre_completo": "Juan Pérez García",
    "foto": "/photos/666.jpg",
    "fecha_ingreso": "2024-01-15",
    "delito": "Robo agravado"
  },
  "pbx_data": {
    "by_pin": [...],
    "by_name": [...]
  },
  "carpetas_data": {
    "by_pin": {...},
    "by_name": [...]
  },
  "other_data": {},
  "errors": []
}
```

---

## 🎨 Wizard de Configuración

### Instalación Paso a Paso

```bash
# Ejecutar wizard de configuración
python backend/scripts/database_setup_wizard.py
```

### Pantallas del Wizard

**1. Base de Datos PPL (Obligatoria)**
- Tipo de BD (MySQL/PostgreSQL/SQL Server)
- Host, Puerto, Base de datos
- Usuario y Contraseña
- Nombre de tabla de PPL
- Mapeo de campos (PIN, Nombre, Foto, etc.)
- Prueba de conexión

**2. Base de Datos PBX (Opcional)**
- Configuración de conexión
- Tabla de llamadas
- Campos de búsqueda
- Prueba de conexión

**3. Base de Datos Carpetas (Opcional)**
- Configuración de conexión
- Tabla de expedientes
- Campos de búsqueda
- Prueba de conexión

**4. Guardar Configuración**
- Genera `backend/config/database_config.json`
- Resumen de bases configuradas

---

## 📁 Archivo de Configuración

**Ubicación:** `backend/config/database_config.json`

**Estructura:**
```json
{
  "databases": {
    "ppl": {
      "required": true,
      "type": "mysql",
      "host": "192.168.1.100",
      "port": 3306,
      "database": "ppl_database",
      "username": "sentinela_user",
      "password": "encrypted_password",
      "tables": {
        "inmates": "ppl_table"
      },
      "fields_mapping": {
        "pin": "numero_ppl",
        "nombre": "nombre_completo",
        "foto": "ruta_foto"
      }
    },
    "pbx": { ... },
    "carpetas": { ... }
  }
}
```

---

## 🚀 Uso en el Sistema

### Desde el Backend (Python)

```python
from backend.core.database.database_manager import get_database_manager

# Obtener instancia del gestor
manager = get_database_manager()

# Conectar a todas las bases de datos
manager.connect_all()

# Obtener perfil completo de un PPL
profile = manager.get_complete_profile(pin="666")

# Acceder a los datos
ppl_info = profile['ppl_data']
llamadas = profile['pbx_data']
carpetas = profile['carpetas_data']
```

### Desde el Frontend (React)

```typescript
// Obtener perfil completo de un PPL
const response = await axiosInstance.get(`/ppl/profile/666`);

const profile = response.data;
console.log(profile.ppl_data);      // Info del PPL
console.log(profile.pbx_data);      // Llamadas
console.log(profile.carpetas_data); // Expedientes
```

---

## 🔒 Seguridad

### Contraseñas Encriptadas
- Las contraseñas se almacenan encriptadas en el archivo de configuración
- Nunca se exponen en logs o respuestas de API

### Conexiones Seguras
- Soporte para SSL/TLS en todas las bases de datos
- Timeout de conexión configurable
- Pool de conexiones para mejor rendimiento

### Validación de Permisos
- Solo usuarios autenticados pueden acceder a los datos
- Logs de auditoría de todas las consultas
- Rate limiting para prevenir abuso

---

## 📊 Ventajas de esta Arquitectura

### ✅ Escalabilidad
- Fácil agregar nuevas bases de datos
- Adaptadores modulares y reutilizables
- Sin límite de fuentes de datos

### ✅ Flexibilidad
- Soporta diferentes tipos de BD
- Configuración dinámica sin recompilar
- Campos personalizables por instalación

### ✅ Robustez
- Manejo de errores por base de datos
- Continúa funcionando si una BD falla
- Logs detallados para debugging

### ✅ Mantenibilidad
- Código limpio y bien documentado
- Separación de responsabilidades
- Fácil de probar y debuggear

---

## 🛠️ Mantenimiento

### Agregar Nueva Base de Datos

1. Editar `backend/config/database_config.json`
2. Agregar configuración de la nueva BD
3. Reiniciar SENTINELA
4. Verificar estado en `/database/status`

### Modificar Campos de Búsqueda

1. Editar `search_fields` en la configuración
2. Reiniciar SENTINELA
3. Probar búsquedas

### Cambiar Credenciales

1. Ejecutar wizard de configuración nuevamente
2. O editar manualmente el archivo de configuración
3. Reiniciar SENTINELA

---

## 📝 Recomendaciones

### Para Instalación en Producción

1. **Usar cuentas de solo lectura** para las bases de datos externas
2. **Configurar backups** del archivo de configuración
3. **Monitorear conexiones** con `/database/status`
4. **Implementar alertas** si una BD falla
5. **Documentar** el mapeo de campos específico de cada instalación

### Para Desarrollo

1. Usar el archivo `database_config.example.json` como plantilla
2. Crear base de datos de prueba local
3. Probar conexiones antes de producción
4. Validar que todos los campos requeridos existan

---

## 🆘 Solución de Problemas

### Error: "Base de datos PPL no disponible"
- Verificar que el servidor de BD esté corriendo
- Comprobar credenciales en la configuración
- Probar conexión con `/database/test`

### Error: "PIN no encontrado"
- Verificar que el PIN exista en la BD PPL
- Comprobar el mapeo del campo `pin` en la configuración
- Revisar logs del backend para más detalles

### Error: "Timeout de conexión"
- Verificar conectividad de red
- Aumentar timeout en la configuración
- Comprobar firewall y reglas de seguridad

---

## 📞 Soporte

Para más información o soporte técnico, consultar:
- Documentación técnica en `/docs`
- Logs del sistema en `backend/logs/`
- Contactar al equipo de desarrollo

---

**Versión:** 1.0  
**Última actualización:** Diciembre 2025  
**Sistema:** SENTINELA - Sistema de Inteligencia Penitenciaria
