"""Cost reporting API group — 7 tools."""

from typing import Any, Literal

from fastmcp import FastMCP

from .base import BaseAPIGroup


def _report_params(
    start_date: str,
    end_date: str,
    dimensions: str,
    metrics: str,
    filters: list[str] | None = None,
    sort: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    chart: int | None = None,
    view_id: str | None = None,
    apply_allocations: bool | None = None,
    token_id: str | None = None,
    use_dimension_names: bool | None = None,
) -> dict[str, Any]:
    p: dict[str, Any] = {
        "start_date": start_date,
        "end_date": end_date,
        "dimensions": dimensions,
        "metrics": metrics,
    }
    if filters:
        p["filters"] = filters
    if sort:
        p["sort"] = sort
    if limit is not None:
        p["limit"] = limit
    if offset is not None:
        p["offset"] = offset
    if chart is not None:
        p["chart"] = chart
    if view_id is not None:
        p["view_id"] = view_id
    if apply_allocations is not None:
        p["applyAllocations"] = apply_allocations
    if token_id is not None:
        p["tokenId"] = token_id
    if use_dimension_names is not None:
        p["useDimensionNames"] = use_dimension_names
    return p


class CostReportingGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def cldy_cost_report_run(
            start_date: str,
            end_date: str,
            dimensions: str,
            metrics: str,
            filters: list[str] | None = None,
            sort: str | None = None,
            limit: int | None = None,
            offset: int | None = None,
            chart: int | None = None,
            view_id: str | None = None,
            apply_allocations: bool | None = None,
            token_id: str | None = None,
            format: Literal["json", "csv"] = "json",
            response_shape: Literal["full", "summary"] = "full",
            sample_rows: int = 20,
        ) -> dict:
            """Run a cost report dynamically. Returns cost data grouped by dimensions with selected metrics.
            
            Args:
                start_date: Start date in YYYY-MM-DD format or relative date string (e.g., "7 days ago at 00:00:00", "beginning of last month")
                end_date: End date in YYYY-MM-DD format or relative date string (e.g., "yesterday at 23:59:59", "end of month")
                dimensions: Comma-delimited list of dimensions to group by (e.g., "vendor,region,service_name")
                metrics: Comma-delimited list of metrics to include (e.g., "unblended_cost,usage_quantity")
                filters: Array of filter strings. Each filter: "dimension_name<operator>value" (URL-encoded). Example: ["transaction_type==usage", "vendor==Amazon"]
                sort: Comma-delimited measures with ASC/DESC suffix. Example: "total_amortized_costASC,regionDESC"
                limit: Max rows to return (default 10000, set 0 for up to 64000)
                offset: Starting position for pagination
                chart: Set to 1 for chart-format output pivoted around dates
                view_id: View to apply (omit for user default, "0" for unrestricted)
                apply_allocations: If true, report includes post-allocated costs
                token_id: Pagination token from previous response
                format: Output format (json or csv)
                response_shape: Use 'summary' for large reports to get row count + sample rows
                sample_rows: Number of sample rows when using response_shape=summary
            """
            params = _report_params(
                start_date, end_date, dimensions, metrics, filters, sort, limit, offset,
                chart, view_id, apply_allocations, token_id,
            )
            accept = "text/csv" if format == "csv" else None
            return await self._get(
                "/reporting/cost/run",
                params=params,
                accept=accept,
                array_format="repeat",
                response_shape=response_shape,
                sample_rows=sample_rows,
            )

        @mcp.tool()
        async def cldy_cost_report_enqueue(
            start_date: str,
            end_date: str,
            dimensions: str,
            metrics: str,
            filters: list[str] | None = None,
            sort: str | None = None,
            limit: int | None = None,
            offset: int | None = None,
            chart: int | None = None,
            view_id: str | None = None,
            apply_allocations: bool | None = None,
            use_dimension_names: bool | None = None,
        ) -> dict:
            """Enqueue a cost report for async generation. Returns report ID to check status. Rate limit: 20 requests per user.
            
            Args:
                start_date: Start date in YYYY-MM-DD format or relative date string
                end_date: End date in YYYY-MM-DD format or relative date string
                dimensions: Comma-delimited list of dimensions to group by
                metrics: Comma-delimited list of metrics to include
                filters: Array of filter strings
                sort: Comma-delimited measures with ASC/DESC suffix
                limit: Max rows to return
                offset: Starting position
                chart: Set to 1 for chart format
                view_id: View to apply
                apply_allocations: Include post-allocated costs
                use_dimension_names: Use Mapping Name instead of ID in exported Business Mapping columns
            """
            params = _report_params(
                start_date, end_date, dimensions, metrics, filters, sort, limit, offset,
                chart, view_id, apply_allocations, None, use_dimension_names,
            )
            return await self._get("/reporting/cost/enqueue", params=params, array_format="repeat")

        @mcp.tool()
        async def cldy_cost_report_state(report_id: str) -> dict:
            """Check status of an enqueued cost report. Returns status: enqueued, running, errored, or finished.
            
            Args:
                report_id: Report ID returned from enqueue operation
            """
            return await self._get(f"/reporting/reports/{report_id}/state")

        @mcp.tool()
        async def cldy_cost_report_results(
            report_id: str,
            response_shape: Literal["full", "summary"] = "full",
            sample_rows: int = 20,
        ) -> dict:
            """Retrieve results of a finished enqueued cost report.
            
            Args:
                report_id: Report ID of finished report
                response_shape: Use 'summary' for large reports to get row count + sample rows
                sample_rows: Number of sample rows when using response_shape=summary
            """
            return await self._get(
                f"/reporting/reports/{report_id}/results",
                response_shape=response_shape,
                sample_rows=sample_rows,
            )

        @mcp.tool()
        async def cldy_cost_reports_list() -> dict:
            """List all saved cost reports owned by or shared with the user/organization."""
            return await self._get("/reporting/reports/cost")

        @mcp.tool()
        async def cldy_cost_measures_list(apply_allocations: bool | None = None) -> dict:
            """List available dimensions and metrics for cost reports.
            
            Args:
                apply_allocations: If true, only show measures supported by cost sharing
            """
            params = {}
            if apply_allocations is not None:
                params["apply_allocations"] = apply_allocations
            return await self._get("/reporting/cost/measures", params=params or None)

        @mcp.tool()
        async def cldy_cost_filters_list() -> dict:
            """List all available comparison operators for cost report filters."""
            return await self._get("/reporting/cost/filters")
