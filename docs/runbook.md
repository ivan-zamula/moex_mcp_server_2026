# Запуск и проверка

Все команды выполняются из корня проекта.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Запуск MCP-сервера

Сервер использует `stdio`, поэтому обычно его запускает MCP-хост или тестовый
клиент:

```bash
./scripts/run_server.sh
```

## Проверка MCP-клиентом

```bash
PYTHONPATH=src .venv/bin/python -m clients.mcp_client
```

Клиент должен вывести список зарегистрированных инструментов и результат
вызова `get_stock_price`. Для этого шага нужен доступ к MOEX ISS API.

## Локальные тесты

```bash
./scripts/check.sh
```

Тесты используют mock HTTP-ответы и не обращаются к MOEX.
