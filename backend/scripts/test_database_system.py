"""
Script de prueba del sistema de integración de bases de datos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.database.database_manager import get_database_manager
import json


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_connection():
    """Probar conexión a bases de datos"""
    print_header("TEST 1: Conexión a Bases de Datos")
    
    manager = get_database_manager()
    results = manager.connect_all()
    
    print("\n📊 Resultados de conexión:")
    for db_name, success in results.items():
        status = "✅ Conectado" if success else "❌ Error"
        required = "(OBLIGATORIA)" if manager.adapters[db_name].is_required else "(OPCIONAL)"
        print(f"   {db_name.upper()} {required}: {status}")
    
    return all(results.values())


def test_search_by_pin():
    """Probar búsqueda por PIN"""
    print_header("TEST 2: Búsqueda por PIN")
    
    manager = get_database_manager()
    test_pin = "666"
    
    print(f"\n🔍 Buscando PIN: {test_pin}")
    profile = manager.get_complete_profile(test_pin)
    
    print("\n📋 Datos del PPL:")
    if profile['ppl_data']:
        for key, value in profile['ppl_data'].items():
            print(f"   {key}: {value}")
    else:
        print("   ❌ No se encontraron datos")
    
    print("\n📞 Datos de PBX:")
    if profile['pbx_data']:
        print(f"   ✅ Encontrados")
    else:
        print("   ⚠️  No configurado o sin datos")
    
    print("\n📁 Datos de Carpetas:")
    if profile['carpetas_data']:
        print(f"   ✅ Encontrados")
    else:
        print("   ⚠️  No configurado o sin datos")
    
    if profile['errors']:
        print("\n⚠️  Errores encontrados:")
        for error in profile['errors']:
            print(f"   - {error}")
    
    return profile['ppl_data'] is not None


def test_multiple_pins():
    """Probar búsqueda de múltiples PINs"""
    print_header("TEST 3: Búsqueda de Múltiples PINs")
    
    manager = get_database_manager()
    test_pins = ["666", "777", "888"]
    
    results = {}
    for pin in test_pins:
        print(f"\n🔍 Buscando PIN: {pin}")
        profile = manager.get_complete_profile(pin)
        results[pin] = profile['ppl_data'] is not None
        
        if profile['ppl_data']:
            print(f"   ✅ Encontrado")
        else:
            print(f"   ❌ No encontrado")
    
    found = sum(1 for v in results.values() if v)
    print(f"\n📊 Resumen: {found}/{len(test_pins)} PINs encontrados")
    
    return found > 0


def test_database_status():
    """Probar estado de bases de datos"""
    print_header("TEST 4: Estado de Bases de Datos")
    
    manager = get_database_manager()
    
    print("\n📊 Estado de conexiones:")
    for db_name, adapter in manager.adapters.items():
        status = "🟢 Conectado" if adapter.is_connected else "🔴 Desconectado"
        required = "OBLIGATORIA" if adapter.is_required else "OPCIONAL"
        db_type = adapter.config.get('type', 'unknown').upper()
        
        print(f"\n   {db_name.upper()} ({required})")
        print(f"   Tipo: {db_type}")
        print(f"   Estado: {status}")
        
        if adapter.is_connected:
            # Probar conexión
            test_result = adapter.test_connection()
            print(f"   Test: {'✅ OK' if test_result else '❌ FAIL'}")
    
    return True


def test_configuration():
    """Mostrar configuración actual"""
    print_header("TEST 5: Configuración Actual")
    
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'config/database_config.json'
    )
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"\n📁 Archivo: {config_path}")
        print(f"\n📊 Bases de datos configuradas: {len(config.get('databases', {}))}")
        
        for db_name, db_config in config.get('databases', {}).items():
            print(f"\n   {db_name.upper()}:")
            print(f"   - Tipo: {db_config.get('type')}")
            print(f"   - Obligatoria: {'Sí' if db_config.get('required') else 'No'}")
            if 'host' in db_config:
                print(f"   - Host: {db_config.get('host')}")
            if 'database' in db_config:
                print(f"   - Base de datos: {db_config.get('database')}")
    else:
        print(f"\n⚠️  No se encontró archivo de configuración: {config_path}")
    
    return True


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 60)
    print("  SENTINELA - Test del Sistema de Bases de Datos")
    print("=" * 60)
    
    tests = [
        ("Conexión a Bases de Datos", test_connection),
        ("Búsqueda por PIN", test_search_by_pin),
        ("Búsqueda Múltiple", test_multiple_pins),
        ("Estado de Conexiones", test_database_status),
        ("Configuración", test_configuration)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen final
    print_header("RESUMEN DE PRUEBAS")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n📊 Resultados: {passed}/{total} pruebas exitosas\n")
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("✅ El sistema de bases de datos está funcionando correctamente")
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
        print("   Revisa los errores anteriores para más detalles")
    
    # Cerrar conexiones
    manager = get_database_manager()
    manager.disconnect_all()
    print("\n🔌 Conexiones cerradas")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
