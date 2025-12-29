"""
Script de prueba del sistema de licencias USB
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
from scripts.generate_license import LicenseGenerator
from core.licensing.license_manager import LicenseManager


def test_license_generation():
    """Probar generación de licencias"""
    print("\n" + "=" * 60)
    print("TEST 1: Generación de Licencia")
    print("=" * 60)
    
    generator = LicenseGenerator()
    
    # Crear licencia de prueba
    output_path = Path("./test_licenses")
    output_path.mkdir(exist_ok=True)
    
    license_data = generator.create_license(
        client_name="Cliente de Prueba",
        institution="Institución de Prueba",
        validity_days=30,
        max_users=3,
        output_path=output_path
    )
    
    print(f"✅ Licencia generada")
    print(f"   Clave: {license_data['license_key']}")
    print(f"   Cliente: {license_data['client_name']}")
    print(f"   Expira: {license_data['expiry_date'][:10]}")
    
    return output_path


def test_license_reading(license_path: Path):
    """Probar lectura de licencias"""
    print("\n" + "=" * 60)
    print("TEST 2: Lectura de Licencia")
    print("=" * 60)
    
    manager = LicenseManager()
    
    # Leer licencia
    license_file = license_path / "sentinela.lic"
    if not license_file.exists():
        print("❌ Archivo de licencia no encontrado")
        return False
    
    license_data = manager.read_license(license_file)
    
    if license_data:
        print(f"✅ Licencia leída correctamente")
        print(f"   Cliente: {license_data.get('client_name', 'N/A')}")
        print(f"   Institución: {license_data.get('institution', 'N/A')}")
        return True
    else:
        print("❌ Error al leer licencia")
        return False


def test_license_validation(license_path: Path):
    """Probar validación de licencias"""
    print("\n" + "=" * 60)
    print("TEST 3: Validación de Licencia")
    print("=" * 60)
    
    manager = LicenseManager()
    license_file = license_path / "sentinela.lic"
    
    license_data = manager.read_license(license_file)
    if not license_data:
        print("❌ No se pudo leer la licencia")
        return False
    
    is_valid, message = manager.validate_license(license_data)
    
    if is_valid:
        print(f"✅ {message}")
        return True
    else:
        print(f"❌ {message}")
        return False


def test_hardware_id():
    """Probar obtención de Hardware ID"""
    print("\n" + "=" * 60)
    print("TEST 4: Hardware ID")
    print("=" * 60)
    
    manager = LicenseManager()
    hw_id = manager.get_hardware_id()
    
    print(f"✅ Hardware ID obtenido: {hw_id}")
    print(f"   Longitud: {len(hw_id)} caracteres")
    
    return True


def test_usb_detection():
    """Probar detección de USBs"""
    print("\n" + "=" * 60)
    print("TEST 5: Detección de USBs")
    print("=" * 60)
    
    manager = LicenseManager()
    usb_drives = manager.find_usb_drives()
    
    print(f"✅ USBs detectados: {len(usb_drives)}")
    for drive in usb_drives:
        print(f"   - {drive}")
    
    return True


def cleanup(license_path: Path):
    """Limpiar archivos de prueba"""
    print("\n" + "=" * 60)
    print("LIMPIEZA")
    print("=" * 60)
    
    try:
        import shutil
        shutil.rmtree(license_path)
        print("✅ Archivos de prueba eliminados")
    except Exception as e:
        print(f"⚠️  No se pudieron eliminar archivos: {e}")


def main():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 60)
    print("SENTINELA - Test del Sistema de Licencias USB")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Generación
    try:
        license_path = test_license_generation()
        results["Generación"] = True
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Generación"] = False
        return
    
    # Test 2: Lectura
    try:
        results["Lectura"] = test_license_reading(license_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Lectura"] = False
    
    # Test 3: Validación
    try:
        results["Validación"] = test_license_validation(license_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Validación"] = False
    
    # Test 4: Hardware ID
    try:
        results["Hardware ID"] = test_hardware_id()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Hardware ID"] = False
    
    # Test 5: Detección USB
    try:
        results["Detección USB"] = test_usb_detection()
    except Exception as e:
        print(f"❌ Error: {e}")
        results["Detección USB"] = False
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n📊 Resultados: {passed}/{total} tests exitosos\n")
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron!")
        print("✅ Sistema de licencias funcionando correctamente")
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
    
    # Limpiar
    cleanup(license_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrumpidos")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
