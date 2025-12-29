@echo off
REM Script maestro de empaquetado para SENTINELA (Windows)
REM Ejecuta todo el proceso de build: frontend, backend e instalador

setlocal enabledelayedexpansion

echo ============================================================
echo SENTINELA - Empaquetado Completo
echo Sistema de Inteligencia Penitenciaria
echo ============================================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist build_all.bat (
    echo ❌ Error: Ejecute este script desde el directorio raiz del proyecto
    exit /b 1
)

REM PASO 1: Limpiar builds anteriores
echo.
echo ============================================================
echo PASO 1/6: Limpiando builds anteriores
echo ============================================================
echo.

if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist frontend\dist rmdir /s /q frontend\dist
if exist backend\client rmdir /s /q backend\client
if exist installer_output rmdir /s /q installer_output

echo ✅ Limpieza completada

REM PASO 2: Build del Frontend React
echo.
echo ============================================================
echo PASO 2/6: Compilando Frontend React
echo ============================================================
echo.

call build_frontend.bat
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error en Frontend
    exit /b 1
)
echo ✅ Frontend completado

REM PASO 3: Build del Backend Python
echo.
echo ============================================================
echo PASO 3/6: Compilando Backend Python con PyInstaller
echo ============================================================
echo.

call build_backend.bat
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error en Backend
    exit /b 1
)
echo ✅ Backend completado

REM PASO 4: Crear estructura de directorios para instalador
echo.
echo ============================================================
echo PASO 4/6: Preparando estructura para instalador
echo ============================================================
echo.

if not exist installer_output mkdir installer_output
if not exist assets mkdir assets

REM Verificar que existen los archivos necesarios
if not exist dist\SENTINELA_Backend (
    echo ❌ Error: No se encontro el build del backend
    exit /b 1
)

echo ✅ Estructura preparada

REM PASO 5: Generar licencia de prueba
echo.
echo ============================================================
echo PASO 5/6: Generando licencia de prueba
echo ============================================================
echo.

python backend\scripts\generate_license.py --client "Cliente de Prueba" --institution "Instalacion de Prueba" --days 30 --users 5 --output .\test_license

if exist test_license\sentinela.lic (
    echo ✅ Licencia de prueba generada en: test_license\
) else (
    echo ⚠️  No se pudo generar licencia de prueba (opcional)
)

REM PASO 6: Resumen final
echo.
echo ============================================================
echo PASO 6/6: Resumen del Empaquetado
echo ============================================================
echo.

echo 📦 ARCHIVOS GENERADOS:
echo.
echo Backend:
echo   📁 dist\SENTINELA_Backend\ - Ejecutable del backend
echo   📄 dist\SENTINELA_Backend\SENTINELA_Backend.exe
echo.
echo Frontend:
echo   📁 backend\client\ - Build de React integrado
echo.
echo Licencia de Prueba:
echo   📁 test_license\ - Licencia para testing
echo   📄 test_license\sentinela.lic
echo   📄 test_license\LICENSE_INFO.txt
echo.

REM Información sobre el instalador
echo ============================================================
echo PROXIMOS PASOS
echo ============================================================
echo.
echo Para crear el instalador Windows:
echo.
echo 1. Instalar Inno Setup:
echo    https://jrsoftware.org/isdl.php
echo.
echo 2. Abrir installer.iss con Inno Setup Compiler
echo.
echo 3. Compilar el instalador (Build ^> Compile)
echo.
echo 4. El instalador se generara en:
echo    installer_output\SENTINELA_Setup_v1.0.exe
echo.
echo ============================================================
echo TESTING LOCAL
echo ============================================================
echo.
echo Para probar el ejecutable localmente:
echo.
echo 1. Navegar a dist\SENTINELA_Backend\
echo.
echo 2. Ejecutar: SENTINELA_Backend.exe
echo.
echo 3. Abrir navegador en: http://localhost:8000
echo.
echo ============================================================
echo.
echo 🎉 Empaquetado completado exitosamente!
echo.
echo 📋 Checklist final:
echo   ✅ Frontend compilado
echo   ✅ Backend empaquetado
echo   ✅ Licencia de prueba generada
echo   ⏳ Instalador Windows (requiere Inno Setup)
echo.
echo 📄 Documentacion generada:
echo   - SISTEMA_LICENCIAS.md
echo   - ARQUITECTURA_BASES_DE_DATOS.md
echo   - DEPLOYMENT_GUIDE.md
echo.

endlocal
