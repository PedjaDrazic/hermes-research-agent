# Argus Morning Scan — Deployment & Operations

Operational learnings for running the `argus-morning-scan` cron job on Hermes.

## Environment Prerequisites
```env
# .env (in the active Hermes profile)
TELEGRAM_BOT_TOKEN=***                  # Required for Telegram delivery
TELEGRAM_ALLOWED_USERS=<user_id>        # Required for Telegram delivery
OBSIDIAN_VAULT_PATH=C:/path/to/vault    # Absolute path to your vault
```

## Cron Job Setup
```bash
hermes -p hermes-research-agent cron create "0 9 * * *" "...full scan prompt..." \
  --name argus-morning-scan \
  --skill argus-morning-scan --skill obsidian \
  --deliver origin
```

### Time Zone Handling
Cron schedules use the system's local time, not UTC. To target 07:00 UTC:
- UTC+1 (CET) → `0 8 * * *`
- UTC+2 (CEST) → `0 9 * * *`
- UTC+0 (GMT) → `0 7 * * *`

Verify with the `Next run` field in the cron-create response.

### Delivery Routing
| `--deliver` value | Behaviour |
|----------------|-----------|
| `local` | Saves to cron session store only. **Telegram message is never sent.** |
| `origin` | Delivers back to the chat the cron was created from. Use this for Telegram. |
| `telegram:<chat_id>` | Delivers to a specific Telegram chat. |

**Important:** the agent produces Telegram-formatted output regardless of delivery
mode. `--deliver` controls WHERE it goes, not what it looks like. For the scan to
reach Telegram, use `origin` or a `telegram:` target — NOT `local`.

### Approval Mode
Cron jobs can stall on shell commands if `approvals.mode` is `manual` and a command
trips the approval gate (no interactive user in cron context). In `config.yaml`:
```yaml
approvals:
  mode: off          # bypass approval prompts in cron, OR
  cron_mode: deny    # deny all cron approvals by default
```

## Verifying the Scan Ran
```bash
hermes -p hermes-research-agent cron list      # look for "Last run: ... ok"
hermes -p hermes-research-agent gateway status  # cron only fires if gateway is up
# Confirm the Obsidian note was written:
#   {OBSIDIAN_VAULT_PATH}/wiki/synthesis/argus-scan-{YYYY-MM-DD}.md
```

## Known Pitfalls
- **Gateway must be running:** the cron scheduler runs inside the gateway process. If the gateway is down, cron jobs do not fire. Check `gateway status`.
- **`local` delivery never reaches Telegram:** the single most common "why didn't I get my scan" cause. Use `origin`.
- **Sources bootstrap:** if `references/sources.md` is missing, the agent invents its own — works, but you lose your curated source list. Keep `sources.md` in the skill dir.
- **Vault auto-creation:** if `OBSIDIAN_VAULT_PATH` is unset, the agent falls back to `~/Documents/Obsidian Vault/`. Set the env var to point at your real vault.
- **Updates can wipe crons:** `hermes update` may clear the cron store and stop gateways. After any update, re-check `cron list` and `gateway status`, and recreate jobs if needed. Keep your cron definitions in the repo's `cron/` folder so recovery is copy-paste.
