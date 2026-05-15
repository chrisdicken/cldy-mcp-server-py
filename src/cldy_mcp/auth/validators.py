"""Authentication validators with dual env var prefixes."""

import base64
import os
from typing import Any

from ..utils.errors import AuthenticationError, ConfigurationError


def _env(*names: str) -> str | None:
    for name in names:
        val = os.getenv(name)
        if val:
            return val
    return None


def get_credentials_from_env() -> dict[str, str | None]:
    api_key = _env("CLOUDABILITY_API_KEY", "CLDY_API_KEY")
    access_token = _env("CLOUDABILITY_OPENTOKEN", "CLDY_ACCESS_TOKEN")
    environment_id = _env("CLOUDABILITY_ENVIRONMENT_ID", "CLDY_ENVIRONMENT_ID")

    auth_method = _env("CLOUDABILITY_AUTH_METHOD", "CLDY_AUTH_METHOD")
    if auth_method == "opentoken" and access_token and environment_id:
        return {
            "api_key": None,
            "access_token": access_token,
            "environment_id": environment_id,
        }
    if auth_method == "api-key" and api_key:
        return {"api_key": api_key, "access_token": None, "environment_id": None}

    if access_token and environment_id:
        return {
            "api_key": None,
            "access_token": access_token,
            "environment_id": environment_id,
        }
    if api_key:
        return {"api_key": api_key, "access_token": None, "environment_id": None}

    raise ConfigurationError(
        "Set CLOUDABILITY_API_KEY (or CLDY_API_KEY) or "
        "CLOUDABILITY_OPENTOKEN + CLOUDABILITY_ENVIRONMENT_ID"
    )


class AuthValidator:
    @staticmethod
    def validate_api_key(api_key: str | None) -> str:
        if not api_key or not isinstance(api_key, str):
            raise AuthenticationError("API key is required")
        if len(api_key) < 8:
            raise AuthenticationError("API key appears invalid")
        return api_key

    @staticmethod
    def validate_frontdoor(access_token: str | None, environment_id: str | None) -> tuple[str, str]:
        if not access_token or not environment_id:
            raise AuthenticationError("OpenToken and environment ID required")
        return access_token, environment_id

    @staticmethod
    def validate_basic_auth_header(auth_header: str | None) -> str:
        if not auth_header or not auth_header.startswith("Basic "):
            raise AuthenticationError("Authorization header must use Basic auth")
        try:
            decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
            api_key, _, password = decoded.partition(":")
            if password:
                raise AuthenticationError("API key must have empty password")
            return AuthValidator.validate_api_key(api_key)
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"Invalid Basic auth: {e}") from e

    @staticmethod
    def validate_credentials(
        api_key: str | None = None,
        access_token: str | None = None,
        environment_id: str | None = None,
    ) -> dict[str, Any]:
        has_key = bool(api_key)
        has_fd = bool(access_token and environment_id)
        if not has_key and not has_fd:
            raise AuthenticationError("No valid credentials provided")
        out: dict[str, Any] = {}
        if has_key:
            out["api_key"] = AuthValidator.validate_api_key(api_key)
        if has_fd:
            token, env = AuthValidator.validate_frontdoor(access_token, environment_id)
            out["access_token"] = token
            out["environment_id"] = env
        return out
