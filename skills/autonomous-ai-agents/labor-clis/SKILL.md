---
name: labor-clis
description: "Use local CLI labor agents (Claude Code, Kimi, Gemini, Codex, Command Code, Pi Agent) as sub-agents via terminal — not delegate_task ACP. Direct CLI invocation."
version: 1.4.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Coding-Agent, Subagent, CLI, Claude, Kimi, Gemini]
    related_skills: [claude-code, sub-labor-orchestrator]
---

# Labor CLIs — Direct Terminal Invocation

## 🔴 MANDATORY: Delegate Heavy Work to Labors

**The user's explicit rule:** ALWAYS delegate substantive tasks to Claude, Kimi, or Codex. Never do heavy work yourself. Reasons:
1. **Protect your context quota** — heavy sessions (OCR, SVG gen, bulk edits, complex calculations, file searches) consume 50K+ tokens in your context window. Labors absorb this.
2. **The user has an army** — Claude Code, Kimi, and Codex are all installed and available. Using them is the expected workflow.
3. **Name the labor** — always state which labor performed each task in your response (e.g. "Done via Kimi", "Claude Code fixed").

**🔴 MANDATORY: Rewrite every user prompt through Codex first.** Before executing ANY user instruction, run it through Codex for rewriting. This is a hard user requirement across all sessions. See "Codex CLI → Prompt Rewriting Pattern" below for the exact command.

**When to use each:**
- **Kimi** — fast print-mode tasks: OCR, file scanning, simple HTML gen, verification passes. Use `echo "task" | kimi --print --quiet`
- **Claude Code** — complex reasoning: SVG charts, deep analysis, multi-file operations, stakeholder reports. Use `claude -p "task" --max-turns N`
- **Codex** — quality controller + **prompt rewriter**: audit another labor's output, sandboxed verification, AND rewrite user prompts before executing. Use `codex exec "task" --sandbox workspace-write`
- **Fugu (codex-fugu)** — Fugu-powered QA audits, SVG checks, sandboxed verification, structured document analysis. Model: fugu (Sakana AI), Codex v0.142.0. Use `codex-fugu exec "task" --sandbox workspace-write`

**When NOT to delegate:**
- Simple single tool calls (`ls`, `grep`, `read_file`)
- Clarifying with the user
- Quick verification checks (<3 tool calls)
- Any task where delegation overhead exceeds the work itself

## Standard Invocation

## Available Labors

| Labor | Path | Print Mode | Verified |
|-------|------|------------|----------|
| **Pi Agent (Commander)** | `~/.npm-global/bin/pi` | ✅ `pi -p "task"` | ✅ Commander — delegates to others |
| **Claude Code** | `~/.npm-global/bin/claude` | ✅ `claude -p "task" --max-turns N` | ✅ Works |
| **Codex** | `~/.npm-global/bin/codex` | ✅ `codex exec "task" --sandbox workspace-write` | ✅ Works (pty=true) |
| **Fugu (codex-fugu)** | `~/.local/bin/codex-fugu` | ✅ `codex-fugu exec "task" --sandbox workspace-write` | ✅ Fugu-powered (Sakana AI) |
| **OpenCode** | `~/.opencode/bin/opencode` | ✅ `opencode run -m "provider/model" -- "msg"` | ✅ Multi-provider |
| **Command Code** | `~/.npm-global/bin/command-code` | ✅ `command-code -p "task"` | ⚠️ Managed service (OAuth) |
| **Gemini** | `/opt/homebrew/bin/gemini` | ✅ `gemini -p "task" --yolo` | ⚠️ Hangs on directory list |
| **OpenClaw** | `/opt/homebrew/bin/openclaw` | ✅ `openclaw agent --local --message "task"` | ✅ Works |

## Codex CLI (Quality Controller + Mandatory Prompt Rewriter)

Codex is the **Quality Controller** gate and **mandatory prompt rewriter** — ALWAYS rewrite user prompts through Codex before executing (**user standing order**). Run the original prompt through Codex first, then act on the rewritten version.

### Prompt Rewriting Pattern

```bash
# Rewrite user prompt before executing
codex exec --skip-git-repo-check "Rewrite this user request to be specific, actionable steps for an AI executing it. Original request: <user_prompt>" 2>&1

# Must be run from a directory; --skip-git-repo-check avoids needing an actual git repo
# The rewritten version gives clear numbered steps that the agent should follow precisely
```

### Sandboxed Execution

```bash
# Git repo required — create scratch repo for standalone tasks
cd $(mktemp -d) && git init && echo "# scratch" > README.md && git add . && git commit -m "init"
codex exec "task description" --sandbox workspace-write

# Non-git directory (fast check): use --skip-git-repo-check
codex exec --skip-git-repo-check "quick analysis" --sandbox workspace-write

# Background mode (long tasks)
terminal(command="codex exec '...' --sandbox workspace-write", workdir="/tmp", background=true, pty=true, notify_on_complete=true)

# YOLO mode (fastest, no sandbox — use for trusted tasks only)
codex exec "task" --yolo
```

Key limitations:
- Must run inside a git repo (refuses otherwise) — unless `--skip-git-repo-check` is used
- Requires pty=true in terminal calls (no ACP/stdio support)
- `--full-auto` deprecated → use `--sandbox workspace-write` instead
- Model: gpt-5.5 (OpenAI), reasoning: medium

## Claude Code (Preferred)

```bash
# Print mode — preferred for automation
claude -p "task description" --max-turns 10 --allowedTools "Read,Edit,Bash" --output-format json

# With workdir
claude -p "Fix the auth bug" --max-turns 5 --allowedTools "Read,Edit" --work-dir /path/to/project

# Session continuation
claude -p "Continue the refactor" --continue --max-turns 5

# With model selection
claude -p "task" --model sonnet --max-turns 3
```

### Authentication Troubleshooting (401 / expired token)

Claude Code OAuth tokens expire (~4-5 day lifetime). When `claude -p` returns `401 Invalid authentication credentials`:

1. **Check expiry** — inspect `~/.claude/.credentials.json`. The `expiresAt` field is a millisecond epoch timestamp. Compare `date -r $((expiresAt/1000))` to confirm expiration.
2. **Remove stale credentials** — backup and delete the file so the login flow starts fresh:
   ```bash
   cp ~/.claude/.credentials.json{,.bak} && rm ~/.claude/.credentials.json
   ```
3. **Run `claude auth login`** (not `claude login` — `auth login` is the correct subcommand). This opens the user's default browser for Anthropic OAuth:
   ```bash
   claude auth login
   ```
   - If running headless or the browser didn't open, the terminal prints a URL to visit manually
   - The command blocks waiting for the OAuth callback — after signing in the browser, control returns and auth succeeds
4. **Verify** — `claude -p "hello"` should respond normally instead of the 401 error

**Note:** `claude login` (without `auth`) enters an interactive session with prompts (trust-folder, browser-tools) rather than pure login flow. Use `claude auth login` for the headless authentication path.

## Kimi CLI (Print Mode via Stdin)

**Key flags discovered in practice:**
- `--max-steps-per-turn N` (not `--max-steps`) — limits the number of steps per turn
- `--print` — auto-approves tool calls
- `--quiet` — suppresses session resume message
- `-y` or `--yes` — auto-approves all actions (combine with `--print` for fully automated runs)

Kimi's `-p` mode requires stdin pipe for the prompt — do NOT use a positional argument with `-p`:

```bash
# ✅ CORRECT — pipe input to stdin
echo "List all Python files in src/" | kimi --print --quiet

# ✅ With workdir
echo "Fix the auth bug" | kimi --print --quiet --work-dir /path/to/project

# ✅ Pipe extracted file content for summarization
pdftotext -layout "file.pdf" - | kimi --print -y --max-steps-per-turn 5

# ❌ WRONG — will fail
kimi -p "task"
kimi --print "task"
```

## OneDrive Sandbox Access Restriction

OneDrive files carry `com.apple.macl` extended attributes that block sandboxed labors (Fugu, Codex) from reading/writing them via terminal or Python. The `cp` command, Python `open()`, and any sandboxed process all fail with `Operation not permitted`. **Always stage OneDrive files to `/tmp/` before delegating to sandboxed labors.**

**🔴 CRITICAL PITFALL — Never use `mv` to reorganize OneDrive folders from terminal.** Moving files with `mv` inside OneDrive directories triggers macOS TCC (Transparency, Consent, and Control) sync locks that make ALL files in those directories inaccessible for extended periods. Consequences:
- Terminal `ls`, `cp`, `find`, `read_file` all return `Operation not permitted`
- File listings become inconsistent — `ls` may show different file counts on each invocation
- Cloud-only files get stuck in a half-synced state (files appear with odd permissions or empty)
- The lock persists until OneDrive cloud sync completes, which can take minutes to hours
- **Any file moved out of its original OneDrive location by `mv` may need to be re-downloaded**

Do NOT restructure OneDrive project folders via command line. If reorganization is needed, do it through Finder (drag-and-drop) or OneDrive web UI. If you already did this, the fix is `cp` via Finder osascript (see below), not `rmdir` or `rm`.

**Pitfall: OneDrive `ls` output is inconsistent.** The `ls` command may return different file counts on successive invocations because OneDrive cloud sync processes changes incrementally. A file that appears in one `ls` call may disappear in the next. Do NOT assume files are deleted just because they don't appear in an `ls` listing. Check `du -sh` for disk usage as a secondary signal, and prefer osascript Finder for reliable enumeration. A file that appears in one `ls` call may disappear in the next. Do NOT assume files are deleted just because they don't appear in an `ls` listing. Check `du -sh` for disk usage as a secondary signal, and prefer osascript Finder for reliable enumeration.

### Reliable staging via Finder (osascript)

**The only reliable method that works first time** is `osascript` via Finder, which bypasses the terminal TCC sandbox:

```bash
osascript -e 'tell application "Finder" to duplicate file POSIX file "/Users/me/Library/CloudStorage/OneDrive/.../file.png" to POSIX file "/private/tmp/" with replacing'
```

After this, the staged file at `/private/tmp/filename` is accessible to all terminal and sandboxed processes.

### Methods that DO NOT work (do not waste tool calls trying them)

| Method | Failure mode |
|--------|-------------|
| `cp source /tmp/` | `Operation not permitted` |
| `python3 -c "open(path).read()"` | `Operation not permitted` |
| `mdfind -name file` | Returns nothing (Spotlight blocked) |
| `ls path` | `Operation not permitted` |
| `read_file` (Hermes tool) | Returns empty content or "File not found" |

### When to use which staging method

| File Type | Method | Why |
|-----------|--------|-----|
| Text files only | Hermes `read_file` chunk-read + `write_file` | Faster but limited to ~100K chars |
| Binary files, images, .docx, .xlsx | osascript Finder copy | Only method that works for non-text |

### Staging patterns

```bash
# Print mode with auto-approve
gemini -p "task" --yolo --approval-mode yolo

# With model
gemini -p "task" --model gemini-2.5-flash

# Work directory
cd /path/to/project && gemini -p "task" --skip-trust
```

## Command Code

**Managed service** (OAuth-based, no BYO providers). Auth via `command-code login` opens a browser for OAuth. Default model is `deepseek/deepseek-v4-flash`.

```bash
# Print mode
command-code -p "your task" [--max-turns N]

# Model selection
command-code -m deepseek/deepseek-v4-flash     # (default) fast hybrid-attention
command-code -m claude-sonnet-4-6              # Anthropic Claude
command-code -m kimi-k2.7-code                 # Kimi coding model
command-code -m gpt-5.5                        # OpenAI
command-code -m google/gemini-3.5-flash        # Google

# Interactive session
command-code "fix the login bug"

# Continue last session
command-code -c

# Available model families (--list-models)
# Open Source: deepseek, moonshotai/Kimi, Qwen, GLM, MiniMax, xiaomi, stepfun, nvidia
# Anthropic: claude-sonnet-4-6, claude-fable-5, claude-opus-4-8, claude-haiku-4-5
# OpenAI: gpt-5.5, gpt-5.4, gpt-5.3-codex, gpt-5.4-mini
# Google: gemini-3.5-flash, gemini-3.1-flash-lite
```

**Key difference from other labors:** command-code routes all models through its own backend — you don't supply your own API keys. Auth is via `command-code login` (OAuth), not environment variables. The tradeoff: simpler setup, but you're tied to their credit/plan system.

**Limitations:** Docs site at commandcode.ai has several 404s (Available Models, Pricing, Provider API pages are missing). v0.40.0 installed at `~/.npm-global/bin/command-code` (also aliased as `commandcode`).

## Pi Agent (Commander Role)

Pi Agent (`@earendil-works/pi-coding-agent`) is a local coding agent — **always use it as commander/orchestrator** that delegates to other labor CLIs (Claude Code, Codex, Kimi), NOT as a simple worker.

See `references/fugu-html-qa-pattern.md` for a reusable HTML QA script (SVG count, base64 validation, element breakdown) that Fugu can run autonomously.
See `references/arabic-rtl-proposal-generation.md` for generating large Arabic RTL technical proposals via delegate_task (proven on 35-section, 215KB documents).

```bash
# Print mode — preferred for automation
pi -p "task description"

# With provider/model
pi --provider google --model gemini-2.5-flash -p "task"

# Interactive mode
pi "task description"

# Print mode with session naming
pi -p "task" --name "Audit session"

# List options
pi --help
```

Default provider is `google`. Supports model switching at runtime (`Ctrl+P`). Version 0.78.0 installed at `~/.npm-global/bin/pi`.

Note: Pi Agent has a separate Python package `pi` (v0.1.2) at `~/.venvs/pi/bin/pi` which is a different tool and is broken on Python 3.14 — ignore it.

## OpenAI CLI (API Mode)

```bash
# Simple API call
openai api chat.completions.create -m gpt-4o -m "Hello"

# Not agentic — better for one-shot API tasks
```

## Fugu (codex-fugu) — Fugu-Powered Labor

`codex-fugu` is a Codex CLI variant routed through the **Fugu model** (Sakana AI, Codex v0.142.0). Installed at `~/.local/bin/codex-fugu`. Use for QA audits, SVG checks, structured document verification, and code review where Fugu's reasoning depth adds value. Fugu can autonomously write and run Python checker scripts, parse HTML, validate base64, and produce structured JSON output.

```bash
# Sandboxed execution (requires git repo)
cd $(mktemp -d) && git init && echo "# fugu task" > README.md && git add . && git commit -m "init"
codex-fugu exec "task description" --sandbox workspace-write

# Background mode for long tasks
terminal(command="codex-fugu exec 'task' --sandbox workspace-write", workdir="/tmp", background=true, pty=true, notify_on_complete=true)
```

**Limitations:** 
- Same as Codex — requires git repo, pty=true, no ACP/stdio support
- **OneDrive files must be staged to `/tmp` first** (see OneDrive Sandbox Access below)
- **Fugu free-tier rate limits** — returns `ERROR: You've hit your usage limit. Try again at 8:13 AM.` when the free queue is exhausted. This is a hard cap — retrying within the cooldown window is pointless. Switch to another labor (delegate_task, Kimi, direct Python). Rate limit resets are typically daily. Prefer shorter, single-shot prompts to conserve Fugu's free quota for critical passes (QA audits, SVG validation).
- **Sandbox cannot write to `~` (homedir)** — outputs go to the sandbox workdir (`/private/tmp/fugu_work/` by default). If the prompt requests saving to `~/some/path/`, Fugu will fail with "filesystem sandbox prevented writing". Always stage outputs to workdir first, then copy.

## Orchestration Pattern

When you need to delegate work to a labor:

1. **Choose the right tool** for the task
2. **Set workdir** so the labor operates on the correct project
3. **Set --max-turns** to prevent runaway loops
4. **Set --allowedTools** to scope permissions
5. **Report back** to user when done, mentioning which labor was used

For simple CLI tasks:
```
You → Hermes (orchestrator) → Claude Code (-p print mode) → Report result back
You → Hermes (orchestrator) → Kimi (stdin pipe) → Report result back
```

**For tasks needing web research:** See the Research Phase section in the `sub-labor-orchestrator` skill. Quick reference:
- Fast lookup (1-2 questions) → Kimi (SearchWeb built-in, ~2s startup)
- Parallel multi-aspect → Hermes delegate_task with toolsets=["web"]
<!-- DUPLICATE — consolidated OneDrive section below (after Fugu and Labor Fallback Pattern) -->

### Labor Fallback Pattern — When All Labors Fail

Both Claude Code and Kimi can fail in different ways:
- **Claude Code**: Auth error 401 (API key expired, socket closed). The `claude -p` call returns immediately with `api_error_status: 401`. The JSON response contains `"is_error":true,"api_error_status":401,"result":"Failed to authenticate..."`.
- **Kimi**: Timeout on long/complex tasks (>300s shell timeout). Kimi's `--print` mode runs but the shell times out when the combined ReadFile + response cycle exceeds 300s. This happens with files >30KB, 30+ slide decks, or multi-stage prompts.
- **Codex**: Requires pty=true AND a git repo. Cannot run complex PPTX/Excel operations that need openpyxl or other non-stdlib packages.
- **delegate_task**: The most reliable fallback for complex generation tasks. Uses Hermes subprocess transport (not Claude API). Handles large HTML generation, multi-file operations, and tasks requiring web research.

**Fallback chain for PPTX/HTML/Excel/file-generation tasks:**

```
Try Claude Code CLI → (401) → Try Kimi CLI → (timeout) → delegate_task → (600s timeout) → Direct Python script
```

**Delegate_task pattern for large document generation (proven):**
For generating large structured documents (35+ sections, 200K+ bytes), delegate_task with toolsets=["terminal","file"] is the most reliable approach. Pass the full specification in the `goal` and all source knowledge in `context`. This worked when CLI labors hit rate limits or timeouts:
- Generated a 35-section, 215 KB Arabic RTL technical proposal in ~10 min
- Handled 1.7M input tokens, 75K output tokens across 22 tool calls
- Result: fully structured HTML with compliance matrix, diagrams, and section cross-references
- Session ID persisted for continuation if needed

For Arabic RTL documents specifically: include the exact required structure with Arabic headings in the `goal`, pass all source knowledge (gallery names, materials, company stats, project data) in `context`, and explicitly state the Definition of Done checklist. The subagent will produce a complete self-contained HTML file with proper `dir="rtl"`, Arabic fonts, and RTL-aware CSS.

```python
delegate_task(goal="full spec with required structure, format, and rules",
              context="all source knowledge, gallery names, materials, company data",
              toolsets=["terminal", "file"])
```

**When delegate_task fails** (exceeds 600s timeout): fall back to Direct Python — write the content generation script and run via terminal(). This works for known programmatic tasks (openpyxl, python-pptx, Pillow) but not for natural-language document generation.

Implementation pattern:
```
# Attempt 1: Claude Code CLI
result = terminal("claude -p 'task...' --allowedTools Read,Edit,Write,Bash --max-turns 40 --output-format json", timeout=300)
if 401 error in result:
    failed.append("Claude Code (401 auth)")
    # Attempt 2: Kimi
    result = terminal("cat << 'EOF' | kimi --print 2>&1\ntask...\nEOF", timeout=300)
    if timeout:
        failed.append("Kimi (timeout)")
        # Attempt 3: delegate_task (for HTML gen, analysis, document creation)
        delegate_task(goal="task...", context="...", toolsets=["terminal", "file"])
        # OR if delegate_task also fails:
        # Attempt 4: Direct Python (for known programmatic tasks)
        write_file("script.py", "python code...")
        terminal("python3 script.py", timeout=120)
```

**When to skip labors entirely:** If the task is a known class of programmatic operation (openpyxl formula fix, python-pptx restyle, regex bulk rename, Pillow image processing) that requires specific Python libraries, skip the labor CLI and write the Python script directly. Labors are for research, analysis, design decisions, and natural-language document generation — not for running `pip install openpyxl; python3 script.py`.

**Pitfall: Do NOT retry the same labor with the same prompt after it fails — change approach or change labor. Claude 401 auth won't resolve on retry. Kimi timeout won't resolve with a longer timeout on the same task — the issue is prompt complexity, not wall time.

**Pitfall: OneDrive file staging — skip cp/Python, go directly to osascript.** Do NOT waste tool calls trying `cp`, `python3 -c "open()"`, or `mdfind` to copy OneDrive files to `/tmp`. The macOS TCC sandbox blocks ALL terminal-based operations on OneDrive files with `Operation not permitted`. The only reliable method that works first time is osascript via Finder:
```bash
osascript -e 'tell application "Finder" to duplicate file POSIX file "SOURCE" to POSIX file "/private/tmp/" with replacing'
```

**Pitfall: Fugu (Sakana AI) free-tier rate limits.** Fugu returns `ERROR: You've hit your usage limit. Try again at 8:13 AM.` when the free queue is exhausted. This is a hard cap — retrying within the cooldown window is pointless. Switch to another labor (delegate_task, Kimi, direct Python) and log fugu as unavailable until the named time. Rate limit resets are typically daily (e.g. 8:13 AM based on first usage that day). Prefer shorter, single-shot prompts to conserve Fugu's free quota for critical passes (QA audits, SVG validation).

**Pitfall:** If ALL labors fail (Claude 401 + Kimi timeout + delegate_task fails), report the complete failure chain to the user rather than fabricating a result. Say "all 3 labors failed: X, Y, Z" and ask how they want to proceed.

Each labor stores memory and skills in its own format and location. A cronjob (`memory-skills-exchange`) syncs knowledge across all agents every 6 hours.

### Storage Locations

| Labor | Memory Location | Skills Location |
|-------|----------------|-----------------|
| **Hermes** | `~/.hermes/memories/MEMORY.md` + `USER.md` | `~/.hermes/skills/` |
| **Claude Code** | `~/.claude/CLAUDE.md` + `history.jsonl` | `~/.claude/skills/` |
| **Codex** | `~/.codex/memories/` (markdown files) | `~/.codex/skills/` |
| **Kimi** | `~/.kimi/memories/MEMORY.md` + `USER.md` | `~/.kimi/skills/` |
| **Pi Agent** | `~/.pi/agent/AGENTS.md` (consolidated) | `~/.pi/agent/skills/` |
| **OpenClaw** | `~/.openclaw/workspace/MEMORY.md` + `USER.md` | `~/.openclaw/workspace/skills/` |

### Exchange Mechanism (`memory-skills-exchange` cronjob)

Runs every 6h via Hermes cron (watchdog/no-agent mode, no tokens consumed). Script: `~/.hermes/scripts/memory_skills_exchange.sh`.

**Pipeline:**
1. **Collect skills** — rsync each agent's skills dir into `~/.hermes/shared_exchange/skills/<agent>/`
2. **Build SKILL_INDEX.md** — consolidated catalog of all 500+ skills across all agents
3. **Collect memory** — merge MEMORY.md / USER.md / AGENTS.md / CLAUDE.md from all agents
4. **Generate UNIFIED_MEMORY.md** — extract key facts (user profile, projects, rules, people, tools, contracts, locations)
5. **Distribute** — write unified memory to each agent's native format

**Output files under `~/.hermes/shared_exchange/`:**
- `SKILL_INDEX.md` — full skill catalog with descriptions per agent
- `UNIFIED_MEMORY.md` — cross-agent consolidated knowledge
- `skills/<agent>/` — raw skill files per labor

### How Each Agent Receives the Sync

| Labor | What Gets Written |
|-------|------------------|
| Claude Code | `## Unified Memory Exchange` section appended to `CLAUDE.md` |
| Codex | `unified_exchange_memory.md` in `memories/` |
| Kimi | `unified_exchange_memory.md` in `memories/` |
| Pi Agent | `memory_collection.md` in `agent/` |
| Hermes | Reads from `shared_exchange/` directly |
| OpenClaw | `unified_exchange_memory.md` + `HERMES_MEMORY.md` + `HERMES_USER.md` in `workspace/` |

### Querying Another Agent's Skills

To discover what skills another labor has:
```bash
# Full index
cat ~/.hermes/shared_exchange/SKILL_INDEX.md

# Skills from a specific agent
ls ~/.hermes/shared_exchange/skills/claude/
ls ~/.hermes/shared_exchange/skills/codex/

# Unified memory
head -100 ~/.hermes/shared_exchange/UNIFIED_MEMORY.md
```

### Pi Agent's AGENTS.md — Best Single Source

Pi Agent's `AGENTS.md` (~20KB) is the most comprehensive consolidated memory. It already contains merged knowledge from all other agents: user profile, project data, critical safety rules, key people, and orchestration workflows. When any agent needs a complete picture of this user's setup, Pi's AGENTS.md is the richest single source.

### OpenClaw — Knowledge Exchange Partner

OpenClaw is installed and running as a separate agent gateway with its own workspace. Skills and memory were migrated from Hermes to OpenClaw in this session. See `references/openclaw-setup.md` for install, setup flow, and known pitfalls (Telegram token capture bug, migration `baseUrl` cascading error).

## Cleanup

Always clean up tmux sessions when done:
```bash
tmux kill-session -t <session-name> 2>/dev/null
```