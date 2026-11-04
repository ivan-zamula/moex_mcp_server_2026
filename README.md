# MOEX MCP Server (2026)

[English](README.md) | [Русский](README.ru.md)

A Python MCP server that provides an AI host with a tool for retrieving Moscow Exchange stock quotations.
## Features

- Standard MCP server built with the official Python SDK.
- Tools for current quotations, historical prices and security information backed by the Moscow Exchange ISS API.
- Minimal MCP client for protocol checks.

The current transport is `stdio`. Production security and deployment are outside the current scope.

## Architecture

```text
MCP host/client -> stdio -> MCP server -> MOEX tools -> MOEX ISS API
```

The MCP client discovers tools through the standard MCP session and calls
`get_stock_price`, `get_stock_history` and `get_stock_info` through the `stdio` transport.

## Tools

### `get_stock_price`

Returns the current stock price on the Moscow Exchange.

Parameter:

```text
ticker: SBER
```

Example result:

```json
{
  "ticker": "SBER",
  "price": 291.41,
  "currency": "RUB"
}
```

### `get_stock_history`

Returns historical stock prices for a specified period. Parameters are `ticker`,
`from_date` and `to_date` in `YYYY-MM-DD` format. The result contains the trading
date, opening, high, low and closing prices, as well as trading volume.

### `get_stock_info`

Returns the ticker, name, trading board, board name and instrument status. It
accepts the `ticker` parameter.

### Market tools

- `get_market_summary(limit)` — market summary with the number of instruments and top gainers and losers.
- `get_top_gainers(limit)` — stocks with the largest increase during the current session.
- `get_top_losers(limit)` — stocks with the largest decrease during the current session.

The `limit` parameter controls the number of returned results.

### Additional tools

- `get_dividends(ticker)` — dividend events for a security.
- `compare_stocks(tickers)` — compares current prices and changes for several stocks.
- `calculate_portfolio_value(portfolio)` — calculates portfolio value. Each position contains `ticker` and `quantity`.

## Stack and structure

Python 3.11+, the official MCP Python SDK and Requests.

| Path | Purpose |
| --- | --- |
| [`src/mcp_server/mcp_app.py`](src/mcp_server/mcp_app.py) | MCP server and tool registration |
| [`src/mcp_server/tools/market.py`](src/mcp_server/tools/market.py) | Market tools |
| [`src/mcp_server/tools/stocks.py`](src/mcp_server/tools/stocks.py) | Stock tools |
| [`src/mcp_server/tools/portfolio.py`](src/mcp_server/tools/portfolio.py) | Portfolio tools |
| [`src/mcp_server/tools/moex.py`](src/mcp_server/tools/moex.py) | Shared ISS API helpers |
| [`src/clients/mcp_client.py`](src/clients/mcp_client.py) | MCP client for protocol checks |
| [`tests/`](tests/) | Local test files |
| [`docs/`](docs/) | Architecture and runbook notes |
| [`scripts/`](scripts/) | Server and test commands |

## Setup

Python 3.11 or newer is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Run

Start the MCP client from the project root:

```bash
PYTHONPATH=src python -m clients.mcp_client
```

The client starts the MCP server over `stdio`, discovers its tools and calls
`get_stock_price`.

Then enter a question such as:

```text
How much does Sberbank stock cost today?
```

## Checks

Compile the Python sources without making external API requests:

```bash
python -m compileall -q src tests
```

The live MOEX request requires network access.

## Idea

The project idea and initial implementation approach are based on
[RedMadRobot's custom MCP article project](https://github.com/RedMadRobot/custom-mcp-article).
