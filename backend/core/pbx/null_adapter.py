"""
Adaptador nulo para cuando no se usa PBX
"""

from typing import Dict, Any, Optional
from .base_adapter import BasePBXAdapter


class NullAdapter(BasePBXAdapter):
    """Adaptador nulo para modo sin PBX"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        print("ℹ️  Modo sin PBX activado - Las llamadas deben cargarse manualmente")
    
    def connect(self) -> bool:
        """No hay conexión en modo sin PBX"""
        self.connected = True
        return True
    
    def disconnect(self):
        """No hay desconexión en modo sin PBX"""
        self.connected = False
    
    def start_recording(self, channel: str, call_id: str) -> bool:
        """No se puede grabar sin PBX"""
        print("⚠️  No se puede iniciar grabación sin PBX configurado")
        return False
    
    def stop_recording(self, call_id: str) -> Optional[str]:
        """No se puede detener grabación sin PBX"""
        return None
    
    def start_listening(self):
        """No hay eventos que escuchar sin PBX"""
        print("ℹ️  Modo manual - No hay eventos de PBX que escuchar")
