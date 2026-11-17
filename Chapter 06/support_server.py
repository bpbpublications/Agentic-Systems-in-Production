from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SupportServer")

_ACCOUNTS = {
    "CUST-1001": {"customer_id": "CUST-1001", "name": "Asha Mehta", "plan": "pro", "billing_status": "current"},
    "CUST-1002": {"customer_id": "CUST-1002", "name": "Rohan Iyer", "plan": "starter", "billing_status": "past_due"},
}

_TICKETS = {
    "CUST-1001": [
        {"ticket_id": "T-501", "status": "open", "category": "technical"},
        {"ticket_id": "T-477", "status": "resolved", "category": "billing"},
    ],
    "CUST-1002": [
        {"ticket_id": "T-610", "status": "open", "category": "billing"},
    ],
}


@mcp.tool()
def get_customer_account(customer_id: str) -> dict:
    """Return the account profile for a customer."""
    return _ACCOUNTS.get(customer_id, {"customer_id": customer_id, "plan": "unknown", "billing_status": "unknown"})


@mcp.tool()
def get_recent_tickets(customer_id: str) -> list[dict]:
    """Return recent support tickets for a customer."""
    return _TICKETS.get(customer_id, [])


if __name__ == "__main__":
    mcp.run(transport="stdio")
