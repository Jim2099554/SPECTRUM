#!/bin/bash
# Script de build para Frontend React de SENTINELA

echo "============================================================"
echo "SENTINELA - Build del Frontend React"
echo "============================================================"
echo ""

# Navegar al directorio frontend
cd frontend || exit 1

# Verificar que Node.js esté instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado"
    echo "   Por favor instale Node.js desde https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js versión: $(node --version)"
echo "✅ npm versión: $(npm --version)"
echo ""

# Instalar dependencias si es necesario
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Error instalando dependencias"
        exit 1
    fi
    echo "✅ Dependencias instaladas"
    echo ""
fi

# Limpiar build anterior
if [ -d "build" ]; then
    echo "🧹 Limpiando build anterior..."
    rm -rf build
fi

# Crear build de producción
echo "🔨 Creando build de producción..."
echo ""
npm run build

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
echo "📁 Archivos generados en: frontend/build/"
echo ""

# Copiar build al directorio del backend
echo "📋 Copiando build al backend..."
cd ..
rm -rf backend/client
cp -r frontend/build backend/client

echo "✅ Build copiado a backend/client/"
echo ""
echo "🎉 Frontend listo para empaquetado"
