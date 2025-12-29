@echo off
REM Script de inicio para SENTINELA
REM Sistema de Inteligencia Penitenciaria

title SENTINELA - Sistema de Inteligencia Penitenciaria

echo ============================================================
echo SENTINELA - Iniciando Sistema
echo ============================================================
echo.

REM Cambiar al directorio de instalación
cd /d "%~dp0"

REM Verificar que el ejecutable existe
if not exist "backend\SENTINELA_Backend.exe" (
    echo ERROR: No se encontro el ejecutable del backend
    echo Por favor reinstale SENTINELA
    pause
    exit /b 1
)

REM Iniciar el backend
echo Iniciando servidor backend...
start "SENTINELA Backend" /MIN "backend\SENTINELA_Backend.exe"

REM Esperar a que el servidor inicie
timeout /t 5 /nobreak > nul

REM Abrir navegador con la aplicación
echo Abriendo interfaz web...
start http://localhost:8000

echo.
echo ============================================================
echo SENTINELA iniciado correctamente
echo ============================================================
echo.
echo La aplicacion se abrira en su navegador predeterminado
echo Para cerrar SENTINELA, cierre esta ventana
echo.
echo Presione cualquier tecla para ver los logs del servidor...
pause > nul

REM Mostrar logs (el proceso ya está corriendo en segundo plano)
echo.
echo Sistema en ejecucion. Cierre esta ventana para detener SENTINELA.
echo.

REM Mantener la ventana abierta
:loop
timeout /t 60 /nobreak > nul
goto loop
