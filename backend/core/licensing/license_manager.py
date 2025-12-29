"""
Sistema de Licencias USB Dongle para SENTINELA
Verifica la presencia y validez de una licencia en USB antes de permitir el uso del sistema
"""

import os
import json
import hashlib
import platform
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LicenseManager:
    """Gestor de licencias USB Dongle"""
    
    LICENSE_FILENAME = "sentinela.lic"
    HARDWARE_ID_CACHE = None
    
    def __init__(self):
        self.license_data: Optional[Dict[str, Any]] = None
        self.usb_path: Optional[Path] = None
        self.is_valid = False
    
    def get_hardware_id(self) -> str:
        """
        Obtener ID único del hardware de la computadora
        Combina: CPU ID, MAC Address, Disk Serial
        """
        if LicenseManager.HARDWARE_ID_CACHE:
            return LicenseManager.HARDWARE_ID_CACHE
        
        components = []
        
        try:
            # CPU ID
            if platform.system() == "Windows":
                cpu_id = subprocess.check_output("wmic cpu get processorid", shell=True).decode().split("\n")[1].strip()
            elif platform.system() == "Darwin":  # macOS
                cpu_id = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True).decode().strip()
            else:  # Linux
                cpu_id = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | head -1", shell=True).decode().strip()
            components.append(cpu_id)
        except:
            components.append("CPU_UNKNOWN")
        
        try:
            # MAC Address
            if platform.system() == "Windows":
                mac = subprocess.check_output("getmac", shell=True).decode().split("\n")[3].split()[0]
            elif platform.system() == "Darwin":
                mac = subprocess.check_output("ifconfig en0 | grep ether", shell=True).decode().split()[1]
            else:
                mac = subprocess.check_output("cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/address", shell=True).decode().strip()
            components.append(mac)
        except:
            components.append("MAC_UNKNOWN")
        
        # Generar hash único
        hardware_string = "|".join(components)
        hardware_id = hashlib.sha256(hardware_string.encode()).hexdigest()[:32]
        
        LicenseManager.HARDWARE_ID_CACHE = hardware_id
        return hardware_id
    
    def find_usb_drives(self) -> list[Path]:
        """Buscar unidades USB conectadas"""
        usb_drives = []
        
        if platform.system() == "Windows":
            # Windows: Buscar en letras de unidad
            for letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
                drive = Path(f"{letter}:\\")
                if drive.exists():
                    usb_drives.append(drive)
        
        elif platform.system() == "Darwin":  # macOS
            # macOS: Buscar en /Volumes
            volumes = Path("/Volumes")
            if volumes.exists():
                for volume in volumes.iterdir():
                    if volume.is_dir() and volume.name != "Macintosh HD":
                        usb_drives.append(volume)
        
        else:  # Linux
            # Linux: Buscar en /media y /mnt
            for base in [Path("/media"), Path("/mnt")]:
                if base.exists():
                    for mount in base.iterdir():
                        if mount.is_dir():
                            usb_drives.append(mount)
        
        return usb_drives
    
    def find_license_file(self) -> Optional[Path]:
        """Buscar archivo de licencia en USBs conectados"""
        usb_drives = self.find_usb_drives()
        
        for drive in usb_drives:
            license_path = drive / self.LICENSE_FILENAME
            if license_path.exists():
                logger.info(f"✅ Licencia encontrada en: {license_path}")
                return license_path
        
        logger.warning("⚠️  No se encontró licencia USB")
        return None
    
    def read_license(self, license_path: Path) -> Optional[Dict[str, Any]]:
        """Leer y parsear archivo de licencia"""
        try:
            with open(license_path, 'r', encoding='utf-8') as f:
                encrypted_data = f.read()
            
            # Decodificar licencia (simple XOR con clave)
            decrypted_data = self._decrypt_license(encrypted_data)
            license_data = json.loads(decrypted_data)
            
            return license_data
        except Exception as e:
            logger.error(f"❌ Error leyendo licencia: {e}")
            return None
    
    def _decrypt_license(self, encrypted_data: str) -> str:
        """Desencriptar datos de licencia (XOR simple)"""
        # Clave de encriptación (debe ser la misma que en el generador)
        key = "SENTINELA_2025_SECURE_KEY"
        
        # Decodificar de hex
        try:
            encrypted_bytes = bytes.fromhex(encrypted_data)
        except:
            return encrypted_data  # Si no está encriptado, retornar tal cual
        
        # XOR con la clave
        decrypted = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            decrypted.append(byte ^ ord(key[i % len(key)]))
        
        return decrypted.decode('utf-8')
    
    def validate_license(self, license_data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validar licencia
        Retorna: (es_valida, mensaje)
        """
        # 1. Verificar firma
        if not self._verify_signature(license_data):
            return False, "Firma de licencia inválida"
        
        # 2. Verificar fecha de expiración
        expiry_date = datetime.fromisoformat(license_data.get('expiry_date', '2000-01-01'))
        if datetime.now() > expiry_date:
            return False, f"Licencia expirada el {expiry_date.strftime('%d/%m/%Y')}"
        
        # 3. Verificar hardware ID (si está presente)
        if 'hardware_id' in license_data:
            current_hw_id = self.get_hardware_id()
            if license_data['hardware_id'] != current_hw_id:
                return False, "Licencia no válida para este equipo"
        
        # 4. Verificar que no esté revocada
        if license_data.get('revoked', False):
            return False, "Licencia revocada"
        
        return True, "Licencia válida"
    
    def _verify_signature(self, license_data: Dict[str, Any]) -> bool:
        """Verificar firma digital de la licencia"""
        if 'signature' not in license_data:
            return False
        
        # Crear string de datos para verificar
        data_string = f"{license_data.get('license_key', '')}"
        data_string += f"{license_data.get('client_name', '')}"
        data_string += f"{license_data.get('expiry_date', '')}"
        
        # Generar firma esperada
        expected_signature = hashlib.sha256(data_string.encode()).hexdigest()
        
        return license_data['signature'] == expected_signature
    
    def check_license(self) -> tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Verificar licencia USB
        Retorna: (es_valida, mensaje, datos_licencia)
        """
        # 1. Buscar archivo de licencia
        license_path = self.find_license_file()
        if not license_path:
            return False, "No se encontró USB con licencia válida", None
        
        self.usb_path = license_path.parent
        
        # 2. Leer licencia
        license_data = self.read_license(license_path)
        if not license_data:
            return False, "Error al leer archivo de licencia", None
        
        # 3. Validar licencia
        is_valid, message = self.validate_license(license_data)
        
        if is_valid:
            self.license_data = license_data
            self.is_valid = True
            logger.info(f"✅ Licencia válida para: {license_data.get('client_name', 'N/A')}")
            logger.info(f"   Expira: {license_data.get('expiry_date', 'N/A')}")
        else:
            logger.error(f"❌ {message}")
        
        return is_valid, message, license_data
    
    def get_license_info(self) -> Dict[str, Any]:
        """Obtener información de la licencia actual"""
        if not self.license_data:
            return {
                'valid': False,
                'message': 'No hay licencia cargada'
            }
        
        return {
            'valid': self.is_valid,
            'license_key': self.license_data.get('license_key', 'N/A'),
            'client_name': self.license_data.get('client_name', 'N/A'),
            'institution': self.license_data.get('institution', 'N/A'),
            'expiry_date': self.license_data.get('expiry_date', 'N/A'),
            'max_users': self.license_data.get('max_users', 1),
            'modules': self.license_data.get('modules', []),
            'usb_path': str(self.usb_path) if self.usb_path else None
        }
    
    def monitor_usb(self) -> bool:
        """
        Monitorear que el USB siga conectado
        Retorna True si el USB está presente, False si se desconectó
        """
        if not self.usb_path:
            return False
        
        license_path = self.usb_path / self.LICENSE_FILENAME
        return license_path.exists()


# Singleton global
_license_manager_instance: Optional[LicenseManager] = None


def get_license_manager() -> LicenseManager:
    """Obtener instancia única del gestor de licencias"""
    global _license_manager_instance
    if _license_manager_instance is None:
        _license_manager_instance = LicenseManager()
    return _license_manager_instance


def require_valid_license():
    """
    Decorador para endpoints que requieren licencia válida
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            manager = get_license_manager()
            
            # Verificar que el USB siga conectado
            if not manager.monitor_usb():
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=403,
                    detail="USB de licencia no detectado. Por favor conecte el USB de licencia."
                )
            
            if not manager.is_valid:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=403,
                    detail="Licencia no válida. Contacte con soporte técnico."
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
