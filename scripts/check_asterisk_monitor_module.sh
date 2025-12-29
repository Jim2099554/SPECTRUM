#!/bin/bash
# Verifica si el módulo res_monitor.so está cargado en Asterisk

OUTPUT=$(sudo asterisk -rx "module show like monitor")

if echo "$OUTPUT" | grep -q "res_monitor.so"; then
    echo "✅ El módulo res_monitor.so está cargado correctamente."
    exit 0
else
    echo "❌ El módulo res_monitor.so NO está cargado."
    exit 1
fi
