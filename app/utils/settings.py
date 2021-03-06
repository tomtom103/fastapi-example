import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # FastAPI settings
    PORT = 5000
    SUBDOMAIN = "inf3995-localhost-102"
    BASE_URL = "http://localhost:5000"
    USE_NGROK = os.environ.get("USE_NGROK") is not None
