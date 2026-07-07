---
name: codex
description: "Quality Controller + Order Rewriter + coding agent. Audits ALL Claude Code output, rewrites user orders into structured specs, and can execute coding tasks and research/document-creation workflows."
version: 2.2.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Quality-Controller, Codex, OpenAI, Code-Review, QC-Gate, HTML-Audit]
    related_skills: [claude-code, hermes-agent, sub-labor-orchestrator]
---

# Codex CLI — Quality Controller & Order Rewriter

Codex CLI is OpenAI's autonomous coding agent CLI, now serving as the **Quality Controller** in the labor org chart. Three roles:

1. **Order Rewriter** — rewrites/structures ALL user orders before any labor executes them
2. **QC Gate** — audits ALL Claude Code output before delivery
3. **Coding** — can also execute coding tasks directly

## 🔴 Standing Rule: Order Rewriter Is Always On

**ALL user prompts MUST be rewritten/restructured before any execution begins.** This is a standing requirement, not an optional convenience.

### Two Modes of Rewriting

**Mode A — Codex CLI Rewrite (preferred for Samaya sessions):** When the user has stated or implied "rewrite my prompt using codex", or when the session involves complex multi-step work:

1. Run the user's prompt through Codex CLI for rewriting:
   ```bash
   codex exec --skip-git-repo-check "Rewrite this user request to be specific, actionable steps for an AI executing it. Original request: [paste user's prompt]" 
   ```
2. Use the rewritten output as your execution plan
3. Present the Codex-rewritten spec to the user before executing

**Mode B — Manual Rewrite (fallback):** When Codex CLI is unavailable or the task is trivial (1-2 tool calls):

1. **Rewrite first, execute second** — before delegating, reading files, or running any tool, restate the user's request as a structured spec:
   - Restate the goal in clear terms
   - Break into steps with acceptance criteria
   - Identify which labor (if any) should execute each step
   - Note any research needs, context, or file paths
2. **Show the rewritten spec to the user** as your first response — this confirms understanding before any time is spent executing
3. **Only proceed to execution** after presenting the rewritten spec
4. **No exceptions** — even for "simple" requests. A 1-line prompt still gets a 2-3 line restatement.

**Why this is mandatory:** The user explicitly requires all prompts to be rewritten/structured. Skipping this step is a workflow violation. The rewritten spec is your first response, not something you plan to do next.

### Known Pitfall: `--skip-git-repo-check` Required

When running `codex exec` outside a git repo (e.g., inside a OneDrive path), Codex refuses with:
```
Not inside a trusted directory and --skip-git-repo-check was not specified.
```
Always pass `--skip-git-repo-check` when running Codex outside a git repo. Without it, Codex won't execute.

## Labor Position
```
Hermes Agent (Leader)
  │
  ├── Codex CLI (QC Gate + Order Rewriter) ← YOU ARE HERE
  │
  ├── Claude Code (Main Labor — executes after Codex rewrites)
  │
  └── Kimi (Monkey Work)
```

## QC Role: HTML Audit Checklist

When auditing Claude Code's HTML output, Codex MUST check all 10 quality standards:

| # | Check | What to verify |
|---|-------|----------------|
| 1 | **DOCTYPE** | `<!DOCTYPE html>` present at start |
| 2 | **Tag balance** | All divs, tables, bodies, html properly opened and closed. Use Python regex: count `<div[>\s]` vs `</div>` — diff should be 0 |
| 3 | **No line-number contamination** | First line must NOT start with spaces+digits+pipe like `     1|<!DOCTYPE...` |
| 4 | **Closing tags** | `</html>`, `</body>` must exist at end of file |
| 5 | **CSS @page** | Must have `@page{size:A4 portrait;margin:0}` for print layout |
| 6 | **Sheet sizing** | `.sheet{width:210mm;min-height:297mm;overflow:hidden;page-break-after:always}` |
| 7 | **Logo paths** | Must use relative `../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/` prefix |
| 8 | **Fonts** | Calibri/Carlito loaded from Google Fonts (`fonts.googleapis.com`) |
| 9 | **Div balance per sheet** | Count open/close divs inside each `.sheet` — imbalance clips content |
| 10 | **Content overflow** | `overflow:hidden` clips content that exceeds 297mm per sheet — verify sheet fits |

## 🔴 Order Rewriting Pattern (Mandatory — First Step of Every Task)

**Before ANY execution — including reading files or running tools — the leader agent MUST rewrite the user's prompt into a structured spec.** This applies whether the leader executes directly or delegates:

1. **Restate** the goal — confirm you understood what the user wants
2. **Clarify** ambiguous items — note assumptions, missing context, implied scope
3. **Break into steps** — structured sub-tasks with acceptance criteria
4. **Identify labor** — which sub-labor (if any) should execute each step
5. **Present the spec** to the user in chat as your first response
6. **Only execute** after the user has seen the restated spec

The spec can be a short formatted section or a full structured document depending on task complexity. For simple tasks (1-2 tool calls), a few bullet points suffice. For complex work, write a full spec with context, deliverables, and quality criteria.

## QC Role: Scope Audit Pattern

For contract scope verification (proven 2026-05-29):
1. Read the deliverable tree/report HTML
2. Extract all deliverables with their descriptions
3. Cross-reference against contract docs (ER clauses, SOW sections, BOQ pricing sections)
4. Classify each as: In Scope / Excluded / Deferred / Clarification Required
5. Produce: Executive Summary + Per-Category Matrix + Gap Register + Risk & Action Log

## Research & Document Creation Workflow

Codex can execute research-heavy tasks combining **web search** with structured document creation. Proven workflow (31 May 2026 — vendor evaluation meeting prep):

### Workflow Steps

1. **Create a scratch git repo** (Codex requires one):
   ```bash
   cd $(mktemp -d) && git init
   ```

2. **Set git config locally** (if global config is absent — Codex will fail to commit without this):
   ```bash
   git config user.email "user@example.com"
   git config user.name "Your Name"
   ```

3. **Add reference files** the agent should read:
   ```bash
   cp /path/to/input.pdf ./ && pdftotext input.pdf reference.txt
   # or copy any supporting documents
   ```

4. **Commit the reference data**:
   ```bash
   git add -A && git commit -m "init"
   ```

5. **Launch Codex with a structured spec** — write a detailed prompt with:
   - **Context paragraph** — project, audience, who the output is for
   - **Explicit sections** with bullet points for what each section must contain
   - **Research requirements** — what to search for online (prices, alternatives, specs)
   - **Output file name** — tell Codex where to save the result
   - **Quality constraints** — cite sources, don't make up prices, write for the audience
   
   ```bash
   codex exec "Long structured prompt..." --sandbox workspace-write
   ```

6. **Monitor in background** (for long tasks):
   ```bash
   terminal(command="codex exec '...' --sandbox workspace-write", workdir="/tmp/repo", background=true, pty=true, notify_on_complete=true)
   # Monitor with process(action="poll") or process(action="wait")
   ```

7. **Copy output to target location** after completion:
   ```bash
   cp /tmp/repo/Output_File.md ~/Desktop/Output_File.md
   ```

### Structured Prompt Template

For research/document-creation tasks, write the prompt as a detailed outline:

```
Create [document type] for [purpose]. Save as '[filename]'.

## Context
[Background, who needs it, what decision it supports]

## The document MUST cover:

### Section 1
- [sub-point A]
- [sub-point B]

### Section 2
- [sub-point A]
...

## Important
- Research actual data online — don't fabricate
- Cite sources with URLs
- Write for [audience description]
- Add a table of contents
```

This pattern works for: vendor evaluations, market research, project proposals, technical comparison documents, feasibility studies, and procurement analysis.

> **Template available:** `references/research-document-prompt-template.md` — reusable structured prompt skeleton with placeholders. Copy and adapt for each new task.

### Known Pitfall: Git Config

Codex (`git commit`) fails with `fatal: unable to auto-detect email address` if `user.email` and `user.name` are not set. Always set them locally before committing in the scratch repo. Do NOT assume global config exists.

### Known Pitfall: Initial Commit Required

Codex refuses to run (`"Not inside a trusted directory"`) even in a `git init`'d repo **if there are no commits**. Always run `git add -A && git commit -m "init"` after `git init` — not just `git init` alone. The `git init` + first commit must happen before `codex exec`, not inside the Codex prompt.

This is why the combined one-liner works:
```bash
cd $(mktemp -d) && git init && git config user.email "agent@hermes" && git config user.name "Hermes Agent" && git add -A && git commit -m "init" && codex exec "..." --sandbox workspace-write
```
While the partial form fails:
```bash
cd $(mktemp -d) && git init && codex exec "..."  # FAILS — no commit
```

### Known Pitfall: Codex Full-Component Rewrites Break Existing Layouts

Codex may introduce CSS Grid (`gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 220px), 1fr))'`) or complex layout properties when rewriting entire components. These can break:
- **Page layout**: Grid can overflow containers, misalign sections, or add unwanted scroll
- **Desktop appearance**: A component that looked fine in flex may break in grid
- **Mobile appearance**: Complex grid formulas may not fall back gracefully

**Prevention:**
1. After any Codex component rewrite, always verify the FULL page layout — not just the changed component
2. Prefer simple flexbox layouts over CSS Grid for this project — the user values predictable rendering over layout novelty
3. If Codex introduces grid, test on both desktop and mobile before deploying
4. When in doubt, specify "use simple flexbox, no CSS Grid" in the Codex prompt for layout changes
5. After delegation, visually scroll through all sections of the page — not just the footer/component that was changed — to catch overflow or alignment issues

Codex may need multiple web search + write cycles. The `--sandbox workspace-write` mode auto-approves file writes but not web search results — Codex handles web search autonomously. Trust the process and monitor with `process(action="wait")`.

### Known Pitfall: UI Interactions Broken After CSS Rewrite

When Codex rewrites CSS (especially for mobile responsiveness), it may comprehensively replace an `@media` block. This can **silently break** interactive UI elements:

- **Close buttons** can end up with wrong `position`/`z-index` stacking, making them invisible or unclickable
- **Event handlers** on buttons can be shadowed by newly-positioned backdrop/overlay elements that intercept clicks
- **Stacking contexts** can change (e.g. `display: block` instead of `display: flex` on a modal), causing sibling elements to overlap

**Prevention:**
1. After ANY CSS change from Codex, verify interactive elements in the browser:
   - Is the element visible at the expected position?
   - Does clicking it fire the expected handler (close modal, toggle state)?
   - Is there any higher-z-index element intercepting the click?
2. Check that the CSS change didn't remove or alter `position`, `z-index`, or `pointer-events` on interactive elements
3. Test on both desktop viewport AND mobile viewport (≤768px)
4. If Codex replaced an entire media query block, diff the old vs new CSS and manually check each property on interactive elements

**Specific mobile modal pitfalls:**
- `display: block` on a modal that was `display: flex` can change how the backdrop and content stack
- Removing `position: relative` on a container breaks children with `position: absolute`
- `env(safe-area-inset-*)` functions can cause unexpected positioning on non-Apple devices
- `z-index` values must account for ALL sibling elements, including backdrop overlays

### Known Pitfall: Arabic/Unicode Folder Names on macOS

When Codex writes Python rename scripts that deal with Arabic folder names, the script may silently skip folders because macOS/OneDrive uses non-breaking space (U+00A0 = 0xC2 0xA0) characters that look like regular spaces. See `references/arabic-folder-unicode-pitfall.md` for detection, reproduction, and fix patterns.

### Known Pitfall: Sub-Agent JSON Key Casing Mismatch

When delegating data-analysis tasks to sub-agents (e.g., "study these JSON files and propose field mappings"), sub-agents read the raw schedule files on disk. But the app may use a **normalized runtime data file** (e.g., `materials.json`) where key casing differs from the raw schedule files.

**Example from Aseer project:**
- Raw schedule JSON has `Description` (capital D), `Supplier` (capital S), `Susbtrate` (typo, capital S)
- Runtime `materials.json` normalizes to: `description` (lowercase), `supplier` (lowercase), `substrate` (lowercase, typo fixed)

**Prevention:**
1. When the task involves mapping JSON keys to code, explicitly tell sub-agents to verify against the **runtime data file**, not just the raw source schedules
2. After sub-agents deliver proposals, run a quick validation against the actual data: `python3 -c "import json; d=json.load(open('data.json')); print(list(d[0].keys()))"`
3. Fix any casing mismatches before building

### Known Practice: Multi-Sub-Agent Reconciliation

When parallel sub-agents all modify the same code section (e.g., different entries in the same TypeScript constant):

1. **One sub-agent may already have applied its changes** to the file if it had write access. Always read the current state before applying other agents' proposals.
2. **Compare proposals** for overlapping sections — if two agents proposed different designs for the same section, pick the better one.
3. **Apply changes incrementally** using patch() per section, not write_file() on the whole file — this preserves improvements already applied and only fixes what is still stale.
4. **Verify against actual runtime data** after reconciliation (see pitfall above).

## Excel Cost Data Restructuring Workflow

A common Codex task is restructuring raw accounting/costing Excel files into standardized, classified, formula-based workbooks. This workflow applies to client/vendor accounting data (Ibrahim Shaban files), factory cost records (FCA), and cross-project reallocation.

### Standard File Structure (target output)

Each output file must have these 6 sections in a SINGLE reference document:

| # | Section | Content |
|---|---------|---------|
| 1 | Accounting Statement | Items grouped by category, each with seq#, original#, invoice/doc#, category, amount, item type. Formula-based subtotals per category. Grand total. |
| 2 | Moved Out | Items transferred to other projects — full original Arabic description, invoice#, amount, destination, split method, amount kept (if partial) |
| 3 | Received From | Items received from other projects — full description, source project, amount, reason |
| 4 | Item Type Summary | SUMIF breakdown: Construction / Equipment / Operations totals |
| 5 | Factory Cost | Raw Materials + Factory Labor — ONE LINE each (details in Remarks column) |
| 6 | Final Total | Accounting Total + Factory Cost + Supervision 10% = Grand Total. ALL values are FORMULAS. |

**Critical rules:**
- **Right-to-Left**: Set `ws.sheet_view.rightToLeft = True` for Arabic documents
- **Formula-based only**: All totals/subtotals/supervision must be `=SUM()`, `=cell*0.1`, etc. No hardcoded numbers.
- **Full descriptions**: Moved items must use the EXACT original Arabic description from the source statement, not a summary
- **Invoice numbers**: Extract and display invoice/document numbers from descriptions
- **Original item #**: Preserve the original item number for cross-referencing

### Format Standards
- Navy headers: fill `#1E293B`, white bold font
- Number format: `#,##0.00`
- Bilingual headers: Arabic primary / English in parentheses
- Category headers: bold with `▶` prefix, subtotal rows bold
- All totals must be Excel formulas (`=SUM()`, `=cell*0.1`), not plain numbers

### Classification Rules (Arabic keywords)

| Type | Keywords | Label |
|------|----------|-------|
| **Construction** | خشب, نجارة, حديد, دهان, جبس, أرضيات, رخام, ميكانيكا, تكييف, سباكة, مكافحة حريق, عمال, توريد, تركيب, زجاج, اكريليك, بروفايل, صاج, سيراميك | إنشاءات (Construction) |
| **Equipment** | شاشة, كيبل, ليد, لمبة, جهاز, ماكينة, كمبيوتر, طابعة, كاميرا, بروجكتر, راوتر, مكيف, ثلاجة, خلاط, نظام, صوت, سماعات, ميزان | معدات (Equipment) |
| **Operations** | سفر, تذكرة, فندق, سكن, نقل, شحن, مواصلات, اكل, عشاء, طعام, ضيافة, قرطاسية, طباعة, بنك, تأمين, رسوم, صيانة, دومين, مصروفات, ماء, مبيد, تراخيص, ايجار, هاتف, انترنت, دعاية, اعلان | تشغيلية (Operations) |

### Cross-Project Reallocation Pattern
When items are recorded under the wrong project:
1. Identify which store/project each line belongs to (check descriptions for other store names)
2. Apply area-based split when costs are shared between stores with known areas
3. Apply equal split when no area data available or item not area-dependent (signage, cashier devices)
4. Document reallocation in BOTH source file (as outgoing) and target file (as incoming)
5. Update factory cost & supervision accordingly

### Equipment/Operations Separation
After all items are classified, **separate non-construction items from the main sheet**:
1. Remove Equipment and Operations rows from the main data
2. Create separate sheets `معدات (Equipment)` and `تشغيلية (Operations)` with those items
3. Keep the separated sheets intact for future independent invoicing
4. Recalculate main sheet totals as Construction-only
5. Add note: "Non-construction items moved to separate sheets for independent invoicing"

### See Reference
`references/excel-cost-restructuring-reference.md` for the complete step-by-step guide with examples from this session.

### See Reference
`references/aseer-schedule-key-casing.md` for key casing mappings between raw schedule files and runtime materials.json in the Aseer Museum project.

## Invocation

### One-Shot Task (via terminal)
```bash
codex exec "task description" --sandbox workspace-write
```

**Note:** `--full-auto` is deprecated — use `--sandbox workspace-write` instead.

### QC Audit (HTML verification with Python validation scripts)
```bash
codex exec "Read file X.html and create a QA report listing all HTML quality issues: div balance, missing tags, doctype, font loading, @page CSS, sheet sizing, logo paths, line number contamination" --sandbox workspace-write
```

### Must run inside a git repo
```bash
cd $(mktemp -d) && git init && git config user.email "agent@hermes" && git config user.name "Hermes Agent" && git add -A && git commit -m "init" && codex exec "task" --sandbox workspace-write
```

### Background mode (long tasks)
```bash
terminal(command="codex exec '...' --sandbox workspace-write", workdir="/path", background=true, pty=true, notify_on_complete=true)
```

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- **Must run inside a git repository** — Codex refuses to run outside one
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo with at least one commit):
```
terminal(command="cd $(mktemp -d) && git init && git config user.email 'agent@hermes' && git config user.name 'Hermes Agent' && touch .gitkeep && git add -A && git commit -m 'init' && codex exec 'Build a snake game in Python' --sandbox workspace-write", pty=true)
```

## Background Mode (Long Tasks)

```bash
# Start in background with PTY
terminal(command="codex exec 'Refactor the auth module' --sandbox workspace-write", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--sandbox workspace-write` | Auto-approves file changes in workspace (replaces deprecated `--full-auto`) |
| `--sandbox read` | Read-only sandbox (no file writes allowed) |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
