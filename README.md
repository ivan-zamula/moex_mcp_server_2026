# MOEX MCP Server (2026)

[English](README.md) | [Русский](README.ru.md)

A Python server that provides an AI agent with an HTTP tool for retrieving Moscow Exchange stock quotations.

## Features

- FastAPI server with health and tools endpoints.
- Stock quotation tool backed by the Moscow Exchange ISS API.
- Console AI-agent client written in Python.
- External model access through OpenRouter and the OpenAI-compatible API.
- Tool-call loop that returns the server result to the model for the final answer.

This is an MCP-like HTTP implementation, not a complete implementation of the MCP standard. Production security and deployment are outside the current scope.

## Architecture

```text
User -> agent.py -> OpenRouter model
             |             |
             +-> tools ----+
                  |
                  v
            FastAPI server -> MOEX ISS API
```

The client discovers tools through `GET /tools`. When the model requests `get_stock_price`, the client calls the local server and sends the JSON result back to the model.

## Stack and structure

Python 3.11+, FastAPI, Uvicorn, Requests, OpenAI Python SDK, OpenRouter and `python-dotenv`.

| Path | Purpose |
| --- | --- |
| [`src/mcp_server/server.py`](src/mcp_server/server.py) | FastAPI application and HTTP endpoints |
| [`src/mcp_server/tools.py`](src/mcp_server/tools.py) | Tool schemas exposed to the client |
| [`src/clients/agent.py`](src/clients/agent.py) | OpenRouter client and tool-call loop |
| [`src/clients/agent_openai.py`](src/clients/agent_openai.py) | Agents SDK client with the same OpenRouter configuration |
| [`tests/`](tests/) | Local test files |
| [`docs/`](docs/) | Architecture and runbook notes |

## Setup

Python 3.11 or newer is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp .env.example .env
```

Create an API key at [OpenRouter](https://openrouter.ai/) and set the local `.env` values:

```env
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openrouter/free
MCP_SERVER_URL=http://127.0.0.1:8080
```

Keep the real `.env` file local. It is excluded from Git.

## Run

Start the server in the first terminal:

```bash
cd src/mcp_server
uvicorn server:app --reload --port 8080
```

Open the API documentation at <http://127.0.0.1:8080/docs>.

Start the client from the project root in a second terminal:

```bash
PYTHONPATH=src python -m clients.agent
```

The Agents SDK variant can be started with:

```bash
PYTHONPATH=src python -m clients.agent_openai
```

Then enter a question such as:

```text
How much does Sberbank stock cost today?
```

## Checks

Compile the Python sources without making external API requests:

```bash
python -m compileall -q src tests
```

The OpenRouter call and the live MOEX request require configured credentials and a running network service.

## Idea

Materials from [RedMadRobot's custom MCP article project](https://github.com/RedMadRobot/custom-mcp-article)
were used while preparing this project.
