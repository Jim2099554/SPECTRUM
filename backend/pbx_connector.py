"""
Script de ejemplo para usar el sistema PBX con SENTINELA
Demuestra cómo inicializar y usar el adaptador de PBX
"""

import time
from backend.core.pbx import get_pbx_adapter


def on_call_start(event_data):
    """Manejador cuando inicia una llamada"""
    print(f"\n🔔 NUEVA LLAMADA")
    print(f"   ID: {event_data['call_id']}")
    print(f"   Origen: {event_data['caller_id']}")
    print(f"   Destino: {event_data['destination']}")
    print(f"   Canal: {event_data['channel']}")


def on_call_end(event_data):
    """Manejador cuando termina una llamada"""
    print(f"\n📞 LLAMADA FINALIZADA")
    print(f"   ID: {event_data['call_id']}")
    print(f"   Duración: {event_data['duration']}s")
    print(f"   Audio: {event_data['audio_path']}")
    
    # Aquí enviarías el audio a SENTINELA para transcripción
    # send_to_sentinela(event_data['audio_path'], event_data['call_id'])


def main():
    """Función principal"""
    print("=" * 60)
    print("  SENTINELA - Sistema de Grabación PBX")
    print("=" * 60)
    
    # Obtener adaptador de PBX según configuración
    pbx = get_pbx_adapter()
    
    # Registrar manejadores de eventos
    pbx.register_event_handler('call_start', on_call_start)
    pbx.register_event_handler('call_end', on_call_end)
    
    # Conectar al PBX
    if not pbx.connect():
        print("\n❌ No se pudo conectar al PBX")
        print("   Verifique la configuración en backend/config/pbx_config.json")
        return
    
    # Iniciar escucha de eventos
    pbx.start_listening()
    
    print("\n✅ Sistema PBX activo")
    print("👂 Escuchando llamadas...")
    print("\nPresione Ctrl+C para detener\n")
    
    # Mantener el programa en ejecución
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo sistema PBX...")
        pbx.disconnect()
        print("👋 Sistema detenido")


if __name__ == "__main__":
    main()
