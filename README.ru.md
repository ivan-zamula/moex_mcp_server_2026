# MOEX MCP Server (2026)

[English](README.md) | [Русский](README.ru.md)

Python MCP-сервер, который предоставляет AI-хосту инструмент для получения котировок акций Московской биржи.

## Возможности

- Стандартный MCP-сервер на официальном Python SDK.
- Инструменты получения текущей котировки, истории и информации об акции через ISS API Московской биржи.
- Минимальный MCP-клиент для проверки протокола.

Текущий транспорт — `stdio`. Production-защита и развертывание находятся вне текущего объёма.

## Архитектура

```text
MCP host/client -> stdio -> MCP-сервер -> MOEX tools -> ISS API MOEX
```

MCP-клиент получает список инструментов через стандартную MCP-сессию и вызывает
инструменты `get_stock_price`, `get_stock_history` и `get_stock_info` через транспорт `stdio`.

## Инструменты

### `get_stock_price`

Возвращает текущую цену акции на Московской бирже.

Параметр:

```text
ticker: SBER
```

Пример результата:

```json
{
  "ticker": "SBER",
  "price": 291.41,
  "currency": "RUB"
}
```

### `get_stock_history`

Возвращает исторические цены акции за указанный период. Параметры: `ticker`,
`from_date` и `to_date` в формате `YYYY-MM-DD`. Результат содержит дату торгов,
цены открытия, максимума, минимума и закрытия, а также объём торгов.

### `get_stock_info`

Возвращает тикер, название, торговую площадку, название режима торгов и статус
инструмента. Принимает параметр `ticker`.

### Рыночные инструменты

- `get_market_summary(limit)` — сводка по количеству инструментов и лидерам роста и падения.
- `get_top_gainers(limit)` — акции с наибольшим ростом за текущую сессию.
- `get_top_losers(limit)` — акции с наибольшим падением за текущую сессию.

Параметр `limit` задаёт количество результатов.

### Дополнительные инструменты

- `get_dividends(ticker)` — дивидендные события по тикеру.
- `compare_stocks(tickers)` — сравнение текущих цен и изменений нескольких акций.
- `calculate_portfolio_value(portfolio)` — расчёт стоимости портфеля. Позиция содержит `ticker` и `quantity`.

## Стек и структура

Python 3.11+, официальный MCP Python SDK и Requests.

| Путь | Назначение |
| --- | --- |
| [`src/mcp_server/mcp_app.py`](src/mcp_server/mcp_app.py) | MCP-сервер и регистрация инструментов |
| [`src/mcp_server/tools/market.py`](src/mcp_server/tools/market.py) | Рыночные инструменты MOEX |
| [`src/mcp_server/tools/stocks.py`](src/mcp_server/tools/stocks.py) | Инструменты работы с акциями |
| [`src/mcp_server/tools/portfolio.py`](src/mcp_server/tools/portfolio.py) | Инструменты работы с портфелем |
| [`src/mcp_server/tools/moex.py`](src/mcp_server/tools/moex.py) | Общие функции доступа к ISS API |
| [`src/clients/mcp_client.py`](src/clients/mcp_client.py) | MCP-клиент для проверки протокола |
| [`tests/`](tests/) | Файлы локальных проверок |
| [`docs/`](docs/) | Заметки по архитектуре и запуску |
| [`scripts/`](scripts/) | Команды запуска сервера и тестов |

## Установка

Требуется Python 3.11 или новее.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Запуск

Запустите MCP-клиент из корня проекта:

```bash
PYTHONPATH=src python -m clients.mcp_client
```

Клиент сам запускает MCP-сервер через `stdio`, получает список инструментов и
вызывает `get_stock_price`.

Затем введите, например:

```text
Сколько сегодня стоит акция Сбербанка?
```

## Проверки

Проверить компиляцию Python-исходников без внешних API-запросов:

```bash
python -m compileall -q src tests
```

Для получения котировки MOEX нужен доступ к сети.

## Идея

Идея проекта и первоначальный подход к реализации основаны на
[проекте RedMadRobot к статье о создании собственного MCP](https://github.com/RedMadRobot/custom-mcp-article).
