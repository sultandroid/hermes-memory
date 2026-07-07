# Agent Memory & Skills Storage — Full Reference

Discovered 2026-06-02 while building the memory-skills-exchange cronjob.

## Pi Agent

- Config: `~/.pi/agent/` (240B auth.json, 414B models.json, 351B settings.json)
- AGENTS.md: `~/.pi/agent/AGENTS.md` (~20KB) — consolidated memory from all agents
- SYSTEM.md: `~/.pi/agent/SYSTEM.md` (1.9KB)
- Skills: `~/.pi/agent/skills/` (34 entries, 110 SKILL.md)
- Sessions: `~/.pi/agent/sessions/` (11 sessions)
- Orchestration protocol embedded in AGENTS.md — Pi is the Commander

## Claude Code

- Config dir: `~/.claude/`
- CLAUDE.md: `~/.claude/CLAUDE.md` (4KB) — memory + orchestration protocol
- History: `~/.claude/history.jsonl` (717KB) — session logs
- Skills: `~/.claude/skills/` (112 SKILL.md)
- Projects: `~/.claude/projects/`
- Tasks: `~/.claude/tasks/`
- Plans: `~/.claude/plans/`
- Settings: `~/.claude/settings.json` (149B) + `settings.local.json`
- Backups: `~/.claude/backups/`
- Claude app bundle: `~/Library/Application Support/Claude/claude-code/2.1.149/claude.app`

## Codex

- Config dir: `~/.codex/`
- Memories: `~/.codex/memories/` — markdown files including:
  - `memory_summary.md` (2.5KB) — user profile, preferences, tips
  - `raw_memories.md` (17KB) — raw session memory dumps
  - `phase2_workspace_diff.md` (36KB) — consolidation diff log
  - `rollout_summaries/` — per-session summaries
- SQLite: `memories_1.sqlite` (80KB) — structured memory store
- Skills: `~/.codex/skills/` (29 entries, 114 SKILL.md)
- Rules: `~/.codex/rules/`
- AGENTS.md: `~/.codex/AGENTS.md` (4KB) — orchestration protocol
- Config: `~/.codex/config.toml`
- Auth: `~/.codex/auth.json`
- Goals: `~/.codex/goals_1.sqlite` (24KB)
- Session state: `state_5.sqlite` (266KB)
- Models cache: `models_cache.json` (194KB)
- History: `history.jsonl` (6.5KB)

## Kimi

- Config dir: `~/.kimi/`
- Memories: `~/.kimi/memories/` — 4 files:
  - `MEMORY.md` (2KB) — project memories (Zamzam, Aseer, registers)
  - `USER.md` (1KB) — user profile
  - `HERMES_SOUL.md` — persona definition
  - `HERMES_CONFIG.yaml` (14KB) — agent configuration
- Skills: `~/.kimi/skills/` (110 SKILL.md)
- Config: `~/.kimi/config.toml` (1.6KB)
- Sessions: `~/.kimi/sessions/` (21 sessions)
- User history: `~/.kimi/user-history/`
- Plans: `~/.kimi/plans/`
- Credentials: `~/.kimi/credentials/`
- Session log: `~/.kimi/kimi.json` (3.6KB)

## Hermes

- Config dir: `~/.hermes/`
- Memories: `~/.hermes/memories/MEMORY.md` + `USER.md` + lock files
- Skills: `~/.hermes/skills/` (categorized in subdirs, 113 SKILL.md)
- Scripts: `~/.hermes/scripts/` (runnable automation scripts)
- Shared exchange: `~/.hermes/shared_exchange/` (cross-agent sync hub)

## Cross-Agent Sync Summary

The `memory-skills-exchange` cronjob (every 6h) syncs:
- 559 total skills across 5 agents
- 36KB merged memory collection
- 31KB unified memory with extracted key facts
