"""Cloudability MCP Server — HTTP/SSE streaming transport on port 9000."""

import os

from cldy_mcp.server import create_server_from_env

os.environ.setdefault("CLDY_MODE", "streaming")

mcp = create_server_from_env()

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.getenv("CLDY_PORT", "9000")))
