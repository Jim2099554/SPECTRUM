"""
Wizard Maestro de Configuración Inicial de SENTINELA
Este script coordina todos los wizards de configuración en el orden correcto
"""

import os
import sys

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def print_header(title: str):
    """Imprimir encabezado decorado"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_section(title: str):
    """Imprimir sección"""
    print("\n" + "─" * 70)
    print(f"  {title}")
    print("─" * 70 + "\n")


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Obtener respuesta sí/no del usuario"""
    default_str = "S/n" if default else "s/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    return response in ['s', 'si', 'sí', 'y', 'yes']


def run_pbx_wizard():
    """Ejecutar wizard de configuración de PBX"""
    print_section("1️⃣  CONFIGURACIÓN DE SISTEMA TELEFÓNICO (PBX)")
    print("El PBX permite grabar llamadas automáticamente y enviarlas a SENTINELA")
    print("para transcripción y análisis en tiempo real.\n")
    
    if not get_yes_no("¿Desea configurar la integración con PBX?", True):
        print("⏭️  Saltando configuración de PBX")
        return None
    
    try:
        from backend.scripts import pbx_setup_wizard
        return pbx_setup_wizard.main()
    except Exception as e:
        print(f"❌ Error en configuración de PBX: {e}")
        return None


def run_database_wizard():
    """Ejecutar wizard de configuración de bases de datos"""
    print_section("2️⃣  CONFIGURACIÓN DE BASES DE DATOS")
    print("Las bases de datos permiten a SENTINELA acceder a información de PPL,")
    print("registros de llamadas, y carpetas de investigación.\n")
    
    if not get_yes_no("¿Desea configurar las bases de datos?", True):
        print("⏭️  Saltando configuración de bases de datos")
        return None
    
    try:
        from backend.scripts import database_setup_wizard
        return database_setup_wizard.main()
    except Exception as e:
        print(f"❌ Error en configuración de bases de datos: {e}")
        return None


def show_final_summary(pbx_configured: bool, db_configured: bool):
    """Mostrar resumen final de la configuración"""
    print_header("🎉 CONFIGURACIÓN INICIAL COMPLETADA")
    
    print("Estado de la configuración:\n")
    
    # PBX
    if pbx_configured:
        print("✅ Sistema PBX: CONFIGURADO")
        print("   Archivo: backend/config/pbx_config.json")
    else:
        print("⚠️  Sistema PBX: NO CONFIGURADO")
        print("   SENTINELA funcionará en modo manual (sin grabación automática)")
    
    print()
    
    # Bases de datos
    if db_configured:
        print("✅ Bases de Datos: CONFIGURADAS")
        print("   Archivo: backend/config/database_config.json")
    else:
        print("⚠️  Bases de Datos: NO CONFIGURADAS")
        print("   SENTINELA usará base de datos local SQLite")
    
    print("\n" + "─" * 70)
    print("\n📝 Próximos pasos:\n")
    
    if pbx_configured or db_configured:
        print("1. Revise los archivos de configuración generados")
        print("2. Verifique que las credenciales sean correctas")
        print("3. Asegúrese de que los servicios externos estén accesibles")
    
    print("\n🚀 Para iniciar SENTINELA, ejecute:\n")
    print("   # Modo Centro (con PBX)")
    print("   python -m uvicorn backend.main:app --reload\n")
    print("   # Modo Administración Global")
    print("   python -m uvicorn backend.main_admin:app --reload\n")
    
    print("📚 Documentación adicional:")
    print("   • INSTALLATION.md - Guía de instalación completa")
    print("   • ARQUITECTURA_BASES_DE_DATOS.md - Detalles de bases de datos")
    print("   • README.md - Información general del sistema\n")


def main():
    """Función principal del wizard maestro"""
    print_header("🔧 SENTINELA - Asistente de Configuración Inicial")
    
    print("Bienvenido al asistente de configuración de SENTINELA.")
    print("Este proceso le guiará paso a paso en la configuración de:\n")
    print("  1️⃣  Sistema Telefónico (PBX) - Para grabación automática")
    print("  2️⃣  Bases de Datos - Para información de PPL y registros\n")
    
    print("⏱️  Tiempo estimado: 10-15 minutos")
    print("📝 Tenga a mano las credenciales de acceso a sus sistemas\n")
    
    if not get_yes_no("¿Desea continuar con la configuración?", True):
        print("\n👋 Configuración cancelada. Puede ejecutar este wizard más tarde.")
        return
    
    # Ejecutar wizards en orden
    pbx_configured = False
    db_configured = False
    
    try:
        # 1. Configurar PBX
        pbx_result = run_pbx_wizard()
        pbx_configured = pbx_result is not None
        
        # 2. Configurar Bases de Datos
        db_result = run_database_wizard()
        db_configured = db_result is not None
        
        # Mostrar resumen final
        show_final_summary(pbx_configured, db_configured)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración interrumpida por el usuario")
        print("Puede reanudar ejecutando este wizard nuevamente.")
    except Exception as e:
        print(f"\n\n❌ Error durante la configuración: {e}")
        print("Por favor, revise los errores y ejecute el wizard nuevamente.")


if __name__ == "__main__":
    main()
