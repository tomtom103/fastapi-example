import sys

import uvicorn
from config import logger
from main import settings


def start_ngrok():
    from pyngrok import ngrok

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000

    public_url = ngrok.connect(port).public_url
    logger.debug(f"ngrok tunnel \"{public_url}\" running on -> \"http://localhost:{port}\"")

    settings.BASE_URL = public_url

if __name__ == "__main__":
    start_ngrok()

    uvicorn.run("debug:app", host="0.0.0.0", port=5000, log_level="debug", reload=True, debug=True)
