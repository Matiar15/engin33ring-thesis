import logging.config
import sys
from backend.src.settings import get_settings


def logging_config() -> None:
    settings = get_settings()
    logging_level = settings.logging.level.upper()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s %(levelname)s %(name)s :: %(message)s"
                },
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                },
            },
            "handlers": {
                "console_simple": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "level": logging_level,
                    "stream": sys.stdout,
                },
                "console_json": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "level": logging_level,
                    "stream": sys.stdout,
                },
            },
            "loggers": {
                "backend": {
                    "handlers": ["console_json"],
                    "level": logging_level,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console_simple"],
                    "level": logging_level,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["console_simple"],
                    "level": logging_level,
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["console_simple"],
                "level": "INFO",
            },
        }
    )
