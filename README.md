# hermes-research-agent

An autonomous AI research agent built on [Hermes Agent](https://github.com/NousResearch/hermes-agent).

Every morning it scans AI/tech news, X, arXiv, and YouTube trends — scores each signal — and delivers a ranked digest to your Telegram. Every Monday it checks your market positions and scans Polymarket for relevant predictions.

You configure it once. It runs without you.

---

## What it does

### Daily morning scan (09:00 local time)
- AI and tech news from the web, X/Twitter, arXiv, YouTube
- Every item scored 1–5 (breaking → noise)
- Only items scoring 3+ reach Telegram
- Full scan always written to Obsidian for reference
- Format: `**[breaking]**`, `**[emerging]**`, `**[backfill]**`, `**[evergreen]**` labels in a rich markdown table

### Weekly market scan (Monday)
- Real-time quotes via Finnhub API: NVDA, MSFT, GOOGL, SPY, QQQ, BTC, ETH, Gold, Silver
- Best 3 / worst 3 ranked
- Written to Obsidian

### Weekly prediction market scan (Monday)
- Polymarket predictions: AI/tech, crypto, macro
- Written to Obsidian

---

## Install

Requires [Hermes Agent](https://github.com/NousResearch/hermes-agent) v0.16.0+ and Node.js (for the agentwikis MCP server).

```bash
hermes profile install github.com/PedjaDrazic/hermes-research-agent --alias
```

Then fill in your credentials:

```bash
cp ~/.hermes/profiles/hermes-research-agent/.env.EXAMPLE \
   ~/.hermes/profiles/hermes-research-agent/.env
# Edit .env with your API keys
```

Start the agent:

```bash
hermes-research-agent gateway start
```

Enable the cron jobs (not auto-scheduled — you choose when to activate):

```bash
hermes -p hermes-research-agent cron list
# Enable the ones you want from the list
```

Set your Telegram home channel so the agent knows where to send digests:

```bash
# In your Telegram bot chat, send:
/sethome
```

---

## Required credentials

| Variable | Where to get it |
|---|---|
| `OPENROUTER_API_KEY` | [openrouter.ai](https://openrouter.ai) — free to start |
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` |
| `TELEGRAM_ALLOWED_USERS` | Your user ID from [@userinfobot](https://t.me/userinfobot) |
| `OBSIDIAN_VAULT_PATH` | Absolute path to your local Obsidian vault |
| `FINNHUB_API_KEY` | [finnhub.io](https://finnhub.io) — free tier, needed for market-scan |

---

## Included MCP servers

| Server | Purpose |
|---|---|
| `agentwikis` | Hermes Agent documentation — agent queries this when it needs config help |
| `finnhub` | Real-time stock, ETF, crypto, and commodity quotes |

The Finnhub server is a local Python script at `tools/finnhub_server.py`. It requires `FINNHUB_API_KEY` in your `.env`.

---

## Recommended model

`deepseek/deepseek-v4-flash` via OpenRouter. Fast, cheap (~$0.10/day for all three cron jobs combined), handles research and scoring well.

You can change this in `config.yaml` to any OpenRouter-supported model.

---

## Updates

```bash
hermes profile update hermes-research-agent
```

Your `.env`, memories, and sessions are never touched on update.

---

## Built by

[Pedja Drazic](https://pedjadrazic.com) — AI educator building honest, reproducible agent workflows for solo operators.

Questions or issues → open a GitHub issue or find me on [X](https://x.com/PedjaDrazic).
