from typing import Any

from fastapi_example.settings import LoggingSettings


def get_logging_config(settings: LoggingSettings) -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "datefmt": settings.LOG_DATE_FORMAT,
                "format": settings.LOG_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "default",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {"level": settings.LOG_LEVEL, "handlers": ["console"]},
            "uvicorn.access": {"level": "WARN", "handlers": ["console"]},
        },
    }
