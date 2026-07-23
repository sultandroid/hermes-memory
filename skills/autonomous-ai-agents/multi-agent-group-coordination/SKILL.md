---
name: multi-agent-group-coordination
description: "Coordinate with peer autonomous agents in shared Telegram groups — silent observer rules, correct @mention handles, knowledge sync patterns, and non-responsive agent handling."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [multi-agent, group-chat, telegram, coordination, peer-agents]
    related_skills: [sub-labor-orchestrator, labor-clis]
---

# Multi-Agent Group Chat Coordination

## Context

When Hermes operates in a Telegram group alongside other autonomous agents (SulKimiClaw_bot, SultanMacBook_Bot, etc.), special coordination rules apply. These are **peer agents**, not sub-labors — they have their own knowledge bases, reply rules, and capabilities.

## Rules

### 1. Reply Rule (User-Configurable)

The user sets the reply rule explicitly. Two modes:

| Mode | Behaviour | When |
|------|-----------|------|
| **Silent observer** | Read all, never reply unless @mentioned | Default — user may set this initially |
| **Reply to all** | Reply to every message in the group | User may change this later |

**Pitfall:** The user can change this rule mid-conversation. When they say "reply to all messages not only mentioned", switch immediately. Update memory. Do not keep citing the old rule.

### 2. Correct @Mention Handles

Each agent has a specific Telegram handle. Using the wrong handle means the agent won't see the message. Verify handles before mentioning:

| Agent | Correct Handle |
|-------|---------------|
| SulKimiClaw | @SulKimiClaw_bot |
| SultanMacBook | @SultanMacBook_Bot |

**Pitfall:** The user corrected this — @SulKimiClaw (without _bot suffix) does NOT reach the agent. Always use the full handle.

### 3. Knowledge Sync Pattern

When the user says "talk to [agent], know it, discuss the project":

1. **Prepare your knowledge summary** — compact bullet list of key facts (client, contractor, team, status, risks)
2. **@mention the agent** with the correct handle
3. **Lead with your summary** — state what you know first, then ask what they know
4. **Offer to fill gaps** — "I can fill gaps and correct anything that's off"
5. **If no response, try again** — the agent may not be active, may need a different trigger, or may not be configured to reply
6. **Report back to the user** — what the other agent knew, what was wrong, what was missing

### 4. Knowledge Sync Message Template

```
@AgentHandle — I'm [Name], [Role] for the [Project]. I've been asked to sync with you.

**What I know about the project:**
- [Key fact 1]
- [Key fact 2]
- [Key fact 3]
- [Key fact 4]

**What do you know?** Let me know your understanding of the project — team, scope, status, key risks. I can fill gaps and correct anything that's off.
```

### 5. When an Agent Doesn't Respond

Possible reasons:
- **Not active** — the bot may not be running or logged into the group
- **Not configured to reply** — may need a specific trigger or @mention format
- **No access** — may not have permission to read the group
- **Wrong handle** — verify the correct @handle

Action: try again with the correct @mention. If still no response, report to the user.

### 6. User's Reply Rule for Hermes

The user set this rule explicitly: "read all messages, never reply unless explicitly @mentioned. Silent observer by default." This is stored in memory and applies to ALL group interactions.

### 7. Distinction from Sub-Labor Orchestration

This skill covers **peer agents** in a shared chat — they are not under your control, you cannot delegate to them, and they may or may not respond. This is fundamentally different from `sub-labor-orchestrator` which covers delegating tasks to Claude Code, Kimi, and Codex as worker sub-labors.

**When to load this skill:** You are in a Telegram group with other autonomous agents and need to coordinate, sync knowledge, or understand the group's interaction rules.

**When NOT to load this skill:** You are delegating a task to a sub-labor (use `sub-labor-orchestrator` or `labor-clis` instead).
