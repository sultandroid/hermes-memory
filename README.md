# Hermes Memory — Mohamed Essa

> Central knowledge base for all AI agents working with Samaya Investment and Mohamed Essa.
> Share this repo across devices and agents for consistent context.

## ⚠️ Read First

**`AGENTS.md`** is the machine-readable contract every synced agent must read on wake. It defines:
- The two-layer model (hub = identity + skills; project repos = work)
- The wake-up checklist (which files to read in which order)
- The sync contract (when to push back, when to keep project-local)
- When to scaffold a new project repo

If you are an agent, **read `AGENTS.md` before doing anything else.**

---

## Contents

| File | Description |
|------|-------------|
| `AGENTS.md` | **Wake-up contract — read this first** |
| `USER.md` | User profile — communication style, preferences |
| `RULES.md` | Working rules, pitfalls, conventions |
| `MEMORY.md` | Procedural memory — Odoo, projects, recurring pitfalls |
| `PROJECTS.md` | Project INDEX — routes to each project repo (WORK / CONSULTING / PERSONAL) |
| `ODOO.md` | Odoo Samaya connection guide + XML-RPC patterns + PO/task templates |
| `ODOO_FULL.md` | Full Odoo reference (long-form) |
| `CONTACTS.md` | Key people, roles, emails, Odoo IDs |
| `unified/UNIFIED_MEMORY.md` | Auto-generated consolidated view across all agents |
| `templates/PROJECT_TEMPLATE/` | Scaffold for new project repos |
| `scripts/` | Sync engine + health check + watchdog scripts |
| `sync_conflicts.md` | Manual review queue for bidirectional sync conflicts |
| `references/sister-companies-knowledge-map.md` | Cross-entity reference (read-only) |

## Two-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  HUB  (this repo)                           │
│  Identity · Skills · Project INDEX          │
│  - USER.md, RULES.md, MEMORY.md, AGENTS.md  │
│  - skills/                                  │
│  - PROJECTS.md (routes to repos below)     │
└──────────────────┬──────────────────────────┘
                   │ cd into project
     ┌─────────────┼─────────────┬─────────────┐
     ▼             ▼             ▼             ▼
┌─────────┐ ┌─────────┐ ┌──────────┐  ┌─────────────┐
│ aseer-  │ │ samaya- │ │ RCRC-    │  │ sultan-     │
│ museum- │ │ workspc │ │ Exhibit. │  │ house       │
│ pm      │ │         │ │ (consul.)│  │ (personal)  │
└─────────┘ └─────────┘ └──────────┘  └─────────────┘
   WORK       WORK       CONSULTING      PERSONAL
```

Cross-project facts → hub. Project-specific facts → project repo.

## Quick Start

```bash
# Clone on any device
git clone https://github.com/sultandroid/hermes-memory.git ~/hermes-memory
cd ~/hermes-memory

# Read the contract
cat AGENTS.md

# Set up Odoo credentials (do NOT commit)
mkdir -p ~/.config/samaya
cp ODOO_CREDENTIALS.md ~/.config/samaya/odoo.env 2>/dev/null || true
chmod 600 ~/.config/samaya/odoo.env

# Load into Hermes agent
hermes config set memory_file ~/hermes-memory/MEMORY.md
```

## Daily Sync

Runs at 10:00 Cairo via cron:

1. `scripts/hub_health_check.sh` — integrity check
2. `scripts/memory_skills_exchange.sh` — cross-agent collect
3. `scripts/memory_github_sync.sh` — push to GitHub

On failure → Telegram alert.

## Agents Using This Hub

- **Hermes** — primary agent on this machine (`~/.hermes/skills`)
- **Claude Code** — `~/.claude/skills`
- **Codex** — `~/.codex/skills`
- **Kimi** — `~/.kimi/skills`
- **Pi Agent** — `~/.pi/agent/skills`
- **Gemini / Antigravity** — `~/.gemini/antigravity/skills`
- **OpenClaw** — `~/.openclaw/workspace/skills`
- **Kilo** — `~/.kilo/skills`
- **Grok** — `~/.grok/skills`

See `AGENTS.md` §4 for the full per-agent path table and sync homes.
