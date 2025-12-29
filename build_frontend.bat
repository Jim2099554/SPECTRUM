@echo off
REM Script de build para Frontend React de SENTINELA (Windows)

echo ============================================================
echo SENTINELA - Build del Frontend React
echo ============================================================

REM Verificar Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: Node.js no esta instalado
    echo Por favor instale Node.js desde https://nodejs.org/
    exit /b 1
)

echo ✅ Node.js version:
node --version
echo ✅ npm version:
npm --version
echo.

REM Ir al directorio del frontend
cd frontend
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: No se encontro el directorio frontend
    exit /b 1
)

echo 🔨 Creando build de produccion...
echo.

REM Build de produccion
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error en el build
    cd ..
    exit /b 1
)

cd ..

echo.
echo ============================================================
echo ✅ Build completado exitosamente
echo ============================================================
echo.
echo 📁 Archivos generados en: frontend\dist\
echo 📋 Copiando build al backend...

REM Eliminar directorio anterior si existe
if exist backend\client (
    rmdir /s /q backend\client
)

REM Copiar build al backend
xcopy /E /I /Y frontend\dist backend\client
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Advertencia: No se pudo copiar el build al backend
) else (
    echo ✅ Build copiado a backend\client\
)

echo.
echo 🎉 Frontend listo para empaquetado
echo.
