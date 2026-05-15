"""Progressive tool discovery."""

from typing import Literal

from fastmcp import FastMCP

from ..registry import DetailLevel, search_catalog
from .base import BaseAPIGroup


class DiscoveryGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def search_tools(
            query: str = "",
            category: str | None = None,
            detail: Literal["name", "summary", "full"] = "summary",
        ) -> dict:
            """
            Search available Cloudability MCP tools without loading all schemas.

            Use detail='name' for minimal tokens, 'summary' for name+category+description,
            or 'full' to include parameter outlines. Call this before invoking domain tools.
            """
            return search_catalog(query=query, category=category, detail=detail)  # type: ignore[arg-type]
