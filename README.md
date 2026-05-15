# Cloudability MCP Server (Python)

A Python MCP server for the IBM Cloudability API V3 with **77 tools** across 12 domains. Works with Bob, Cursor, Claude Desktop, VS Code, and any MCP-compatible interface.

![Demo](CLDY-MCP.gif)

> **Migrating from the TypeScript server?** Tool names are identical — just swap the command. See [Migration](#migration-from-typescript-server).

---

## Prerequisites

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — fast Python package manager

Install `uv` if you don't have it:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Installation

```bash
cd cldy-mcp-server-py
uv sync
```

That's it. `uv sync` creates a virtual environment and installs all dependencies automatically — no `pip install`, no `venv` commands needed.

---

## Authentication

You need one of the following:

| Method | When to use |
|--------|-------------|
| **API Key** (recommended) | Most users |
| **OpenToken** (Frontdoor) | Enterprise SSO |

### Get your API key

Log in to Cloudability → Account Settings → API Access → copy your key.

---

## Client Setup

Pick the interface you're using:

### Bob

In Bob's MCP server config (`.mcp.json` or Bob settings):

```json
{
  "mcpServers": {
    "cloudability": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/cldy-mcp-server-py",
        "run",
        "mcp_server_local.py"
      ],
      "env": {
        "CLOUDABILITY_API_KEY": "your-api-key"
      }
    }
  }
}
```

Replace `/absolute/path/to/cldy-mcp-server-py` with the actual path on your machine (e.g. `/Users/yourname/Documents/Bob The Builder/cldy-mcp-server-py`).

---

### Cursor

In Cursor → Settings → MCP (or `.cursor/mcp.json` in your project):

```json
{
  "mcpServers": {
    "cloudability": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/cldy-mcp-server-py",
        "run",
        "mcp_server_local.py"
      ],
      "env": {
        "CLOUDABILITY_API_KEY": "your-api-key"
      }
    }
  }
}
```

---

### Claude Desktop

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "cloudability": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/cldy-mcp-server-py",
        "run",
        "mcp_server_local.py"
      ],
      "env": {
        "CLOUDABILITY_API_KEY": "your-api-key"
      }
    }
  }
}
```

Restart Claude Desktop after saving.

---

### VS Code (Copilot / GitHub Copilot Chat)

Add to `.vscode/mcp.json` in your workspace or user settings:

```json
{
  "servers": {
    "cloudability": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/cldy-mcp-server-py",
        "run",
        "mcp_server_local.py"
      ],
      "env": {
        "CLOUDABILITY_API_KEY": "your-api-key"
      }
    }
  }
}
```

---

### OpenToken (Frontdoor) Authentication

If your organization uses Frontdoor SSO instead of API keys, replace the `env` block in any config above:

```json
"env": {
  "CLOUDABILITY_OPENTOKEN": "your-opentoken",
  "CLOUDABILITY_ENVIRONMENT_ID": "your-environment-id",
  "CLOUDABILITY_REGION": "us"
}
```

---

### Run manually (terminal)

```bash
export CLOUDABILITY_API_KEY="your-api-key"
uv run mcp_server_local.py
```

---

## HTTP/SSE Streaming Mode

For integrations that connect over HTTP rather than launching a subprocess:

```bash
export CLOUDABILITY_API_KEY="your-api-key"
export CLDY_MODE=streaming
uv run mcp_server_streaming.py
# Server listens on http://localhost:9000
```

Pass credentials per request instead of via env:

```bash
curl -X POST http://localhost:9000/mcp \
  -H "Authorization: Basic $(echo -n 'YOUR_API_KEY:' | base64)" \
  -H "Content-Type: application/json"
```

---

## Configuration Reference

| Variable | Aliases | Description | Default |
|----------|---------|-------------|---------|
| `CLOUDABILITY_API_KEY` | `CLDY_API_KEY` | API key (Basic auth) | — |
| `CLOUDABILITY_OPENTOKEN` | `CLDY_ACCESS_TOKEN` | Frontdoor access token | — |
| `CLOUDABILITY_ENVIRONMENT_ID` | `CLDY_ENVIRONMENT_ID` | Frontdoor environment ID | — |
| `CLOUDABILITY_REGION` | `CLDY_REGION` | `us`, `eu`, `au`, `me` | `us` |
| `CLOUDABILITY_BASE_URL` | `CLDY_API_URL` | Override API base URL | — |
| `CLDY_RESPONSE_FORMAT` | — | `toon` or `json` | `json` |
| `CLDY_MODE` | — | `local` or `streaming` | `local` |
| `CLDY_PORT` | — | Streaming server port | `9000` |

Both the `CLOUDABILITY_*` and `CLDY_*` prefixes work — use whichever matches your existing setup.

---

## Available Tools (77)

Use `search_tools` to find tools without loading all schemas at once:

```
search_tools(query="cost report", detail="summary")
```

| Category | Tools |
|----------|------:|
| Account Groups | 5 |
| Budgets | 5 |
| Budget Subscriptions | 5 |
| Business Mappings | 10 |
| Cost Reporting | 7 |
| Forecasts | 2 |
| Views | 7 |
| Users | 3 |
| Anomalies | 7 |
| Containers | 6 |
| Rightsizing | 2 |
| Workload Planning | 18 |
| **Total** | **77** |

---

## Testing

```bash
uv sync --all-extras   # installs dev dependencies
uv run pytest
```

---

## Migration from TypeScript Server

Tool names are identical between this server and `cldy-mcp-server-master`. To migrate:

1. Replace the MCP command from `node dist/index.js` → `uv run mcp_server_local.py`
2. `CLOUDABILITY_API_KEY` works unchanged — no env var changes needed

What this server adds over the TypeScript version:
- Returns full `{result, meta}` envelope including pagination tokens
- `search_tools` for progressive tool discovery
- `response_shape=summary` on cost reports (returns row count + sample rows — safe for agents)
- Proper multipart upload for workload resources
