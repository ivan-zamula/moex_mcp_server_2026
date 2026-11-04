"""Точка входа и HTTP/MCP-инструменты сервера."""

from fastapi import FastAPI, HTTPException
import requests
import uvicorn

import xml.etree.ElementTree as ET


from tools import STOCK_PRICE_TOOL

app = FastAPI(title="MCP Server", description="MCP Server API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "MCP Server is running."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Tools endpoint
@app.get("/tools")
async def get_tools():
    return [STOCK_PRICE_TOOL]


@app.get("/get_stock_price")
async def get_stock_price(ticker: str):
    """Получает текущую цену акции на Московской бирже по её тикеру"""

    # Запрос к API Московской биржи
    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml?iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST"

    try:
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.text)

        for row in root.findall(".//row"):
            if row.get("SECID") == ticker:
                price = row.get("LAST")
                return {
                    "ticker": ticker,
                    "price": float(price) if price else None,
                    "currency": "RUB",
                }

        raise HTTPException(status_code=404, detail=f"Акция с тикером '{ticker}' не найдена на Московской бирже.")


    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к API Московской биржи: {str(e)}")





if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)