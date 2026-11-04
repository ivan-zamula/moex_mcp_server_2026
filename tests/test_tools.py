"""Тесты инструментов MCP-сервера без внешних сетевых запросов."""

from unittest.mock import Mock, patch

import pytest
import requests

from mcp_server.tools.stocks import (
    get_stock_history,
    get_stock_info,
    get_stock_price,
)


MOEX_XML = """
<document>
    <marketdata>
        <rows>
            <row SECID="SBER" LAST="291.41" />
            <row SECID="GAZP" LAST="174.20" />
        </rows>
    </marketdata>
</document>
"""

HISTORY_XML = """
<document>
    <history>
        <rows>
            <row TRADEDATE="2026-01-15" OPEN="280.1" HIGH="293.0"
                 LOW="278.5" CLOSE="291.4" VOLUME="12450000" />
        </rows>
    </history>
</document>
"""

INFO_XML = """
<document>
    <securities>
        <rows>
            <row SECID="SBER" SHORTNAME="Сбербанк" BOARDID="TQBR"
                 BOARDNAME="Т+: Акции и ДР" STATUS="1" />
        </rows>
    </securities>
</document>
"""


def mock_response(text: str, status_code: int = 200) -> Mock:
    response = Mock()
    response.text = text
    response.status_code = status_code
    response.raise_for_status.return_value = None
    return response


@patch("mcp_server.tools.moex.requests.get")
def test_get_stock_price_returns_quote(mock_get: Mock) -> None:
    mock_get.return_value = mock_response(MOEX_XML)

    result = get_stock_price("sber")

    assert result == {
        "ticker": "SBER",
        "price": 291.41,
        "currency": "RUB",
    }
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["timeout"] == 15


@patch("mcp_server.tools.moex.requests.get")
def test_get_stock_price_returns_error_for_unknown_ticker(mock_get: Mock) -> None:
    mock_get.return_value = mock_response(MOEX_XML)

    result = get_stock_price("unknown")

    assert result == {"error": "Акция с тикером UNKNOWN не найдена"}


@patch("mcp_server.tools.moex.requests.get")
def test_get_stock_price_propagates_http_error(mock_get: Mock) -> None:
    response = mock_response("", status_code=503)
    response.raise_for_status.side_effect = requests.HTTPError("503 Service Unavailable")
    mock_get.return_value = response

    with pytest.raises(requests.HTTPError, match="503 Service Unavailable"):
        get_stock_price("SBER")


@patch("mcp_server.tools.moex.requests.get")
def test_get_stock_history_returns_rows(mock_get: Mock) -> None:
    mock_get.return_value = mock_response(HISTORY_XML)

    result = get_stock_history("sber", "2026-01-01", "2026-01-31")

    assert result == {
        "ticker": "SBER",
        "history": [
            {
                "date": "2026-01-15",
                "open": 280.1,
                "high": 293.0,
                "low": 278.5,
                "close": 291.4,
                "volume": 12450000.0,
            }
        ],
    }


def test_get_stock_history_rejects_invalid_date_range() -> None:
    with pytest.raises(ValueError, match="from_date"):
        get_stock_history("SBER", "2026-02-01", "2026-01-01")


@patch("mcp_server.tools.moex.requests.get")
def test_get_stock_info_returns_security_data(mock_get: Mock) -> None:
    mock_get.return_value = mock_response(INFO_XML)

    result = get_stock_info("sber")

    assert result == {
        "ticker": "SBER",
        "name": "Сбербанк",
        "board": "TQBR",
        "board_name": "Т+: Акции и ДР",
        "status": "1",
    }
