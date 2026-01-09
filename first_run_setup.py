"""
Script de instalación y configuración inicial de SENTINELA
Este script se ejecuta automáticamente la primera vez que se inicia SENTINELA
"""

import os
import sys
import json


def check_first_run():
    """Verificar si es la primera ejecución"""
    # Buscar archivos de configuración
    config_dir = os.path.join(os.path.dirname(__file__), 'backend', 'config')
    
    pbx_config = os.path.join(config_dir, 'pbx_config.json')
    db_config = os.path.join(config_dir, 'database_config.json')
    
    # Si no existen configuraciones, es primera ejecución
    return not (os.path.exists(pbx_config) or os.path.exists(db_config))


def run_initial_setup():
    """Ejecutar wizard de configuración inicial"""
    print("=" * 70)
    print("  🎉 ¡Bienvenido a SENTINELA!")
    print("=" * 70)
    print("\nParece ser la primera vez que ejecuta SENTINELA.")
    print("Vamos a configurar el sistema paso a paso.\n")
    
    try:
        # Importar y ejecutar wizard maestro
        from backend.scripts.initial_setup_wizard import main as setup_main
        setup_main()
        return True
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        print("\nPuede ejecutar la configuración manualmente más tarde con:")
        print("   python backend/scripts/initial_setup_wizard.py")
        return False


def main():
    """Función principal"""
    if check_first_run():
        print("\n🔧 Primera ejecución detectada - Iniciando configuración...\n")
        
        if run_initial_setup():
            print("\n✅ Configuración completada exitosamente!")
            print("\nSENTINELA está listo para usar.")
        else:
            print("\n⚠️  Configuración incompleta.")
            print("SENTINELA funcionará con configuración por defecto.")
    else:
        print("✅ SENTINELA ya está configurado.")
        print("\nPara reconfigurar, ejecute:")
        print("   python backend/scripts/initial_setup_wizard.py")


if __name__ == "__main__":
    main()
