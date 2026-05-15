"""Tests for business mapping transforms."""

from cldy_mcp.transforms.business_mappings import dimension_body_from_params, rules_to_statements


def test_rules_to_statements() -> None:
    rules = [{"condition": "DIMENSION['vendor'] == 'Amazon'", "value": "AWS"}]
    stmts = rules_to_statements(rules)
    assert stmts[0]["matchExpression"] == "DIMENSION['vendor'] == 'Amazon'"
    assert stmts[0]["valueExpression"] == "'AWS'"


def test_dimension_body() -> None:
    body = dimension_body_from_params({"name": "BU", "rules": [{"condition": "true", "value": "Other"}]})
    assert body["name"] == "BU"
    assert "statements" in body
