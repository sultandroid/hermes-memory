# Cross-Platform Agent Skill Formats

Reference for converting Hermes skills to other AI coding agent platforms.

## Command Code (command-code)

**Skill directory:** `~/.commandcode/skills/<name>/SKILL.md`

Also auto-detects `.agents/skills/<name>/SKILL.md` and `.commandcode/skills/<name>/SKILL.md` in project directories.

**Format:**
```yaml
---
name: skill-name            # lowercase-hyphens
description: "One-line trigger + behavior"
category: optional-category  # optional
---
<markdown body>
```

- No `version`, `author`, `license`, or `metadata.hermes` fields needed.
- Description length limit is generous (same as Hermes ~1024 chars).
- Init: `command-code login` (OAuth, opens browser).
- Default model: `deepseek/deepseek-v4-flash` (same as Hermes).
- Model switch: `-m <model-name>` flag or `/model` slash command.

**Conversion approach (Hermes → command-code):**
1. Parse Hermes SKILL.md frontmatter (YAML between `---` markers).
2. Extract `name` and `description`.
3. Extract category from path (e.g., `software-development/test-driven-development/` → `software-development`).
4. Write simplified frontmatter (`name`, `description`, optional `category`) + body to `~/.commandcode/skills/<name>/SKILL.md`.

**Taste learning** (project/coding-style learning, separate from skills):
```
command-code taste learn .              # learn from current repo
command-code taste learn owner/repo     # learn from GitHub
command-code learn-taste                # learn from past sessions
```

**Auth:** `command-code login` — OAuth-based managed service. No BYO API keys.

## OpenCode (opencode CLI)

**Config:** `~/.opencode/` directory.
**Model selection:** via `--model` flag or environment variables (`OPENCODE_API_KEY`, `OPENCODE_GO_API_KEY`, `OPENCODE_ZEN_API_KEY`).

No native skill system — operates as a general coding agent.

## Claude Code (claude CLI)

**Config:** Project-level CLAUDE.md in repo root provides instructions/constraints.
**Model:** Claude models only (Anthropic-managed).
**Init:** `claude` (auto-auth via OAuth if configured).

No native skill system like Hermes/command-code. Relies on CLAUDE.md for project-specific context.

## Migration Pattern

When the user says "teach X all my skills":

1. Locate the target platform's skill/config directory.
2. Determine their skill format (SKILL.md with frontmatter is most common).
3. Batch-convert: iterate all Hermes skills, parse frontmatter, write to target format.
4. Account for differences: some platforms need `category` in frontmatter, others derive it from directory structure.
5. Verify with the platform's list command (e.g., `command-code skills list`).
