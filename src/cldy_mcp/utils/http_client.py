"""HTTP client for Cloudability API V3."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode

import httpx

from .errors import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
)


def build_query_params(
    params: dict[str, Any] | None,
    *,
    array_format: str = "comma",
) -> dict[str, Any] | list[tuple[str, str]]:
    """Build query params; use list of tuples for repeated keys (filters)."""
    if not params:
        return {}

    if array_format == "repeat":
        pairs: list[tuple[str, str]] = []
        for key, value in params.items():
            if value is None or value == "":
                continue
            if isinstance(value, list):
                for item in value:
                    if item is not None and item != "":
                        pairs.append((key, str(item)))
            else:
                pairs.append((key, str(value)))
        return pairs

    cleaned: dict[str, Any] = {}
    for key, value in params.items():
        if value is None or value == "":
            continue
        if isinstance(value, list):
            filtered = [str(v) for v in value if v is not None and v != ""]
            if filtered:
                cleaned[key] = ",".join(filtered)
        else:
            cleaned[key] = value
    return cleaned


class CloudabilityHTTPClient:
    def __init__(
        self,
        api_key: str | None = None,
        access_token: str | None = None,
        environment_id: str | None = None,
        base_url: str = "https://api.cloudability.com/v3",
        timeout: int = 60,
        response_format: str = "toon",
    ):
        self.response_format = response_format
        self.timeout = timeout
        base = base_url.rstrip("/")
        self.base_url = base if base.endswith("/v3") else f"{base}/v3"

        if not api_key and not (access_token and environment_id):
            raise AuthenticationError(
                "Either api_key or both access_token and environment_id required"
            )

        headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        auth: httpx.Auth | None = None

        if access_token and environment_id:
            headers["apptio-opentoken"] = access_token
            headers["apptio-environmentid"] = environment_id
        if api_key:
            auth = httpx.BasicAuth(api_key, "")

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            auth=auth,
            headers=headers,
            timeout=timeout,
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | list[tuple[str, str]] | None = None,
        json_body: Any = None,
        content: bytes | None = None,
        headers: dict[str, str] | None = None,
        files: Any = None,
        array_format: str = "comma",
    ) -> httpx.Response:
        rel = path if path.startswith("/") else f"/{path}"
        req_headers = dict(headers or {})
        req_params: Any = params
        if isinstance(params, dict) and array_format == "repeat":
            req_params = build_query_params(params, array_format="repeat")

        try:
            response = await self.client.request(
                method,
                rel,
                params=req_params,
                json=json_body,
                content=content,
                headers=req_headers,
                files=files,
            )
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out after {self.timeout}s") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e

        if response.status_code == 401:
            raise AuthenticationError("Authentication failed")
        if response.status_code == 403:
            raise AuthorizationError("Access forbidden")
        if response.status_code == 404:
            raise NotFoundError(f"Not found: {rel}", status_code=404)
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded", status_code=429)
        if response.status_code >= 400:
            raise APIError(
                f"API error {response.status_code}: {response.text}",
                status_code=response.status_code,
                response_body=response.text,
            )
        return response

    async def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        accept: str | None = None,
        array_format: str = "comma",
    ) -> dict[str, Any]:
        headers = {"Accept": accept} if accept else None
        resp = await self.request(
            "GET", path, params=params, headers=headers, array_format=array_format
        )
        ct = resp.headers.get("content-type", "")
        if "text/csv" in ct or (accept and "csv" in accept):
            return {"result": resp.text, "meta": {"content_type": ct}}
        try:
            data = resp.json()
        except json.JSONDecodeError:
            return {"result": resp.text}
        if isinstance(data, dict) and "result" in data:
            out: dict[str, Any] = {"result": data["result"]}
            if data.get("meta") is not None:
                out["meta"] = data["meta"]
            return out
        return {"result": data}

    async def post_json(
        self,
        path: str,
        body: Any = None,
        *,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        resp = await self.request("POST", path, json_body=body, params=params, **kwargs)
        if resp.status_code == 204:
            return {"result": None}
        data = resp.json()
        if isinstance(data, dict) and "result" in data:
            out: dict[str, Any] = {"result": data["result"]}
            if data.get("meta") is not None:
                out["meta"] = data["meta"]
            return out
        return {"result": data}

    async def put_json(
        self,
        path: str,
        body: Any = None,
        *,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        resp = await self.request("PUT", path, json_body=body, params=params, **kwargs)
        if resp.status_code == 204:
            return {"result": None}
        data = resp.json()
        if isinstance(data, dict) and "result" in data:
            out: dict[str, Any] = {"result": data["result"]}
            if data.get("meta") is not None:
                out["meta"] = data["meta"]
            return out
        return {"result": data}

    async def delete_json(self, path: str, **kwargs: Any) -> dict[str, Any]:
        resp = await self.request("DELETE", path, **kwargs)
        if resp.status_code == 204 or not resp.content:
            return {"result": None}
        data = resp.json()
        if isinstance(data, dict) and "result" in data:
            return {"result": data["result"], **({"meta": data["meta"]} if data.get("meta") else {})}
        return {"result": data}

    async def get_binary(
        self, path: str, *, params: dict[str, Any] | None = None, accept: str | None = None
    ) -> dict[str, Any]:
        import base64

        headers = {"Accept": accept} if accept else None
        resp = await self.request("GET", path, params=params, headers=headers)
        ct = resp.headers.get("content-type", "application/octet-stream")
        return {
            "result": {
                "content_base64": base64.b64encode(resp.content).decode("ascii"),
                "content_type": ct,
                "size_bytes": len(resp.content),
            }
        }

    async def close(self) -> None:
        await self.client.aclose()
