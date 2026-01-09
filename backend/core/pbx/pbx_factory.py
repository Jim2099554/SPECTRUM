"""
Factory para crear adaptadores de PBX según configuración
"""

import json
import os
from typing import Optional, Dict, Any

from .base_adapter import BasePBXAdapter
from .asterisk_adapter import AsteriskAdapter
from .grandstream_adapter import GrandstreamAdapter
from .null_adapter import NullAdapter


class PBXFactory:
    """Factory para crear el adaptador de PBX correcto"""
    
    @staticmethod
    def load_config() -> Optional[Dict[str, Any]]:
        """
        Cargar configuración de PBX desde archivo
        
        Returns:
            Diccionario con configuración o None si no existe
        """
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'config',
                'pbx_config.json'
            )
            
            if not os.path.exists(config_path):
                print("⚠️  No se encontró configuración de PBX")
                return None
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            return config
            
        except Exception as e:
            print(f"❌ Error al cargar configuración de PBX: {e}")
            return None
    
    @staticmethod
    def create_adapter(config: Optional[Dict[str, Any]] = None) -> BasePBXAdapter:
        """
        Crear adaptador de PBX según configuración
        
        Args:
            config: Configuración del PBX (si no se provee, se carga del archivo)
            
        Returns:
            Instancia del adaptador apropiado
        """
        # Cargar configuración si no se proveyó
        if config is None:
            config = PBXFactory.load_config()
        
        # Si no hay configuración, usar adaptador nulo
        if not config:
            print("ℹ️  Usando modo sin PBX")
            return NullAdapter({'pbx_type': 'none'})
        
        # Obtener tipo de PBX
        pbx_type = config.get('pbx_type', 'none')
        enabled = config.get('enabled', False)
        
        # Si está deshabilitado, usar adaptador nulo
        if not enabled:
            print(f"ℹ️  PBX {pbx_type} está deshabilitado")
            return NullAdapter(config)
        
        # Crear adaptador según tipo
        if pbx_type == 'asterisk':
            print("🔧 Creando adaptador Asterisk")
            return AsteriskAdapter(config)
        
        elif pbx_type == 'grandstream':
            print("🔧 Creando adaptador Grandstream UCM")
            return GrandstreamAdapter(config)
        
        elif pbx_type in ['freeswitch', '3cx', 'cisco', 'avaya', 'huawei', 'teams', 'other']:
            print(f"⚠️  PBX {pbx_type} requiere desarrollo adicional")
            print("   Usando modo sin PBX temporalmente")
            return NullAdapter(config)
        
        elif pbx_type == 'none':
            print("ℹ️  Modo sin PBX configurado")
            return NullAdapter(config)
        
        else:
            print(f"❌ Tipo de PBX desconocido: {pbx_type}")
            return NullAdapter(config)
    
    @staticmethod
    def test_connection(config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Probar conexión con el PBX configurado
        
        Args:
            config: Configuración del PBX (si no se provee, se carga del archivo)
            
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            adapter = PBXFactory.create_adapter(config)
            return adapter.test_connection()
        except Exception as e:
            print(f"❌ Error probando conexión: {e}")
            return False


# Función de conveniencia para obtener adaptador
def get_pbx_adapter(config: Optional[Dict[str, Any]] = None) -> BasePBXAdapter:
    """
    Obtener instancia del adaptador de PBX
    
    Args:
        config: Configuración del PBX (opcional)
        
    Returns:
        Instancia del adaptador de PBX
    """
    return PBXFactory.create_adapter(config)
