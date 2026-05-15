"""Tests for tool registry and search."""

from cldy_mcp.registry import TOOL_CATALOG, search_catalog


def test_catalog_has_77_tools() -> None:
    assert len(TOOL_CATALOG) == 77


def test_search_by_category() -> None:
    result = search_catalog(category="cost_reporting", detail="name")
    assert result["meta"]["count"] == 7
    assert all(t["name"].startswith("cldy_cost") for t in result["result"])


def test_search_query() -> None:
    result = search_catalog(query="budget", detail="summary")
    assert result["meta"]["count"] >= 5
