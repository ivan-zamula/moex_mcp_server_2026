"""Тесты регистрации инструментов в MCP-сервере."""

from mcp_server.mcp_app import mcp


def test_mcp_server_has_stock_price_tool() -> None:
    registered_tools = getattr(mcp._tool_manager, "_tools", {})

    assert "get_stock_price" in registered_tools
    assert "get_stock_history" in registered_tools
    assert "get_stock_info" in registered_tools
    assert "get_market_summary" in registered_tools
    assert "get_top_gainers" in registered_tools
    assert "get_top_losers" in registered_tools
    assert "get_dividends" in registered_tools
    assert "compare_stocks" in registered_tools
    assert "calculate_portfolio_value" in registered_tools
