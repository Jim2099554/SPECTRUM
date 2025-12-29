#!/bin/bash
# Sincroniza risk_phrases_corrected.json para backend y frontend
# Ejecuta este script desde la raíz del proyecto

SRC="$(pwd)/data/risk_phrases_corrected.json"
FRONTEND="$(pwd)/frontend/tailadmin-react/src/data/risk_phrases_corrected.json"
BACKEND="$(pwd)/backend/data/risk_phrases_corrected.json"

# Copia al frontend
if [ -f "$SRC" ]; then
  cp "$SRC" "$FRONTEND"
  echo "✔ Copiado a $FRONTEND"
else
  echo "❌ No se encontró $SRC"
fi

# Copia al backend (opcional, si usas esa ruta)
if [ -d "$(pwd)/backend/data" ]; then
  cp "$SRC" "$BACKEND"
  echo "✔ Copiado a $BACKEND"
fi

echo "Sincronización completa."
