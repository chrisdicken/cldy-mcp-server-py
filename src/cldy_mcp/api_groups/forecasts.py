"""Forecasts and estimates — 2 tools."""

from fastmcp import FastMCP

from .base import BaseAPIGroup


class ForecastsGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def cldy_forecast_get(view_id: str | None = None) -> dict:
            """Retrieve spending forecast data for future periods.
            
            Args:
                view_id: Optional view ID to filter forecast data
            """
            params = {"view_id": view_id} if view_id else None
            return await self._get("/forecast", params=params)

        @mcp.tool()
        async def cldy_estimate_get(view_id: str | None = None) -> dict:
            """Retrieve current month/period spend estimate based on usage to date.
            
            Args:
                view_id: Optional view ID to filter estimate data
            """
            params = {"view_id": view_id} if view_id else None
            return await self._get("/estimate", params=params)
