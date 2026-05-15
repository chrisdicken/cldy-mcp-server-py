"""Users — 3 tools."""

from typing import Any

from fastmcp import FastMCP

from .base import BaseAPIGroup


class UsersGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def list_users(
            limit: int | None = None,
            offset: int | None = None,
            sort_field: str | None = None,
            sort_direction: str | None = None,
            search: str | None = None,
            include_pagination_details: bool | None = None,
        ) -> dict:
            """List all users in the organization.
            
            Args:
                limit: Maximum number of results to return
                offset: Number of results to skip
                sort_field: Field to sort by
                sort_direction: Sort order (asc or desc)
                search: Search term to filter users
                include_pagination_details: Include pagination metadata in response
            """
            params = {k: v for k, v in {
                "limit": limit,
                "offset": offset,
                "sort_field": sort_field,
                "sort_direction": sort_direction,
                "search": search,
                "include_pagination_details": include_pagination_details,
            }.items() if v is not None}
            return await self._get("/users", params=params or None)

        @mcp.tool()
        async def get_user(id: str) -> dict:  # noqa: A002
            """Get a specific user by ID.
            
            Args:
                id: User ID
            """
            return await self._get(f"/users/{id}")

        @mcp.tool()
        async def update_user(
            id: str,  # noqa: A002
            full_name: str | None = None,
            role: str | None = None,
            restricted: bool | None = None,
            default_dimension_filter_set_id: int | None = None,
            new_shared_dimension_filter_set_ids: list[int] | None = None,
            shared_dimension_filter_set_ids: list[int] | None = None,
            unshare_existing_dimension_filter_sets: bool | None = None,
            default_dashboard_id: int | None = None,
        ) -> dict:
            """Update user settings and permissions.
            
            Args:
                id: User ID
                full_name: Full name of the user
                role: User role
                restricted: Whether the user account is restricted
                default_dimension_filter_set_id: Default view/filter set ID
                new_shared_dimension_filter_set_ids: New view IDs to share with user
                shared_dimension_filter_set_ids: Complete list of shared view IDs
                unshare_existing_dimension_filter_sets: Remove existing shared views
                default_dashboard_id: Default dashboard ID
            """
            body: dict[str, Any] = {}
            if full_name is not None:
                body["full_name"] = full_name
            if role is not None:
                body["role"] = role
            if restricted is not None:
                body["restricted"] = restricted
            if default_dimension_filter_set_id is not None:
                body["default_dimension_filter_set_id"] = default_dimension_filter_set_id
            if new_shared_dimension_filter_set_ids is not None:
                body["new_shared_dimension_filter_set_ids"] = new_shared_dimension_filter_set_ids
            if shared_dimension_filter_set_ids is not None:
                body["shared_dimension_filter_set_ids"] = shared_dimension_filter_set_ids
            if unshare_existing_dimension_filter_sets is not None:
                body["unshare_existing_dimension_filter_sets"] = unshare_existing_dimension_filter_sets
            if default_dashboard_id is not None:
                body["default_dashboard_id"] = default_dashboard_id
            return await self._put(f"/users/{id}", body)
