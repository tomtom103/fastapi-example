import asyncio
import json
from concurrent.futures.process import ProcessPoolExecutor
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

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

@app.get("/async-endpoint")
async def test_endpoint():
    random_args = { "a": 1, "b": 2, "c": 3 }
    res = await run_in_process(lambda x: f"Hello from async endpoint, received: {json.dumps(x)}", random_args)
    return {"result": res}
