"""Views — 7 tools."""

from typing import Any

from fastmcp import FastMCP

from .base import BaseAPIGroup


class ViewsGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def create_view(
            title: str,
            filters: list[dict[str, Any]] | None = None,
            shared_with_organization: bool | None = None,
        ) -> dict:
            """Create a new filtered view for cost analysis.
            
            Args:
                title: Title of the view
                filters: Array of filters to apply. Each filter has 'field' (e.g., vendor, tag_user_Environment), 'comparator' (==, !=, >, <, >=, <=, in, not_in), and 'value' (string or array)
                shared_with_organization: Whether to share the view with the entire organization
            """
            body: dict[str, Any] = {"title": title}
            if filters:
                body["filters"] = filters
            if shared_with_organization is not None:
                body["sharedWithOrganization"] = shared_with_organization
            return await self._post("/views", body)

        @mcp.tool()
        async def list_views(
            limit: int | None = None,
            offset: int | None = None,
            sort_by: str | None = None,
            sort_order: str | None = None,
        ) -> dict:
            """List all views.
            
            Args:
                limit: Maximum number of results to return
                offset: Number of results to skip
                sort_by: Field to sort by
                sort_order: Sort order (asc or desc)
            """
            params = {k: v for k, v in {
                "limit": limit, "offset": offset, "sort_by": sort_by, "sort_order": sort_order,
            }.items() if v is not None}
            return await self._get("/views", params=params or None)

        @mcp.tool()
        async def get_view(id: str) -> dict:  # noqa: A002
            """Get a specific view by ID.
            
            Args:
                id: View ID
            """
            return await self._get(f"/views/{id}")

        @mcp.tool()
        async def update_view(
            id: str,  # noqa: A002
            title: str | None = None,
            filters: list[dict[str, Any]] | None = None,
            shared_with_organization: bool | None = None,
        ) -> dict:
            """Update an existing view.
            
            Args:
                id: View ID
                title: New title for the view
                filters: Updated array of filters with 'field', 'comparator', and 'value'
                shared_with_organization: Whether to share the view with the entire organization
            """
            body: dict[str, Any] = {}
            if title:
                body["title"] = title
            if filters:
                body["filters"] = filters
            if shared_with_organization is not None:
                body["sharedWithOrganization"] = shared_with_organization
            return await self._put(f"/views/{id}", body)

        @mcp.tool()
        async def delete_view(id: str) -> dict:  # noqa: A002
            """Delete a view.
            
            Args:
                id: View ID to delete
            """
            return await self._delete(f"/views/{id}")

        @mcp.tool()
        async def views_get_for_user(user_id: str, org_id: str) -> dict:
            """List all views that a specific user can see and apply.
            
            Args:
                user_id: ID of the user to get views for
                org_id: Organization ID
            """
            return await self._get(f"/views/user/{user_id}", params={"orgId": org_id})

        @mcp.tool()
        async def views_get_for_multiple_users(
            user_ids: list[str],
            org_id: str | None = None,
        ) -> dict:
            """List all views that multiple users can see and apply.
            
            Args:
                user_ids: List of user IDs to get views for
                org_id: Optional organization ID
            """
            params: dict[str, Any] = {"userIds": ",".join(user_ids)}
            if org_id:
                params["orgId"] = org_id
            return await self._get("/views/users", params=params)
