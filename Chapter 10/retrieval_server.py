from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RetrievalServer")

_DOCS = [
    {"doc_id": "policy_2025_refunds", "title": "Refund Policy", "tenant_id": "acme",
     "text": "Refunds are allowed within 30 days of purchase for annual plans."},
    {"doc_id": "billing_faq", "title": "Billing FAQ", "tenant_id": "acme",
     "text": "Billing questions are answered by the support team within one business day."},
    {"doc_id": "globex_refunds", "title": "Globex Refund Policy", "tenant_id": "globex",
     "text": "Globex refunds follow a 15 day window."},
]


@mcp.tool()
def search_docs(query: str, tenant_id: str, top_k: int = 5) -> dict:
    """Search approved documents with filters."""
    results = retriever_search(query=query, filters={"tenant_id": tenant_id}, top_k=top_k)
    return {
        "results": [
            {"doc_id": r["doc_id"], "title": r["title"], "score": r["score"], "uri": f"resource://kb/{r['doc_id']}"}
            for r in results
        ]
    }


def retriever_search(query: str, filters: dict, top_k: int) -> list[dict]:
    """Stand-in for a real retriever -- simple prefix overlap so 'refund' still credits 'refunds'."""
    q_words = query.lower().split()
    scored = []
    for doc in _DOCS:
        if doc["tenant_id"] != filters["tenant_id"]:
            continue
        text_words = doc["text"].lower().split()
        overlap = sum(1 for qw in q_words if any(tw.startswith(qw) or qw.startswith(tw) for tw in text_words))
        scored.append({**doc, "score": overlap})
    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[:top_k]


@mcp.resource("resource://kb/{doc_id}")
def get_document(doc_id: str) -> dict:
    """Read the approved text and metadata for one document."""
    for doc in _DOCS:
        if doc["doc_id"] == doc_id:
            return doc
    return {"doc_id": doc_id, "error": "not found"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
