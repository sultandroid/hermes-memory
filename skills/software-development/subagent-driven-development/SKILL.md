---
name: subagent-driven-development
description: "Execute plans via delegate_task subagents (2-stage review)."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [writing-plans, requesting-code-review, test-driven-development, hermes-quality-assurance]
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching fresh subagents per task with systematic two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use

Use this skill when:
- You have an implementation plan (from writing-plans skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Automated review process catches issues early
- Consistent quality checks across all tasks
- Subagents can ask questions before starting work

## The Process

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent

Use `delegate_task` with complete context:

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### Step 2: Dispatch Spec Compliance Reviewer

After the implementer completes, verify against the original spec:

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer

After spec compliance passes:

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review

After ALL tasks are complete, dispatch a final integration reviewer:

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. Verify and Commit

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## Task Granularity

**Each task = 2-5 minutes of focused work.**

**Too big:**
- "Implement user authentication system"

**Right size:**
- "Create User model with email and password fields"
- "Add password hashing function"
- "Create login endpoint"
- "Add JWT token generation"
- "Create registration endpoint"

## Red Flags — Never Do These

- **Deploy a sub-agent's CSS/UI changes without visual verification**: Sub-agents often introduce CSS that works in isolation but breaks the live page due to cascade specificity, z-index stacking, or mobile breakpoint overrides. After a sub-agent modifies CSS, (a) check the deployed CSS `@media` query rules aren't overridden by base class declarations that load later, (b) verify the page renders correctly in both desktop and mobile viewport, (c) check that `position: fixed/absolute` elements with `z-index` actually stack above their intended layer. A passing `tsc` does NOT mean the CSS is correct.
- **Accept sub-agent performance recommendations without verifying actual impact**: A sub-agent may suggest 6+ issues ranked by severity. Apply only the top 2-3 HIGH severity fixes, then re-test before applying the rest. The marginal gain from MEDIUM/LOW fixes may not justify the code churn.
- Start implementation without a plan
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed critical/important issues
- Dispatch multiple implementation subagents for tasks that touch the same files
- Make subagent read the plan file (provide full text in context instead)
- Skip scene-setting context (subagent needs to understand where the task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues → implementer fixes → review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is PASS** (wrong order)
- Move to next task while either review has open issues
- **Trust a subagent's patch on a multi-page file without full-document verification**: When a subagent patches one page of a large HTML file (e.g. redesigning a timeline on page 15 of 18), verify the ENTIRE document still works — not just the edited section. An injected `<style>` block with bare selectors (`.boq`, `.pay`, `.page`) can leak across all pages. Pages that were within A4 bounds before can overflow after CSS changes. Always check: page count, section balance, footer numbers, page heights, and CSS selector scoping. See `hermes-quality-assurance` skill for the full QA checklist.
- **Invent or extrapolate data that doesn't exist in the specified source files**: When a user provides source data (Excel, JSON, PPTX, CSV), only use the fields and values that actually exist in those files. Never create synthetic thumbnails, swatches, placeholder images, or derived data that wasn't in the source. If a materials list has no image field, don't generate one from PPTX slide images or color swatches. The user will call this out as fabricating data. If enrichment is needed, ask first. See `references/data-integrity-pitfalls.md`.
- **Trust a subagent's merge of data files without verification**: When a subagent is asked to "rebuild materials.json with new data" (e.g., adding AV equipment or lighting schedules), their merge script can **corrupt existing records** by overwriting `schedule_key`, `source`, or `code` for ALL previously-extracted materials. This manifests as user saying "info card changed" or "known codes don't work anymore." **Prevention:** Back up the data file before delegating. After the subagent completes, verify that known codes from each schedule type still exist with their correct `schedule_key`. Restore from backup and re-merge manually if corrupted. Always instruct subagents to APPEND new items, never wholesale replace. See `references/mass-data-extraction-from-excel-schedule-files.md` for the verification script.

## Handling Issues

### Delegation Times Out on Large Files

**Symptom:** `delegate_task` returns `timed out after 600.0s` — the subagent made many API calls but couldn't finish.

**Root cause:** Files >150KB or >2500 lines of content overwhelm the subagent's context window. The subagent spends all its budget reading the file and has none left to write it back.

**Prevention (check file size before delegating):**
```bash
wc -c file.html   # If >150KB, do NOT delegate the whole file
```
```python
# If >3000 lines, split the work
MAX_SAFE_HTML_SIZE = 150_000  # bytes
```

**Workarounds (in order of preference):**
1. **CSS-only redesign** — replace the `<style>` block, keep HTML content untouched. Much smaller input.
2. **Phase by page group** — delegate 4-5 pages at a time, not all 18.
3. **Shell + content split** — create structural shell (small, <50KB), then fill content in separate delegations.
4. **Use patch() directly** instead of delegate_task for targeted edits on large files — patching specific strings is much cheaper than reading the whole file.
5. **Extract to reference script** — for extraction/analysis tasks, have the subagent write a Python script (no HTML) that does the work, then run the script yourself.

**Recovery:** When a large-file delegation times out, the file may be partially modified (inconsistent state). Always restore from the known-good backup (`cp /tmp/surge-full/index.html` or the working source) before retrying with a smaller scope.

### Delegation Fails with HTTP 404 or Connection Refused

**Symptom:** `delegate_task` returns `API call failed after 3 retries: HTTP 404 — Not Found | opencode` or similar transport errors.

**Root causes (check in order):**

1. **Wrong transport mode for the current provider.** The session's provider (e.g. `opencode-go`) doesn't support the default Hermes subprocess transport for `delegate_task`.
   - Fix A (per-call): pass a model with a working API-backed provider:
     ```python
     delegate_task(goal="...", model={"model": "anthropic/claude-sonnet-4", "provider": "anthropic"})
     ```
   - Fix B (persistent): set in `~/.hermes/config.yaml`:
     ```yaml
     delegation:
       provider: openrouter   # any provider with a working API key
     ```

2. **ACP transport explicitly requested but unavailable.** If passing `acp_command: 'copilot'`, the GitHub Copilot CLI must be installed and reachable.
   - Verify: `which copilot` — if not found, ACP is unavailable
   - Fix: Remove `acp_command` and use Fix A or B above, or install the Copilot CLI

3. **No delegation provider configured.** If delegation still fails, set a default in config.yaml so every subagent launch has a known-good transport.

**Recovery:** Retry the delegation with the correct provider. Do not manually implement the subagent's work in the controller session — fix the transport and retry.

### 🔴 CRITICAL: File Safety — Never Let Subagents Write to Source Files

When delegating a task that involves READING and ANALYZING a source file (audit, review, diff, count), the subagent MUST NEVER write to that same file.

**Why:** The subagent has full file system access. A task like "audit the TOC of this HTML" can accidentally overwrite the 289KB HTML file with a 2KB test snippet. This has happened and caused total data loss.

**Rules for delegation context:**
- Always include: `"🔴 CRITICAL: This is a READ-ONLY task. Do NOT write to the source files under any circumstances. If you need to save findings, write to /tmp/ or create a separate .md file."`
- After the subagent returns, verify the source file was not modified: `ls -la source_file` to check size/timestamp hasn't changed unexpectedly
- If the subagent needed to create artifacts (audit report, analysis), explicitly tell it to write to a SEPARATE file in `/tmp/` — never inline results into the source

**When file modification IS the goal (edits, fixes):** Prefer `patch()` for targeted edits on large files rather than delegating the whole file. If you must delegate, provide the exact page/line ranges and tell the subagent to use `patch()` only, not `write_file()`. After the subagent returns, verify the file size hasn't changed drastically (e.g., 289KB → 31KB is a red flag).

**Recovery after accidental overwrite:**
1. Check if OneDrive version history has the previous version (OneDrive cloud storage keeps ~30 days of versions)
2. Check for `.bak` files or git history in the directory
3. Restore from the nearest backup version (older revision HTML files in the same directory)
4. Re-apply the session's changes on top of the restored file

### Orchestrator: Analysis + QC Pattern

When you need to analyze data AND get quality control, use an orchestrator subagent (with delegation enabled) that spawns analysis and QC children:

```python
delegate_task(
    goal="Analyze all schedule files and recommend field groups",
    context="...detailed context...",
    role="orchestrator",  # allows nested delegation
    toolsets=["terminal", "file", "delegation"]
)
```

The orchestrator can then delegate to:
- **Kimi** or an analysis subagent — *"Study the data, find all available fields"*
- **Codex** or a QC subagent — *"Review the recommendations for correctness"*

This keeps the parent's context clean while allowing multi-agent collaboration on complex analytical tasks. The orchestrator returns only the conclusion, not raw data dumps.

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

### If Reviewer Finds Issues

- Implementer subagent (or a new one) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent Fails a Task

- Dispatch a new fix subagent with specific instructions about what went wrong
- Don't try to fix manually in the controller session (context pollution)

## Efficiency Notes

**Why fresh subagent per task:**
- Prevents context pollution from accumulated state
- Each subagent gets clean, focused context
- No confusion from prior tasks' code or reasoning

**Why two-stage review:**
- Spec review catches under/over-building early
- Quality review ensures the implementation is well-built
- Catches issues before they compound across tasks

**Cost trade-off:**
- More subagent invocations (implementer + 2 reviewers per task)
- But catches issues early (cheaper than debugging compounded problems later)

## Integration with Other Skills

### With writing-plans

This skill EXECUTES plans created by the writing-plans skill:
1. User requirements → writing-plans → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development

Implementer subagents should follow TDD:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging

If a subagent encounters bugs during implementation:
1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

## Example Workflow

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## Design &amp; Text Delegation (Samaya Profile Pattern)

When the user asks to **"use Claude for design"** or **"play with text using Claude"** for the Samaya Factory Profile website:

1. Do NOT manually edit HTML/CSS/text content — delegate ALL design/text work to a subagent
2. The user's preference: **replace existing content, don't add new blocks/sections** unless explicitly requested
3. Use `delegate_task` with `toolsets=['terminal', 'file']` and provide:
   - The exact file paths (index.html, CSS files)
   - The section ID (e.g., `id="p4-hse"`)
   - Clear description of what to change (replace photo X with photo Y, rewrite the text, redesign layout)
   - The design constraints (navy/gold palette, A4 landscape, RTL, bilingual AR/EN, fonts: Tajawal/Inter/Cormorant Garamond)
4. For multi-page grids: use `grid-auto-rows: auto`, remove `overflow: hidden`, set fixed `height` on images (e.g., 48mm for materiality cells)
5. After the subagent completes, run the deploy process yourself — subagents don't deploy
6. Always verify the deployed result with `curl | grep` for the changed content

### When NOT to delegate
- Simple single-step file copies (cp, mkdir)
- Deploy commands (run these yourself after subagent finishes)
- Quick read-and-answer questions about file content

## Universal Reporting Rule — ALWAYS

**This rule overrides every other skill in this library.**

> For every task completed — terminal command, file edit, subagent result, script run, web search, anything — report completion to the user before moving on. Even `ls` or a 2-second find warrants a one-line confirmation: "Done — found 3 files." The user must never wonder whether something finished silently.

This applies to:
- Terminal commands (always report exit status + what happened)
- Subagent results (always relay the outcome with specifics, not just "done")
- File operations (confirm what was created/modified)
- Cron jobs / background scripts (deliver results or confirm silent completion)
- API calls (confirm what was fetched/posted/updated)

**Never respond with just "ok", "done", "✅", or silence after a tool completes.** Always give the user a concrete outcome summary — what ran, what changed, what was found, or what the next step is.

```
Bad:  "ok done"
Good: "Done — ZAM-NWC-CTR-MUM-001_Rev03.pdf appended to register (row 312, 14:35)."

Bad:  "found it"
Good: "Found — Al Faw BOQ pre-VE Rev07 at /Aseer/docs/BOQ_BEFORE_VE.rev07.html"
```

## Remember

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
ALWAYS report task completion — even terminal commands
```

**Quality is not an accident. It's the result of systematic process.**

- **`references/document-audit-subagent.md`** — Protocol for delegating a document cross-reference audit to a sub-agent (e.g., Kimi). Covers context construction, target document pre-read, reference doc location, output format specification, and read-only guardrails. Use when the user asks to audit a technical proposal, tender document, or report against project reference documents (SOW, ER, spec sheets, plans).

## Further reading (load when relevant)

When the orchestration involves significant context usage, long review loops, or complex validation checkpoints, load these references for the specific discipline:

- **`references/react-threejs-performance-debugging.md`** — Systematic checklist for diagnosing React + Three.js performance: WebGL pause when hidden, backdrop-filter over animated canvas, expensive per-render computations, duplicate rAF loops, mix-blend-mode cost, ScrollTrigger global kill. Apply HIGH severity fixes first, re-test before applying MEDIUM/LOW items.
- **`references/context-budget-discipline.md`** — Four-tier context degradation model (PEAK / GOOD / DEGRADING / POOR), read-depth rules that scale with context window size, and early warning signs of silent degradation. Load when a run will clearly consume significant context (multi-phase plans, many subagents, large artifacts).
- **`references/gates-taxonomy.md`** — The four canonical gate types (Pre-flight, Revision, Escalation, Abort) with behavior, recovery, and examples. Load when designing or reviewing any workflow that has validation checkpoints — use the vocabulary explicitly so each gate has defined entry, failure behavior, and resumption rules.
- **`references/data-integrity-pitfalls.md`** — The cardinal rule: never invent or extrapolate data from source files. Only use fields that actually exist. Load when building UI from raw data (JSON, Excel, CSV) to avoid fabricating fields the user will later reject.
- **`references/interactive-hotspot-patterns.md`** — Architecture/interior design material visualization on 3D render images. Pin styling, proximity detection, tooltip edge-flip positioning, rAF mouse throttle, editor mode architecture. Load when building any image-based interactive hotspot system.
- **`references/mass-data-extraction-from-excel-schedule-files.md`** — Extracting 1200+ material records from 17+ Excel schedule files with auto-header detection, column matching, and merge strategy. Load when working with museum/exhibition schedule spreadsheets.
- **`references/dimension-stripping-patterns.md`** — Regex patterns to strip dimensions and units from material descriptions for cleaner info card display. Includes JS implementation and common patterns. Load when building info card tooltips or sidebars from raw descriptive data.

All references adapted from gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).
