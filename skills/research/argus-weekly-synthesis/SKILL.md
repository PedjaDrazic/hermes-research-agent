---
name: argus-weekly-synthesis
description: "Weekly synthesis — reads all Argus daily scans from the past 7 days, surfaces patterns, top signals, and the strongest content angle."
version: 1.0.0
author: Pedja Drazic
tool_sets:
  - file
---

# Argus Weekly Synthesis

## Trigger
Cron — every Sunday at 18:00 local time. Manual: "run weekly synthesis" or "synthesize this week's scans".

## Instructions

### Step 1 — Read the week's scans
Open the Obsidian vault at `$OBSIDIAN_VAULT_PATH`.

Read all daily scan files from the past 7 days:
- Path pattern: `wiki/synthesis/argus-scan-{YYYY-MM-DD}.md`
- Read each file that exists. Some days may have no scan file — skip them.
- Also read `wiki/inbox/` for any handoff files from this week: `argus-handoff-{YYYY-MM-DD}.json`

If fewer than 3 scan files exist for the week, write a short Obsidian note noting the gap and stop — do not send a Telegram summary.

### Step 2 — Identify patterns
Across all scans you just read, find:

**Recurring signals** — topics, tools, or names that appeared in 3 or more daily scans. These are the signals with staying power.

**Emerging theme** — the single strongest thread running through the week. What was the AI space actually talking about, underneath the individual stories?

**Score distribution** — how many items scored 5 (breaking), 4 (emerging), 3 (backfill) across the week. A week with many 4s and 5s is a high-signal week. A week dominated by 3s is a low-signal week.

**Best content angle** — the single most specific, non-obvious insight from the week that Pedja has not yet written about. Must be concrete. "AI agents are growing" is not an angle. "Developers are switching from building agents to installing agent profiles" is an angle.

### Step 3 — Telegram delivery
Send to home channel via `send_message(action='send', target='telegram', message=...)`.

Max 1000 characters. Format:

```
📊 ARGUS WEEK — {Mon DD} → {Sun DD}

🔁 RECURRING ({N} signals)
• [Topic/tool that kept appearing] — seen N days
• [Second recurring signal] — seen N days

🧵 THEME
[One sentence: the thread running through the week]

✍️ BEST ANGLE
[Specific, non-obvious content hook Pedja can open with]

{N} scans · {N} total signals · {high/medium/low} signal week
```

No intro. No fake urgency. If there is no strong content angle, write "No clear angle this week." Do not invent one.

### Step 4 — Obsidian note
Save to: `wiki/synthesis/argus-week-{YYYY-WNN}.md`

Where `WNN` = ISO week number (e.g., `W24`).

**YAML frontmatter:**
```yaml
---
type: weekly-synthesis
title: "Argus Week {WNN} — {Mon DD} to {Sun DD YYYY}"
date: {YYYY-MM-DD}
week: {WNN}
tags: [argus, weekly-synthesis]
scans_read: {N}
total_signals: {N}
signal_level: high | medium | low
---
```

Include in the body:
- Full list of recurring signals with day counts
- Emerging theme with reasoning
- Score distribution table
- Best content angle with source scans cited
- Any signals that appeared only once but scored 5 (breaking) — these may matter even without recurrence

After saving, append an entry to `wiki/log.md`.

## Rules
- Read before synthesizing. Do not summarize from memory — read the actual files.
- Cite which scan files each finding comes from.
- Stop after delivering. No follow-up questions.
