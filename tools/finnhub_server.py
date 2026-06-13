#!/usr/bin/env python3
"""
Finnhub MCP Server for Argus
Real-time stock, ETF, crypto, and commodity quotes via Finnhub API.
STDIO transport — registered in Argus config.yaml as an mcpServer.

Supported symbols:
  Stocks/ETFs : NVDA, MSFT, GOOGL, SPY, QQQ (and any US-listed ticker)
  Crypto      : BTC, ETH  → mapped to BINANCE:BTCUSDT / BINANCE:ETHUSDT
  Metals      : GOLD, XAU → OANDA:XAU_USD | SILVER, XAG → OANDA:XAG_USD
"""

import json
import sys
import os
import urllib.request
import urllib.parse
import urllib.error
from typing import Any

API_KEY = os.environ.get("FINNHUB_API_KEY", "")
BASE_URL = "https://finnhub.io/api/v1"

# Symbol normalization map
SYMBOL_MAP = {
    "BTC":    "BINANCE:BTCUSDT",
    "ETH":    "BINANCE:ETHUSDT",
    "GOLD":   "OANDA:XAU_USD",
    "XAU":    "OANDA:XAU_USD",
    "SILVER": "OANDA:XAG_USD",
    "XAG":    "OANDA:XAG_USD",
}


def finnhub_get(endpoint: str, params: dict) -> dict:
    params["token"] = API_KEY
    url = f"{BASE_URL}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "argus-finnhub-mcp/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def resolve_symbol(raw: str) -> tuple[str, str]:
    """Returns (display_name, finnhub_symbol)"""
    upper = raw.upper().strip()
    mapped = SYMBOL_MAP.get(upper, upper)
    return upper, mapped


def fetch_quote(raw_symbol: str) -> dict:
    display, finnhub_sym = resolve_symbol(raw_symbol)
    try:
        data = finnhub_get("quote", {"symbol": finnhub_sym})
        c = data.get("c", 0)
        pc = data.get("pc", 0)
        if c == 0 and pc == 0:
            return {
                "symbol": display,
                "error": f"No quote data returned for {finnhub_sym}. "
                         "Symbol may not be supported on free tier."
            }
        change = round(c - pc, 4)
        change_pct = round((change / pc * 100), 2) if pc else 0.0
        return {
            "symbol":     display,
            "current":    c,
            "change":     change,
            "change_pct": change_pct,
            "high":       data.get("h"),
            "low":        data.get("l"),
            "open":       data.get("o"),
            "prev_close": pc,
            "source":     "finnhub"
        }
    except urllib.error.HTTPError as e:
        return {"symbol": display, "error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"symbol": display, "error": str(e)}


# ── MCP tool definitions ───────────────────────────────────────────────────

TOOLS = [
    {
        "name": "get_quote",
        "description": (
            "Get a real-time quote for a single stock, ETF, crypto, or commodity. "
            "Supports: US tickers (NVDA, SPY…), BTC, ETH, GOLD/XAU, SILVER/XAG."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Ticker or asset name, e.g. NVDA, BTC, GOLD"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_quote_batch",
        "description": (
            "Get real-time quotes for a list of symbols in one call. "
            "Returns a list of quote objects. Use for market_scan."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of tickers/assets, e.g. [\"NVDA\",\"BTC\",\"GOLD\"]"
                }
            },
            "required": ["symbols"]
        }
    }
]


# ── MCP JSON-RPC handler ───────────────────────────────────────────────────

def handle(request: dict) -> dict | None:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "finnhub", "version": "1.0.0"}
            }
        }

    if method == "notifications/initialized":
        return None  # no response for notifications

    if method == "tools/list":
        return {
            "jsonrpc": "2.0", "id": req_id,
            "result": {"tools": TOOLS}
        }

    if method == "tools/call":
        name = request["params"]["name"]
        args = request["params"].get("arguments", {})
        try:
            if name == "get_quote":
                result = fetch_quote(args["symbol"])
            elif name == "get_quote_batch":
                result = [fetch_quote(s) for s in args["symbols"]]
            else:
                result = {"error": f"Unknown tool: {name}"}

            return {
                "jsonrpc": "2.0", "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            }
        except Exception as exc:
            return {
                "jsonrpc": "2.0", "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"error": str(exc)})}],
                    "isError": True
                }
            }

    return {
        "jsonrpc": "2.0", "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"}
    }


# ── Main loop ──────────────────────────────────────────────────────────────

def main() -> None:
    if not API_KEY:
        sys.stderr.write("ERROR: FINNHUB_API_KEY not set in environment\n")
        sys.exit(1)

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle(req)
            if resp is not None:
                print(json.dumps(resp), flush=True)
        except Exception as exc:
            print(json.dumps({
                "jsonrpc": "2.0", "id": None,
                "error": {"code": -32700, "message": f"Parse error: {exc}"}
            }), flush=True)


if __name__ == "__main__":
    main()
