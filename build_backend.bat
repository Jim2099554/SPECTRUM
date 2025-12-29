@echo off
REM Script de build para Backend Python de SENTINELA (Windows)

echo ============================================================
echo SENTINELA - Build del Backend Python
echo ============================================================

REM Verificar Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: Python no esta instalado
    echo Por favor instale Python 3.11+ desde https://www.python.org/
    exit /b 1
)

echo ✅ Python version:
python --version
echo.

REM Verificar que existe el entorno virtual o las dependencias
if not exist venv (
    echo ⚠️  No se encontro entorno virtual
    echo 📦 Instalando dependencias globalmente...
    python -m pip install --upgrade pip
    pip install -r backend\requirements.txt
    pip install pyinstaller
) else (
    echo 🔧 Activando entorno virtual...
    call venv\Scripts\activate.bat
    if %ERRORLEVEL% NEQ 0 (
        echo ⚠️  No se pudo activar entorno virtual, usando Python global
    ) else (
        echo ✅ Entorno virtual activado
    )
)

echo.
echo 📦 Verificando PyInstaller...
pip install --upgrade pyinstaller

echo.
echo 🔨 Creando ejecutable con PyInstaller...
echo.

REM Crear directorios necesarios si no existen
if not exist backend\audios mkdir backend\audios
if not exist backend\photos mkdir backend\photos
if not exist backend\transcripts mkdir backend\transcripts

REM Ejecutar PyInstaller
pyinstaller sentinela.spec --clean --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error en el build
    exit /b 1
)

echo.
echo ============================================================
echo ✅ Build completado exitosamente
echo ============================================================
echo.
echo 📁 Ejecutable generado en: dist\SENTINELA_Backend\
echo 🎉 Backend listo para empaquetado
echo.
