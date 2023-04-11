from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
)
from opentelemetry.proto.collector.trace.v1.trace_service_pb2_grpc import (
    TraceServiceStub,
)
import grpc

otel_host = "localhost"
otel_port = 4317

# Create gRPC client for OpenTelemetry collector
channel = grpc.insecure_channel(f"{otel_host}:{otel_port}")
stub = TraceServiceStub(channel)

# Query all traces
request = ExportTraceServiceRequest()
response = stub.Export(request)

print(response)
# Print trace IDs
trace_ids = [
    span.trace_id for resource_span in response.resource_spans for span in resource_span.instrumentation_library_spans[0].spans
] if response.resource_spans else []
print(f"Found {len(trace_ids)} traces")
print(trace_ids)
