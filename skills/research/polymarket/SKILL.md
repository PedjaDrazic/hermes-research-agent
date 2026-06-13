---
name: polymarket
description: "Query Polymarket: markets, prices, orderbooks, history. Weekly scan of AI/tech, crypto, and macro prediction markets."
version: 1.0.0
author: Hermes Agent + Teknium
tags: [polymarket, prediction-markets, market-data]
platforms: [linux, macos, windows]
tool_sets:
  - web
  - file
---

# Polymarket — Prediction Market Data

Query prediction market data from Polymarket using their public REST APIs.
All endpoints are read-only and require zero authentication.

## When to Use
- User asks about prediction markets, betting odds, or event probabilities
- User wants to know "what are the odds of X happening?"
- User asks about Polymarket specifically
- User wants market prices, orderbook data, or price history
- User asks to monitor or track prediction market movements

## Key Concepts
- **Events** contain one or more **Markets** (1:many relationship)
- **Markets** are binary outcomes with Yes/No prices between 0.00 and 1.00
- Prices ARE probabilities: price 0.65 means the market thinks 65% likely
- `outcomePrices` field: JSON-encoded array like `["0.80", "0.20"]`
- `clobTokenIds` field: JSON-encoded array of two token IDs [Yes, No] for price/book queries
- `conditionId` field: hex string used for price history queries
- Volume is in USDC (US dollars)

## Three Public APIs
1. **Gamma API** at `gamma-api.polymarket.com` — Discovery, search, browsing
2. **CLOB API** at `clob.polymarket.com` — Real-time prices, orderbooks, history
3. **Data API** at `data-api.polymarket.com` — Trades, open interest

## Typical Workflow
When a user asks about prediction market odds:
1. **Search** using the Gamma API public-search endpoint with their query
2. **Parse** the response — extract events and their nested markets
3. **Present** market question, current prices as percentages, and volume
4. **Deep dive** if asked — use clobTokenIds for orderbook, conditionId for history

## Presenting Results
Format prices as percentages for readability:
- outcomePrices `["0.652", "0.348"]` becomes "Yes: 65.2%, No: 34.8%"
- Always show the market question and probability
- Include volume when available

Example: `"Will X happen?" — 65.2% Yes ($1.2M volume)`

## Parsing Double-Encoded Fields
The Gamma API returns `outcomePrices`, `outcomes`, and `clobTokenIds` as JSON strings
inside JSON responses (double-encoded). When processing with Python, parse them with
`json.loads(market['outcomePrices'])` to get the actual array.

## Rate Limits
Generous — unlikely to hit for normal usage:
- Gamma: 4,000 requests per 10 seconds
- CLOB: 9,000 requests per 10 seconds
- Data: 1,000 requests per 10 seconds

## Scheduled Weekly Scan

A cron-driven scan runs every Monday (30 minutes after market-scan) using this skill.

### Categories Scanned
1. **AI / Tech** — model releases (GPT-5, Claude, Gemini), regulation, AGI timelines, company valuations
2. **Crypto** — BTC/ETH targets, ETF approvals, exchange events, regulation
3. **Macro/Geopolitical** — Fed rate decisions, elections, recession probability, geopolitical events

### Output

For each category, surface top 3–5 by volume, biggest movers (10%+ probability shifts), and interesting outliers.

**Telegram format (max 1500 chars):**
```
🎯 POLYMARKET — {YYYY-MM-DD}

🤖 AI / TECH
- [question] — [X]% YES | $[volume]

₿ CRYPTO
- [question] — [X]% YES | $[volume]

🌍 MACRO
- [question] — [X]% YES | $[volume]
```

**Obsidian (save after Telegram):**
- Use obsidian skill
- Path: `wiki/synthesis/polymarket-scan-{YYYY-MM-DD}.md`
- Include full analysis per category with all markets surfaced, not just top 3

**YAML frontmatter:**
```yaml
---
type: polymarket-scan
title: "Polymarket Scan – {YYYY-MM-DD}"
date: {YYYY-MM-DD}
tags: [argus, polymarket, weekly]
---
```

## Limitations
- This skill is read-only — it does not support placing trades
- Trading requires wallet-based crypto authentication (EIP-712 signatures)
- Some new markets may have empty price history
- Geographic restrictions apply to trading; read-only data is globally accessible
