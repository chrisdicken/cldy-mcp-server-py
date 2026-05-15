"""Server wiring tests."""

import os

import pytest

from cldy_mcp.server import create_server


@pytest.fixture
def env_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLOUDABILITY_API_KEY", "test-api-key-12345678")
    monkeypatch.delenv("CLOUDABILITY_OPENTOKEN", raising=False)
    monkeypatch.delenv("CLDY_MODE", raising=False)


def test_create_server_registers_tools(env_credentials: None) -> None:
    mcp = create_server(
        api_key=os.environ["CLOUDABILITY_API_KEY"],
        response_format="json",
        mode="local",
    )
    assert mcp.name == "cloudability-mcp-server"
