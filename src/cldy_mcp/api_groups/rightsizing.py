"""Rightsizing ROI — 2 tools."""

from fastmcp import FastMCP

from .base import BaseAPIGroup


class RightsizingGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def cldy_rightsizing_list(
            filters: list[str] | None = None,
            limit: int | None = None,
            offset: int | None = None,
            sort: str | None = None,
            viewId: str | None = None,
        ) -> dict:
            """List tracked rightsizing recommendations with realized savings. Shows instances that were resized and the actual cost savings achieved.
            
            Args:
                filters: Optional list of filters (e.g., ["vendor==aws", "region==us-east-1"])
                limit: Maximum number of results to return
                offset: Number of results to skip for pagination
                sort: Sort field (e.g., "savings" or "-savings" for descending)
                viewId: Optional view ID to filter results
            """
            params = {k: v for k, v in {
                "limit": limit, "offset": offset, "sort": sort, "viewId": viewId,
            }.items() if v is not None}
            if filters:
                params["filters"] = filters
            return await self._get(
                "/rightsizing-roi/actioned",
                params=params or None,
                array_format="repeat" if filters else "comma",
            )

        @mcp.tool()
        async def cldy_rightsizing_delete(orgId: int, resourceId: str) -> dict:
            """Delete a tracked rightsizing recommendation from the ROI tracking system.
            
            Args:
                orgId: Organization ID
                resourceId: Resource ID of the rightsizing recommendation to delete
            """
            return await self._delete(
                "/rightsizing-roi/actioned",
                params={"orgId": orgId, "ResourceId": resourceId},
            )
