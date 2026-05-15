"""FastMCP server setup."""

import os

from fastmcp import FastMCP

from .api_groups import (
    AccountGroupsGroup,
    AnomaliesGroup,
    BudgetSubscriptionsGroup,
    BudgetsGroup,
    BusinessMappingsGroup,
    ContainersGroup,
    CostReportingGroup,
    DiscoveryGroup,
    ForecastsGroup,
    RightsizingGroup,
    UsersGroup,
    ViewsGroup,
    WorkloadPlanningGroup,
)
from .auth import get_credentials_from_env
from .auth.mcp_middleware import CloudabilityAuthMiddleware
from .auth.validators import AuthValidator
from .constants import resolve_base_url
from .utils.errors import ConfigurationError
from .utils.http_client import CloudabilityHTTPClient

API_GROUPS = [
    DiscoveryGroup,
    CostReportingGroup,
    AccountGroupsGroup,
    BudgetsGroup,
    BudgetSubscriptionsGroup,
    BusinessMappingsGroup,
    ForecastsGroup,
    ViewsGroup,
    UsersGroup,
    AnomaliesGroup,
    ContainersGroup,
    RightsizingGroup,
    WorkloadPlanningGroup,
]


def create_server(
    api_key: str | None = None,
    access_token: str | None = None,
    environment_id: str | None = None,
    base_url: str | None = None,
    timeout: int = 60,
    response_format: str = "toon",
    mode: str = "local",
) -> FastMCP:
    base = base_url or resolve_base_url()
    auth_middleware: CloudabilityAuthMiddleware | None = None

    if mode == "local":
        if not api_key and not (access_token and environment_id):
            creds = get_credentials_from_env()
            api_key = creds.get("api_key")
            access_token = creds.get("access_token")
            environment_id = creds.get("environment_id")
        AuthValidator.validate_credentials(api_key, access_token, environment_id)
        client = CloudabilityHTTPClient(
            api_key=api_key,
            access_token=access_token,
            environment_id=environment_id,
            base_url=base,
            timeout=timeout,
            response_format=response_format,
        )
    else:
        client = CloudabilityHTTPClient(
            api_key="placeholder",
            base_url=base,
            timeout=timeout,
            response_format=response_format,
        )
        auth_middleware = CloudabilityAuthMiddleware(
            base_url=base,
            timeout=timeout,
            response_format=response_format,
        )

    mcp = FastMCP(name="cloudability-mcp-server", version="1.0.0")
    if auth_middleware:
        mcp.add_middleware(auth_middleware)

    for group_cls in API_GROUPS:
        group_cls(client).register_tools(mcp)

    return mcp


def create_server_from_env() -> FastMCP:
    try:
        creds = get_credentials_from_env()
    except ConfigurationError:
        creds = {"api_key": None, "access_token": None, "environment_id": None}

    return create_server(
        api_key=creds.get("api_key"),
        access_token=creds.get("access_token"),
        environment_id=creds.get("environment_id"),
        base_url=resolve_base_url(),
        timeout=int(os.getenv("CLDY_TIMEOUT", os.getenv("CLOUDABILITY_TIMEOUT", "60"))),
        response_format=os.getenv(
            "CLDY_RESPONSE_FORMAT",
            os.getenv("CLOUDABILITY_RESPONSE_FORMAT", "toon"),
        ),
        mode=os.getenv("CLDY_MODE", "local"),
    )
