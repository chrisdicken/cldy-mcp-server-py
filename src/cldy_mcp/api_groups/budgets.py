"""Budgets — 5 tools."""

from typing import Any

from fastmcp import FastMCP

from .base import BaseAPIGroup


class BudgetsGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def create_budget(
            name: str,
            view_id: str,
            basis: str,
            months: list[dict[str, Any]],
        ) -> dict:
            """Create a new budget for cost tracking and alerts.
            
            Args:
                name: Name of the budget
                view_id: ID of the view to apply the budget to
                basis: Cost basis for the budget (amortized, unblended, or blended)
                months: Array of monthly budget thresholds. Each item should have 'month' (YYYY-MM format) and 'threshold' (number)
            """
            body = {"name": name, "viewId": view_id, "basis": basis, "months": months}
            return await self._post("/budgets", body)

        @mcp.tool()
        async def list_budgets(
            limit: int | None = None,
            offset: int | None = None,
            sort_by: str | None = None,
            sort_order: str | None = None,
        ) -> dict:
            """List all budgets.
            
            Args:
                limit: Maximum number of results to return
                offset: Number of results to skip
                sort_by: Field to sort by
                sort_order: Sort order (asc or desc)
            """
            params = {k: v for k, v in {
                "limit": limit, "offset": offset, "sort_by": sort_by, "sort_order": sort_order,
            }.items() if v is not None}
            return await self._get("/budgets", params=params or None)

        @mcp.tool()
        async def get_budget(id: str) -> dict:  # noqa: A002
            """Get a specific budget by ID.
            
            Args:
                id: Budget ID
            """
            return await self._get(f"/budgets/{id}")

        @mcp.tool()
        async def update_budget(
            id: str,  # noqa: A002
            name: str | None = None,
            view_id: str | None = None,
            basis: str | None = None,
            months: list[dict[str, Any]] | None = None,
        ) -> dict:
            """Update an existing budget.
            
            Args:
                id: Budget ID
                name: New name for the budget
                view_id: New view ID to apply the budget to
                basis: New cost basis for the budget (amortized, unblended, or blended)
                months: Updated array of monthly budget thresholds with 'month' (YYYY-MM) and 'threshold' (number)
            """
            body: dict[str, Any] = {}
            if name is not None:
                body["name"] = name
            if view_id is not None:
                body["viewId"] = view_id
            if basis is not None:
                body["basis"] = basis
            if months is not None:
                body["months"] = months
            return await self._put(f"/budgets/{id}", body)

        @mcp.tool()
        async def delete_budget(id: str) -> dict:  # noqa: A002
            """Delete a budget.
            
            Args:
                id: Budget ID to delete
            """
            return await self._delete(f"/budgets/{id}")
