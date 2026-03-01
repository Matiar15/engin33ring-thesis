import logging.config

from backend.src.settings import get_settings


def logging_config() -> None:
    settings = get_settings()
    logging_level = settings.logging.level.upper()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s %(levelname)s %(name)s :: %(message)s"
                }
            },
            "handlers": {
                "console_simple": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "level": logging_level,
                },
            },
            "loggers": {
                "backend": {
                    "handlers": ["console_simple"],
                    "level": logging_level,
                },
                "uvicorn": {
                    "handlers": ["console_simple"],
                    "level": logging_level,
                },
                "uvicorn.access": {
                    "handlers": ["console_simple"],
                    "level": logging_level,
                },
            },
        }
    )
