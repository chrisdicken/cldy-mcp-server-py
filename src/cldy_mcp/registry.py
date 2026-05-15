"""Static catalog of all 77 Cloudability MCP tools for progressive discovery."""

from typing import Any, Literal, TypedDict


class ToolEntry(TypedDict):
    name: str
    category: str
    description: str
    parameters: dict[str, str]


TOOL_CATALOG: list[ToolEntry] = [
    # Account groups (5)
    {"name": "create_account_group", "category": "account_groups", "description": "Create a new account group", "parameters": {"name": "string", "position": "number?"}},
    {"name": "list_account_groups", "category": "account_groups", "description": "List all account groups", "parameters": {"limit": "number?", "offset": "number?"}},
    {"name": "get_account_group", "category": "account_groups", "description": "Get account group by ID", "parameters": {"id": "string"}},
    {"name": "update_account_group", "category": "account_groups", "description": "Update account group", "parameters": {"id": "string", "name": "string?", "position": "number?"}},
    {"name": "delete_account_group", "category": "account_groups", "description": "Delete account group", "parameters": {"id": "string"}},
    # Budgets (5)
    {"name": "create_budget", "category": "budgets", "description": "Create a new budget", "parameters": {"name": "string", "view_id": "string", "basis": "string", "months": "array"}},
    {"name": "list_budgets", "category": "budgets", "description": "List all budgets", "parameters": {}},
    {"name": "get_budget", "category": "budgets", "description": "Get budget by ID", "parameters": {"id": "string"}},
    {"name": "update_budget", "category": "budgets", "description": "Update budget", "parameters": {"id": "string"}},
    {"name": "delete_budget", "category": "budgets", "description": "Delete budget", "parameters": {"id": "string"}},
    # Budget subscriptions (5)
    {"name": "cldy_budget_subscriptions_list", "category": "budget_subscriptions", "description": "List budget alert subscriptions", "parameters": {}},
    {"name": "cldy_budget_subscription_get", "category": "budget_subscriptions", "description": "Get budget subscription", "parameters": {"subscription_id": "string"}},
    {"name": "cldy_budget_subscription_create", "category": "budget_subscriptions", "description": "Create budget subscription", "parameters": {"budgetId": "string"}},
    {"name": "cldy_budget_subscription_update", "category": "budget_subscriptions", "description": "Update budget subscription", "parameters": {"subscription_id": "string"}},
    {"name": "cldy_budget_subscription_delete", "category": "budget_subscriptions", "description": "Delete budget subscription", "parameters": {"subscription_id": "string"}},
    # Business mappings (10)
    {"name": "create_business_dimension", "category": "business_mappings", "description": "Create business dimension", "parameters": {"name": "string", "rules": "array?"}},
    {"name": "list_business_mappings", "category": "business_mappings", "description": "List business dimensions", "parameters": {}},
    {"name": "get_business_mapping", "category": "business_mappings", "description": "Get business dimension", "parameters": {"id": "string"}},
    {"name": "update_business_dimension", "category": "business_mappings", "description": "Update business dimension", "parameters": {"id": "string"}},
    {"name": "delete_business_dimension", "category": "business_mappings", "description": "Delete business dimension", "parameters": {"id": "string"}},
    {"name": "cldy_business_metrics_list", "category": "business_mappings", "description": "List business metrics", "parameters": {}},
    {"name": "cldy_business_metric_get", "category": "business_mappings", "description": "Get business metric", "parameters": {"index": "integer"}},
    {"name": "cldy_business_metric_create", "category": "business_mappings", "description": "Create business metric", "parameters": {"name": "string"}},
    {"name": "cldy_business_metric_update", "category": "business_mappings", "description": "Update business metric", "parameters": {"index": "integer"}},
    {"name": "cldy_business_metric_delete", "category": "business_mappings", "description": "Delete business metric", "parameters": {"index": "integer"}},
    # Cost reporting (7)
    {"name": "cldy_cost_report_run", "category": "cost_reporting", "description": "Run dynamic cost report", "parameters": {"start_date": "string", "end_date": "string", "dimensions": "string", "metrics": "string"}},
    {"name": "cldy_cost_report_enqueue", "category": "cost_reporting", "description": "Enqueue async cost report", "parameters": {"start_date": "string", "end_date": "string", "dimensions": "string", "metrics": "string"}},
    {"name": "cldy_cost_report_state", "category": "cost_reporting", "description": "Check enqueued report status", "parameters": {"report_id": "string"}},
    {"name": "cldy_cost_report_results", "category": "cost_reporting", "description": "Get enqueued report results", "parameters": {"report_id": "string"}},
    {"name": "cldy_cost_reports_list", "category": "cost_reporting", "description": "List saved cost reports", "parameters": {}},
    {"name": "cldy_cost_measures_list", "category": "cost_reporting", "description": "List cost dimensions and metrics", "parameters": {}},
    {"name": "cldy_cost_filters_list", "category": "cost_reporting", "description": "List cost filter operators", "parameters": {}},
    # Forecasts (2)
    {"name": "cldy_forecast_get", "category": "forecasts", "description": "Get spending forecast", "parameters": {"view_id": "string?"}},
    {"name": "cldy_estimate_get", "category": "forecasts", "description": "Get current period estimate", "parameters": {"view_id": "string?"}},
    # Views (7)
    {"name": "create_view", "category": "views", "description": "Create filtered view", "parameters": {"title": "string"}},
    {"name": "list_views", "category": "views", "description": "List views", "parameters": {}},
    {"name": "get_view", "category": "views", "description": "Get view by ID", "parameters": {"id": "string"}},
    {"name": "update_view", "category": "views", "description": "Update view", "parameters": {"id": "string"}},
    {"name": "delete_view", "category": "views", "description": "Delete view", "parameters": {"id": "string"}},
    {"name": "views_get_for_user", "category": "views", "description": "Get views for user", "parameters": {"user_id": "string", "org_id": "string"}},
    {"name": "views_get_for_multiple_users", "category": "views", "description": "Get views for multiple users", "parameters": {"user_ids": "array"}},
    # Users (3)
    {"name": "list_users", "category": "users", "description": "List organization users", "parameters": {}},
    {"name": "get_user", "category": "users", "description": "Get user by ID", "parameters": {"id": "string"}},
    {"name": "update_user", "category": "users", "description": "Update user views and roles", "parameters": {"id": "string"}},
    # Anomalies (7)
    {"name": "cldy_anomalies_list", "category": "anomalies", "description": "List cost anomalies", "parameters": {"startDate": "string", "endDate": "string", "viewId": "string"}},
    {"name": "cldy_anomaly_get", "category": "anomalies", "description": "Get single anomaly", "parameters": {"id": "string", "viewId": "string"}},
    {"name": "cldy_anomaly_subscriptions_list", "category": "anomalies", "description": "List anomaly subscriptions", "parameters": {"viewId": "string"}},
    {"name": "cldy_anomaly_subscription_get", "category": "anomalies", "description": "Get anomaly subscription", "parameters": {"subscription_id": "string"}},
    {"name": "cldy_anomaly_subscription_create", "category": "anomalies", "description": "Create anomaly subscription", "parameters": {"viewId": "string"}},
    {"name": "cldy_anomaly_subscription_update", "category": "anomalies", "description": "Update anomaly subscription", "parameters": {"subscription_id": "string", "viewId": "string"}},
    {"name": "cldy_anomaly_subscription_delete", "category": "anomalies", "description": "Delete anomaly subscription", "parameters": {"subscription_id": "string"}},
    # Containers (6)
    {"name": "cldy_containers_provision", "category": "containers", "description": "Provision K8s cluster", "parameters": {"cluster_name": "string"}},
    {"name": "cldy_containers_cluster_deployment", "category": "containers", "description": "Get cluster deployment YAML", "parameters": {"cluster_id": "string"}},
    {"name": "cldy_containers_clusters_list", "category": "containers", "description": "List provisioned clusters", "parameters": {}},
    {"name": "cldy_containers_usage", "category": "containers", "description": "Get container usage", "parameters": {"start_date": "string", "end_date": "string"}},
    {"name": "cldy_containers_labels", "category": "containers", "description": "Get container label keys", "parameters": {"start_date": "string", "end_date": "string"}},
    {"name": "cldy_containers_counts", "category": "containers", "description": "Count dimension values", "parameters": {"start_date": "string", "end_date": "string", "dimension": "string"}},
    # Rightsizing (2)
    {"name": "cldy_rightsizing_list", "category": "rightsizing", "description": "List rightsizing recommendations", "parameters": {}},
    {"name": "cldy_rightsizing_delete", "category": "rightsizing", "description": "Delete rightsizing recommendation", "parameters": {"orgId": "integer", "resourceId": "string"}},
    # Workload planning (18)
    {"name": "cldy_workload_create", "category": "workload_planning", "description": "Create workload", "parameters": {"name": "string", "status": "string", "csp": "array"}},
    {"name": "cldy_workloads_list", "category": "workload_planning", "description": "List workloads", "parameters": {}},
    {"name": "cldy_workload_get_resources", "category": "workload_planning", "description": "Get workload resources", "parameters": {"workload_id": "string"}},
    {"name": "cldy_workload_download_template", "category": "workload_planning", "description": "Download workload template", "parameters": {"download_type": "string", "format": "string", "workload_id": "string"}},
    {"name": "cldy_workload_upload_resources", "category": "workload_planning", "description": "Upload workload resources", "parameters": {"upload_type": "string", "workload_id": "string", "file_content": "string"}},
    {"name": "cldy_workload_upload_errors", "category": "workload_planning", "description": "Get upload errors", "parameters": {"workload_id": "string"}},
    {"name": "cldy_workload_generate_recommendations", "category": "workload_planning", "description": "Generate recommendations", "parameters": {"workload_id": "string"}},
    {"name": "cldy_workload_job_status", "category": "workload_planning", "description": "Check job status", "parameters": {"workload_id": "string"}},
    {"name": "cldy_workload_get_recommendations", "category": "workload_planning", "description": "Get recommendations", "parameters": {"workload_id": "string", "vendor": "string"}},
    {"name": "cldy_workload_save_recommendations", "category": "workload_planning", "description": "Save recommendations", "parameters": {"workload_id": "string", "selections": "array"}},
    {"name": "cldy_workload_summary", "category": "workload_planning", "description": "Workload cost summary", "parameters": {"workload_id": "string", "vendor": "string"}},
    {"name": "cldy_workload_analysis", "category": "workload_planning", "description": "Workload analysis", "parameters": {"workload_id": "string", "vendor": "string"}},
    {"name": "cldy_workload_export", "category": "workload_planning", "description": "Export workload Excel", "parameters": {"workload_id": "string"}},
    {"name": "cldy_workload_duplicate", "category": "workload_planning", "description": "Duplicate workload", "parameters": {"workload_id": "string", "new_name": "string"}},
    {"name": "cldy_workload_delete", "category": "workload_planning", "description": "Delete workload", "parameters": {"workload_id": "string"}},
    {"name": "cldy_workload_preferences_get", "category": "workload_planning", "description": "Get workload preferences", "parameters": {}},
    {"name": "cldy_workload_preferences_update", "category": "workload_planning", "description": "Update workload preferences", "parameters": {"preferences": "array"}},
    {"name": "cldy_workload_static_data", "category": "workload_planning", "description": "Get static workload data", "parameters": {}},
]

DetailLevel = Literal["name", "summary", "full"]


def search_catalog(
    query: str = "",
    category: str | None = None,
    detail: DetailLevel = "summary",
) -> dict[str, Any]:
    q = query.lower().strip()
    results = []
    for tool in TOOL_CATALOG:
        if category and tool["category"] != category:
            continue
        hay = f"{tool['name']} {tool['category']} {tool['description']}".lower()
        if q and q not in hay:
            continue
        if detail == "name":
            results.append({"name": tool["name"]})
        elif detail == "summary":
            results.append(
                {
                    "name": tool["name"],
                    "category": tool["category"],
                    "description": tool["description"],
                }
            )
        else:
            results.append(dict(tool))
    return {"result": results, "meta": {"count": len(results), "total_tools": len(TOOL_CATALOG)}}
