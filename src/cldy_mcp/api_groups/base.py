"""Base API group with envelope preservation and TOON encoding."""

from __future__ import annotations

import json
from typing import Any

from fastmcp import FastMCP

from ..auth.request_context import request_http_client, request_response_format
from ..utils.errors import APIError, AuthenticationError, AuthorizationError, NotFoundError, RateLimitError, ValidationError
from ..utils.http_client import CloudabilityHTTPClient
from ..utils.response import ResponseShape, parse_envelope, shape_cost_report
from ..utils.toon_encoder import TOONEncoder


def _map_exception(exc: Exception) -> Exception:
    if isinstance(exc, (AuthenticationError, AuthorizationError, ValidationError, NotFoundError, RateLimitError)):
        return exc
    if isinstance(exc, APIError):
        if exc.status_code == 429:
            return RateLimitError(exc.message, status_code=429)
        if exc.status_code == 404:
            return NotFoundError(exc.message, status_code=404)
        if exc.status_code in (401,):
            return AuthenticationError(exc.message)
        if exc.status_code in (403,):
            return AuthorizationError(exc.message)
        if exc.status_code in (400, 422):
            return ValidationError(exc.message)
    return exc


class BaseAPIGroup:
    def __init__(self, client: CloudabilityHTTPClient):
        self.default_client = client

    def _get_client(self) -> CloudabilityHTTPClient:
        req = request_http_client.get()
        return req if req else self.default_client

    def _format(
        self,
        envelope: dict[str, Any],
        *,
        response_shape: ResponseShape = "full",
        sample_rows: int = 20,
    ) -> dict[str, Any]:
        env = parse_envelope(envelope)
        if response_shape == "summary":
            env = shape_cost_report(env, "summary", sample_rows)
        fmt = request_response_format.get()
        use_fmt = fmt if fmt else self._get_client().response_format
        if use_fmt == "toon":
            return {"toon": TOONEncoder.encode_response(env)}
        return env

    async def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        accept: str | None = None,
        array_format: str = "comma",
        response_shape: ResponseShape = "full",
        sample_rows: int = 20,
    ) -> dict[str, Any]:
        try:
            data = await self._get_client().get_json(
                path, params=params, accept=accept, array_format=array_format
            )
            return self._format(data, response_shape=response_shape, sample_rows=sample_rows)
        except Exception as e:
            raise _map_exception(e) from e

    async def _post(
        self,
        path: str,
        body: Any = None,
        *,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        try:
            data = await self._get_client().post_json(path, body, params=params, **kwargs)
            return self._format(data)
        except Exception as e:
            raise _map_exception(e) from e

    async def _put(
        self,
        path: str,
        body: Any = None,
        *,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        try:
            data = await self._get_client().put_json(path, body, params=params, **kwargs)
            return self._format(data)
        except Exception as e:
            raise _map_exception(e) from e

    async def _delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            data = await self._get_client().delete_json(path, **kwargs)
            return self._format(data)
        except Exception as e:
            raise _map_exception(e) from e

    async def _get_binary(self, path: str, *, params: dict[str, Any] | None = None, accept: str | None = None) -> dict[str, Any]:
        try:
            data = await self._get_client().get_binary(path, params=params, accept=accept)
            return self._format(data)
        except Exception as e:
            raise _map_exception(e) from e

    def register_tools(self, mcp: FastMCP) -> None:
        raise NotImplementedError
