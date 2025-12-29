from asterisk.manager import Manager
import threading
import time
import json
from typing import Dict, Any

class PBXConnector:
    def __init__(self, ami_host: str, ami_port: int, ami_user: str, ami_password: str):
        self.host = ami_host
        self.port = ami_port
        self.user = ami_user
        self.password = ami_password
        self.manager = Manager()
        self.connected = False
        self.call_events = []

    def connect(self):
        """Establece conexión con Asterisk AMI"""
        try:
            self.manager.connect(self.host, self.port)
            self.manager.login(self.user, self.password)
            self.connected = True
            print("✅ Conectado a Asterisk AMI")
            return True
        except Exception as e:
            print(f"❌ Error al conectar con Asterisk: {e}")
            return False

    def disconnect(self):
        """Cierra la conexión con Asterisk"""
        if self.connected:
            self.manager.logoff()
            self.connected = False
            print("🔌 Desconectado de Asterisk")

    def handle_event(self, event: Dict[str, Any]):
        """Manejador de eventos de Asterisk"""
        event_type = event.get('Event')
        
        if event_type == 'Newchannel':
            # Nueva llamada iniciada
            caller_id = event.get('CallerIDNum')
            destination = event.get('Destination')
            channel = event.get('Channel')
            print(f"📞 Llamada entrante: {caller_id} -> {destination}")
            
            # Iniciar grabación
            self.start_recording(channel)
            
        elif event_type == 'Hangup':
            # Llamada finalizada
            uniqueid = event.get('Uniqueid')
            duration = event.get('Duration')
            print(f"🔚 Llamada finalizada (ID: {uniqueid}, Duración: {duration}s)")
            
            # Detener grabación y enviar a SentinelA
            recording_path = self.stop_recording(uniqueid)
            if recording_path:
                self.send_to_sentinela(uniqueid, recording_path, duration)

    def start_recording(self, channel: str):
        """Inicia grabación de audio"""
        # Comando para iniciar grabación en Asterisk
        command = f"MixMonitor {channel}-in.wav,b"
        self.manager.send_action({'Action': 'Command', 'Command': command})

    def stop_recording(self, uniqueid: str) -> str:
        """Detiene grabación y retorna la ruta del archivo"""
        # Comando para detener grabación
        command = f"StopMixMonitor {uniqueid}-in.wav"
        self.manager.send_action({'Action': 'Command', 'Command': command})
        
        # Retornar ruta del archivo WAV
        return f"/var/spool/asterisk/monitor/{uniqueid}-in.wav"

    def send_to_sentinela(self, call_id: str, audio_path: str, duration: int):
        """Envía datos a SentinelA para procesamiento"""
        # Aquí deberías implementar la llamada a tu API de SentinelA
        # Por ejemplo usando requests:
        # response = requests.post("http://localhost:8000/stream/fragment", 
        #                         files={"file": open(audio_path, "rb")},
        #                         data={"pin": "PIN_DEL_INTERNO"})
        print(f"📤 Enviando llamada {call_id} a SentinelA para transcripción")

    def listen_for_events(self):
        """Escucha eventos de Asterisk en segundo plano"""
        while self.connected:
            try:
                event = self.manager.wait_for_event(timeout=1)
                if event:
                    self.handle_event(event)
            except Exception as e:
                print(f"⚠️ Error al escuchar eventos: {e}")
                time.sleep(5)

    def start_listening(self):
        """Inicia el hilo para escuchar eventos"""
        listener_thread = threading.Thread(target=self.listen_for_events)
        listener_thread.daemon = True
        listener_thread.start()

# Ejemplo de uso
if __name__ == "__main__":
    connector = PBXConnector(
        ami_host="192.168.1.100",
        ami_port=5038,
        ami_user="sentinela",
        ami_password="password_seguro"
    )
    
    if connector.connect():
        connector.start_listening()
        
        # Mantener el programa en ejecución
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            connector.disconnect()
