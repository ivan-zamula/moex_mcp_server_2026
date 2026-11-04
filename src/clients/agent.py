"""Клиент агента: OpenRouter + инструменты локального MCP-сервера."""

import json
import os
from typing import Any

import requests
from dotenv import load_dotenv
from openai import OpenAI


MAX_TOOL_ROUNDS = 5
SYSTEM_PROMPT = """Ты инвестиционный помощник.
Отвечай на русском языке. Если вопрос касается текущей цены акции,
используй инструмент get_stock_price. Не придумывай котировки.
"""


def get_settings() -> tuple[str, str, str, str]:
    """Читает настройки из окружения и проверяет наличие API-ключа."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENAI_MODEL", "openrouter/free")
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8080")

    if not api_key:
        raise RuntimeError("Не задана переменная окружения OPENAI_API_KEY")

    return api_key, base_url, model, mcp_server_url.rstrip("/")


def get_tools(mcp_server_url: str) -> list[dict[str, Any]]:
    """Получает описания инструментов у локального сервера."""
    response = requests.get(f"{mcp_server_url}/tools", timeout=10)
    response.raise_for_status()
    return response.json()


def call_tool(
    mcp_server_url: str, tool_name: str, arguments: dict[str, Any]
) -> dict[str, Any]:
    """Вызывает инструмент через HTTP API локального сервера."""
    response = requests.get(
        f"{mcp_server_url}/{tool_name}", params=arguments, timeout=15
    )
    response.raise_for_status()
    return response.json()


def ask_agent(query: str) -> str:
    """Отправляет вопрос модели и обрабатывает её вызовы инструментов."""
    api_key, base_url, model, mcp_server_url = get_settings()
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    tools = get_tools(mcp_server_url)

    for _ in range(MAX_TOOL_ROUNDS):
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            temperature=0.2,
        )
        assistant_message = completion.choices[0].message
        assistant_dict = assistant_message.model_dump(exclude_none=True)
        messages.append(assistant_dict)

        if not assistant_message.tool_calls:
            return assistant_message.content or "Модель не вернула текстовый ответ."

        for tool_call in assistant_message.tool_calls:
            try:
                arguments = json.loads(tool_call.function.arguments or "{}")
                result = call_tool(mcp_server_url, tool_call.function.name, arguments)
            except (json.JSONDecodeError, requests.RequestException) as error:
                result = {"error": str(error)}

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )

    raise RuntimeError("Превышено максимальное число циклов вызова инструментов")


def main() -> None:
    query = input("Введите вопрос: ").strip()
    if not query:
        raise SystemExit("Вопрос не должен быть пустым")
    print(ask_agent(query))


if __name__ == "__main__":
    main()
