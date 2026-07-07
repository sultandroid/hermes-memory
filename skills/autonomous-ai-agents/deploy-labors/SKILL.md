---
name: deploy-labors
description: "One-command labor army deployment — route any task to Claude/Kimi/Codex automatically following the QA pipeline. Load this, pass your task, and the labors handle it."
version: 1.0.0
author: Hermes Agent
tags: [orchestration, delegation, labors, qa-pipeline]
---

# Deploy Labors — One-Call Labor Army

## Usage

Load this skill, then call `deploy_labors(task_description)` to automatically route any task through the full labor pipeline.

```python
# From execute_code or any Hermes session:
deploy_labors("Check ~/Downloads for new Aseer files and organize them")

# For raw task (no processing needed before dispatch):
deploy_labors_raw("Generate an HTML payment status report for NRS")
```

## What it does

```
Your Task
  │
  ├── Phase 0: Discover current state (do NOT skip)
  │     Check CG_STATUS.md, PROJECT_MEMORY.md, session history first.
  │     Avoid re-doing already-completed work.
  │     (Real example: Comm Plan was already resolved before this session)
  │
  ├── Phase 1: Codex rewrites & structures the order (QC Gate 1)
  ├── Phase 2: [Research phase if needed]
  │     ├── Simple lookup → Kimi (fast, ~2s)
  │     ├── Multi-aspect → delegate_task × 2-3 (parallel)
  │     └── Deep synthesis → Claude Code
  ├── Phase 3: Claude Code executes the work
  ├── Phase 4: Codex audits output (QC Gate 2)
  └── Deliver result
```

## Labor Routing Table

| Task Type | Route | Why |
|-----------|-------|-----|
| **Context check first** (CG_STATUS, memory, project status) | **Do it yourself** | Check what's already done before routing to labors. Saves time + avoids rework |
| HTML/A4/print docs, SVG, design | Claude Code | Strongest frontend + template gen |
| OCR, PDF extraction, data classification | Kimi or Codex | Fast text extraction, fitz/tesseract |
| Payment reconciliation, invoice audit | Codex | Python-led verification |
| Code generation, refactor, PR review | Claude Code → Codex audit | Heavy gen + QC gate |
| File organization, downloads cleanup | Kimi (inventory) → Claude (move) → Codex (audit) | Split by strength |
| Quick check, grep, file sort | Kimi | Lightweight, ~2s startup |
| **File search for unknown term** (supplier name, person, codename) | **Local first: rg/grep/mdfind** | Faster than delegate_task. Only escalate to labor if local search fails |
| Web research (simple, 1-2 facts) | Kimi (SearchWeb built-in) | Fastest startup |
| Web research (multi-aspect, parallel) | delegate_task × 2-3 with toolsets=["web"] | Independent angles simultaneously |
| Web research (deep synthesis, regulatory) | Claude Code (WebSearch + stronger reasoning) | Cross-source analysis |
| QA audit of deliverables | Codex | HTML validation scripts, tag balance, CSS checks |
| Odoo/ERP query | Claude Code | Has Odoo skill + project memory |
| Backup creation before edits | **Do it yourself** | Never delegate backup creation — subagent may skip or corrupt |

## Implementation

```python
from hermes_tools import terminal, delegate_task, read_file, write_file
from datetime import datetime
import json, os, re

def deploy_labors(task: str, workdir: str = None):
    """
    Route a task through the full labor pipeline.
    
    1. Codex rewrites the order into a structured spec
    2. Research phase if needed (auto-detected)
    3. Claude Code executes
    4. Codex audits output
    5. Deliver
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ── Phase 1: Codex rewrites the order ──
    print(f"🔷 Phase 1: Codex rewriting order...")
    scratch_dir = f"/tmp/labor-{timestamp}"
    terminal(f"mkdir -p {scratch_dir} && cd {scratch_dir} && git init && echo '# scratch' > README.md && git add -A && git commit -m init")
    
    codex_spec = terminal(
        command=f"cd {scratch_dir} && codex exec 'Rewrite this user order into a clear, structured task spec with numbered steps, success criteria, and file paths. Mention which labor should execute each step and what to check in QA. User order: {task}' --sandbox workspace-write",
        pty=True, timeout=180
    )
    spec_text = codex_spec.get("output", "")
    print(f"   Codex spec: {spec_text[:300]}...")
    
    # ── Phase 2: Auto-detect research needs ──
    needs_research = any(w in task.lower() for w in [
        "research", "find out", "look up", "what is", "regulation", "standard",
        "code", "requirement", "price", "cost", "supplier", "vendor", "authority"
    ])
    
    if needs_research:
        print(f"🔷 Phase 2: Research...")
        # Simple or complex?
        if len(task) < 200 and not any(w in task.lower() for w in ["regulat", "authorit", "multi", "compare"]):
            # Pattern A: Kimi fast research
            research = terminal(
                command=f"echo '{task}' | kimi --print 2>&1 | python3 -c \"import re,sys;d=sys.stdin.read();m=re.findall(r\\\"text=\'([^\']*)\'\\\",d);print(m[-1] if m else d)\"",
                timeout=60
            )
            print(f"   Kimi research done")
        else:
            # Pattern B: Parallel multi-agent
            research_results = delegate_task(
                tasks=[{"goal": f"Research: {task}", "toolsets": ["web"]}],
                context="Provide comprehensive findings with sources."
            )
            research = research_results[0].get("summary", "")
            print(f"   Parallel research done")
    else:
        research = ""
    
    # ── Phase 3: Claude Code executes ──
    print(f"🔷 Phase 3: Claude Code executing...")
    claude_prompt = f"Execute this task per the structured spec below.\n\nSPEC:\n{spec_text}\n\n{'RESEARCH:\n' + research if research else ''}"
    
    claude_result = terminal(
        command=f"cd {workdir or '.'} && claude -p '{claude_prompt}' --allowedTools 'Read,Edit,Write,Bash,Glob,Grep' --max-turns 20 --output-format json",
        timeout=300
    )
    print(f"   Claude Code execution done")
    
    # ── Phase 4: Codex audits ──
    print(f"🔷 Phase 4: Codex auditing output...")
    
    # Determine what files were produced
    audit_prompt = f"Audit the work done for this task. Check: correctness, completeness, HTML tag balance if HTML, CSS validity, all files created/modified, content accuracy against the spec. Spec: {spec_text}. Task: {task}"
    
    if workdir:
        audit = terminal(
            command=f"cd {workdir} && codex exec '{audit_prompt}' --sandbox workspace-write",
            pty=True, timeout=120
        )
    else:
        audit = terminal(
            command=f"cd {scratch_dir} && codex exec '{audit_prompt}' --sandbox workspace-write",
            pty=True, timeout=120
        )
    
    audit_text = audit.get("output", "")
    print(f"   Audit: {'PASS ✅' if 'PASS' in audit_text.upper() else 'Audit complete'}")
    
    # ── Phase 5: Report ──
    summary = {
        "task": task,
        "timestamp": timestamp,
        "codex_spec_preview": spec_text[:200],
        "research_done": bool(research),
        "execution": "Claude Code",
        "audit": audit_text[:500],
        "workdir": workdir or scratch_dir
    }
    
    return summary


def deploy_labors_raw(task: str, workdir: str = None):
    """
    Fast path — skip Codex rewrite, go straight to Claude Code + Codex audit.
    Use when the task is already well-defined (no restructuring needed).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scratch_dir = f"/tmp/labor-{timestamp}"
    
    print(f"🔷 Claude Code executing: {task[:100]}...")
    claude_result = terminal(
        command=f"cd {workdir or '.'} && claude -p '{task}' --allowedTools 'Read,Edit,Write,Bash,Glob,Grep' --max-turns 20 --output-format json",
        timeout=300
    )
    
    print(f"🔷 Codex auditing...")
    if not workdir:
        terminal(f"mkdir -p {scratch_dir} && cd {scratch_dir} && git init && echo '# scratch' > README.md && git add -A && git commit -m init")
    
    audit = terminal(
        command=f"cd {workdir or scratch_dir} && codex exec 'Audit the work done for this task. Check all files, correctness, completeness: {task}' --sandbox workspace-write",
        pty=True, timeout=120
    )
    
    return {"task": task, "claude": "done", "audit": audit.get("output", "")[:500]}
```

## Quick Reference

```bash
# Via terminal (heavy task)
claude -p "task" --allowedTools "Read,Edit,Write,Bash,Glob,Grep" --max-turns 15

# Via Kimi (fast research)
echo "question" | kimi --print 2>&1

# Via Codex (QA audit)
codex exec "Audit output.html" --sandbox workspace-write

# Parallel research
delegate_task(tasks=[{"goal":"Research A","toolsets":["web"]},{"goal":"Research B","toolsets":["web"]}])
```

## Pitfalls

- **delegate_task timeouts on broad file searches** — searching for an unknown term across all OneDrives can timeout (600s). Pattern: if delegate_task times out, fall back to local rg/grep/mdfind yourself. Faster, more reliable.
- **Codex needs git repo** — always `git init` before calling codex exec
- **Codex needs pty=true** — hangs without pseudo-terminal
- **Kimi `--quiet` times out on long prompts** — use `--print` for anything >500 chars
- **Backup files BEFORE delegating edits** — subagents may corrupt unrelated sections
- **read_file() truncates at 500 lines** — always pass `limit=10000` or use `terminal(cat path)` for raw content
- **Never rename OneDrive folders via sub-labor** — `mv` breaks macOS File Provider sync
- **Entity isolation** — Samaya ≠ Moqtana ≠ Tqanny. Never cross without explicit user OK

## When NOT to use

- Trivial 1-tool calls (simple `ls`/`grep`/`read_file`)
- Clarifying questions to the user
- Quick verification checks (<3 tool calls)
- Any task where delegation overhead exceeds the work itself

## Reference Files

| File | Purpose |
|------|---------|
| `references/cg-status-discovery-pattern.md` | Check CG_STATUS.md before routing plan-revision tasks to avoid re-doing completed work |
