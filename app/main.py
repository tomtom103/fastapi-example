import os
import sys

# We do this to be able to have app as the main directory regardless of where we run the code
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI

from app.routers import sockets
from app.utils.logger import logger
from app.utils.settings import Settings

settings = Settings()

app = FastAPI(debug=settings.USE_NGROK)

app.include_router(sockets.socketRouter, prefix="/ws")


# WARNING: Cannot use async if calling another service (database, API, file system, etc.)
@app.get("/")
async def read_root():
    logger.debug("Root endpoint called!")
    return {"Hello": "World"}
