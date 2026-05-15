"""Pytest fixtures."""

import pytest

from cldy_mcp.utils.http_client import CloudabilityHTTPClient


@pytest.fixture
def mock_client() -> CloudabilityHTTPClient:
    return CloudabilityHTTPClient(api_key="test-api-key-12345678", response_format="json")
