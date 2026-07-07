# Memory & Skills Exchange Cronjob

Multi-agent knowledge synchronization across all 8 labors: **Hermes, Pi, Claude Code, Codex, Kimi, Gemini, OpenClaw, Kilo**.

## Purpose
Ensures every agent has access to the consolidated memory and skills of all others. Runs as a silent watchdog cronjob (no LLM tokens consumed).

## How It Works

```
cronjob (every 6h) → no_agent=true → memory_skills_exchange.sh
```

The shell script (`~/.hermes/scripts/memory_skills_exchange.sh`) executes these steps:

### Step 1: Collect Skills
Rsyncs all `SKILL.md` files from each agent into `~/.hermes/shared_exchange/skills/<agent>/`:
- hermes → `~/.hermes/skills/`
- claude → `~/.claude/skills/`
- codex → `~/.codex/skills/`
- kimi → `~/.kimi/skills/`
- pi → `~/.pi/agent/skills/`
- gemini → `~/.gemini/antigravity/skills/`
- openclaw → `~/.openclaw/workspace/skills/`
- kilo → `~/.kilo/skills/`

### Step 2: Build Skill Index
Creates `SKILL_INDEX.md` with all 610+ skills listed by agent and category.

### Step 3: Collect Memory
Gathers all memory files from all agents into `MEMORY_COLLECTION.md` (~94KB):
- Hermes: MEMORY.md, USER.md
- Codex: memory_summary.md, raw_memories.md, MEMORY.md
- Kimi: MEMORY.md, USER.md, HERMES_SOUL.md
- Pi: AGENTS.md (the most comprehensive — already consolidated)
- Claude: CLAUDE.md (orchestration protocol)
- Gemini: GEMINI.md
- OpenClaw: MEMORY.md, USER.md, AGENTS.md
- Kilo: MEMORY.md, USER.md

### Step 4: Generate Unified Memory
Extracts key facts (user profile, critical rules, projects, people, tools, contracts, locations) into `UNIFIED_MEMORY.md` (~33KB).

### Step 5: Distribute Back
Pushes unified knowledge to each agent in its native format:
- Claude Code → appended as `## Unified Memory Exchange` section in `CLAUDE.md`
- Codex → `unified_exchange_memory.md` in `memories/`
- Kimi → `unified_exchange_memory.md` in `memories/`
- Pi → `memory_collection.md` in `agent/`
- Gemini → `unified_exchange_memory.md` in `antigravity/memories/` + copies Hermes MEMORY/USER.md to `antigravity/memories/` + overwrites `~/.gemini/GEMINI.md`
- OpenClaw → `unified_exchange_memory.md` in `workspace/` + copies Hermes MEMORY/USER.md to `workspace/`
- Kilo → `unified_exchange_memory.md` in `memories/` + copies Hermes MEMORY/USER.md to `memories/`
- Hermes → accessible at `~/.hermes/shared_exchange/`

## Cronjob Setup

```bash
cronjob create \
  --name "memory-skills-exchange" \
  --schedule "every 6h" \
  --no-agent true \
  --script "memory_skills_exchange.sh"
```

Schedule: Every 6 hours
no_agent=true: Zero LLM tokens consumed — pure bash script execution

## File Locations

| Resource | Path |
|----------|------|
| Script | `~/.hermes/scripts/memory_skills_exchange.sh` |
| Shared output | `~/.hermes/shared_exchange/` |
| Skill index | `~/.hermes/shared_exchange/SKILL_INDEX.md` |
| Memory collection | `~/.hermes/shared_exchange/MEMORY_COLLECTION.md` |
| Unified memory | `~/.hermes/shared_exchange/UNIFIED_MEMORY.md` |

## Active Learning Phase — Make Each Agent Learn

⚠️ The cron job (`no_agent=true`) only pushes files. It does NOT make agents actively process and internalize the new memory. After distribution, a leader agent MUST tell each agent to learn from the unified file.

**Why this is needed:** The cron job's distribution step writes files to each agent's memory directory, but no agent reads and processes them until explicitly told to. Without this step, agents continue using their old, stale memory until they happen to load the file in a future session.

**When to run this:** Manually or via a separate LLM cron job after the silent exchange cron completes.

### Per-Agent Learning Commands

**For Claude Code:**
```bash
cat ~/.hermes/shared_exchange/UNIFIED_MEMORY.md | claude -p "Read this unified memory file. Extract key facts you don't already know about Mohamed Essa (projects, rules, people, conventions, quirks). Append the most important new learnings to ~/.claude/CLAUDE.md using '# [topic]' format with bullet points. Be concise — deduplicate against what you already have." --allowedTools "Read,Edit,Write,Bash" --max-turns 8
```

**For Codex CLI:**
```bash
cd $(mktemp -d) && git init && git config user.email 'agent@hermes' && git config user.name 'Hermes Agent' && cp ~/.hermes/shared_exchange/UNIFIED_MEMORY.md ./unified_memory.md && git add -A && git commit -m 'init' && codex exec "Read unified_memory.md. Extract key facts about: (1) user profile & preferences, (2) critical rules, (3) active projects, (4) key people, (5) doc conventions, (6) environment quirks, (7) workbook cleanup patterns. Write a concise 30-40 bullet summary to ~/.codex/memory_summary_updated.md" --sandbox workspace-write
```

**For Hermes (yourself):** Read UNIFIED_MEMORY.md manually, then use `memory(action='replace'|'add')` to consolidate existing entries and add new facts.

**For Kimi:**
```bash
cat ~/.hermes/shared_exchange/UNIFIED_MEMORY.md | kimi --print --quiet 2>&1 | python3 -c "import re,sys;d=sys.stdin.read();m=re.findall(r\"text='([^']*)'\",d);print(m[-1] if m else d)"
```

**For Kilo (same pattern as Kimi):**
```bash
cat ~/.hermes/shared_exchange/UNIFIED_MEMORY.md | kilo --print --quiet 2>&1 | python3 -c "import re,sys;d=sys.stdin.read();m=re.findall(r\"text='([^']*)'\",d);print(m[-1] if m else d)"
```

**For Gemini:** Copy `UNIFIED_MEMORY.md` to `~/.gemini/GEMINI.md` (already done by the script, but Gemini doesn't read it until its next session — force a cognitive load manually if needed).

**For Pi Agent:** Copy to `~/.pi/agent/memory_collection.md` (already done by the script).

## Maintenance: Adding a New Agent

To add a new agent to the exchange, edit `~/.hermes/scripts/memory_skills_exchange.sh` in these locations:

1. **collect_skills** — add line after the openclaw row, e.g. `collect_skills "agentname" "$HOME/.agentname/skills"`
2. **Skill index loop** — add agent to the `for agent in ...` loop (line ~49)
3. **Memory collection** — add `append_memory` lines after the OpenClaw block
4. **Grep patterns** — add agent name to the Agents & Tools grep and agent dir to the Locations grep in Step 4
5. **Distribution** — add a copy block for unified memory + optional Hermes memory copies
6. **Summary loop** — add agent to the second `for agent in ...` loop (line ~232)
7. **Header comment** — update the Purpose line to include the new agent

**Pitfall: `set -euo pipefail`** — When `collect_skills` finds no source dir, it skips creating the shared output dir. The summary loop's `find "$SHARED_DIR/skills/$agent"` then fails because the dir doesn't exist, and with `set -e` the entire script exits with code 1. The fix: move `mkdir -p "$dst"` before the `if [ -d "$src" ]` check so the dir always exists. Already applied in the current script.

## GitHub Distribution Channel

For sharing unified memory **across devices** (not just local agents), use a GitHub-hosted knowledge base:

1. **Create a public/private repo** (e.g. `github.com/USER/hermes-memory`)
2. **Organize with class-level files:**
   - `MEMORY.md` — procedural facts (Odoo IDs, rules, pitfalls)
   - `USER.md` — user profile, communication preferences
   - `PROJECTS.md` — all project details
   - `ODOO.md` — Odoo connection patterns + templates
   - `CONTACTS.md` — team members, roles, emails, Odoo UIDs
   - `RULES.md` — golden rules, never-do items
   - `scripts/memory_exchange.sh` — the exchange script
3. **Clone on each device:** `git clone https://github.com/USER/hermes-memory.git`
4. **Load into each agent** via its native memory mechanism:
   - Hermes: copy `MEMORY.md` + `USER.md` to `~/.hermes/memories/`
   - Claude Code: append relevant sections to `CLAUDE.md`
   - Codex: copy unified files to `memories/unified_exchange_memory.md`
   - Other agents: copy to their respective memory paths
5. **Keep gitignored** credentials files (`ODOO_CREDENTIALS.md`) from ever being committed

### Example Repo Structure
```
hermes-memory/
├── README.md              # Overview + quick start
├── MEMORY.md              # Procedural: projects, Odoo, rules
├── USER.md                # User profile, style, preferences
├── PROJECTS.md            # All project details with tables
├── ODOO.md                # Connection, templates, pitfalls
├── CONTACTS.md            # Team with Odoo UIDs + roles
├── RULES.md               # Golden rules + never-do items
├── .gitignore             # Excludes credentials
└── scripts/
    └── memory_exchange.sh # Local multi-agent sync script
```

### Sync Workflow
1. On the **source device**, push updates to GitHub
2. On the **target device**, pull: `git pull`
3. Run the local exchange script to distribute to all local agents

This replaces ad-hoc file copying with version-controlled, cross-device knowledge distribution.

## When to Use

- **First session of the day** — run the exchange manually to get fresh unified memory: `bash ~/.hermes/scripts/memory_skills_exchange.sh`
- **After major project updates** — force sync so all agents learn about new contracts, people, rules
- **When switching agents** — the unified memory ensures Claude/Kimi/Codex/Pi all have the same context
- **When setting up a new device** — clone the GitHub repo and distribute to each agent

## Pitfalls

- **OneDrive lock** — files under `OneDrive-SAMAYAINVESTMENT/` may be inaccessible during sync if OneDrive holds APFS file leases. Script handles this by focusing on non-OneDrive paths.
- **Claude Code's CLAUDE.md** — if the exchange section grows too large, it may bloat Claude's context. Keep it to 80 lines of key facts.
- **Codex memory format** — Codex uses a git repo for memories. The unified file is added as a plain markdown, not committed. That's intentional — it's ephemeral cache, not version-controlled history.
- **set -euo pipefail exit 1** — Adding a new agent without creating its skills dir crashes the summary loop. The current script handles this (mkdir before the if check), but maintainers need to know.
- **Kimi timeout** — Kimi's `--quiet` flag times out on long prompts. For learning from UNIFIED_MEMORY.md, use `--print` (without `--quiet`) and parse the TextPart output.
