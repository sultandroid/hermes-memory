---
name: hermes-memory
description: Multi-agent memory management — GitHub-backed knowledge base shared across Hermes, Claude Code, Codex, Kimi, Pi, Gemini, OpenClaw, and Grok. Covers MEMORY.md/USER.md files, GitHub sync cron, and the memory_skills_exchange.sh script.
---

# Hermes Memory — Multi-Agent Knowledge Base

Manages the persistent knowledge base shared across all AI agents. Memory data lives in `~/.hermes/memories/` and syncs to GitHub for cross-device sharing.

## Files Managed

| File | Location | Purpose |
|------|----------|---------|
| `MEMORY.md` | `~/.hermes/memories/MEMORY.md` | Procedural facts — projects, Odoo, rules, pitfalls |
| `USER.md` | `~/.hermes/memories/USER.md` | User profile — identity, style, preferences |
| Lock files | `~/.hermes/memories/*.lock` | File locks (system-managed, ignore) |

## GitHub Sync

Repo: `github.com/sultandroid/hermes-memory`

### Cron Job (daily at 7 AM)

The cron job `Memory GitHub Sync` (job_id from `cronjob action='list'`) runs `memory_github_sync.sh` daily at 07:00 AM with `no_agent=True` — no LLM cost, pure script execution.

### Script: `memory_github_sync.sh`

Location: `~/.hermes/scripts/memory_github_sync.sh`

What it does:
1. `git pull --rebase` — avoid conflicts
2. Copies `MEMORY.md` + `USER.md` from `~/.hermes/memories/` into the repo
3. Runs `memory_skills_exchange.sh` — collects memory from all agents
4. Copies unified memory and full reference files
5. `git add -A && git commit -m "Auto-sync" && git push`

### Script: `memory_skills_exchange.sh`

Location: `~/.hermes/scripts/memory_skills_exchange.sh`

Full multi-agent sync covering: Hermes · Claude Code · Codex · Kimi · Pi Agent · Gemini · OpenClaw · Grok

Stages:
1. **Collect Skills** — rsyncs SKILL.md files from each agent into `~/.hermes/shared_exchange/skills/<agent>/`
2. **Build Skill Index** — generates SKILL_INDEX.md with all 615+ skills
3. **Collect Memory** — reads MEMORY.md / USER.md / CLAUDE.md from each agent into MEMORY_COLLECTION.md
4. **Generate Unified Memory** — extracts key facts into UNIFIED_MEMORY.md
5. **Distribute Back** — writes to each agent's memory location
6. **Summary** — skill counts per agent, memory size

Outputs:
- `~/.hermes/shared_exchange/UNIFIED_MEMORY.md`
- `~/.hermes/shared_exchange/MEMORY_COLLECTION.md`
- `~/.hermes/shared_exchange/SKILL_INDEX.md`

## Agents in the Exchange

| Agent | Memory Read From | Distribute To |
|-------|-----------------|---------------|
| Hermes | `~/.hermes/memories/MEMORY.md`, `USER.md` | Via shared_exchange |
| Claude Code | `~/.claude/CLAUDE.md` | `UNIFIED_EXCHANGE_MEMORY.md` (standalone file) |
| Codex | `~/.codex/memories/*.md` | `unified_exchange_memory.md` |
| Kimi | `~/.kimi/memories/*.md` | `unified_exchange_memory.md` |
| Pi Agent | `~/.pi/agent/AGENTS.md` | `memory_collection.md` |
| Gemini | `~/.gemini/GEMINI.md` | Memories + GEMINI.md |
| OpenClaw | `~/.openclaw/workspace/*.md` | Workspace copies |
| Grok | `~/.grok/memory/MEMORY.md` | `~/.grok/memory/UNIFIED_EXCHANGE_MEMORY.md` |

## Setup on a New Device

```bash
# 1. Clone the knowledge base
git clone https://github.com/sultandroid/hermes-memory.git ~/hermes-memory

# 2. Ingest reference files into Hermes
cp ~/hermes-memory/MEMORY.md ~/.hermes/memories/MEMORY.md
cp ~/hermes-memory/USER.md ~/.hermes/memories/USER.md
# Then READ and extract key facts from PROJECTS.md, CONTACTS.md, RULES.md, ODOO.md
# into memory via memory(action='add') — see "Reverse Sync" section above

# 3. (Optional) Set up Grok memory
# If Grok CLI is installed, enable memory in ~/.grok/config.toml:
#   [memory]
#   enabled = true
# Then write MEMORY.md: ~/.grok/memory/MEMORY.md
# The exchange script now auto-syncs to Grok. See references/grok-setup.md.

# 4. Set up Odoo credentials (if Odoo access needed)
mkdir -p ~/.config/samaya
# Create ~/.config/samaya/odoo.env with:
#   ODOO_URL=https://samayainv.odoo.com
#   ODOO_DB=peerless-tech-samaya-18-0-18447146
#   ODOO_USER=sultan@samayainvest.com
#   ODOO_API_KEY=***
chmod 600 ~/.config/samaya/odoo.env

# 5. Set up sync cron (on the device with all agents)
cp ~/hermes-memory/scripts/memory_exchange.sh ~/.hermes/scripts/memory_github_sync.sh
chmod +x ~/.hermes/scripts/memory_github_sync.sh
# Create cron job via cronjob(action='create', script='memory_github_sync.sh', schedule='0 7 * * *', no_agent=True)
```

## Reverse Sync (Repo → Agent Memory)

The repo holds more than just MEMORY.md/USER.md. Supplementary files (PROJECTS.md, CONTACTS.md, RULES.md, ODOO.md) contain structured reference data agents don't natively see. Ingest them manually when first setting up or after repo updates:

1. **List all files in repo** — `ls ~/hermes-memory/*.md` — don't assume only MEMORY.md/USER.md exist
2. **Read each supplementary file** — PROJECTS.md, CONTACTS.md, RULES.md, ODOO.md
3. **Extract key facts** — team assignments, doc codes, connection strings, rules, project structure
4. **Save to Hermes memory** using `memory(action='add')` with concise entries

### Common Supplementary Files

| File | Content | Ingest into memory |
|------|---------|-------------------|
| `PROJECTS.md` | Project list, doc codes, folder structure | Doc codes, project IDs |
| `CONTACTS.md` | Team members, roles, emails, assignment rules | Who does what |
| `RULES.md` | Golden rules, pitfalls, conventions, Excel style | Workflow rules |
| `ODOO.md` | Connection details, XML-RPC patterns, PO process | Connection info, critical pitfalls |

### ⚠️ Pitfall

**Don't ignore supplementary files.** The repo's MEMORY.md/USER.md only hold procedural facts. PROJECTS.md, CONTACTS.md, RULES.md, ODOO.md contain structured data (team roles, doc codes, connection strings, golden rules) that are invisible unless explicitly ingested. When handling a memory-sync request, read ALL `.md` files at the repo root — not just the two you expect.

## Memory Content Guidelines

Keep memory entries compact, factual, and focused on stable knowledge:
- **MEMORY.md** — project structures, Odoo IDs, team members, workflow rules, pitfalls
- **USER.md** — user identity, communication preferences, work style, pet peeves
- **Supplementary files** (PROJECTS.md, CONTACTS.md, RULES.md, ODOO.md) — structured reference data to ingest on first contact

Do NOT save to memory: task progress, session outcomes, PR numbers, commit SHAs, temporary TODO state.

## Verification

```bash
# Check last sync
cd ~/hermes-memory && git log --oneline -3

# Run sync manually
bash ~/.hermes/scripts/memory_github_sync.sh

# List cron jobs
cronjob(action='list')
```

Expected output from a healthy sync:
```
✅ Memory synced to GitHub
   <sha>..<sha>  main -> main
```

---

## Related Skills

| Skill | Relation |
|-------|----------|
| `odoo` | Odoo connection patterns referenced in MEMORY.md |
| `samaya-technical-office` | Project workflows referenced in MEMORY.md |
| `sub-labor-orchestrator` | References `memory-skills-exchange.md` in its references/ |

## Support Files

| File | Purpose |
|------|---------|
| `references/github-sync-setup.md` | Full guide: create repo, sync script, cron, clone to other devices |
| `references/grok-setup.md` | Adding Grok CLI as 9th exchange participant — config, MEMORY.md, verification |
