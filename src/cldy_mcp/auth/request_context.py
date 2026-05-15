"""Request-scoped context for streaming mode."""

from contextvars import ContextVar

from ..utils.http_client import CloudabilityHTTPClient

request_http_client: ContextVar[CloudabilityHTTPClient | None] = ContextVar(
    "request_http_client", default=None
)
request_response_format: ContextVar[str | None] = ContextVar(
    "request_response_format", default=None
)
