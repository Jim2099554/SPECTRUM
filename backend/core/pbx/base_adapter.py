"""
Clase base para adaptadores de PBX
Define la interfaz que todos los adaptadores deben implementar
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable


class BasePBXAdapter(ABC):
    """Clase base abstracta para adaptadores de PBX"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializar adaptador con configuración
        
        Args:
            config: Diccionario con configuración del PBX
        """
        self.config = config
        self.connected = False
        self.event_handlers = {}
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establecer conexión con el PBX
        
        Returns:
            True si la conexión fue exitosa, False en caso contrario
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """Cerrar la conexión con el PBX"""
        pass
    
    @abstractmethod
    def start_recording(self, channel: str, call_id: str) -> bool:
        """
        Iniciar grabación de una llamada
        
        Args:
            channel: Canal de la llamada
            call_id: ID único de la llamada
            
        Returns:
            True si se inició la grabación, False en caso contrario
        """
        pass
    
    @abstractmethod
    def stop_recording(self, call_id: str) -> Optional[str]:
        """
        Detener grabación de una llamada
        
        Args:
            call_id: ID único de la llamada
            
        Returns:
            Ruta del archivo de audio grabado, o None si falló
        """
        pass
    
    @abstractmethod
    def start_listening(self):
        """Iniciar escucha de eventos del PBX en segundo plano"""
        pass
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """
        Registrar manejador de eventos
        
        Args:
            event_type: Tipo de evento (ej: 'call_start', 'call_end')
            handler: Función a llamar cuando ocurra el evento
        """
        self.event_handlers[event_type] = handler
    
    def _trigger_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Disparar evento registrado
        
        Args:
            event_type: Tipo de evento
            event_data: Datos del evento
        """
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type](event_data)
            except Exception as e:
                print(f"Error en manejador de evento {event_type}: {e}")
    
    def test_connection(self) -> bool:
        """
        Probar conexión al PBX
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            success = self.connect()
            if success:
                self.disconnect()
            return success
        except Exception as e:
            print(f"Error probando conexión: {e}")
            return False
