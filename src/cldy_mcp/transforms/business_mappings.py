"""Transform simplified business dimension rules to API statements format."""

from typing import Any


def rules_to_statements(rules: list[dict[str, str]]) -> list[dict[str, str]]:
    """Map {condition, value} rules to {matchExpression, valueExpression}."""
    statements: list[dict[str, str]] = []
    for rule in rules:
        condition = rule.get("condition", "")
        value = rule.get("value", "")
        value_expr = value if value.startswith("'") or value.startswith("TAG") or value.startswith("DIMENSION") or value.startswith("METRIC") else f"'{value}'"
        statements.append(
            {"matchExpression": condition, "valueExpression": value_expr}
        )
    return statements


def dimension_body_from_params(params: dict[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if "name" in params:
        body["name"] = params["name"]
    if "default_value" in params:
        body["defaultValue"] = params["default_value"]
    if "default_value_expression" in params:
        body["defaultValueExpression"] = params["default_value_expression"]
    if "rules" in params and params["rules"]:
        body["statements"] = rules_to_statements(params["rules"])
    elif "statements" in params:
        body["statements"] = params["statements"]
    if "state" in params:
        body["state"] = params["state"]
    return body
