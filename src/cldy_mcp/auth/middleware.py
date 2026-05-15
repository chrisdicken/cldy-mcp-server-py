"""Auth header validation and response format negotiation."""

from typing import Any

from .validators import AuthValidator


def negotiate_response_format(headers: dict[str, str]) -> str:
    fmt = headers.get("x-response-format") or headers.get("X-Response-Format", "")
    if fmt.lower() == "json":
        return "json"
    return "toon"


def validate_auth_headers(headers: dict[str, str]) -> dict[str, Any]:
    auth_header = headers.get("authorization") or headers.get("Authorization")
    if auth_header:
        api_key = AuthValidator.validate_basic_auth_header(auth_header)
        return {"api_key": api_key, "access_token": None, "environment_id": None}

    token = headers.get("apptio-opentoken")
    env_id = headers.get("apptio-environmentid")
    if token and env_id:
        access_token, environment_id = AuthValidator.validate_frontdoor(token, env_id)
        return {
            "api_key": None,
            "access_token": access_token,
            "environment_id": environment_id,
        }

    from ..utils.errors import AuthenticationError

    raise AuthenticationError(
        "Use Basic Auth (API key) or apptio-opentoken + apptio-environmentid headers"
    )
