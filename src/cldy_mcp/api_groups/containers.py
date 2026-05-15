"""Kubernetes containers — 6 tools."""

from typing import Any

from fastmcp import FastMCP

from .base import BaseAPIGroup


class ContainersGroup(BaseAPIGroup):
    def register_tools(self, mcp: FastMCP) -> None:
        @mcp.tool()
        async def cldy_containers_provision(cluster_name: str) -> dict:
            """Provision a new Kubernetes cluster for cost collection. Returns cluster ID and configuration details.
            
            Args:
                cluster_name: Name for the new cluster
            """
            return await self._post("/containers/provisioning", {"cluster_name": cluster_name})

        @mcp.tool()
        async def cldy_containers_cluster_deployment(cluster_id: str) -> dict:
            """Get the YAML deployment manifest for a provisioned cluster. Use this to deploy the Cloudability agent to your cluster.
            
            Args:
                cluster_id: Cluster ID from provisioning
            """
            return await self._get(f"/containers/provisioning/{cluster_id}")

        @mcp.tool()
        async def cldy_containers_clusters_list() -> dict:
            """List all provisioned Kubernetes clusters with their status and configuration."""
            return await self._get("/containers/clusters")

        @mcp.tool()
        async def cldy_containers_usage(
            start_date: str,
            end_date: str,
            cluster_id: str | None = None,
            namespace: str | None = None,
            filters: list[str] | None = None,
        ) -> dict:
            """Get container resource usage metrics including CPU, memory, network, and filesystem usage. Useful for understanding resource consumption patterns.
            
            Args:
                start_date: Start date in YYYY-MM-DD format
                end_date: End date in YYYY-MM-DD format
                cluster_id: Optional cluster ID to filter results
                namespace: Optional namespace to filter results
                filters: Optional list of filters (e.g., ["label_app==nginx", "node==worker-1"])
            """
            params: dict[str, Any] = {"start_date": start_date, "end_date": end_date}
            if cluster_id:
                params["cluster_id"] = cluster_id
            if namespace:
                params["namespace"] = namespace
            if filters:
                params["filters"] = filters
            return await self._get("/containers/usage", params=params, array_format="repeat")

        @mcp.tool()
        async def cldy_containers_labels(
            start_date: str,
            end_date: str,
            cluster_id: str | None = None,
        ) -> dict:
            """Get all observed Kubernetes label keys within a timeframe. Useful for discovering available labels for filtering.
            
            Args:
                start_date: Start date in YYYY-MM-DD format
                end_date: End date in YYYY-MM-DD format
                cluster_id: Optional cluster ID to filter results
            """
            params: dict[str, Any] = {"start_date": start_date, "end_date": end_date}
            if cluster_id:
                params["cluster_id"] = cluster_id
            return await self._get("/containers/labels", params=params)

        @mcp.tool()
        async def cldy_containers_counts(
            start_date: str,
            end_date: str,
            dimension: str,
            cluster_id: str | None = None,
        ) -> dict:
            """Count distinct values for a container dimension (e.g., namespace, pod, container). Useful for understanding cardinality.
            
            Args:
                start_date: Start date in YYYY-MM-DD format
                end_date: End date in YYYY-MM-DD format
                dimension: Dimension to count (e.g., "namespace", "pod", "container", "node")
                cluster_id: Optional cluster ID to filter results
            """
            params: dict[str, Any] = {
                "start_date": start_date,
                "end_date": end_date,
                "dimension": dimension,
            }
            if cluster_id:
                params["cluster_id"] = cluster_id
            return await self._get("/containers/counts", params=params)
