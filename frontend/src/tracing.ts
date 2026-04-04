import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request';
import { resourceFromAttributes } from '@opentelemetry/resources';
import { ATTR_SERVICE_NAME } from '@opentelemetry/semantic-conventions';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { CompositePropagator, W3CTraceContextPropagator, W3CBaggagePropagator } from '@opentelemetry/core';

const serviceName = 'engin33ring-thesis-frontend';
const resource = resourceFromAttributes({
  [ATTR_SERVICE_NAME]: serviceName,
});

// Tracing configuration
const traceExporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces',
});

const tracerProvider = new WebTracerProvider({
  resource: resource,
  spanProcessors: [
    new BatchSpanProcessor(traceExporter),
  ],
});

tracerProvider.register({
  contextManager: new ZoneContextManager(),
  propagator: new CompositePropagator({
    propagators: [
      new W3CTraceContextPropagator(),
      new W3CBaggagePropagator(),
    ],
  }),
});

// Metrics configuration
const metricExporter = new OTLPMetricExporter({
  url: 'http://localhost:4318/v1/metrics',
});

const meterProvider = new MeterProvider({
  resource: resource,
  readers: [
    new PeriodicExportingMetricReader({
      exporter: metricExporter,
      exportIntervalMillis: 10000,
    }),
  ],
});

// Export meter for use in other parts of the application
export const meter = meterProvider.getMeter(serviceName);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

registerInstrumentations({
  instrumentations: [
    new FetchInstrumentation({
      propagateTraceHeaderCorsUrls: [
        new RegExp(`${API_BASE_URL}/.*`),
      ],
    }),
    new XMLHttpRequestInstrumentation({
      propagateTraceHeaderCorsUrls: [
        new RegExp(`${API_BASE_URL}/.*`),
      ],
    }),
  ],
});