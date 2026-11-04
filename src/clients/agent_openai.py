"""Клиент агента на OpenAI Agents SDK с моделью из OpenRouter."""

import asyncio
import json
import os
from typing import Any

import requests
from agents import (
    Agent,
    FunctionTool,
    OpenAIChatCompletionsModel,
    RunContextWrapper,
    RunConfig,
    Runner,
)
from dotenv import load_dotenv
from openai import AsyncOpenAI


SYSTEM_PROMPT = """Ты инвестиционный помощник.
Отвечай на русском языке. Если вопрос касается текущей цены акции,
используй инструмент get_stock_price. Не придумывай котировки.
"""


def get_settings() -> tuple[str, str, str, str]:
    """Читает настройки OpenRouter и локального сервера из .env."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENAI_MODEL", "openrouter/free")
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8080")

    if not api_key:
        raise RuntimeError("Не задана переменная окружения OPENAI_API_KEY")

    return api_key, base_url, model, mcp_server_url.rstrip("/")


def get_tools(mcp_server_url: str) -> list[dict[str, Any]]:
    """Получает описания инструментов у локального HTTP-сервера."""
    response = requests.get(f"{mcp_server_url}/tools", timeout=10)
    response.raise_for_status()
    return response.json()


def call_tool(
    mcp_server_url: str, tool_name: str, arguments: dict[str, Any]
) -> dict[str, Any]:
    """Вызывает инструмент локального HTTP-сервера."""
    response = requests.get(
        f"{mcp_server_url}/{tool_name}", params=arguments, timeout=15
    )
    response.raise_for_status()
    return response.json()


def create_tool(
    mcp_server_url: str, tool_info: dict[str, Any]
) -> FunctionTool:
    """Создаёт один FunctionTool, сохраняя его имя в отдельном замыкании."""
    function_info = tool_info["function"]
    tool_name = function_info["name"]

    async def run_function(
        _ctx: RunContextWrapper[Any], args: str
    ) -> str:
        """Выполняет HTTP-вызов инструмента и возвращает JSON-строку."""
        try:
            arguments = json.loads(args or "{}")
            result = await asyncio.to_thread(
                call_tool, mcp_server_url, tool_name, arguments
            )
        except (json.JSONDecodeError, requests.RequestException) as error:
            result = {"error": str(error)}

        return json.dumps(result, ensure_ascii=False)

    return FunctionTool(
        name=tool_name,
        description=function_info["description"],
        params_json_schema=function_info["parameters"],
        on_invoke_tool=run_function,
    )


def create_tools(mcp_server_url: str) -> list[FunctionTool]:
    """Создаёт FunctionTool для каждого инструмента сервера."""
    return [
        create_tool(mcp_server_url, tool_info)
        for tool_info in get_tools(mcp_server_url)
    ]


def create_agent(tools: list[FunctionTool]) -> Agent:
    """Создаёт агента с инструкциями и доступными инструментами."""
    return Agent(
        name="Инвестиционный помощник",
        instructions=SYSTEM_PROMPT,
        tools=tools,
    )


async def ask_agent(query: str) -> str:
    """Запускает агента и возвращает его финальный ответ."""
    api_key, base_url, model, mcp_server_url = get_settings()
    tools = create_tools(mcp_server_url)
    agent = create_agent(tools)

    run_config = RunConfig(
        model=OpenAIChatCompletionsModel(
            model=model,
            openai_client=AsyncOpenAI(
                api_key=api_key,
                base_url=base_url,
            ),
        ),
        tracing_disabled=True,
    )

    result = await Runner.run(
        agent,
        input=query,
        run_config=run_config,
    )
    return result.final_output


async def main() -> None:
    query = input("Введите вопрос: ").strip()
    if not query:
        raise SystemExit("Вопрос не должен быть пустым")
    print(await ask_agent(query))


if __name__ == "__main__":
    asyncio.run(main())
