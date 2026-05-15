"""Integration tests for cost reporting with mocked HTTP."""

import pytest
import respx
import httpx

from cldy_mcp.api_groups.cost_reporting import CostReportingGroup
from cldy_mcp.utils.http_client import CloudabilityHTTPClient


@pytest.mark.asyncio
@respx.mock
async def test_cost_report_run_preserves_meta() -> None:
    client = CloudabilityHTTPClient(api_key="test-key-12345678", response_format="json")
    group = CostReportingGroup(client)

    respx.get("https://api.cloudability.com/v3/reporting/cost/run").mock(
        return_value=httpx.Response(
            200,
            json={
                "result": {"results": [{"vendor": "AWS", "unblended_cost": 100}]},
                "meta": {"pagination": {"next": "abc"}},
            },
        )
    )

    out = await group._get(
        "/reporting/cost/run",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "dimensions": "vendor",
            "metrics": "unblended_cost",
        },
        array_format="repeat",
    )
    assert "result" in out
    assert out["meta"]["pagination"]["next"] == "abc"
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_cost_report_summary_shape() -> None:
    client = CloudabilityHTTPClient(api_key="test-key-12345678", response_format="json")
    group = CostReportingGroup(client)
    rows = [{"cost": i} for i in range(30)]

    respx.get("https://api.cloudability.com/v3/reporting/cost/run").mock(
        return_value=httpx.Response(
            200,
            json={"result": {"results": rows}, "meta": {"total_results": 30}},
        )
    )

    out = await group._get(
        "/reporting/cost/run",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "dimensions": "vendor",
            "metrics": "unblended_cost",
        },
        response_shape="summary",
        sample_rows=5,
    )
    assert out["result"]["summary"] is True
    assert out["result"]["total_rows"] == 30
    assert len(out["result"]["results"]) == 5
    await client.close()
