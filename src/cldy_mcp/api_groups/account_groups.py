"""Account groups — 5 tools."""

from typing import Any

from fastmcp import FastMCP

from .base import BaseAPIGroup


class AccountGroupsGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def create_account_group(name: str, position: int | None = None) -> dict:
            """Create a new account group in Cloudability.
            
            Args:
                name: Name of the account group
                position: Position/order of the account group (optional)
            """
            body: dict[str, Any] = {"name": name}
            if position is not None:
                body["position"] = position
            return await self._post("/account_groups", body)

        @mcp.tool()
        async def list_account_groups(
            limit: int | None = None,
            offset: int | None = None,
            sort_by: str | None = None,
            sort_order: str | None = None,
        ) -> dict:
            """List all account groups.
            
            Args:
                limit: Maximum number of results to return (default: 100)
                offset: Number of results to skip (default: 0)
                sort_by: Field to sort by
                sort_order: Sort order (asc or desc)
            """
            params = {k: v for k, v in {
                "limit": limit, "offset": offset, "sort_by": sort_by, "sort_order": sort_order,
            }.items() if v is not None}
            return await self._get("/account_groups", params=params or None)

        @mcp.tool()
        async def get_account_group(id: str) -> dict:  # noqa: A002
            """Get a specific account group by ID.
            
            Args:
                id: Account group ID
            """
            return await self._get(f"/account_groups/{id}")

        @mcp.tool()
        async def update_account_group(
            id: str,  # noqa: A002
            name: str | None = None,
            position: int | None = None,
        ) -> dict:
            """Update an existing account group.
            
            Args:
                id: Account group ID
                name: New name for the account group
                position: New position/order for the account group
            """
            body = {k: v for k, v in {"name": name, "position": position}.items() if v is not None}
            return await self._put(f"/account_groups/{id}", body)

        @mcp.tool()
        async def delete_account_group(id: str) -> dict:  # noqa: A002
            """Delete an account group.
            
            Args:
                id: Account group ID to delete
            """
            return await self._delete(f"/account_groups/{id}")
