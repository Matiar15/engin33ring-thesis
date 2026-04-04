import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from backend.src.settings import get_settings

_logger = logging.getLogger(__name__)


def tracing_config() -> None:
    settings = get_settings()
    _logger.info("Initializing tracing...")

    resource = Resource.create({SERVICE_NAME: settings.application_name})

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=f"{settings.otel.endpoint}/v1/traces")
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    set_global_textmap(TraceContextTextMapPropagator())

    _logger.info("Tracing initialized.")
