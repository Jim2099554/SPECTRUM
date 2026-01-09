"""
Wizard de configuración de PBX para SENTINELA
Este script guía al usuario en la configuración del sistema telefónico (PBX)
"""

import json
import os
from typing import Dict, Any, Optional
from getpass import getpass


def print_header(title: str):
    """Imprimir encabezado decorado"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_step(step: int, total: int, title: str):
    """Imprimir paso actual"""
    print(f"\n[Paso {step}/{total}] {title}")
    print("-" * 60)


def get_input(prompt: str, default: str = None, required: bool = True) -> str:
    """Obtener input del usuario con valor por defecto"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        if not value and default:
            return default
        if not value and required:
            print("⚠️  Este campo es obligatorio")
            continue
        return value


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Obtener respuesta sí/no del usuario"""
    default_str = "S/n" if default else "s/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    return response in ['s', 'si', 'sí', 'y', 'yes']


def test_ami_connection(config: Dict[str, Any]) -> bool:
    """Probar conexión AMI (Asterisk/Grandstream)"""
    try:
        from asterisk.manager import Manager
        
        print("🔄 Probando conexión AMI...")
        manager = Manager()
        manager.connect(config['host'], config['port'])
        manager.login(config['username'], config['password'])
        
        print("✅ Conexión AMI exitosa!")
        manager.logoff()
        return True
    except ImportError:
        print("⚠️  Librería 'asterisk-ami' no instalada. No se puede probar la conexión.")
        print("   Instale con: pip install asterisk-ami")
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False


def select_pbx_type() -> str:
    """Paso 1: Seleccionar tipo de PBX"""
    print_step(1, 2, "Selección de Sistema PBX")
    print("¿Qué sistema PBX utiliza su centro penitenciario?\n")
    
    print("✅ TOTALMENTE COMPATIBLE (Listo para usar)")
    print("  1. Asterisk")
    print("  2. Grandstream UCM (UCM6200, UCM6300, etc.)")
    print("  3. Elastix / Issabel / FreePBX")
    print("  4. FreeSWITCH")
    
    print("\n🔄 COMPATIBLE (Requiere configuración adicional)")
    print("  5. 3CX")
    print("  6. Microsoft Teams")
    
    print("\n⚠️  REQUIERE DESARROLLO PERSONALIZADO")
    print("  7. Cisco CUCM")
    print("  8. Avaya Aura")
    print("  9. Huawei eSpace")
    print("  10. Mitel / NEC / Panasonic")
    
    print("\n❌ SIN PBX")
    print("  11. No usar integración PBX (solo análisis manual de audio)")
    
    choice = get_input("\nSeleccione una opción [1-11]", "1")
    
    pbx_map = {
        "1": "asterisk",
        "2": "grandstream",
        "3": "asterisk",  # Elastix/Issabel son compatibles con Asterisk
        "4": "freeswitch",
        "5": "3cx",
        "6": "teams",
        "7": "cisco",
        "8": "avaya",
        "9": "huawei",
        "10": "other",
        "11": "none"
    }
    
    return pbx_map.get(choice, "none")


def configure_asterisk_ami(pbx_type: str) -> Optional[Dict[str, Any]]:
    """Configuración para Asterisk/Grandstream (AMI)"""
    print_step(2, 2, f"Configuración {pbx_type.upper()} (AMI)")
    print("El protocolo AMI (Asterisk Manager Interface) permite controlar")
    print("el sistema telefónico y grabar llamadas automáticamente.\n")
    
    config = {
        "pbx_type": pbx_type,
        "protocol": "ami",
        "enabled": True,
        "connection": {},
        "recording": {
            "enabled": True,
            "format": "wav",
            "command": "MixMonitor"
        }
    }
    
    # Configuración de conexión
    config["connection"]["host"] = get_input("Host/IP del PBX", "192.168.1.100")
    config["connection"]["port"] = int(get_input("Puerto AMI", "5038"))
    config["connection"]["username"] = get_input("Usuario AMI", "sentinela")
    config["connection"]["password"] = getpass("Contraseña AMI: ")
    
    # Configuración de grabación
    print("\n📁 Configuración de Grabación")
    
    if pbx_type == "grandstream":
        print("Grandstream UCM puede usar 'Monitor' o 'MixMonitor'")
        use_mixmonitor = get_yes_no("¿Usar MixMonitor? (recomendado)", True)
        config["recording"]["command"] = "MixMonitor" if use_mixmonitor else "Monitor"
    
    default_path = "/var/spool/asterisk/monitor/"
    config["recording"]["path"] = get_input("Ruta de archivos de audio", default_path)
    
    # Probar conexión
    print("\n🔍 Validando configuración...")
    if test_ami_connection(config["connection"]):
        return config
    else:
        retry = get_yes_no("¿Desea reintentar la configuración?")
        if retry:
            return configure_asterisk_ami(pbx_type)
        else:
            print("⚠️  Configuración guardada sin validar")
            return config


def configure_freeswitch() -> Optional[Dict[str, Any]]:
    """Configuración para FreeSWITCH (ESL)"""
    print_step(2, 2, "Configuración FreeSWITCH (ESL)")
    print("⚠️  NOTA: FreeSWITCH requiere desarrollo adicional.")
    print("Esta configuración se guardará pero no estará funcional hasta")
    print("que se implemente el adaptador FreeSWITCH.\n")
    
    if not get_yes_no("¿Desea continuar con la configuración?", False):
        return None
    
    config = {
        "pbx_type": "freeswitch",
        "protocol": "esl",
        "enabled": False,  # Deshabilitado hasta implementar adaptador
        "connection": {},
        "recording": {
            "enabled": True,
            "format": "wav"
        }
    }
    
    config["connection"]["host"] = get_input("Host/IP del FreeSWITCH", "localhost")
    config["connection"]["port"] = int(get_input("Puerto ESL", "8021"))
    config["connection"]["password"] = getpass("Contraseña ESL: ")
    
    print("\n⚠️  Configuración guardada. Requiere implementación del adaptador FreeSWITCH.")
    return config


def configure_3cx() -> Optional[Dict[str, Any]]:
    """Configuración para 3CX (REST API)"""
    print_step(2, 2, "Configuración 3CX (REST API)")
    print("⚠️  NOTA: 3CX requiere desarrollo adicional.")
    print("Esta configuración se guardará pero no estará funcional hasta")
    print("que se implemente el adaptador 3CX.\n")
    
    if not get_yes_no("¿Desea continuar con la configuración?", False):
        return None
    
    config = {
        "pbx_type": "3cx",
        "protocol": "rest",
        "enabled": False,  # Deshabilitado hasta implementar adaptador
        "connection": {},
        "recording": {
            "enabled": True,
            "format": "wav"
        }
    }
    
    config["connection"]["host"] = get_input("URL de 3CX", "https://3cx.example.com")
    config["connection"]["username"] = get_input("Usuario API")
    config["connection"]["password"] = getpass("Contraseña API: ")
    
    print("\n⚠️  Configuración guardada. Requiere implementación del adaptador 3CX.")
    return config


def configure_enterprise_pbx(pbx_type: str) -> Optional[Dict[str, Any]]:
    """Configuración para PBX empresariales (Cisco, Avaya, Huawei, etc.)"""
    pbx_names = {
        "cisco": "Cisco CUCM",
        "avaya": "Avaya Aura",
        "huawei": "Huawei eSpace",
        "teams": "Microsoft Teams",
        "other": "Otro PBX"
    }
    
    print_step(2, 2, f"Configuración {pbx_names.get(pbx_type, 'PBX')}")
    print("\n⚠️  IMPORTANTE: Este PBX requiere desarrollo personalizado.")
    print("SENTINELA no incluye soporte nativo para este sistema.\n")
    
    print("Para integrar este PBX necesitará:")
    print("  • Desarrollo de adaptador específico (2-6 semanas)")
    print("  • Posibles licencias CTI/API del fabricante")
    print("  • Documentación técnica del PBX")
    print("  • Soporte técnico especializado\n")
    
    print("💡 Recomendación: Contacte al equipo de desarrollo de SENTINELA")
    print("   para solicitar un presupuesto de integración personalizada.\n")
    
    if not get_yes_no("¿Desea guardar esta selección para referencia futura?", False):
        return None
    
    config = {
        "pbx_type": pbx_type,
        "protocol": "custom",
        "enabled": False,
        "requires_development": True,
        "connection": {},
        "notes": f"Requiere desarrollo de adaptador para {pbx_names.get(pbx_type, 'este PBX')}"
    }
    
    return config


def configure_no_pbx() -> Dict[str, Any]:
    """Configuración sin PBX"""
    print_step(2, 2, "Sin Integración PBX")
    print("Ha seleccionado no usar integración con PBX.")
    print("SENTINELA funcionará en modo manual:\n")
    print("  • Deberá cargar archivos de audio manualmente")
    print("  • No habrá grabación automática de llamadas")
    print("  • Todas las demás funciones estarán disponibles\n")
    
    config = {
        "pbx_type": "none",
        "protocol": "none",
        "enabled": False,
        "connection": {},
        "notes": "Sin integración PBX - Modo manual"
    }
    
    return config


def save_configuration(config: Dict[str, Any]):
    """Guardar configuración en archivo JSON"""
    config_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'config'
    )
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, 'pbx_config.json')
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Configuración PBX guardada en: {config_path}")
    return config_path


def main():
    """Función principal del wizard"""
    print_header("SENTINELA - Asistente de Configuración de PBX")
    print("Este asistente le ayudará a configurar la integración con su")
    print("sistema telefónico (PBX) para grabación automática de llamadas.\n")
    
    input("Presione ENTER para continuar...")
    
    # Paso 1: Seleccionar tipo de PBX
    pbx_type = select_pbx_type()
    
    # Paso 2: Configurar según el tipo
    config = None
    
    if pbx_type in ["asterisk", "grandstream"]:
        config = configure_asterisk_ami(pbx_type)
    elif pbx_type == "freeswitch":
        config = configure_freeswitch()
    elif pbx_type == "3cx":
        config = configure_3cx()
    elif pbx_type in ["cisco", "avaya", "huawei", "teams", "other"]:
        config = configure_enterprise_pbx(pbx_type)
    elif pbx_type == "none":
        config = configure_no_pbx()
    
    if not config:
        print("\n⚠️  Configuración de PBX cancelada")
        return None
    
    # Guardar configuración
    config_path = save_configuration(config)
    
    # Resumen
    print_header("Configuración de PBX Completada")
    
    pbx_status = "✅ ACTIVO" if config.get("enabled") else "⚠️  INACTIVO"
    print(f"Sistema PBX: {config['pbx_type'].upper()} {pbx_status}")
    print(f"Protocolo: {config.get('protocol', 'N/A').upper()}")
    
    if config.get("requires_development"):
        print("\n⚠️  ATENCIÓN: Este PBX requiere desarrollo personalizado")
        print("   Contacte al equipo de SENTINELA para más información")
    elif config.get("enabled"):
        print("\n✅ El sistema PBX está configurado y listo para usar")
    else:
        print("\n⚠️  El sistema PBX está configurado pero inactivo")
        print("   Se requiere desarrollo adicional para activarlo")
    
    return config_path


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
