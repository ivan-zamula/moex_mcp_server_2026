from mcp_server.tools.moex import get_market_rows


def calculate_portfolio_value(portfolio: list[dict]) -> dict:
    """Рассчитывает текущую стоимость портфеля по тикерам и количеству."""
    prices = {row["ticker"]: row["price"] for row in get_market_rows()}
    positions = []
    total = 0.0
    for position in portfolio:
        ticker = position["ticker"].upper()
        quantity = float(position["quantity"])
        price = prices.get(ticker)
        value = price * quantity if price is not None else None
        if value is not None:
            total += value
        positions.append({"ticker": ticker, "quantity": quantity, "price": price, "value": value})
    return {"positions": positions, "total_value": total}
