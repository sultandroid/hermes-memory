# Grok CLI — Memory Setup for Multi-Agent Sync

Adds Grok (xAI CLI, `~/.grok/`) as an exchange participant in the multi-agent memory exchange.

## Enable Memory in Grok

```toml
# ~/.grok/config.toml
[memory]
enabled = true
```

## Write Initial MEMORY.md

Create `~/.grok/memory/MEMORY.md` with the structured knowledge from the shared repo. Include:
- Team contacts and assignment rules (from CONTACTS.md)
- Golden rules and conventions (from RULES.md)
- Project doc codes and structure (from PROJECTS.md)
- Odoo connection details and patterns (from ODOO.md)
- User identity and preferences (from USER.md)
- OneDrive/file workflow rules

Format as a single markdown file with `##` section headings. Grok's watcher auto-indexes external edits on next memory search.

## Verify

```bash
ls ~/.grok/memory/
# Should show: MEMORY.md  UNIFIED_EXCHANGE_MEMORY.md  HERMES_MEMORY.md  HERMES_USER.md
grok inspect  # Confirm memory enabled
```

## What the Exchange Script Does

The `memory_skills_exchange.sh` script now:
1. Collects Grok's skills from `~/.grok/skills/`
2. Reads Grok's `~/.grok/memory/MEMORY.md` into the shared collection
3. Distributes unified memory to `~/.grok/memory/UNIFIED_EXCHANGE_MEMORY.md`
4. Also copies Hermes MEMORY.md → `~/.grok/memory/HERMES_MEMORY.md` and USER.md → `~/.grok/memory/HERMES_USER.md`

## Pitfalls

- Grok's memory is **experimental** — ensure the `[memory] enabled = true` config survives any `grok --no-memory` flag or `GROK_MEMORY=0` env var
- Grok uses `~/.grok/memory/MEMORY.md` as the global memory file — one file for cross-project facts
- The file watcher reindexes on external edits, but changes only surface on the **next memory search**, not immediately
- No workspace/project-specific memory setup needed for Grok — the unified exchange file covers all context
