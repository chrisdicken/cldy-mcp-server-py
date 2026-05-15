"""Budget subscriptions — 5 tools."""

from typing import Any

from fastmcp import FastMCP

from .base import BaseAPIGroup


class BudgetSubscriptionsGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def cldy_budget_subscriptions_list() -> dict:
            """List all budget subscriptions for alert notifications."""
            return await self._get("/budget-subscriptions")

        @mcp.tool()
        async def cldy_budget_subscription_get(subscription_id: str) -> dict:
            """Get a specific budget subscription by ID.
            
            Args:
                subscription_id: Budget subscription ID
            """
            return await self._get(f"/budget-subscriptions/{subscription_id}")

        @mcp.tool()
        async def cldy_budget_subscription_create(
            budgetId: str,
            notifyExceeded: bool | None = None,
            notifyExpected: bool | None = None,
        ) -> dict:
            """Create a new budget subscription for alert notifications when budget thresholds are exceeded or expected to be exceeded.
            
            Args:
                budgetId: ID of the budget to subscribe to
                notifyExceeded: Send notification when budget is exceeded
                notifyExpected: Send notification when budget is expected to be exceeded
            """
            body: dict[str, Any] = {"budgetId": budgetId}
            if notifyExceeded is not None:
                body["notifyExceeded"] = notifyExceeded
            if notifyExpected is not None:
                body["notifyExpected"] = notifyExpected
            return await self._post("/budget-subscriptions", body)

        @mcp.tool()
        async def cldy_budget_subscription_update(
            subscription_id: str,
            budgetId: str | None = None,
            notifyExceeded: bool | None = None,
            notifyExpected: bool | None = None,
        ) -> dict:
            """Update an existing budget subscription.
            
            Args:
                subscription_id: Budget subscription ID
                budgetId: ID of the budget to subscribe to
                notifyExceeded: Send notification when budget is exceeded
                notifyExpected: Send notification when budget is expected to be exceeded
            """
            body: dict[str, Any] = {}
            if budgetId is not None:
                body["budgetId"] = budgetId
            if notifyExceeded is not None:
                body["notifyExceeded"] = notifyExceeded
            if notifyExpected is not None:
                body["notifyExpected"] = notifyExpected
            return await self._put(f"/budget-subscriptions/{subscription_id}", body)

        @mcp.tool()
        async def cldy_budget_subscription_delete(subscription_id: str) -> dict:
            """Delete a budget subscription.
            
            Args:
                subscription_id: Budget subscription ID to delete
            """
            return await self._delete(f"/budget-subscriptions/{subscription_id}")
