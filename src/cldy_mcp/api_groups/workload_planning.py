"""Workload planning — 18 tools."""

import base64
from typing import Any, Literal

from fastmcp import FastMCP

from .base import BaseAPIGroup


class WorkloadPlanningGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def cldy_workload_create(
            name: str,
            status: str,
            csp: list[dict[str, Any]],
            description: str | None = None,
            preferredCsp: str | None = None,
        ) -> dict:
            """Create a new multi-cloud workload for cost comparison across AWS, Azure, GCP, and OCI. Define resources once and get pricing for all clouds.
            
            Args:
                name: Name of the workload
                status: Status (e.g., "draft", "active")
                csp: List of cloud service provider configurations with resource definitions
                description: Optional description of the workload
                preferredCsp: Preferred cloud provider (e.g., "aws", "azure", "gcp", "oci")
            """
            body: dict[str, Any] = {"name": name, "status": status, "csp": csp}
            if description:
                body["description"] = description
            if preferredCsp:
                body["preferredCsp"] = preferredCsp
            return await self._post("/workload", body)

        @mcp.tool()
        async def cldy_workloads_list(
            offset: int | None = None,
            limit: int | None = None,
            search: str | None = None,
            user_type: Literal["all", "admin", "mine", "shared"] | None = None,
        ) -> dict:
            """List all workloads with optional filtering by ownership and search terms.
            
            Args:
                offset: Number of results to skip for pagination
                limit: Maximum number of results to return
                search: Search term to filter workloads by name or description
                user_type: Filter by ownership - "all", "admin", "mine", or "shared"
            """
            params: dict[str, Any] = {}
            if offset is not None:
                params["offset"] = offset
            if limit is not None:
                params["limit"] = limit
            if search:
                params["search"] = search
            if user_type:
                params["user-type"] = user_type
            return await self._get("/internal/workload", params=params or None)

        @mcp.tool()
        async def cldy_workload_get_resources(workload_id: str) -> dict:
            """Get all resources defined in a workload with their specifications.
            
            Args:
                workload_id: Workload ID
            """
            return await self._get(f"/workload/{workload_id}/resource")

        @mcp.tool()
        async def cldy_workload_download_template(
            download_type: Literal["template", "resources"],
            format: Literal["json", "xlsx"],  # noqa: A002
            workload_id: str,
        ) -> dict:
            """Download workload template or resources in JSON or Excel format. Templates help you define resources in bulk.
            
            Args:
                download_type: Type to download - "template" (empty structure) or "resources" (current data)
                format: Output format - "json" or "xlsx"
                workload_id: Workload ID
            """
            if format == "xlsx":
                return await self._get_binary(
                    f"/workload/{download_type}/{format}/export/{workload_id}",
                    accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            return await self._get(f"/workload/{download_type}/{format}/export/{workload_id}")

        @mcp.tool()
        async def cldy_workload_upload_resources(
            upload_type: Literal["JSON", "XLSX"],
            workload_id: str,
            file_content: str,
        ) -> dict:
            """Upload workload resources in bulk from a JSON or Excel file. File content must be base64-encoded.
            
            Args:
                upload_type: File type - "JSON" or "XLSX"
                workload_id: Workload ID
                file_content: Base64-encoded file content
            """
            raw = base64.b64decode(file_content)
            filename = "upload.json" if upload_type == "JSON" else "upload.xlsx"
            content_type = (
                "application/json" if upload_type == "JSON"
                else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            client = self._get_client()
            resp = await client.request(
                "POST",
                f"/workload/bulk-upload/{upload_type}/{workload_id}",
                files={"file": (filename, raw, content_type)},
            )
            data = resp.json() if resp.content else {}
            if isinstance(data, dict) and "result" in data:
                envelope = {"result": data["result"]}
                if data.get("meta"):
                    envelope["meta"] = data["meta"]
                return self._format(envelope)
            return self._format({"result": data})

        @mcp.tool()
        async def cldy_workload_upload_errors(workload_id: str) -> dict:
            """Get resources that failed validation during the last upload with error details.
            
            Args:
                workload_id: Workload ID
            """
            return await self._get(f"/workload/errors/export/{workload_id}")

        @mcp.tool()
        async def cldy_workload_generate_recommendations(workload_id: str) -> dict:
            """Trigger the recommendation generation job to calculate pricing across all cloud providers. This is an async operation.
            
            Args:
                workload_id: Workload ID
            """
            return await self._post(f"/workload/job/{workload_id}")

        @mcp.tool()
        async def cldy_workload_job_status(workload_id: str) -> dict:
            """Check the status of the recommendation generation job (pending, running, completed, failed).
            
            Args:
                workload_id: Workload ID
            """
            return await self._get(f"/workload/job/status/{workload_id}")

        @mcp.tool()
        async def cldy_workload_get_recommendations(
            workload_id: str,
            vendor: Literal["aws", "azure", "gcp", "oci"],
        ) -> dict:
            """Get detailed pricing recommendations for a specific cloud vendor. Shows instance types, pricing, and configurations.
            
            Args:
                workload_id: Workload ID
                vendor: Cloud vendor - "aws", "azure", "gcp", or "oci"
            """
            return await self._get(f"/workload/{workload_id}/recommendations/{vendor}")

        @mcp.tool()
        async def cldy_workload_save_recommendations(
            workload_id: str,
            selections: list[dict[str, Any]],
        ) -> dict:
            """Save user-selected recommendations for specific resources. Used to lock in preferred instance types or configurations.
            
            Args:
                workload_id: Workload ID
                selections: List of selected recommendations with resource IDs and chosen configurations
            """
            return await self._put(f"/workload/{workload_id}/cloud-cost", selections)

        @mcp.tool()
        async def cldy_workload_summary(workload_id: str, vendor: str) -> dict:
            """Get a high-level cost summary for a vendor showing total monthly costs and resource counts.
            
            Args:
                workload_id: Workload ID
                vendor: Cloud vendor (e.g., "aws", "azure", "gcp", "oci")
            """
            return await self._get(
                f"/workload/report/summary/{workload_id}",
                params={"vendor": vendor},
            )

        @mcp.tool()
        async def cldy_workload_analysis(workload_id: str, vendor: str) -> dict:
            """Get detailed cost analysis for a vendor with breakdowns by resource type, region, and service.
            
            Args:
                workload_id: Workload ID
                vendor: Cloud vendor (e.g., "aws", "azure", "gcp", "oci")
            """
            return await self._get(
                f"/workload/report/analysis/{workload_id}",
                params={"vendor": vendor},
            )

        @mcp.tool()
        async def cldy_workload_export(workload_id: str) -> dict:
            """Export the complete workload summary as an Excel file with all vendor comparisons and details.
            
            Args:
                workload_id: Workload ID
            """
            return await self._get_binary(
                f"/workload/report/export/{workload_id}",
                accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        @mcp.tool()
        async def cldy_workload_duplicate(workload_id: str, new_name: str) -> dict:
            """Create a copy of an existing workload with a new name. Useful for creating variations or what-if scenarios.
            
            Args:
                workload_id: Source workload ID to duplicate
                new_name: Name for the new workload
            """
            return await self._post("/workload/duplicate", {"id": workload_id, "name": new_name})

        @mcp.tool()
        async def cldy_workload_delete(workload_id: str) -> dict:
            """Delete a workload and all its associated resources and recommendations.
            
            Args:
                workload_id: Workload ID to delete
            """
            return await self._delete(f"/workload/{workload_id}")

        @mcp.tool()
        async def cldy_workload_preferences_get() -> dict:
            """Get organization-wide workload planning preferences and default settings."""
            return await self._get("/workload/admin-preferences")

        @mcp.tool()
        async def cldy_workload_preferences_update(preferences: list[dict[str, Any]]) -> dict:
            """Update organization-wide workload planning preferences such as default regions, instance families, or pricing models.
            
            Args:
                preferences: List of preference settings to update
            """
            return await self._put("/workload/admin-preferences", {"preferences": preferences})

        @mcp.tool()
        async def cldy_workload_static_data() -> dict:
            """Get static reference data including available regions, instance types, and configuration options for all cloud providers."""
            return await self._get("/workload/static-data")
