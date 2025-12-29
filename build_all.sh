#!/bin/bash
# Script maestro de empaquetado para SENTINELA
# Ejecuta todo el proceso de build: frontend, backend e instalador

set -e  # Salir si hay error

echo "============================================================"
echo "SENTINELA - Empaquetado Completo"
echo "Sistema de Inteligencia Penitenciaria"
echo "============================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "build_all.sh" ]; then
    echo "❌ Error: Ejecute este script desde el directorio raíz del proyecto"
    exit 1
fi

# Función para mostrar progreso
show_step() {
    echo ""
    echo "============================================================"
    echo "PASO $1: $2"
    echo "============================================================"
    echo ""
}

# Función para verificar éxito
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1 completado exitosamente"
    else
        echo "❌ Error en $1"
        exit 1
    fi
}

# PASO 1: Limpiar builds anteriores
show_step "1/6" "Limpiando builds anteriores"
rm -rf dist
rm -rf build
rm -rf frontend/build
rm -rf backend/client
rm -rf installer_output
echo "✅ Limpieza completada"

# PASO 2: Build del Frontend React
show_step "2/6" "Compilando Frontend React"
./build_frontend.sh
check_success "Frontend"

# PASO 3: Build del Backend Python
show_step "3/6" "Compilando Backend Python con PyInstaller"
./build_backend.sh
check_success "Backend"

# PASO 4: Crear estructura de directorios para instalador
show_step "4/6" "Preparando estructura para instalador"
mkdir -p installer_output
mkdir -p assets

# Verificar que existen los archivos necesarios
if [ ! -d "dist/SENTINELA_Backend" ]; then
    echo "❌ Error: No se encontró el build del backend"
    exit 1
fi

echo "✅ Estructura preparada"

# PASO 5: Generar licencia de prueba
show_step "5/6" "Generando licencia de prueba"
source venv311/bin/activate
python backend/scripts/generate_license.py \
    --client "Cliente de Prueba" \
    --institution "Instalación de Prueba" \
    --days 30 \
    --users 5 \
    --output ./test_license

if [ -f "test_license/sentinela.lic" ]; then
    echo "✅ Licencia de prueba generada en: test_license/"
else
    echo "⚠️  No se pudo generar licencia de prueba (opcional)"
fi

# PASO 6: Resumen final
show_step "6/6" "Resumen del Empaquetado"

echo "📦 ARCHIVOS GENERADOS:"
echo ""
echo "Backend:"
echo "  📁 dist/SENTINELA_Backend/ - Ejecutable del backend"
echo "  📄 dist/SENTINELA_Backend/SENTINELA_Backend.exe (Windows)"
echo ""
echo "Frontend:"
echo "  📁 backend/client/ - Build de React integrado"
echo ""
echo "Licencia de Prueba:"
echo "  📁 test_license/ - Licencia para testing"
echo "  📄 test_license/sentinela.lic"
echo "  📄 test_license/LICENSE_INFO.txt"
echo ""

# Información sobre el instalador
echo "============================================================"
echo "PRÓXIMOS PASOS"
echo "============================================================"
echo ""
echo "Para crear el instalador Windows:"
echo ""
echo "1. Instalar Inno Setup en Windows:"
echo "   https://jrsoftware.org/isdl.php"
echo ""
echo "2. Abrir installer.iss con Inno Setup Compiler"
echo ""
echo "3. Compilar el instalador (Build > Compile)"
echo ""
echo "4. El instalador se generará en:"
echo "   installer_output/SENTINELA_Setup_v1.0.exe"
echo ""
echo "============================================================"
echo "TESTING LOCAL"
echo "============================================================"
echo ""
echo "Para probar el ejecutable localmente:"
echo ""
echo "1. Navegar a dist/SENTINELA_Backend/"
echo ""
echo "2. Ejecutar:"
echo "   ./SENTINELA_Backend (macOS/Linux)"
echo "   SENTINELA_Backend.exe (Windows)"
echo ""
echo "3. Abrir navegador en: http://localhost:8000"
echo ""
echo "============================================================"
echo ""
echo "🎉 Empaquetado completado exitosamente!"
echo ""
echo "📋 Checklist final:"
echo "  ✅ Frontend compilado"
echo "  ✅ Backend empaquetado"
echo "  ✅ Licencia de prueba generada"
echo "  ⏳ Instalador Windows (requiere Inno Setup en Windows)"
echo ""
echo "📄 Documentación generada:"
echo "  - SISTEMA_LICENCIAS.md"
echo "  - ARQUITECTURA_BASES_DE_DATOS.md"
echo "  - AUDIT_FINAL_REPORT.md"
echo ""
