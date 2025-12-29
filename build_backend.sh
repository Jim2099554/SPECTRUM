#!/bin/bash
# Script de build para Backend Python de SENTINELA

echo "============================================================"
echo "SENTINELA - Build del Backend Python"
echo "============================================================"
echo ""

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

echo "✅ Python versión: $(python3 --version)"
echo ""

# Activar entorno virtual
if [ -d "venv311" ]; then
    echo "🔧 Activando entorno virtual..."
    source venv311/bin/activate
    echo "✅ Entorno virtual activado"
else
    echo "⚠️  No se encontró venv311, usando Python del sistema"
fi
echo ""

# Instalar/actualizar PyInstaller
echo "📦 Verificando PyInstaller..."
pip install --upgrade pyinstaller
echo ""

# Limpiar builds anteriores
if [ -d "dist" ]; then
    echo "🧹 Limpiando builds anteriores..."
    rm -rf dist
fi

if [ -d "build" ]; then
    rm -rf build
fi

# Crear build con PyInstaller
echo "🔨 Creando ejecutable con PyInstaller..."
echo ""
pyinstaller sentinela.spec --clean

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error en el build"
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ Build completado exitosamente"
echo "============================================================"
echo ""
echo "📁 Ejecutable generado en: dist/SENTINELA_Backend/"
echo ""
echo "🎉 Backend listo para empaquetado"
