from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WorkflowServer")

_vendor_counter = 1000


@mcp.tool()
def create_vendor(name: str) -> dict:
    """Create a vendor record and return its details."""
    global _vendor_counter
    if not name.strip():
        raise ValueError("vendor name is required")
    _vendor_counter += 1
    return {"ok": True, "vendor_id": f"V-{_vendor_counter}", "name": name, "status": "created"}


@mcp.tool()
def send_message(team: str, template: str) -> dict:
    """Send a workflow notification message to an internal team."""
    if not team.strip() or not template.strip():
        raise ValueError("team and template are required")
    return {"ok": True, "team": team, "template": template, "delivery_status": "sent"}


@mcp.tool()
def update_tracker(stage: str) -> dict:
    """Create or update the onboarding tracker stage."""
    if not stage.strip():
        raise ValueError("stage is required")
    return {"ok": True, "stage": stage, "tracker_status": "updated"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
