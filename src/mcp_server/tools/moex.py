import xml.etree.ElementTree as ET

import requests


MOEX_BASE_URL = "https://iss.moex.com/iss"


def get_xml(url: str, **params: str) -> ET.Element:
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return ET.fromstring(response.text)


def to_float(value: str | None) -> float | None:
    return float(value) if value else None


def get_market_rows() -> list[dict]:
    root = get_xml(
        f"{MOEX_BASE_URL}/engines/stock/markets/shares/boards/TQBR/securities.xml",
        **{
            "iss.meta": "off",
            "iss.only": "marketdata",
            "marketdata.columns": "SECID,LAST,PREVPRICE,CHANGE,CHANGEPRCNT,VOLRUR",
        },
    )
    rows = []
    for row in root.findall(".//row"):
        last = to_float(row.get("LAST"))
        change_percent = to_float(row.get("CHANGEPRCNT"))
        if last is not None and change_percent is not None:
            rows.append(
                {
                    "ticker": row.get("SECID"),
                    "price": last,
                    "change": to_float(row.get("CHANGE")),
                    "change_percent": change_percent,
                    "volume": to_float(row.get("VOLRUR")),
                }
            )
    return rows
