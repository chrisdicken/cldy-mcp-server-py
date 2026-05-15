"""Cloudability MCP Server — local STDIO transport."""

from cldy_mcp.server import create_server_from_env

mcp = create_server_from_env()

if __name__ == "__main__":
    mcp.run()
