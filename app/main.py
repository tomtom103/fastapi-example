import asyncio
import json
from concurrent.futures.process import ProcessPoolExecutor
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.connection_manager import ConnectionManager

app = FastAPI()

# Manager allows us to handle websocket requests coming from multiple clients
manager = ConnectionManager()

def cpu_intensive_fn(*args):
    return f"Hello from async endpoint, received: {json.dumps(*args)}"

async def run_in_process(fn, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(app.state.executor, fn, *args) # wait and return result

@app.on_event("startup")
async def startup():
    app.state.executor = ProcessPoolExecutor()

@app.on_event("shutdown")
async def on_shutdown():
    app.state.executor.shutdown()


# WARNING: Cannot use async if calling another service (database, API, file system, etc.)
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Note to self: NO LAMBDA FUNCTIONS!!!!!!!!
# ProcessPoolExecutor cant pickle lambdas
@app.get("/async-endpoint")
async def test_endpoint():
    random_args = { "a": 1, "b": 2, "c": 3 }
    res = await run_in_process(cpu_intensive_fn, random_args)
    return {"result": res}

# Example of a websocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        data = await websocket.receive_text()
        await manager.send_personal_message(f"You wrote: {data}", websocket)
        await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected")
