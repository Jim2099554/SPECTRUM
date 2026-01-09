"""
Módulo de integración con sistemas PBX
"""

from .base_adapter import BasePBXAdapter
from .asterisk_adapter import AsteriskAdapter
from .grandstream_adapter import GrandstreamAdapter
from .null_adapter import NullAdapter
from .pbx_factory import PBXFactory, get_pbx_adapter

__all__ = [
    'BasePBXAdapter',
    'AsteriskAdapter',
    'GrandstreamAdapter',
    'NullAdapter',
    'PBXFactory',
    'get_pbx_adapter'
]
