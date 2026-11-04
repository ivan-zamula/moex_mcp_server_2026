from datetime import date

from mcp_server.tools.moex import MOEX_BASE_URL, get_market_rows, get_xml, to_float


def get_stock_price(ticker: str) -> dict:
    """Получает текущую цену акции на Московской бирже по тикеру."""
    root = get_xml(
        f"{MOEX_BASE_URL}/engines/stock/markets/shares/boards/TQBR/securities.xml",
        **{"iss.meta": "off", "iss.only": "marketdata", "marketdata.columns": "SECID,LAST"},
    )
    ticker = ticker.upper()
    for row in root.findall(".//row"):
        if row.get("SECID") == ticker:
            return {"ticker": ticker, "price": to_float(row.get("LAST")), "currency": "RUB"}
    return {"error": f"Акция с тикером {ticker} не найдена"}


def get_stock_history(ticker: str, from_date: str, to_date: str) -> dict:
    """Получает исторические цены акции за указанный период."""
    if date.fromisoformat(from_date) > date.fromisoformat(to_date):
        raise ValueError("from_date не может быть позже to_date")
    ticker = ticker.upper()
    root = get_xml(
        f"{MOEX_BASE_URL}/history/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.xml",
        **{"iss.meta": "off", "history.columns": "TRADEDATE,OPEN,HIGH,LOW,CLOSE,VOLUME", "from": from_date, "till": to_date},
    )
    return {
        "ticker": ticker,
        "history": [
            {"date": row.get("TRADEDATE"), "open": to_float(row.get("OPEN")), "high": to_float(row.get("HIGH")), "low": to_float(row.get("LOW")), "close": to_float(row.get("CLOSE")), "volume": to_float(row.get("VOLUME"))}
            for row in root.findall(".//row")
        ],
    }


def get_stock_info(ticker: str) -> dict:
    """Получает основную информацию об акции на Московской бирже."""
    ticker = ticker.upper()
    root = get_xml(
        f"{MOEX_BASE_URL}/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.xml",
        **{"iss.meta": "off", "iss.only": "securities", "securities.columns": "SECID,SHORTNAME,BOARDID,BOARDNAME,STATUS"},
    )
    row = root.find(".//row")
    if row is None:
        return {"error": f"Акция с тикером {ticker} не найдена"}
    return {"ticker": row.get("SECID"), "name": row.get("SHORTNAME"), "board": row.get("BOARDID"), "board_name": row.get("BOARDNAME"), "status": row.get("STATUS")}


def get_dividends(ticker: str) -> dict:
    """Получает доступные дивидендные события по тикеру."""
    ticker = ticker.upper()
    root = get_xml(f"{MOEX_BASE_URL}/securities/{ticker}/dividends.xml", **{"iss.meta": "off"})
    return {"ticker": ticker, "dividends": [dict(row.attrib) for row in root.findall(".//row")]}


def compare_stocks(tickers: list[str]) -> dict:
    """Сравнивает текущие цены и изменения выбранных акций."""
    requested = {ticker.upper() for ticker in tickers}
    return {"stocks": [row for row in get_market_rows() if row["ticker"] in requested]}
