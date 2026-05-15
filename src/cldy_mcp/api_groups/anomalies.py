"""Anomaly detection — 7 tools."""

from typing import Any

from fastmcp import FastMCP

from .base import BaseAPIGroup


class AnomaliesGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def cldy_anomalies_list(
            startDate: str,
            endDate: str,
            viewId: str,
            filter: str | None = None,  # noqa: A002
            id: str | None = None,  # noqa: A002
        ) -> dict:
            """List cost anomalies detected within a date range for a specific view. Returns unusual spending patterns with details about affected services and resources.
            
            Args:
                startDate: Start date in YYYY-MM-DD format
                endDate: End date in YYYY-MM-DD format
                viewId: View ID to filter anomalies
                filter: Optional filter (e.g., "enhancedServiceName==AWS EC2")
                id: Optional anomaly ID to look up a single anomaly
            """
            params: dict[str, Any] = {"startDate": startDate, "endDate": endDate, "viewId": viewId}
            if filter:
                params["filter"] = filter
            if id:
                params["id"] = id
            return await self._get("/anomalies", params=params)

        @mcp.tool()
        async def cldy_anomaly_get(id: str, viewId: str) -> dict:  # noqa: A002
            """Get a specific anomaly by ID.
            
            Args:
                id: Anomaly ID
                viewId: View ID
            """
            return await self._get("/anomalies", params={"id": id, "viewId": viewId})

        @mcp.tool()
        async def cldy_anomaly_subscriptions_list(viewId: str) -> dict:
            """List all anomaly alert subscriptions for a view.
            
            Args:
                viewId: View ID to list subscriptions for
            """
            return await self._get("/anomaly-subscriptions", params={"viewId": viewId})

        @mcp.tool()
        async def cldy_anomaly_subscription_get(subscription_id: str) -> dict:
            """Get a specific anomaly subscription by ID.
            
            Args:
                subscription_id: Anomaly subscription ID
            """
            return await self._get(f"/anomaly-subscriptions/{subscription_id}")

        @mcp.tool()
        async def cldy_anomaly_subscription_create(
            viewId: str,
            delivery: dict[str, str],
            unusualSpendThreshold: float | None = None,
            unusualPercentageThreshold: float | None = None,
            description: str | None = None,
            sharedUserIds: list[str] | None = None,
        ) -> dict:
            """Create a new anomaly alert subscription. Set thresholds for unusual spend (dollar amount) and/or unusual percentage. Omit a threshold to not apply it. Setting to 0 is valid.
            
            Args:
                viewId: View ID to monitor for anomalies
                delivery: Delivery method configuration with 'method' key (email or pagerduty)
                unusualSpendThreshold: Dollar threshold for unusual spend (optional)
                unusualPercentageThreshold: Percentage threshold for unusual spend (optional)
                description: Optional description of the subscription
                sharedUserIds: User IDs to receive alerts
            """
            body: dict[str, Any] = {"delivery": delivery}
            if unusualSpendThreshold is not None:
                body["unusualSpendThreshold"] = unusualSpendThreshold
            if unusualPercentageThreshold is not None:
                body["unusualPercentageThreshold"] = unusualPercentageThreshold
            if description:
                body["description"] = description
            if sharedUserIds:
                body["sharedUserIds"] = sharedUserIds
            return await self._post(
                "/anomaly-subscriptions",
                body,
                params={"viewId": viewId},
            )

        @mcp.tool()
        async def cldy_anomaly_subscription_update(
            subscription_id: str,
            viewId: str,
            delivery: dict[str, str] | None = None,
            unusualSpendThreshold: float | None = None,
            unusualPercentageThreshold: float | None = None,
            description: str | None = None,
            sharedUserIds: list[str] | None = None,
        ) -> dict:
            """Update an existing anomaly subscription.
            
            Args:
                subscription_id: Anomaly subscription ID
                viewId: View ID
                delivery: Updated delivery method configuration
                unusualSpendThreshold: Updated dollar threshold
                unusualPercentageThreshold: Updated percentage threshold
                description: Updated description
                sharedUserIds: Updated list of user IDs to receive alerts
            """
            body: dict[str, Any] = {}
            if delivery:
                body["delivery"] = delivery
            if unusualSpendThreshold is not None:
                body["unusualSpendThreshold"] = unusualSpendThreshold
            if unusualPercentageThreshold is not None:
                body["unusualPercentageThreshold"] = unusualPercentageThreshold
            if description is not None:
                body["description"] = description
            if sharedUserIds is not None:
                body["sharedUserIds"] = sharedUserIds
            return await self._put(
                f"/anomaly-subscriptions/{subscription_id}",
                body,
                params={"viewId": viewId},
            )

        @mcp.tool()
        async def cldy_anomaly_subscription_delete(subscription_id: str) -> dict:
            """Delete an anomaly subscription.
            
            Args:
                subscription_id: Anomaly subscription ID to delete
            """
            return await self._delete(f"/anomaly-subscriptions/{subscription_id}")
