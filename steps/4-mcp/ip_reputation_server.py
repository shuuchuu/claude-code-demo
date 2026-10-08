# /// script
# dependencies = ["mcp>=2,<3"]
# ///
"""Demo MCP server: an IP address's reputation, from a made-up threat intelligence base."""

from mcp.server.mcpserver import MCPServer

REPUTATION = {
    "203.0.113.45": "Known scanner: port scans reported by 37 organizations this month.",
    "198.51.100.77": "SSH brute-force attacks, reported for the last 3 days.",
    "198.51.100.66": "Command-and-control server of a ransomware strain, active.",
}

mcp = MCPServer("ip-reputation")


@mcp.tool()
def ip_reputation(ip: str) -> str:
    """Gives the reputation of a public IP address (threat intelligence base)."""
    return REPUTATION.get(ip, "No known report for this address.")


if __name__ == "__main__":
    mcp.run()
