from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ResearchServer")


@mcp.tool()
def search_documents(query: str) -> dict:
    """Search policy and industry documents for a research question."""
    q = query.lower()
    if "policy" in q or "trade" in q:
        hits = ["Battery Import Policy Outlook 2025: trade controls may raise import costs.",
                "Critical Minerals Policy Brief: export restrictions affect some regions."]
    else:
        hits = ["EV Supply Chain Notes: recent policy and sourcing changes affect planning."]
    return {"query": query, "hits": hits, "source_type": "documents"}


@mcp.tool()
def query_supplier_database(query: str) -> dict:
    """Return supplier concentration metrics for EV makers."""
    rows = [
        {"company": "EV Maker A", "top_supplier_share": 0.58, "risk": "high"},
        {"company": "EV Maker B", "top_supplier_share": 0.41, "risk": "medium"},
        {"company": "EV Maker C", "top_supplier_share": 0.29, "risk": "lower"},
    ]
    return {"query": query, "rows": rows, "source_type": "database"}


@mcp.tool()
def search_market_web(query: str) -> dict:
    """Search recent market updates relevant to a research question."""
    results = [
        "Battery raw material prices remain volatile due to shipping delays.",
        "EV makers diversify sourcing with second-source supplier contracts.",
    ]
    return {"query": query, "results": results, "source_type": "search"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
