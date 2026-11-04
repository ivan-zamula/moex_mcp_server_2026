"""Описание и реализация инструментов MCP-сервера."""

STOCK_PRICE_TOOL = {
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Получает текущую цену акции на Московской бирже по её тикеру",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Тикерный символ акции, например, SBER для Сбербанка или GAZP для Газпрома",
                }
            },
            "required": ["ticker"],
        },
    },
}