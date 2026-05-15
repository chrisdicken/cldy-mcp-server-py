"""FastMCP middleware for per-request credential pass-through."""

from typing import Any

from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext

from ..constants import resolve_base_url
from ..utils.errors import AuthenticationError
from ..utils.http_client import CloudabilityHTTPClient
from .middleware import negotiate_response_format, validate_auth_headers
from .request_context import request_http_client, request_response_format


class CloudabilityAuthMiddleware(Middleware):
    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 60,
        response_format: str = "toon",
    ) -> None:
        super().__init__()
        self.base_url = base_url or resolve_base_url()
        self.timeout = timeout
        self.response_format = response_format

    async def on_request(self, context: MiddlewareContext, call_next: Any) -> Any:
        try:
            headers = get_http_headers()
            if headers:
                headers_dict = dict(headers)
                creds = validate_auth_headers(headers_dict)
                request_response_format.set(negotiate_response_format(headers_dict))
                client = CloudabilityHTTPClient(
                    api_key=creds.get("api_key"),
                    access_token=creds.get("access_token"),
                    environment_id=creds.get("environment_id"),
                    base_url=self.base_url,
                    timeout=self.timeout,
                    response_format=self.response_format,
                )
                request_http_client.set(client)
        except AuthenticationError:
            raise
        except Exception:
            pass
        return await call_next(context)
