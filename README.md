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

### Weekly synthesis (Sunday 18:00)
- Reads all 7 daily Argus scans from the week
- Surfaces recurring signals, the week's emerging theme, score distribution
- Delivers the single best content angle to Telegram
- Saves full synthesis to Obsidian at `wiki/synthesis/argus-week-{YYYY-WNN}.md`

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

### Model provider (pick one)

| Option | How to set up |
|---|---|
| **Nous Portal** ✅ recommended | No API key needed. Run `hermes setup --portal` after installing. One OAuth login covers 300+ models + Tool Gateway. [portal.nousresearch.com](https://portal.nousresearch.com/manage-subscription) |
| **OpenRouter** | Set `OPENROUTER_API_KEY` in `.env`. Account free, ~$5 credits to start. [openrouter.ai](https://openrouter.ai) |

### Always required

| Variable | Where to get it |
|---|---|
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

## Model provider

**Option 1 — Nous Portal** (recommended)

[portal.nousresearch.com](https://portal.nousresearch.com) — the native provider for Hermes Agent. One OAuth login covers 300+ frontier models and the Nous Tool Gateway (web search, browser automation, image gen, TTS — no separate API keys).

No API key file needed. After installing the profile, run:
```bash
hermes setup --portal
```
Or if you already have Hermes configured with another provider:
```bash
hermes model
# pick "Nous Portal" from the list
```
The Portal refresh token is shared across all Hermes profiles automatically — if you're already logged in, this profile picks it up with no extra setup.

Recommended models for agent work (prices per million tokens — input / output):

| Model | Input | Output | Notes |
|---|---|---|---|
| `deepseek/deepseek-v4-flash` | $0.10 | $0.20 | Default — best value for cron jobs |
| `deepseek/deepseek-v4-pro` | $1.60 | $3.20 | Higher reasoning quality |
| `anthropic/claude-sonnet-4.6` | $3.00 | $15.00 | Best general-purpose agent model |
| `anthropic/claude-haiku-4.5` | $1.00 | $5.00 | Fast, cheap Anthropic option |
| `google/gemini-3.5-flash` | $1.50 | $9.00 | Large context window |
| `stepfun/step-3.7-flash` | $0.20 | $1.15 | Cheap alternative to DeepSeek Flash |

> **Note:** Hermes 4 models (Hermes-4-70B, Hermes-4-405B) are tuned for chat, not tool-calling loops. Do not use them inside Hermes Agent — this is official guidance from Nous Research.

> **Free models** (`nvidia/nemotron-3-ultra:free`, `stepfun/step-3.7-flash:free`) are available but not recommended for scheduled cron jobs — no SLA, variable latency.

**Option 2 — OpenRouter**

[openrouter.ai](https://openrouter.ai) — works out of the box with the default `config.yaml`. Account is free, but you need credits loaded (~$5 to start). Do not use free-tier models — they have rate limits and queue latency that break scheduled cron jobs.

Add your key to `.env`:
```
OPENROUTER_API_KEY=your_key_here
```

Recommended model: `deepseek/deepseek-v4-flash` (~$0.10/day, ~$3/month for all three cron jobs).

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
