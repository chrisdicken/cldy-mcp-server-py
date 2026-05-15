"""Response shaping — preserve envelopes and agent-safe cost report summaries."""

from typing import Any, Literal

ResponseShape = Literal["full", "summary"]


def parse_envelope(data: Any) -> dict[str, Any]:
    """Normalize API response to {result, meta?} envelope."""
    if isinstance(data, dict) and "result" in data:
        envelope: dict[str, Any] = {"result": data["result"]}
        if "meta" in data and data["meta"] is not None:
            envelope["meta"] = data["meta"]
        return envelope
    return {"result": data}


def shape_cost_report(
    envelope: dict[str, Any],
    response_shape: ResponseShape = "full",
    sample_rows: int = 20,
) -> dict[str, Any]:
    """Optionally truncate large cost report result rows for agents."""
    if response_shape == "full":
        return envelope

    result = envelope.get("result")
    meta = envelope.get("meta", {})

    rows: list[Any] = []
    if isinstance(result, dict):
        rows = result.get("results") or result.get("rows") or []
    elif isinstance(result, list):
        rows = result

    if not isinstance(rows, list):
        return envelope

    truncated = rows[:sample_rows]
    summary_result: dict[str, Any] = {
        "summary": True,
        "total_rows": len(rows),
        "sample_rows": len(truncated),
        "columns": list(truncated[0].keys()) if truncated and isinstance(truncated[0], dict) else [],
        "results": truncated,
    }
    if isinstance(result, dict):
        for key, val in result.items():
            if key not in ("results", "rows"):
                summary_result[key] = val

    return {"result": summary_result, "meta": meta}
