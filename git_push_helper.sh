#!/bin/bash
# Helper script para hacer push a GitHub con token

# Tu información de GitHub
GITHUB_USER="Jim2099554"
GITHUB_TOKEN="github_pat_11B0MVMY0N6yV78PNSckD_X0Uq2YvxfcYG0ZwBk4FkHRmm09C"
REPO_NAME="sentinela"

echo "🔧 Configurando Git para push automático..."

# Configurar remote con token embebido
git remote set-url origin https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git

echo "✅ Configuración completada"
echo ""
echo "📤 Haciendo push a GitHub..."

# Hacer push
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡Push exitoso!"
    echo ""
    echo "📍 Tu código está en: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo "🚀 GitHub Actions comenzará a compilar automáticamente"
    echo "⏱️  Tiempo estimado: 10-15 minutos"
    echo ""
    echo "Para ver el progreso:"
    echo "👉 https://github.com/${GITHUB_USER}/${REPO_NAME}/actions"
else
    echo ""
    echo "❌ Error en el push"
    echo "Verifica que el repositorio exista en GitHub"
fi
