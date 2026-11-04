from mcp_server.tools.moex import get_market_rows


def get_market_summary(limit: int = 5) -> dict:
    """Возвращает сводку по лидерам роста и падения рынка акций."""
    rows = get_market_rows()
    return {"instruments": len(rows), "top_gainers": sorted(rows, key=lambda item: item["change_percent"], reverse=True)[:limit], "top_losers": sorted(rows, key=lambda item: item["change_percent"])[:limit]}


def get_top_gainers(limit: int = 10) -> list[dict]:
    """Возвращает акции с наибольшим ростом за текущую сессию."""
    return sorted(get_market_rows(), key=lambda item: item["change_percent"], reverse=True)[:limit]


def get_top_losers(limit: int = 10) -> list[dict]:
    """Возвращает акции с наибольшим падением за текущую сессию."""
    return sorted(get_market_rows(), key=lambda item: item["change_percent"])[:limit]
