# Hermes Memory — Mohamed Essa

> Central knowledge base for all AI agents working with Samaya Investment and Mohamed Essa.
> Share this repo across devices and agents for consistent context.

## Contents

| File | Description |
|------|-------------|
| `MEMORY.md` | Procedural memory — Odoo, projects, rules, pitfalls |
| `USER.md` | User profile — communication style, preferences |
| `PROJECTS.md` | All projects — Aseer Museum, Zamzam, Masjid Alnoor, Hera', El-Haramain, Tqanny |
| `ODOO.md` | Odoo Samaya connection guide + XML-RPC patterns + PO/task templates |
| `ODOO_CREDENTIALS.md` | Odoo credentials (API key) — **DO NOT COMMIT** |
| `CONTACTS.md` | Key people, roles, emails, Odoo IDs |
| `RULES.md` | Working rules, pitfalls, conventions |
| `scripts/memory_exchange.sh` | Sync script for multi-agent memory exchange |

## Quick Start

```bash
# Clone on any device
git clone https://github.com/sultandroid/hermes-memory.git ~/hermes-memory

# Set up Odoo credentials
mkdir -p ~/.config/samaya
cp ODOO_CREDENTIALS.md ~/.config/samaya/odoo.env
chmod 600 ~/.config/samaya/odoo.env

# Load into Hermes agent
hermes config set memory_file ~/hermes-memory/MEMORY.md
```

## Agents Using This Memory

- **Hermes** — primary agent on this machine
- **Claude Code** — via `.claude/CLAUDE.md` exchange section
- **Codex** — via `.codex/memories/unified_exchange_memory.md`
- **Kimi** — via `.kimi/memories/unified_exchange_memory.md`
- **Pi Agent** — via `.pi/agent/memory_collection.md`
- **Gemini** — via `.gemini/antigravity/memories/`
- **OpenClaw** — via `.openclaw/workspace/`
- **Kilo** — via `.kilo/memories/`
