from mcp.server import MCPServer

from mcp_server.tools.market import get_market_summary, get_top_gainers, get_top_losers
from mcp_server.tools.portfolio import calculate_portfolio_value
from mcp_server.tools.stocks import compare_stocks, get_dividends, get_stock_history, get_stock_info, get_stock_price

mcp = MCPServer("MOEX MCP Server")

mcp.add_tool(get_stock_price)
mcp.add_tool(get_stock_history)
mcp.add_tool(get_stock_info)
mcp.add_tool(get_market_summary)
mcp.add_tool(get_top_gainers)
mcp.add_tool(get_top_losers)
mcp.add_tool(get_dividends)
mcp.add_tool(compare_stocks)
mcp.add_tool(calculate_portfolio_value)


if __name__ == "__main__":
    mcp.run(transport="stdio")
