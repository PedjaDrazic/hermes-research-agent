---
name: market-scan
description: "Weekly market snapshot — AI stocks, indices, commodities, crypto. Best 3 and worst 3 performers."
version: 1.1.0
author: Pedja Drazic
tool_sets:
  - web
  - file
---

# Market Scan

## Trigger
Cron — every Monday at 09:00 local time. Manual: "run market scan" or "market update".

## Instructions

1. **Batch price pull** — Call `mcp_finnhub_get_quote_batch` with all 9 symbols.
2. **Weekly % change** — Derive from Finnhub data.
3. **News scan** — Web search for context on the biggest movers.
4. **Score** — Rank by weekly % change. Best 3 and worst 3.
5. **Deliver** — Telegram short summary → Obsidian full table.

## Watchlist

### AI Stocks
- NVDA (NVIDIA)
- MSFT (Microsoft)
- GOOGL (Google)

### Indices
- SPY (S&P 500)
- QQQ (NASDAQ)

### Commodities
- GOLD (spot price)
- SILVER (spot price)

### Crypto
- BTC (Bitcoin)
- ETH (Ethereum)

## How to pull data

### Prices — Finnhub MCP (single batch call)
Call `mcp_finnhub_get_quote_batch` with:
```
["NVDA", "MSFT", "GOOGL", "SPY", "QQQ", "BTC", "ETH", "GOLD", "SILVER"]
```
Returns current price, change, % change, high, low for all 9 symbols in one call.
No web scraping needed for prices. The batch call replaces all former web finance lookups.

**Note:** `FINNHUB_API_KEY` must be set in your `.env`. If unset, the Finnhub MCP server will fail — fall back to web search for prices.

### Weekly % change — derive from Finnhub data
Finnhub returns `prev_close`. Use `(current - prev_close) / prev_close * 100` for daily change.
For weekly change, subtract your previous scan's recorded price from the current price.

### News & context — web search
Web search is only needed for context around notable moves:
- Earnings, product announcements, regulatory news
- Macro events affecting broad markets
- Crypto-specific news (ETF flows, halving, regulations)
- Commodity drivers (USD moves, supply shocks, central bank buying)

## Scoring
After pulling all data, rank by weekly % change:
- **Best 3** = highest positive % change
- **Worst 3** = lowest negative % change (or least positive)

## Output format

### Telegram (max 1500 characters):
```
📊 MARKET SCAN — {YYYY-MM-DD}

🟢 BEST
1. [Asset] $[price] [+X.X%] — [1-line reason if known]
2. [Asset] $[price] [+X.X%]
3. [Asset] $[price] [+X.X%]

🔴 WORST
1. [Asset] $[price] [-X.X%] — [1-line reason if known]
2. [Asset] $[price] [-X.X%]
3. [Asset] $[price] [-X.X%]

Full table → Obsidian.
```

### Obsidian (save after Telegram):
- Use obsidian skill
- Path: `wiki/synthesis/market-scan-{YYYY-MM-DD}.md`
- Include: full table of all 9 assets with price, weekly %, and any context found

**YAML frontmatter:**
```yaml
---
type: market-scan
title: "Market Scan – {YYYY-MM-DD}"
date: {YYYY-MM-DD}
tags: [argus, market-scan, weekly]
---
```

## Rules
- Cited sources only. Include URL or source name for any news context.
- If price data is unavailable for an asset, note it and skip — do not guess.
- Stop after delivering. No follow-up questions.
