"""
Wizard de configuración de bases de datos para SENTINELA
Este script guía al usuario en la configuración de las conexiones a bases de datos
"""

import json
import os
from typing import Dict, Any
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


def test_connection(config: Dict[str, Any]) -> bool:
    """Probar conexión a base de datos"""
    try:
        from backend.core.database.database_manager import DatabaseManager
        
        manager = DatabaseManager()
        adapter = manager._create_adapter(config)
        
        if not adapter:
            print(f"❌ Tipo de base de datos no soportado: {config.get('type')}")
            return False
        
        print("🔄 Probando conexión...")
        success = adapter.test_connection()
        adapter.disconnect()
        
        if success:
            print("✅ Conexión exitosa!")
            return True
        else:
            print("❌ No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def configure_ppl_database() -> Dict[str, Any]:
    """Configurar base de datos PPL (obligatoria)"""
    print_step(1, 4, "Configuración Base de Datos PPL (OBLIGATORIA)")
    print("Esta base de datos contiene la información principal de los PPL.")
    print("Debe incluir al menos: PIN, Nombre completo, y otros datos básicos.\n")
    
    config = {
        "required": True,
        "tables": {},
        "fields_mapping": {}
    }
    
    # Tipo de base de datos
    print("Tipos de base de datos soportados:")
    print("  1. MySQL")
    print("  2. PostgreSQL")
    print("  3. Microsoft SQL Server")
    
    db_type_map = {
        "1": "mysql",
        "2": "postgresql",
        "3": "mssql"
    }
    
    db_type_choice = get_input("Seleccione el tipo (1-3)", "1")
    config["type"] = db_type_map.get(db_type_choice, "mysql")
    
    # Conexión
    config["host"] = get_input("Host/IP del servidor", "localhost")
    
    default_ports = {"mysql": 3306, "postgresql": 5432, "mssql": 1433}
    config["port"] = int(get_input("Puerto", str(default_ports.get(config["type"], 3306))))
    
    config["database"] = get_input("Nombre de la base de datos")
    config["username"] = get_input("Usuario")
    config["password"] = getpass("Contraseña: ")
    
    # Configuración de tablas y campos
    print("\n📋 Configuración de Tablas y Campos")
    config["tables"]["inmates"] = get_input("Nombre de la tabla de PPL", "ppl")
    
    print("\nMapeo de campos (nombre del campo en su base de datos):")
    config["fields_mapping"]["pin"] = get_input("Campo PIN/Número de PPL", "numero_ppl")
    config["fields_mapping"]["nombre"] = get_input("Campo Nombre Completo", "nombre_completo")
    config["fields_mapping"]["foto"] = get_input("Campo Ruta de Foto", "foto", required=False)
    config["fields_mapping"]["ingreso"] = get_input("Campo Fecha de Ingreso", "fecha_ingreso", required=False)
    config["fields_mapping"]["delito"] = get_input("Campo Delito", "delito", required=False)
    
    # Probar conexión
    print("\n🔍 Validando configuración...")
    if test_connection(config):
        return config
    else:
        retry = get_yes_no("¿Desea reintentar la configuración?")
        if retry:
            return configure_ppl_database()
        else:
            print("⚠️  ADVERTENCIA: No se pudo conectar a la base de datos PPL")
            print("   El sistema no funcionará correctamente sin esta conexión.")
            return config


def configure_pbx_database() -> Dict[str, Any]:
    """Configurar base de datos PBX (opcional)"""
    print_step(2, 4, "Configuración Base de Datos PBX (OPCIONAL)")
    print("Esta base de datos contiene los registros de llamadas del sistema telefónico.\n")
    
    if not get_yes_no("¿Desea configurar la base de datos PBX?"):
        return None
    
    config = {
        "required": False,
        "tables": {},
        "search_fields": []
    }
    
    # Tipo de base de datos
    print("\nTipos de base de datos soportados:")
    print("  1. MySQL")
    print("  2. PostgreSQL")
    print("  3. Microsoft SQL Server")
    
    db_type_map = {"1": "mysql", "2": "postgresql", "3": "mssql"}
    db_type_choice = get_input("Seleccione el tipo (1-3)", "2")
    config["type"] = db_type_map.get(db_type_choice, "postgresql")
    
    # Conexión
    config["host"] = get_input("Host/IP del servidor", "localhost")
    default_ports = {"mysql": 3306, "postgresql": 5432, "mssql": 1433}
    config["port"] = int(get_input("Puerto", str(default_ports.get(config["type"], 5432))))
    config["database"] = get_input("Nombre de la base de datos")
    config["username"] = get_input("Usuario")
    config["password"] = getpass("Contraseña: ")
    
    # Configuración de tablas
    config["tables"]["calls"] = get_input("Nombre de la tabla de llamadas", "call_records")
    
    # Campos de búsqueda
    print("\nCampos para buscar llamadas (separados por comas):")
    print("Ejemplo: pin, caller_id, extension")
    search_fields = get_input("Campos de búsqueda", "pin,caller_id")
    config["search_fields"] = [f.strip() for f in search_fields.split(",")]
    
    # Probar conexión
    if test_connection(config):
        return config
    else:
        print("⚠️  No se pudo conectar a la base de datos PBX")
        return None


def configure_carpetas_database() -> Dict[str, Any]:
    """Configurar base de datos de Carpetas/Investigaciones (opcional)"""
    print_step(3, 4, "Configuración Base de Datos Carpetas/Investigaciones (OPCIONAL)")
    print("Esta base de datos contiene expedientes e investigaciones relacionadas con PPL.\n")
    
    if not get_yes_no("¿Desea configurar la base de datos de Carpetas?"):
        return None
    
    config = {
        "required": False,
        "tables": {},
        "search_fields": []
    }
    
    # Tipo de base de datos
    print("\nTipos de base de datos soportados:")
    print("  1. MySQL")
    print("  2. PostgreSQL")
    print("  3. Microsoft SQL Server")
    
    db_type_map = {"1": "mysql", "2": "postgresql", "3": "mssql"}
    db_type_choice = get_input("Seleccione el tipo (1-3)", "3")
    config["type"] = db_type_map.get(db_type_choice, "mssql")
    
    # Conexión
    config["host"] = get_input("Host/IP del servidor", "localhost")
    default_ports = {"mysql": 3306, "postgresql": 5432, "mssql": 1433}
    config["port"] = int(get_input("Puerto", str(default_ports.get(config["type"], 1433))))
    config["database"] = get_input("Nombre de la base de datos")
    config["username"] = get_input("Usuario")
    config["password"] = getpass("Contraseña: ")
    
    # Configuración de tablas
    config["tables"]["cases"] = get_input("Nombre de la tabla de carpetas", "carpetas_investigacion")
    
    # Campos de búsqueda
    print("\nCampos para buscar carpetas (separados por comas):")
    print("Ejemplo: pin, numero_expediente, nombre_investigado")
    search_fields = get_input("Campos de búsqueda", "pin,numero_expediente")
    config["search_fields"] = [f.strip() for f in search_fields.split(",")]
    
    # Probar conexión
    if test_connection(config):
        return config
    else:
        print("⚠️  No se pudo conectar a la base de datos de Carpetas")
        return None


def save_configuration(config: Dict[str, Any]):
    """Guardar configuración en archivo JSON"""
    print_step(4, 4, "Guardando Configuración")
    
    config_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'config'
    )
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, 'database_config.json')
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuración guardada en: {config_path}")


def main():
    """Función principal del wizard"""
    print_header("SENTINELA - Asistente de Configuración de Bases de Datos")
    print("Este asistente le ayudará a configurar las conexiones a las bases de datos")
    print("necesarias para el funcionamiento de SENTINELA.\n")
    
    input("Presione ENTER para continuar...")
    
    # Configurar bases de datos
    databases = {}
    
    # 1. PPL (obligatoria)
    ppl_config = configure_ppl_database()
    if ppl_config:
        databases["ppl"] = ppl_config
    
    # 2. PBX (opcional)
    pbx_config = configure_pbx_database()
    if pbx_config:
        databases["pbx"] = pbx_config
    
    # 3. Carpetas (opcional)
    carpetas_config = configure_carpetas_database()
    if carpetas_config:
        databases["carpetas"] = carpetas_config
    
    # Guardar configuración
    config = {"databases": databases}
    save_configuration(config)
    
    # Resumen
    print_header("Configuración Completada")
    print("✅ Bases de datos configuradas:")
    for db_name in databases.keys():
        required = " (OBLIGATORIA)" if databases[db_name].get("required") else " (OPCIONAL)"
        print(f"   - {db_name.upper()}{required}")
    
    print("\n📝 Puede modificar la configuración editando el archivo:")
    print("   backend/config/database_config.json")
    
    print("\n🚀 SENTINELA está listo para usar!")
    print("\nPara iniciar el sistema, ejecute:")
    print("   python -m uvicorn backend.main:app --reload")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
