"""Business mappings — dimensions and metrics — 10 tools."""

from typing import Any

from fastmcp import FastMCP

from ..transforms.business_mappings import dimension_body_from_params
from .base import BaseAPIGroup


class BusinessMappingsGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def create_business_dimension(
            name: str,
            rules: list[dict[str, str]] | None = None,
            default_value: str | None = None,
            default_value_expression: str | None = None,
        ) -> dict:
            """Create a custom business dimension for cost allocation. Use rules to map cloud resources to business categories based on tags, accounts, or other attributes.
            
            Args:
                name: Name of the business dimension
                rules: List of condition/value pairs (e.g., [{"condition": "tag_Environment==prod", "value": "Production"}])
                default_value: Static default value when no rules match
                default_value_expression: Expression for dynamic default value (e.g., "tag_Team")
            """
            params: dict[str, Any] = {"name": name}
            if rules:
                params["rules"] = rules
            if default_value:
                params["default_value"] = default_value
            if default_value_expression:
                params["default_value_expression"] = default_value_expression
            return await self._post("/business-mappings", dimension_body_from_params(params))

        @mcp.tool()
        async def list_business_mappings(
            limit: int | None = None,
            offset: int | None = None,
        ) -> dict:
            """List all custom business dimensions with their rules and configuration.
            
            Args:
                limit: Maximum number of results to return
                offset: Number of results to skip for pagination
            """
            params = {k: v for k, v in {"limit": limit, "offset": offset}.items() if v is not None}
            return await self._get("/business-mappings/dimensions", params=params or None)

        @mcp.tool()
        async def get_business_mapping(id: str) -> dict:  # noqa: A002
            """Get a specific business dimension by ID with full rule details.
            
            Args:
                id: Business dimension ID
            """
            return await self._get(f"/business-mappings/{id}")

        @mcp.tool()
        async def update_business_dimension(
            id: str,  # noqa: A002
            name: str | None = None,
            rules: list[dict[str, str]] | None = None,
            state: str | None = None,
        ) -> dict:
            """Update an existing business dimension. Note: name is required by the API when updating.
            
            Args:
                id: Business dimension ID
                name: Updated name (required by API)
                rules: Updated list of condition/value pairs
                state: State of the dimension (e.g., "active", "inactive")
            """
            params: dict[str, Any] = {}
            if name:
                params["name"] = name
            if rules:
                params["rules"] = rules
            if state:
                params["state"] = state
            return await self._put(f"/business-mappings/{id}", dimension_body_from_params(params))

        @mcp.tool()
        async def delete_business_dimension(id: str) -> dict:  # noqa: A002
            """Delete a business dimension.
            
            Args:
                id: Business dimension ID to delete
            """
            return await self._delete(f"/business-mappings/{id}")

        @mcp.tool()
        async def cldy_business_metrics_list() -> dict:
            """List all custom business metrics. Business metrics allow you to create calculated fields based on cost data and dimensions."""
            return await self._get("/business-mappings/metrics")

        @mcp.tool()
        async def cldy_business_metric_get(index: int) -> dict:
            """Get a specific business metric by index (1-10).
            
            Args:
                index: Metric index (1-10)
            """
            return await self._get(f"/internal/business-mappings/{index}/metrics")

        @mcp.tool()
        async def cldy_business_metric_create(
            name: str,
            numberFormat: str,
            defaultValueExpression: str,
            statements: list[dict[str, str]],
            preMatchExpression: str | None = None,
        ) -> dict:
            """Create a custom business metric using expression language. Metrics can perform calculations on cost data and dimensions.
            
            Args:
                name: Name of the metric
                numberFormat: Format for displaying numbers (e.g., "currency", "percentage", "decimal")
                defaultValueExpression: Expression for default value calculation
                statements: List of conditional statements with expressions (e.g., [{"condition": "vendor==aws", "expression": "unblended_cost * 1.1"}])
                preMatchExpression: Optional expression to evaluate before matching statements
            """
            body: dict[str, Any] = {
                "name": name,
                "numberFormat": numberFormat,
                "defaultValueExpression": defaultValueExpression,
                "statements": statements,
            }
            if preMatchExpression:
                body["preMatchExpression"] = preMatchExpression
            return await self._post("/internal/business-mappings/metrics/", body)

        @mcp.tool()
        async def cldy_business_metric_update(
            index: int,
            name: str | None = None,
            numberFormat: str | None = None,
            defaultValueExpression: str | None = None,
            statements: list[dict[str, str]] | None = None,
        ) -> dict:
            """Update an existing business metric.
            
            Args:
                index: Metric index (1-10)
                name: Updated name
                numberFormat: Updated number format
                defaultValueExpression: Updated default expression
                statements: Updated list of conditional statements
            """
            body: dict[str, Any] = {}
            if name:
                body["name"] = name
            if numberFormat:
                body["numberFormat"] = numberFormat
            if defaultValueExpression:
                body["defaultValueExpression"] = defaultValueExpression
            if statements:
                body["statements"] = statements
            return await self._put(f"/internal/business-mappings/{index}/metrics", body)

        @mcp.tool()
        async def cldy_business_metric_delete(index: int) -> dict:
            """Delete a business metric.
            
            Args:
                index: Metric index (1-10) to delete
            """
            return await self._delete(f"/internal/business-mappings/{index}/metrics")
