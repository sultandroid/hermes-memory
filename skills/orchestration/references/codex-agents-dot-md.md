# `.codex/AGENTS.md` — Machine-Level Multi-Agent Protocol

Found at `~/.codex/AGENTS.md` on this machine (2026-06-25). Defines the same multi-agent orchestration protocol as the `orchestration` Hermes skill — leader decomposes orders, delegates to other agents, integrates results, has another verify.

## Key difference from Hermes `orchestration` skill

The AGENTS.md file uses a **different sub-agent invocation pattern** — it lists all five agents (pi, claude, codex, kimi, hermes) and their headless commands, which is a subset of what Hermes skills cover. The Hermes `orchestration` skill is the authoritative, more detailed version.

## Relevance

This file exists because another agent (Codex) installed it via its own skill system. All agents on this machine should follow the Hermes `orchestration` skill (more complete), but be aware that this file exists and may be the reference Codex uses internally.

## Path

```
~/.codex/AGENTS.md
```
