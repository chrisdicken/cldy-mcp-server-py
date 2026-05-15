"""Tests for query param building."""

from cldy_mcp.utils.http_client import build_query_params


def test_build_query_params_repeat_filters() -> None:
    pairs = build_query_params(
        {"filters": ["vendor==AWS", "region==us-east-1"], "limit": 10},
        array_format="repeat",
    )
    assert isinstance(pairs, list)
    keys = [p[0] for p in pairs]
    assert keys.count("filters") == 2
    assert ("limit", "10") in pairs


def test_build_query_params_comma() -> None:
    params = build_query_params({"sort": "cost", "offset": 0})
    assert params == {"sort": "cost", "offset": 0}
