import logging
import os
from logging.config import dictConfig

from pydantic import BaseModel, BaseSettings


class LoggingConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME = "app"
    LOG_FORMAT = "%(levelprefix)s %(message)s"
    LOG_LEVEL = "DEBUG"

    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "app": {"handlers": ["default"], "level": LOG_LEVEL},
    }

class Settings(BaseSettings):
    # FastAPI settings

    BASE_URL = "http://localhost:5000"
    USE_NGROK = os.environ.get("USE_NGROK") is not None

dictConfig(LoggingConfig().dict())
logger = logging.getLogger("app")
