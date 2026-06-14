# I Built an AI Agent That Watches the AI Space So I Don't Have To

Most people research manually. They open 10 tabs, check X, read a few articles, and try to make sense of it. Then they do it again tomorrow.

That's not a system. That's a habit that eats 2-3 hours a day.

I built something different.

---

## What it is

It's a Hermes Agent profile called **hermes-research-agent**. An autonomous AI research agent that runs on a schedule, watches the AI space, and delivers a scored digest to your Telegram.

Every morning at 09:00 it scans AI news, model releases, agent frameworks, arXiv, X, and HackerNews. Every signal gets scored 1–5. Only items scoring 3 or higher reach your Telegram. The rest goes to Obsidian for reference.

Every Monday it pulls real-time prices for 9 assets — NVDA, MSFT, GOOGL, SPY, QQQ, BTC, ETH, Gold, Silver — via Finnhub API. Best 3 and worst 3 delivered to Telegram. Then it scans Polymarket for AI, crypto, and macro prediction markets.

You configure it once. It runs without you.

---

## What you need

Before installing, get these 5 things:

1. **Model provider** — two options. **Nous Portal** (portal.nousresearch.com) is the recommended path. One OAuth login, no API key file, 300+ frontier models, and the Nous Tool Gateway included — web search, browser automation, all of it. Run `hermes setup --portal` after installing. If you're already logged into Nous Portal on your main Hermes install, this profile picks up the token automatically — nothing extra needed. **OpenRouter** (openrouter.ai) works out of the box with the default config — account is free but you need ~$5 in credits loaded. Either way: do not use free-tier models. Rate limits and queue latency break scheduled cron jobs. Recommended model: `deepseek/deepseek-v4-flash` — $0.10 per million input tokens. At typical cron job usage, expect under $1/month total for all three jobs.
2. **Telegram bot token** — open Telegram, search @BotFather, send `/newbot`, copy the token.
3. **Your Telegram user ID** — search @userinfobot, it tells you your ID number.
4. **Obsidian vault path** — the full path to your local vault folder.
5. **Finnhub API key** — free at finnhub.io. Needed for the market scan.

---

## How to install

**Step 1 — Install Hermes Agent**

Download Hermes Desktop from the Hermes Agent website. Install it. Open it.

You need version 0.16.0 or higher. You also need Node.js installed for one of the MCP servers.

**Step 2 — Install the profile**

In Hermes Desktop, run this command:

```
hermes profile install github.com/PedjaDrazic/hermes-research-agent --alias
```

This downloads 14 files: the agent's identity (SOUL.md), 3 research skills, 3 cron job definitions, 2 MCP servers, and the config.

**Step 3 — Fill your credentials**

Navigate to the profile folder. Find the `.env.EXAMPLE` file. Copy it to `.env`. Open it and fill in your 5 values.

Never commit this file to GitHub. Your credentials stay local.

**Step 4 — Set your Telegram home channel**

Open a chat with your Telegram bot. Send it this message:

```
/sethome
```

This tells the agent where to deliver its digests.

**Step 5 — Enable the cron jobs**

In Hermes Desktop, open the hermes-research-agent profile. Go to cron jobs. You'll see 4 listed:

- `argus-morning-scan` — daily at 09:00 local time
- `market-scan` — every Monday at 11:00
- `polymarket-scan` — every Monday at 11:30
- `argus-weekly-synthesis` — every Sunday at 18:00

Enable the ones you want. They start running on their next scheduled tick.

---

## What happens next

Tomorrow morning at 09:00, your Telegram gets a message like this:

```
🔭 ARGUS – 2026-06-14

| Signal | ★ | Why |
|---|---|---|
| **[breaking]** Claude 4 Opus released – Anthropic | 5 | Beats GPT-4o on all benchmarks |
| **[emerging]** Hermes Agent v0.17 ships rich messages – X | 4 | Telegram tables now native |
| **[backfill]** DeepSeek V4 Flash pricing cut – HN | 3 | Cheapest frontier reasoning now |

3 signals. Full scan → Obsidian.
```

If there's nothing worth reporting, it sends one line: `🔭 No signal today.`

Full scan always goes to Obsidian. Nothing gets lost.

---

## Why I built it this way

I teach people how to use AI systematically. Not as a chatbot you poke when you're curious. As a system that runs while you work on other things.

This agent does one thing. It watches. It scores. It delivers. Then it stops.

No chat interface. No "would you like me to do anything else?" No noise.

Configure once. Reuse forever.

---

## Get it

Everything is free and open source.

**Install command:**
```
hermes profile install github.com/PedjaDrazic/hermes-research-agent --alias
```

**GitHub:** github.com/PedjaDrazic/hermes-research-agent

Questions? Open an issue on GitHub or find me on X at @PedjaDrazic.

If you want to understand how I build and wire agents like this — that's what I cover at pedjadrazic.com.
