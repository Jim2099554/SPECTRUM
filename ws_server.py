from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

# Permitir CORS para frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto según tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass  # Ignore failed sends

manager = ConnectionManager()

@app.websocket("/ws/calls")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # No procesamos mensajes del cliente
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/notify_new_call")
async def notify_new_call():
    await manager.broadcast("new_call")
    return {"ok": True}
