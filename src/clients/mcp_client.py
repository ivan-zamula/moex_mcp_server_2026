import asyncio
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import (
    StdioServerParameters,
    stdio_client,
)


SERVER_FILE = (
    Path(__file__).resolve().parents[1]
    / "mcp_server"
    / "mcp_app.py"
)


async def main() -> None:
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_FILE)],
    )

    async with stdio_client(server_parameters) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            tools_result = await session.list_tools()

            print("Доступные инструменты:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool(
                "get_stock_price",
                {
                    "ticker": "SBER",
                },
            )

            print("\nРезультат вызова:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
