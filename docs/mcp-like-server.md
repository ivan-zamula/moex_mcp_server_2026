# MCP-like HTTP implementation

This branch preserves the first HTTP-based implementation from the project.

## Components

- `src/mcp_server/server.py` — FastAPI server.
- `src/mcp_server/tools.py` — JSON description of the stock-price tool.
- `src/clients/agent.py` — manual tool-calling client.
- `src/clients/agent_openai.py` — Agents SDK client connected to the HTTP contract.

The implementation is intentionally kept as a comparison point. It exposes
ordinary HTTP endpoints and does not implement the standard MCP protocol.
