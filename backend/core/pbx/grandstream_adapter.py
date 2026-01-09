"""
Adaptador para Grandstream UCM
Hereda de AsteriskAdapter ya que Grandstream usa AMI
"""

from .asterisk_adapter import AsteriskAdapter


class GrandstreamAdapter(AsteriskAdapter):
    """
    Adaptador para Grandstream UCM
    
    Grandstream UCM está basado en Asterisk y usa el mismo protocolo AMI,
    por lo que heredamos toda la funcionalidad de AsteriskAdapter.
    
    Podemos sobrescribir métodos si hay diferencias específicas de Grandstream.
    """
    
    def __init__(self, config):
        super().__init__(config)
        # Configuraciones específicas de Grandstream si es necesario
        
    def connect(self) -> bool:
        """Conectar a Grandstream UCM (usa AMI de Asterisk)"""
        # Grandstream UCM usa el mismo protocolo AMI
        result = super().connect()
        if result:
            print("✅ Conectado a Grandstream UCM (AMI)")
        return result
