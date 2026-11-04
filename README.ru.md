# MOEX MCP Server (2026)

[English](README.md) | [Русский](README.ru.md)

Python-сервер, который предоставляет AI-агенту HTTP-инструмент для получения котировок акций Московской биржи.

## Возможности

- FastAPI-сервер с endpoint проверки состояния и получения инструментов.
- Инструмент получения котировки через ISS API Московской биржи.
- Консольный AI-агент на Python.
- Подключение внешней модели через OpenRouter и OpenAI-compatible API.
- Цикл обработки вызова инструмента с передачей результата обратно модели.

Это HTTP-реализация по мотивам MCP, а не полная реализация стандарта MCP. Production-защита и развертывание находятся вне текущего объёма.

## Архитектура

```text
Пользователь -> agent.py -> модель OpenRouter
                    |              |
                    +-> tools -----+
                         |
                         v
                   FastAPI-сервер -> ISS API MOEX
```

Клиент получает список инструментов через `GET /tools`. Когда модель запрашивает `get_stock_price`, клиент вызывает локальный сервер и передаёт JSON-результат обратно модели.

## Стек и структура

Python 3.11+, FastAPI, Uvicorn, Requests, OpenAI Python SDK, OpenRouter и `python-dotenv`.

| Путь | Назначение |
| --- | --- |
| [`src/mcp_server/server.py`](src/mcp_server/server.py) | FastAPI-приложение и HTTP-endpoint’ы |
| [`src/mcp_server/tools.py`](src/mcp_server/tools.py) | Схемы инструментов, доступных клиенту |
| [`src/clients/agent.py`](src/clients/agent.py) | Клиент OpenRouter и цикл вызова инструментов |
| [`src/clients/agent_openai.py`](src/clients/agent_openai.py) | Вариант клиента на Agents SDK с той же конфигурацией OpenRouter |
| [`tests/`](tests/) | Файлы локальных проверок |
| [`docs/`](docs/) | Заметки по архитектуре и запуску |

## Установка

Требуется Python 3.11 или новее.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp .env.example .env
```

Создайте API-ключ в [OpenRouter](https://openrouter.ai/) и укажите настройки в локальном `.env`:

```env
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openrouter/free
MCP_SERVER_URL=http://127.0.0.1:8080
```

Настоящий `.env` должен оставаться локальным. Он исключён из Git.

## Запуск

В первом терминале запустите сервер:

```bash
cd src/mcp_server
uvicorn server:app --reload --port 8080
```

Документация API будет доступна по адресу <http://127.0.0.1:8080/docs>.

Во втором терминале из корня проекта запустите клиент:

```bash
PYTHONPATH=src python -m clients.agent
```

Вариант на Agents SDK запускается так:

```bash
PYTHONPATH=src python -m clients.agent_openai
```

Затем введите, например:

```text
Сколько сегодня стоит акция Сбербанка?
```

## Проверки

Проверить компиляцию Python-исходников без внешних API-запросов:

```bash
python -m compileall -q src tests
```

Для запроса к OpenRouter и получения котировки MOEX нужны настроенные учетные данные, сеть и запущенный сервер.

## Идея

Идея проекта и первоначальный подход к реализации основаны на
[проекте RedMadRobot к статье о создании собственного MCP](https://github.com/RedMadRobot/custom-mcp-article).
