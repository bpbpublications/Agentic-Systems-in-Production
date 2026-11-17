from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ProductionRAGServer")

_DOCS = [
    {"doc_id": "policy-1", "text": "Refunds are allowed within 30 days of purchase for annual plans. Enterprise plans follow a separate 45 day window.", "tenant_id": "acme", "source": "kb", "access": "support"},
    {"doc_id": "policy-2", "text": "Billing questions are answered by the support team within one business day. Escalate urgent billing issues to a manager.", "tenant_id": "acme", "source": "kb", "access": "support"},
]


@mcp.tool()
def search_docs(query: str, tenant: str) -> dict:
    """Search approved documents for a tenant."""
    q_words = query.lower().split()
    scored = []
    for doc in _DOCS:
        if doc["tenant_id"] != tenant:
            continue
        text_words = doc["text"].lower().split()
        overlap = sum(1 for qw in q_words if any(tw.startswith(qw) or qw.startswith(tw) for tw in text_words))
        if overlap > 0:
            scored.append({"doc_id": doc["doc_id"], "score": overlap, "text": doc["text"]})
    scored.sort(key=lambda r: r["score"], reverse=True)
    return {"results": scored[:5]}


if __name__ == "__main__":
    mcp.run(transport="stdio")
