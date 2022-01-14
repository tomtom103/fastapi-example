from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.internal.connection_manager import ConnectionManager
from app.utils.logger import logger

socketRouter = APIRouter()

manager = ConnectionManager()

# TODO: Remove the client id as it is not needed
# (Unless we let drones label themselves...)
@socketRouter.websocket("/{client_id}")
async def websocket_connect(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    logger.info(f"Client connected! {websocket}")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.reply_text(f"You wrote: {data}", websocket)
            await manager.broadcast_text(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_text(f"Client {client_id} disconnected")
