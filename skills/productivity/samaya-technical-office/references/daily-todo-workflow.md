# Daily Todo Workflow Reference

## Overview

Bilingual daily TODO extraction for Mohamed Essa (Director, Technical Office / BIM Unit).
Scans Aseer + Zamzam email registers → classifies by priority → delivers to Telegram.

**Class-level skill:** `bim-daily-todo` — all logic, priority rules, and output format live there.

This reference documents the data sources and known quirks.

## Data Sources

| Source | Path | Access |
|--------|------|--------|
| Aseer register (CSV) | `OneDrive/.../Aseer-Museum/Docs/Email Archive/مشروع متحف عسير الإقليمي/Register_ASEER_Professional.csv` | ✅ Direct read |
| Zamzam register (CSV) | `OneDrive/.../Zamzam Museum/Docs/Email Archive/مشروع تأهيل مسار الزوار زمزم/Project_Log_مشروع تأهيل مسار الزوار زمزم.csv` | ❌ OneDrive-locked |
| Watchdog state | `~/.hermes/scripts/.watchdog_state.json` | ✅ Primary Zamzam source |

## Zamzam — OneDrive Lock Workaround

The Zamzam CSV cannot be read when OneDrive sync is active (`Resource deadlock avoided`).
In practice:

1. **Cron/scheduled context**: Use `watchdog_state.json` only. Filter paths containing `Zamzam` where `mtime` within last 3 days.
2. **Manual session**: Ask user to close the CSV in Excel, then read directly.

**Watchdog Zamzam extraction (Python):**
```python
import json
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=3)
cutoff_ts = cutoff.timestamp()
with open('/Users/mohamedessa/.hermes/scripts/.watchdog_state.json') as f:
    watchdog = json.load(f)
zamzam_recent = [
    {'path': p, 'mtime': datetime.fromtimestamp(info['mtime']).strftime('%Y-%m-%d')}
    for p, info in watchdog.items()
    if 'Zamzam' in p and info.get('mtime', 0) >= cutoff_ts
]
```

## Telegram Delivery

| Config | Value |
|--------|-------|
| Bot token | `hermes config set telegram.bot_token <TOKEN>` |
| Channel | `-5832026231` (configured in `gateway.telegram.home_channel`) |

If bot_token is not in env → print to stdout (cron log), add delivery note to output.

## Projects

- **Aseer Regional Museum** — Project 3092, MoC client, NRS reviewer
- **Zamzam Museum** — ID 121/P0639, NWC client, Wael Al-Masri architect
