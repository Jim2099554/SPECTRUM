"""
Adaptador para Asterisk PBX usando AMI (Asterisk Manager Interface)
También compatible con Grandstream UCM y otros PBX basados en Asterisk
"""

import threading
import time
from typing import Dict, Any, Optional

from .base_adapter import BasePBXAdapter


class AsteriskAdapter(BasePBXAdapter):
    """Adaptador para Asterisk y sistemas compatibles (Grandstream, Elastix, etc.)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.manager = None
        self.listener_thread = None
        
    def connect(self) -> bool:
        """Establecer conexión con Asterisk AMI"""
        try:
            from asterisk.manager import Manager
            
            conn_config = self.config.get('connection', {})
            host = conn_config.get('host', 'localhost')
            port = conn_config.get('port', 5038)
            username = conn_config.get('username', 'admin')
            password = conn_config.get('password', '')
            
            self.manager = Manager()
            self.manager.connect(host, port)
            self.manager.login(username, password)
            self.connected = True
            
            print(f"✅ Conectado a {self.config.get('pbx_type', 'Asterisk').upper()} AMI")
            return True
            
        except ImportError:
            print("❌ Error: Librería 'asterisk-ami' no instalada")
            print("   Instale con: pip install asterisk-ami")
            return False
        except Exception as e:
            print(f"❌ Error al conectar con Asterisk: {e}")
            return False
    
    def disconnect(self):
        """Cerrar la conexión con Asterisk"""
        if self.connected and self.manager:
            try:
                self.manager.logoff()
                self.connected = False
                print("🔌 Desconectado de Asterisk")
            except Exception as e:
                print(f"⚠️  Error al desconectar: {e}")
    
    def start_recording(self, channel: str, call_id: str) -> bool:
        """Iniciar grabación de audio"""
        if not self.connected or not self.manager:
            print("❌ No hay conexión con Asterisk")
            return False
        
        try:
            recording_config = self.config.get('recording', {})
            command_type = recording_config.get('command', 'MixMonitor')
            audio_format = recording_config.get('format', 'wav')
            
            # Comando para iniciar grabación
            if command_type == 'MixMonitor':
                command = f"MixMonitor {channel},{audio_format},{call_id}"
            else:  # Monitor (para Grandstream antiguo)
                command = f"Monitor {channel},{audio_format},{call_id}"
            
            self.manager.send_action({
                'Action': 'Command',
                'Command': command
            })
            
            print(f"🎙️  Grabación iniciada: {call_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error al iniciar grabación: {e}")
            return False
    
    def stop_recording(self, call_id: str) -> Optional[str]:
        """Detener grabación y retornar la ruta del archivo"""
        if not self.connected or not self.manager:
            return None
        
        try:
            recording_config = self.config.get('recording', {})
            command_type = recording_config.get('command', 'MixMonitor')
            
            # Comando para detener grabación
            if command_type == 'MixMonitor':
                command = f"StopMixMonitor {call_id}"
            else:
                command = f"StopMonitor {call_id}"
            
            self.manager.send_action({
                'Action': 'Command',
                'Command': command
            })
            
            # Construir ruta del archivo
            audio_path = recording_config.get('path', '/var/spool/asterisk/monitor/')
            audio_format = recording_config.get('format', 'wav')
            file_path = f"{audio_path}{call_id}.{audio_format}"
            
            print(f"⏹️  Grabación detenida: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Error al detener grabación: {e}")
            return None
    
    def _handle_event(self, event: Dict[str, Any]):
        """Manejador de eventos de Asterisk"""
        event_type = event.get('Event')
        
        if event_type == 'Newchannel':
            # Nueva llamada iniciada
            caller_id = event.get('CallerIDNum')
            destination = event.get('Exten')
            channel = event.get('Channel')
            uniqueid = event.get('Uniqueid')
            
            print(f"📞 Llamada entrante: {caller_id} → {destination}")
            
            # Disparar evento personalizado
            self._trigger_event('call_start', {
                'call_id': uniqueid,
                'caller_id': caller_id,
                'destination': destination,
                'channel': channel
            })
            
            # Iniciar grabación automáticamente
            if self.config.get('recording', {}).get('enabled', True):
                self.start_recording(channel, uniqueid)
        
        elif event_type == 'Hangup':
            # Llamada finalizada
            uniqueid = event.get('Uniqueid')
            duration = event.get('Duration', 0)
            
            print(f"🔚 Llamada finalizada (ID: {uniqueid}, Duración: {duration}s)")
            
            # Detener grabación
            audio_path = self.stop_recording(uniqueid)
            
            # Disparar evento personalizado
            self._trigger_event('call_end', {
                'call_id': uniqueid,
                'duration': duration,
                'audio_path': audio_path
            })
    
    def _listen_for_events(self):
        """Escuchar eventos de Asterisk en segundo plano"""
        while self.connected:
            try:
                event = self.manager.wait_for_event(timeout=1)
                if event:
                    self._handle_event(event)
            except Exception as e:
                if self.connected:  # Solo mostrar error si aún estamos conectados
                    print(f"⚠️  Error al escuchar eventos: {e}")
                time.sleep(5)
    
    def start_listening(self):
        """Iniciar el hilo para escuchar eventos"""
        if not self.connected:
            print("❌ Debe conectarse primero antes de escuchar eventos")
            return
        
        self.listener_thread = threading.Thread(target=self._listen_for_events)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        print("👂 Escuchando eventos de Asterisk...")
