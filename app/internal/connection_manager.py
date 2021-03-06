from typing import List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def reply_text(self, data: str, websocket: WebSocket):
        await websocket.send_text(data)

    async def broadcast_text(self, data: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(data)
