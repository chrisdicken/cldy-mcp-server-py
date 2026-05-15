"""Tests for response shaping."""

from cldy_mcp.utils.response import parse_envelope, shape_cost_report


def test_parse_envelope_with_meta() -> None:
    data = {"result": [{"a": 1}], "meta": {"pagination": {"next": "tok"}}}
    env = parse_envelope(data)
    assert env["result"] == [{"a": 1}]
    assert env["meta"]["pagination"]["next"] == "tok"


def test_parse_envelope_bare() -> None:
    env = parse_envelope({"foo": "bar"})
    assert env["result"] == {"foo": "bar"}


def test_shape_cost_report_summary() -> None:
    rows = [{"cost": i} for i in range(50)]
    env = {"result": {"results": rows}, "meta": {"total": 50}}
    shaped = shape_cost_report(env, "summary", sample_rows=5)
    assert shaped["result"]["summary"] is True
    assert shaped["result"]["total_rows"] == 50
    assert len(shaped["result"]["results"]) == 5
    assert shaped["meta"]["total"] == 50
