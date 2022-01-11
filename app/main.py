from typing import Optional

from fastapi import FastAPI

app = FastAPI()

# WARNING: Cannot use async if calling another service (database, API, file system, etc.)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
