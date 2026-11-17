from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AnalysisServer")

_SCHEMAS = {
    "sales.weekly_revenue": {
        "dataset": "sales.weekly_revenue",
        "columns": ["week_start", "region", "channel", "revenue", "orders", "returns", "sessions"],
    }
}
_METRIC_DEFS = {
    "revenue": {"metric": "revenue", "definition": "Sum of recognized revenue for a week after cancellations."}
}


@mcp.resource("schema://{dataset_ref}")
def schema_resource(dataset_ref: str) -> dict:
    """Expose dataset schema as an MCP resource."""
    return _SCHEMAS.get(dataset_ref, {"dataset": dataset_ref, "columns": []})


@mcp.resource("metrics://{metric_name}")
def metrics_resource(metric_name: str) -> dict:
    """Expose a governed metric definition as an MCP resource."""
    return _METRIC_DEFS.get(metric_name, {"metric": metric_name, "definition": "unknown"})


@mcp.tool()
def profile_dataset(dataset_ref: str) -> dict:
    """Profile a dataset: row count, missing rate, and dimension values."""
    return {
        "dataset_ref": dataset_ref,
        "row_count": 448,
        "missing_rate": 0.01,
        "regions": ["Northeast", "South", "West", "Midwest"],
        "channels": ["online", "retail", "partner"],
    }


@mcp.tool()
def run_analysis(question: str) -> dict:
    """Run a natural-language analytical query over the dataset."""
    q = question.lower()
    if "compare weekly revenue" in q:
        return {
            "window_weeks": 8,
            "region_change_pct": {"Northeast": -18.4, "South": 4.2, "West": 2.1, "Midwest": 1.3},
            "top_driver": {"region": "Northeast", "channel": "online", "change_pct": -24.6},
        }
    if "returns, discounting, or traffic" in q:
        return {
            "region": "Northeast",
            "channel": "online",
            "returns_change_pct": 3.1,
            "discount_rate_change_pct": 1.2,
            "sessions_change_pct": -19.7,
            "conclusion": "Traffic decline is the strongest explanation for the revenue drop.",
        }
    return {"note": "No matching analysis for this question."}


if __name__ == "__main__":
    mcp.run(transport="stdio")
