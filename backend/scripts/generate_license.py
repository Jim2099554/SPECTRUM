"""
Generador de Licencias USB para SENTINELA
Crea archivos de licencia encriptados para distribuir en USBs
"""

import json
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
import argparse


class LicenseGenerator:
    """Generador de licencias USB"""
    
    def __init__(self):
        self.encryption_key = "SENTINELA_2025_SECURE_KEY"
    
    def generate_license_key(self) -> str:
        """Generar clave de licencia única"""
        # Formato: SENT-XXXX-XXXX-XXXX-XXXX
        parts = []
        for _ in range(4):
            part = secrets.token_hex(2).upper()
            parts.append(part)
        return f"SENT-{'-'.join(parts)}"
    
    def create_signature(self, license_key: str, client_name: str, expiry_date: str) -> str:
        """Crear firma digital de la licencia"""
        data_string = f"{license_key}{client_name}{expiry_date}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def encrypt_data(self, data: str) -> str:
        """Encriptar datos con XOR"""
        encrypted = bytearray()
        for i, char in enumerate(data):
            encrypted.append(ord(char) ^ ord(self.encryption_key[i % len(self.encryption_key)]))
        return encrypted.hex()
    
    def create_license(
        self,
        client_name: str,
        institution: str,
        validity_days: int = 365,
        max_users: int = 5,
        modules: list = None,
        hardware_id: str = None,
        output_path: Path = None
    ) -> dict:
        """
        Crear archivo de licencia
        
        Args:
            client_name: Nombre del cliente
            institution: Institución/Organización
            validity_days: Días de validez (default: 365)
            max_users: Número máximo de usuarios simultáneos
            modules: Lista de módulos habilitados
            hardware_id: ID de hardware (opcional, para vincular a equipo específico)
            output_path: Ruta donde guardar el archivo
        """
        if modules is None:
            modules = ["dashboard", "analytics", "network", "alerts", "reports"]
        
        # Generar datos de licencia
        license_key = self.generate_license_key()
        issue_date = datetime.now()
        expiry_date = issue_date + timedelta(days=validity_days)
        
        license_data = {
            "license_key": license_key,
            "client_name": client_name,
            "institution": institution,
            "issue_date": issue_date.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "max_users": max_users,
            "modules": modules,
            "version": "1.0",
            "revoked": False
        }
        
        # Agregar hardware ID si se proporciona
        if hardware_id:
            license_data["hardware_id"] = hardware_id
        
        # Crear firma
        license_data["signature"] = self.create_signature(
            license_key,
            client_name,
            expiry_date.isoformat()
        )
        
        # Convertir a JSON
        json_data = json.dumps(license_data, indent=2)
        
        # Encriptar
        encrypted_data = self.encrypt_data(json_data)
        
        # Guardar archivo
        if output_path:
            output_file = output_path / "sentinela.lic"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(encrypted_data)
            print(f"✅ Licencia generada: {output_file}")
        
        return license_data
    
    def create_license_info_file(self, license_data: dict, output_path: Path):
        """Crear archivo de información legible (para referencia)"""
        info_file = output_path / "LICENSE_INFO.txt"
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("SENTINELA - INFORMACIÓN DE LICENCIA\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Clave de Licencia: {license_data['license_key']}\n")
            f.write(f"Cliente: {license_data['client_name']}\n")
            f.write(f"Institución: {license_data['institution']}\n")
            f.write(f"Fecha de Emisión: {license_data['issue_date'][:10]}\n")
            f.write(f"Fecha de Expiración: {license_data['expiry_date'][:10]}\n")
            f.write(f"Usuarios Máximos: {license_data['max_users']}\n")
            f.write(f"Módulos Habilitados: {', '.join(license_data['modules'])}\n")
            
            if 'hardware_id' in license_data:
                f.write(f"Hardware ID: {license_data['hardware_id']}\n")
                f.write("⚠️  Esta licencia está vinculada a un equipo específico\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("INSTRUCCIONES DE USO\n")
            f.write("=" * 60 + "\n\n")
            f.write("1. Copie el archivo 'sentinela.lic' a una memoria USB\n")
            f.write("2. Conecte el USB al equipo donde instalará SENTINELA\n")
            f.write("3. Inicie SENTINELA - detectará automáticamente la licencia\n")
            f.write("4. Mantenga el USB conectado mientras usa el sistema\n\n")
            f.write("⚠️  IMPORTANTE:\n")
            f.write("   - No modifique el archivo sentinela.lic\n")
            f.write("   - No comparta este USB con otros equipos\n")
            f.write("   - Guarde una copia de seguridad en lugar seguro\n\n")
            f.write("Soporte Técnico: soporte@sentinela.com\n")
        
        print(f"✅ Información guardada: {info_file}")


def main():
    """Función principal con interfaz de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Generador de Licencias USB para SENTINELA'
    )
    
    parser.add_argument('--client', required=True, help='Nombre del cliente')
    parser.add_argument('--institution', required=True, help='Institución/Organización')
    parser.add_argument('--days', type=int, default=365, help='Días de validez (default: 365)')
    parser.add_argument('--users', type=int, default=5, help='Usuarios máximos (default: 5)')
    parser.add_argument('--hardware-id', help='ID de hardware (opcional)')
    parser.add_argument('--output', required=True, help='Directorio de salida')
    parser.add_argument(
        '--modules',
        nargs='+',
        default=['dashboard', 'analytics', 'network', 'alerts', 'reports'],
        help='Módulos habilitados'
    )
    
    args = parser.parse_args()
    
    # Crear directorio de salida
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generar licencia
    generator = LicenseGenerator()
    
    print("\n" + "=" * 60)
    print("SENTINELA - Generador de Licencias USB")
    print("=" * 60 + "\n")
    
    license_data = generator.create_license(
        client_name=args.client,
        institution=args.institution,
        validity_days=args.days,
        max_users=args.users,
        modules=args.modules,
        hardware_id=args.hardware_id,
        output_path=output_path
    )
    
    # Crear archivo de información
    generator.create_license_info_file(license_data, output_path)
    
    print("\n" + "=" * 60)
    print("RESUMEN DE LICENCIA")
    print("=" * 60)
    print(f"\n✅ Licencia generada exitosamente")
    print(f"   Clave: {license_data['license_key']}")
    print(f"   Cliente: {license_data['client_name']}")
    print(f"   Válida hasta: {license_data['expiry_date'][:10]}")
    print(f"   Usuarios: {license_data['max_users']}")
    print(f"\n📁 Archivos generados en: {output_path}")
    print(f"   - sentinela.lic (archivo de licencia)")
    print(f"   - LICENSE_INFO.txt (información de referencia)")
    print("\n💡 Próximos pasos:")
    print("   1. Copie sentinela.lic a una memoria USB")
    print("   2. Entregue el USB al cliente")
    print("   3. Guarde LICENSE_INFO.txt para sus registros")
    print()


def interactive_mode():
    """Modo interactivo para generar licencias"""
    print("\n" + "=" * 60)
    print("SENTINELA - Generador de Licencias USB (Modo Interactivo)")
    print("=" * 60 + "\n")
    
    # Solicitar información
    client_name = input("Nombre del cliente: ").strip()
    institution = input("Institución/Organización: ").strip()
    
    validity_input = input("Días de validez [365]: ").strip()
    validity_days = int(validity_input) if validity_input else 365
    
    users_input = input("Usuarios máximos [5]: ").strip()
    max_users = int(users_input) if users_input else 5
    
    bind_hardware = input("¿Vincular a equipo específico? (s/n) [n]: ").strip().lower()
    hardware_id = None
    if bind_hardware == 's':
        from backend.core.licensing.license_manager import LicenseManager
        manager = LicenseManager()
        hardware_id = manager.get_hardware_id()
        print(f"   Hardware ID detectado: {hardware_id}")
    
    output_dir = input("Directorio de salida [./licenses]: ").strip()
    output_path = Path(output_dir if output_dir else "./licenses")
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generar licencia
    generator = LicenseGenerator()
    license_data = generator.create_license(
        client_name=client_name,
        institution=institution,
        validity_days=validity_days,
        max_users=max_users,
        hardware_id=hardware_id,
        output_path=output_path
    )
    
    generator.create_license_info_file(license_data, output_path)
    
    print("\n✅ Licencia generada exitosamente!")
    print(f"📁 Archivos en: {output_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # Modo interactivo si no hay argumentos
        interactive_mode()
    else:
        # Modo CLI con argumentos
        main()
