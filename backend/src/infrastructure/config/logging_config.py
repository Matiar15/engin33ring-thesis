import logging.config
import sys
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from backend.src.settings import get_settings


def logging_config() -> None:
    settings = get_settings()
    logging_level = settings.logging.level.upper()

    # OTel Logging Setup
    resource = Resource.create({SERVICE_NAME: settings.application_name})
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    otlp_exporter = OTLPLogExporter(
        endpoint=f"{settings.otel.endpoint}/v1/logs",
    )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

    otlp_handler = LoggingHandler(level=logging.getLevelName(logging_level), logger_provider=logger_provider)

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
                "otlp": {
                    "()": lambda: otlp_handler,
                },
            },
            "loggers": {
                "backend": {
                    "handlers": ["console_json", "otlp"],
                    "level": logging_level,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console_simple", "otlp"],
                    "level": logging_level,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["console_simple", "otlp"],
                    "level": logging_level,
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["console_simple", "otlp"],
                "level": "INFO",
            },
        }
    )
