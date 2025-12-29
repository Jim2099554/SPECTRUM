# 🚀 SENTINELA - Guía de GitHub Actions para Build en Windows

**Sin necesidad de máquina Windows física**

---

## 📋 ¿Qué es GitHub Actions?

GitHub Actions es un servicio de CI/CD gratuito que te permite ejecutar código en máquinas virtuales de GitHub, incluyendo Windows, Linux y macOS.

**Ventajas:**
- ✅ **Gratis** para repositorios públicos (2,000 minutos/mes para privados)
- ✅ **Automático** - Se ejecuta al hacer push
- ✅ **Windows nativo** - Compila .exe real de Windows
- ✅ **Sin configuración** - Solo necesitas GitHub

---

## 🎯 Cómo Funciona

1. **Subes tu código** a GitHub
2. **GitHub Actions detecta** el push
3. **Máquina Windows en la nube** compila automáticamente
4. **Descargas el .exe** listo para usar

---

## 📦 Configuración Inicial

### Paso 1: Crear Repositorio en GitHub

```bash
# Si aún no tienes repositorio
cd /Users/jorgeivancantumartinez/CascadeProjects/spectrum
git init
git add .
git commit -m "Initial commit - SENTINELA v1.0"

# Crear repositorio en GitHub (desde la web)
# Luego conectar:
git remote add origin https://github.com/TU_USUARIO/sentinela.git
git branch -M main
git push -u origin main
```

### Paso 2: Verificar Workflow

El archivo `.github/workflows/build-windows.yml` ya está creado y configurado.

**Ubicación:** `.github/workflows/build-windows.yml`

---

## 🚀 Uso del Sistema

### Opción 1: Build Automático (al hacer push)

```bash
# Hacer cambios en tu código
git add .
git commit -m "Actualización de SENTINELA"
git push

# GitHub Actions compilará automáticamente
# Espera 10-15 minutos
# Descarga el ejecutable desde GitHub
```

### Opción 2: Build Manual (desde GitHub)

1. Ve a tu repositorio en GitHub
2. Click en **"Actions"** (menú superior)
3. Selecciona **"Build SENTINELA for Windows"**
4. Click en **"Run workflow"** (botón derecho)
5. Selecciona la rama (main)
6. Click en **"Run workflow"** (botón verde)

**Tiempo estimado:** 10-15 minutos

### Opción 3: Build con Release Tag

```bash
# Crear un release
git tag -a v1.0.0 -m "SENTINELA v1.0.0 - Release inicial"
git push origin v1.0.0

# Esto creará:
# - Build automático
# - Release en GitHub
# - Descarga directa del .exe
```

---

## 📥 Descargar el Ejecutable

### Desde Actions (Artifacts)

1. Ve a **Actions** en GitHub
2. Click en el workflow completado (✅ verde)
3. Scroll hasta **"Artifacts"**
4. Descarga:
   - **SENTINELA-Windows-Executable** (solo .exe)
   - **SENTINELA-Windows-Release** (paquete completo .zip)

### Desde Releases (si usaste tags)

1. Ve a **Releases** en GitHub
2. Click en el release (ej: v1.0.0)
3. Descarga el archivo .zip
4. Descomprime y usa

---

## 📊 Qué Incluye el Build

### Artifact: SENTINELA-Windows-Executable
```
SENTINELA_Backend.exe          [Ejecutable principal]
_internal/                     [Dependencias]
├── backend/
│   ├── client/               [Frontend integrado]
│   ├── config/
│   ├── data/
│   └── transcripts.db
└── [librerías Python...]
```

### Artifact: SENTINELA-Windows-Release (Completo)
```
SENTINELA-Windows-v1.0.0.zip
├── SENTINELA_Backend.exe
├── _internal/
├── start_sentinela.bat       [Script de inicio]
├── LICENSE.txt
├── README.md
├── SISTEMA_LICENCIAS.md
├── DEPLOYMENT_GUIDE.md
└── test_license/             [Licencia de prueba]
    ├── sentinela.lic
    └── LICENSE_INFO.txt
```

---

## 🔧 Configuración del Workflow

### Cuándo se Ejecuta

El workflow se ejecuta automáticamente en:

1. **Push a ramas principales:**
   - `main`
   - `master`
   - `develop`

2. **Pull Requests** a ramas principales

3. **Tags de versión:**
   - `v1.0.0`
   - `v1.1.0`
   - etc.

4. **Manualmente** desde GitHub Actions

### Modificar Configuración

Edita `.github/workflows/build-windows.yml`:

```yaml
# Cambiar ramas que activan el build
on:
  push:
    branches: [ main, master, develop, tu-rama ]
    
# Cambiar versión de Python
- name: Set up Python 3.11
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Cambiar aquí
    
# Cambiar versión de Node
- name: Set up Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '20'  # Cambiar aquí
```

---

## 🎯 Proceso Completo del Workflow

### Paso a Paso

1. **Checkout** - Descarga tu código
2. **Setup Python 3.11** - Instala Python
3. **Setup Node.js 20** - Instala Node
4. **Cache** - Cachea dependencias (más rápido)
5. **Install Python deps** - Instala requirements.txt
6. **Install Node deps** - Instala npm packages
7. **Build Frontend** - Compila React
8. **Copy Frontend** - Copia a backend/client
9. **Create directories** - Crea audios, photos, transcripts
10. **Build Backend** - PyInstaller genera .exe
11. **Verify** - Verifica que el .exe existe
12. **Generate license** - Crea licencia de prueba
13. **Package** - Empaqueta todo en .zip
14. **Upload Artifacts** - Sube a GitHub
15. **Create Release** - Si es tag, crea release

**Duración total:** 10-15 minutos

---

## 📝 Logs y Debugging

### Ver Logs del Build

1. Ve a **Actions** en GitHub
2. Click en el workflow en ejecución
3. Click en **"build-windows"**
4. Expande cada paso para ver logs

### Errores Comunes

#### Error: "Module not found"
**Causa:** Falta dependencia en requirements.txt  
**Solución:** Agregar a `backend/requirements.txt`

#### Error: "npm ERR!"
**Causa:** Error en build de frontend  
**Solución:** Verificar `package.json` y código TypeScript

#### Error: "PyInstaller failed"
**Causa:** Error en spec file o imports  
**Solución:** Verificar `sentinela.spec` y imports de Python

#### Error: "Artifact not found"
**Causa:** Build falló antes de crear artifact  
**Solución:** Revisar logs del paso que falló

---

## 💰 Costos y Límites

### Repositorios Públicos
- ✅ **Gratis ilimitado**
- Sin costo por minutos de build

### Repositorios Privados
- ✅ **2,000 minutos gratis/mes**
- Cada build: ~10-15 minutos
- ~130-200 builds gratis/mes
- Después: $0.008 USD/minuto

### Optimizaciones para Ahorrar Tiempo

1. **Cache de dependencias** (ya incluido)
   - Ahorra ~2-3 minutos por build

2. **Build solo en ramas específicas**
   ```yaml
   on:
     push:
       branches: [ main ]  # Solo main
   ```

3. **Skip CI en commits**
   ```bash
   git commit -m "docs: actualizar README [skip ci]"
   ```

---

## 🔐 Seguridad

### Secrets (Variables Seguras)

Si necesitas API keys o credenciales:

1. Ve a **Settings > Secrets and variables > Actions**
2. Click **"New repository secret"**
3. Agrega tus secrets
4. Úsalos en el workflow:

```yaml
- name: Use secret
  env:
    API_KEY: ${{ secrets.MI_API_KEY }}
  run: echo "API Key configurada"
```

### .gitignore

Asegúrate de no subir:
- `venv/`, `venv311/`
- `node_modules/`
- `dist/`, `build/`
- `.env`
- Credenciales o API keys

---

## 📊 Monitoreo

### Badges de Estado

Agrega a tu README.md:

```markdown
![Build Status](https://github.com/TU_USUARIO/sentinela/workflows/Build%20SENTINELA%20for%20Windows/badge.svg)
```

Muestra: ![Build Status](badge-passing.svg)

### Notificaciones

GitHub te notifica automáticamente:
- ✅ Build exitoso
- ❌ Build fallido
- Por email y en GitHub

---

## 🎯 Workflow Avanzado

### Build Multi-Plataforma

Puedes extender para compilar en múltiples OS:

```yaml
strategy:
  matrix:
    os: [windows-latest, ubuntu-latest, macos-latest]
runs-on: ${{ matrix.os }}
```

### Compilar Instalador Automático

Agregar paso de Inno Setup:

```yaml
- name: Install Inno Setup
  run: choco install innosetup -y
  
- name: Compile Installer
  run: iscc installer.iss
  
- name: Upload Installer
  uses: actions/upload-artifact@v3
  with:
    name: SENTINELA-Installer
    path: installer_output/*.exe
```

---

## 📋 Checklist de Configuración

- [ ] Repositorio creado en GitHub
- [ ] Código subido (git push)
- [ ] Archivo `.github/workflows/build-windows.yml` presente
- [ ] `backend/requirements.txt` completo
- [ ] `frontend/package.json` correcto
- [ ] `sentinela.spec` configurado
- [ ] Primera ejecución de workflow exitosa
- [ ] Artifact descargado y probado

---

## 🆘 Soporte

### Recursos

- **Documentación GitHub Actions:** https://docs.github.com/actions
- **Marketplace:** https://github.com/marketplace?type=actions
- **Community:** https://github.community/

### Problemas Comunes

**"Workflow no se ejecuta"**
- Verificar que `.github/workflows/` esté en la raíz
- Verificar sintaxis YAML
- Verificar que la rama coincida con la configuración

**"Build muy lento"**
- Usar cache (ya incluido)
- Reducir dependencias
- Compilar solo en ramas importantes

**"Artifact muy grande"**
- Normal: 200-300 MB
- PyInstaller incluye todas las dependencias
- Considerar excluir módulos no usados en spec

---

## 🎉 Resumen

**Con GitHub Actions puedes:**
- ✅ Compilar ejecutable Windows sin tener Windows
- ✅ Automatizar el proceso completamente
- ✅ Descargar .exe listo para distribuir
- ✅ Crear releases automáticos
- ✅ Todo gratis (para repos públicos)

**Próximos pasos:**
1. Sube tu código a GitHub
2. El workflow se ejecutará automáticamente
3. Descarga el ejecutable desde Actions
4. ¡Listo para distribuir!

---

**SENTINELA - Sistema de Inteligencia Penitenciaria**  
**© 2025 - Build automatizado con GitHub Actions**
