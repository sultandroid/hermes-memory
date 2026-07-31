# AGENTS.md — Wake-up Contract for Synced Agents

> **Read this file FIRST on every session wake.** It is the contract between you (the agent) and the hub (`hermes-memory` repo). The hub is **identity + reusable skills**; project repos hold **work**. Never mix them.

---

## 1. The Two-Layer Model

| Layer | What lives there | Who owns writes | Sync direction |
|---|---|---|---|
| **HUB** = `sultandroid/hermes-memory` | Who you are, how you work, your style, reusable skills, project *index* | Hub is authoritative for settled identity facts | Bidirectional: pull on wake, push back new general facts |
| **PROJECT** = per-project repo (e.g. `aseer-museum-pm`) | Project state, deliverables, scripts, registers, project-specific memory | Agent working on that project | Stays in project repo; never written back to hub |

**Rule:** If a fact is only true inside one project → project repo. If a fact is true across all projects (user style, tools, contacts) → hub.

---

## 2. Wake-up Checklist (every agent, every session)

Read in this order. Skip nothing.

1. **`USER.md`** — who is Eng. Mohamed Sultan, communication style, Egyptian background
2. **`RULES.md`** — golden rules + NEVER-DO list (no `rm -rf`, no auto-update sibling registers, English-only replies, etc.)
3. **`MEMORY.md`** — current procedural memory (Odoo patterns, project pointers, recurring pitfalls)
4. **`AGENTS.md`** (this file) — sync contract, project routing
5. **`PROJECTS.md`** — project index; find which project the user is asking about, then `cd` into its repo
6. **`CONTACTS.md`** — if the request mentions a person, look them up here first
7. **`ODOO.md`** — only if the request involves Odoo (projects, POs, tasks, timesheets)

After reading, **state a one-line summary** of who the user is and what project is in scope before doing work. If no project is in scope, ask which project — do not assume.

---

## 3. Project Routing

Every request from the user maps to exactly one of:

- **WORK** — Samaya / factory / technical office (default if user is at work, mentions MoC, ACE, CG, NRS, Aseer, etc.)
- **CONSULTING** — Amjad Consultancy or other external advisory (default if user mentions Amjad, submittal to non-Samaya client)
- **PERSONAL** — Sultan House, personal matters, anything non-work (default if user says "my house", "personal", or no work signal)

Then **route to the project repo**:

| Type | Project | Repo | Local path (default) |
|---|---|---|---|
| WORK | Aseer Museum | `sultandroid/aseer-museum-pm` | `~/projects/aseer-museum-pm` |
| WORK | Aseer Viz | `sultandroid/aseer-museum-viz` | `~/projects/aseer-museum-viz` |
| WORK | Aseer Weekly Dashboard | `sultandroid/aseer-weekly-dashboard` | `~/projects/aseer-weekly-dashboard` |
| WORK | Samaya Workspace | `sultandroid/samaya-workspace` | `~/projects/samaya-workspace` |
| CONSULTING | RCRC Exhibition | `sultandroid/RCRC-Exhibition-Proposal` | `~/projects/RCRC-Exhibition-Proposal` |
| PERSONAL | Sultan House | (not yet a repo — see `PROJECTS.md`) | — |

If the project has no repo yet but the work meets the "create a repo" rule (see §6), scaffold one from `templates/PROJECT_TEMPLATE/`.

---

## 4. Per-Agent Paths (skill/memory homes)

Each agent has its own skills directory. The sync engine (`scripts/memory_skills_exchange.sh`) reads from these.

| Agent | Skills home | Memory home | Notes |
|---|---|---|---|
| **Hermes** (this machine) | `~/.hermes/skills` | `~/.hermes/memories/MEMORY.md` | Hub sync = Hermes ↔ repo |
| **Claude Code** | `~/.claude/skills` | `~/.claude/CLAUDE.md` (memory section) | |
| **Codex** | `~/.codex/skills` | `~/.codex/memories/` | |
| **Kimi** | `~/.kimi/skills` | `~/.kimi/memories/` | |
| **Pi Agent** | `~/.pi/agent/skills` | `~/.pi/agent/memory_collection.md` | |
| **Gemini / Antigravity** | `~/.gemini/antigravity/skills` | `~/.gemini/antigravity/memories/` | |
| **OpenClaw** | `~/.openclaw/workspace/skills` | `~/.openclaw/workspace/` | |
| **Kilo** | `~/.kilo/skills` | `~/.kilo/memories/` | |
| **Grok** | `~/.grok/skills` | `~/.grok/memories/` | |

If your agent is not in this list, add it by editing this file (proposal PR to hub). The hub is the source of truth for the table.

---

## 5. Sync Contract (bidirectional)

### Pull (on wake)
1. `git pull --no-rebase` in `~/hermes-memory` (per `RULES.md` multi-agent rule)
2. Read top-level md files in the order in §2
3. Reload any skills under `skills/` whose `name` changed since your last sync (track via `.last_sync` in your agent home)

### Push back (write to hub)
**Only** push facts that are:
- **Cross-project** (true for Samaya + personal + consulting), OR
- **Reusable procedural** (a rule, a tool pattern, a pitfall), OR
- **New contact / role mapping**

**Never** push:
- Project-specific deliverables → goes to project repo
- Credentials, tokens, API keys → gitignored at root, also per `RULES.md`
- Unverified guesses → `RULES.md` says "source-verifiable"
- Excel files → `RULES.md` says never create new Excel

**When to push back:**
- On session end, if you learned something reusable
- On explicit user request: "remember this", "add to memory"
- Never mid-session chatter (avoids hub noise)

### Push format
Append a new line to the relevant file with a timestamp prefix:
```
[YYYY-MM-DD AGENT:hermes] New fact here.
```
Use `§` as section separator (matches existing `MEMORY.md` style).

### Conflict resolution
1. **Last-write-wins** for facts with explicit `[YYYY-MM-DD]` timestamps (newer wins)
2. **3-way merge** for unannotated edits (manual review via `sync_conflicts.md` queue)
3. **Never silent overwrite on conflict** — write to `sync_conflicts.md` and notify via `hermes_notify.sh telegram` for human review

---

## 6. When to Create a New Project Repo

A matter becomes a project repo when **any 2 of these** are true:

1. Work will span **3+ sessions** (you'll come back to it)
2. Has its own **deliverables, registers, scripts** (not just a chat thread)
3. Has **external stakeholders** (client, consultant, supplier, family member)
4. Has a **doc code prefix** (e.g. `MOC-MUS-ASE-*`, `ZAM-NWC-*`)
5. User explicitly says "let's set this up as a project"

**Scaffolding:** copy `templates/PROJECT_TEMPLATE/` → new GitHub repo → fill `PROJECTS.md` (this repo) with the new repo path + type → add to hub `PROJECTS.md` table.

**Naming convention:** `<client-or-topic>-<short-name>` in kebab-case, e.g. `aseer-museum-pm`, `samaya-workspace`. Private work: prefix `personal-` is optional.

---

## 7. Daily Sync Routine (the cron-driven path)

Runs daily at **10:00 Cairo / 08:00 UTC** via the user's local cron.

1. `scripts/hub_health_check.sh` — verify hub integrity, no drift, all agent paths exist
2. `scripts/memory_skills_exchange.sh` — bidirectional skill + memory collect across all 8 agents
3. `scripts/memory_github_sync.sh` — push consolidated `MEMORY.md` + `UNIFIED_MEMORY.md` + skills to GitHub
4. On any failure: `hermes_notify.sh telegram "Hub sync FAILED: <reason>"` → Telegram `Home` channel

Manual trigger: `bash ~/hermes-memory/scripts/daily_sync.sh` (alias for the above three).

---

## 8. Anti-Patterns (do not do these)

- ❌ **Don't re-ask the user for identity facts** (name, role, projects) — they're in `USER.md` and `PROJECTS.md`. Re-asking is the #1 user complaint per memory.
- ❌ **Don't load every skill for every task** — load only the ones whose `name` matches the task. `skill_view` first, judge relevance, then load.
- ❌ **Don't write project-specific memory to the hub** — it pollutes cross-project knowledge.
- ❌ **Don't `git push --force`** — the hub is multi-agent; you will clobber another agent's push.
- ❌ **Don't run `rm -rf`** anywhere — OneDrive propagates immediately per `RULES.md`.
- ❌ **Don't respond in Arabic** — user prefers English replies; summarize Arabic sources.
- ❌ **Don't cite unread sources** — `RULES.md` is explicit.
- ❌ **Don't create new Excel files** — only append rows to existing registers.

---

## 9. Quick Self-Test (run once on a new agent setup)

Before doing real work, run:

```bash
# 1. Hub reachable
cd ~/hermes-memory && git pull --no-rebase && echo "✓ hub reachable"

# 2. Top-level files present
for f in USER.md RULES.md MEMORY.md PROJECTS.md AGENTS.md CONTACTS.md ODOO.md; do
  test -f "$f" && echo "✓ $f" || echo "✗ MISSING: $f"
done

# 3. Project index has a row for the in-scope project
grep -i "<project-name>" PROJECTS.md && echo "✓ project routed" || echo "✗ project not in index — add to PROJECTS.md first"

# 4. Skills synced
ls ~/.hermes/skills/github/github-auth-detect/SKILL.md && echo "✓ skills loaded"

# 5. Health check passes
bash scripts/hub_health_check.sh
```

If any check fails, fix before proceeding. Never start work on a broken hub.

---

*Last updated: 2026-07-31 — by Hermes session on Mohamed Essa's instruction to formalize the two-layer model.*
