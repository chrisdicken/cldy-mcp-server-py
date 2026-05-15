"""Constants and regional API base URLs."""

import os
from typing import Literal

Region = Literal["us", "eu", "au", "me"]

REGION_BASE_URLS: dict[Region, str] = {
    "us": "https://api.cloudability.com/v3",
    "eu": "https://api-eu.cloudability.com/v3",
    "au": "https://api-au.cloudability.com/v3",
    "me": "https://api-me.cloudability.com/v3",
}

DEFAULT_REGION: Region = "us"


def resolve_base_url() -> str:
    """Resolve API base URL from env (supports TS and engineering prefixes)."""
    explicit = os.getenv("CLOUDABILITY_BASE_URL") or os.getenv("CLDY_API_URL")
    if explicit:
        url = explicit.rstrip("/")
        return url if url.endswith("/v3") else f"{url}/v3"

    region = (
        os.getenv("CLOUDABILITY_REGION")
        or os.getenv("CLDY_REGION")
        or DEFAULT_REGION
    ).lower()
    if region not in REGION_BASE_URLS:
        region = DEFAULT_REGION
    return REGION_BASE_URLS[region]  # type: ignore[index]
